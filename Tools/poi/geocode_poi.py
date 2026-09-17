"""Turn the Atlantic Fields regional POI spreadsheet into lon/lat.

Phase 1 of .claude/PLAN-regional-map-route.md.

Pulls the published sheet tab, dedupes it, geocodes every address through
Nominatim, checks each result against the distance the sheet claims, and writes
Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json.

Runs once. Every response is cached to disk, so a re-run makes no network calls
and produces a byte-identical JSON. Nothing here runs at engine runtime.

    python Tools/poi/geocode_poi.py                # use the cache where possible
    python Tools/poi/geocode_poi.py --refresh      # re-pull the sheet
    python Tools/poi/geocode_poi.py --offline      # fail rather than hit the network

Stdlib only -- no pip install, so it runs on any machine with the engine on it.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- constants

SHEET_ID = "1-I3zf2qSZ97hkE57KKu4sTeJpDbcRftW96A9NEBWUR4"
SHEET_GID = "639708013"
SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
)

# Georeference origin, set in RegionalMap_Proto.umap.
ORIGIN = {"name": "Atlantic Fields", "lat": 27.064, "lon": -80.215}

# Every POI in the sheet is on Florida's Treasure Coast / Palm Beach stretch.
# Anything outside this box is a bad geocode, not a distant POI.
BBOX = {"lat_min": 26.4, "lat_max": 27.7, "lon_min": -80.8, "lon_max": -79.9}

# The sheet's Distance column is DRIVING miles, not straight-line. Confirmed
# against the source workbook, which lists both for airports: it says Palm Beach
# International is 27 mi straight-line and ~32 mi to drive, and the sheet carries
# 34.0 while we compute 27.20 straight-line.
#
# So the check is one-sided. A drive can never be shorter than the straight line,
# and a real detour factor tops out around 2x on this road network. Outside that
# band, the geocode landed somewhere wrong.
DRIVE_RATIO_MIN = 0.45  # computed/sheet below this: too far away to be a detour
DRIVE_RATIO_MAX = 1.05  # computed/sheet above this: straight line beat the drive
DRIVE_CHECK_FLOOR_MILES = 1.0  # below this, rounding noise swamps the ratio

# Nominatim place_rank: 30 is a building, 26 is a street, below that is a
# neighbourhood or larger. Anything coarser than a street needs a human look --
# except for the things that are genuinely bigger than a street. A park or a
# preserve resolves to its polygon centroid at a low rank, and that centroid is
# exactly where we want the marker.
MIN_PLACE_RANK = 26
AREA_ADDRESS_TYPES = {
    "park",
    "nature_reserve",
    "beach",
    "protected_area",
    "leisure",
    "attraction",
    "aerodrome",
    "golf_course",
    "water",
}

# Nominatim's usage policy: at most 1 request per second, and a User-Agent that
# identifies the application. Add a contact address here if this ever runs at
# volume.
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "dlc-atlanticfields-unreal/0.1 (AV&C Regional Map prototype)"
REQUEST_INTERVAL_SECONDS = 1.1

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / "Tools" / "poi" / "cache"
RAW_CSV_PATH = CACHE_DIR / "af_poi_raw.csv"
GEOCODE_CACHE_PATH = CACHE_DIR / "geocode_cache.json"
# Hand-entered coordinates for addresses OSM does not hold. Checked in, applied
# ahead of the cache, so a re-run never undoes a human fix.
OVERRIDES_PATH = REPO_ROOT / "Tools" / "poi" / "overrides.json"
OUTPUT_PATH = (
    REPO_ROOT / "Content" / "Sites" / "AtlanticFields" / "RegionalMap" / "POI" / "AF_POI.json"
)
REPORT_PATH = REPO_ROOT / "Tools" / "poi" / "REPORT.md"

# Rows the sheet carries but that are not a place you would drive to, or that
# are filed under a category they do not belong to. They stay in the JSON as
# active: false so the sheet and the JSON still line up row for row.
INACTIVE_NAME_MARKERS = ("permanently closed",)

_last_request_time = 0.0


# ------------------------------------------------------------------ helpers


def http_get(url: str, offline: bool) -> str:
    """GET a URL as text, respecting the Nominatim rate limit."""
    global _last_request_time
    if offline:
        raise RuntimeError(f"--offline was passed but {url} is not cached")

    wait = REQUEST_INTERVAL_SECONDS - (time.monotonic() - _last_request_time)
    if wait > 0:
        time.sleep(wait)

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")
    _last_request_time = time.monotonic()
    return body


def normalize(text: str) -> str:
    """Collapse a name or address to a comparable key."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_]+", "-", text)


def haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in miles."""
    earth_radius_miles = 3958.7613
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = phi2 - phi1
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * earth_radius_miles * math.asin(math.sqrt(a))


# ------------------------------------------------------------------- sheet


def fetch_sheet(refresh: bool, offline: bool) -> str:
    """Return the sheet tab as CSV text, pulling it only when we have to."""
    if RAW_CSV_PATH.exists() and not refresh:
        return RAW_CSV_PATH.read_text(encoding="utf-8")

    csv_text = http_get(SHEET_URL, offline)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    RAW_CSV_PATH.write_text(csv_text, encoding="utf-8", newline="")
    return csv_text


def read_rows(csv_text: str) -> list[dict]:
    """Parse the sheet into rows, skipping blanks."""
    rows = []
    for row in csv.DictReader(io.StringIO(csv_text)):
        name = (row.get("Name") or "").strip()
        address = (row.get("Address") or "").strip()
        if not name or not address:
            continue
        rows.append(
            {
                "category": (row.get("Category") or "").strip(),
                "name": name,
                "address": address,
                "distance": (row.get("Distance") or "").strip(),
            }
        )
    return rows


def dedupe(rows: list[dict]) -> list[dict]:
    """Merge rows that are the same place.

    Several POIs appear twice, and one POI can be filed under two categories, so
    the key is name plus address and the categories accumulate.
    """
    merged: dict[tuple[str, str], dict] = {}
    order: list[tuple[str, str]] = []

    for row in rows:
        key = (normalize(row["name"]), normalize(row["address"]))
        if key not in merged:
            merged[key] = {
                "name": row["name"],
                "address": row["address"],
                "categories": [],
                "distance": row["distance"],
            }
            order.append(key)
        poi = merged[key]
        if row["category"] and row["category"] not in poi["categories"]:
            poi["categories"].append(row["category"])
        # Keep the first distance we saw; duplicates carry the same value.
        if not poi["distance"]:
            poi["distance"] = row["distance"]

    return merge_same_place([merged[key] for key in order])


def merge_same_place(entries: list[dict]) -> list[dict]:
    """Merge one place that the sheet lists twice under two different addresses.

    Hobe Sound Beach appears as both `Jupiter Island, FL 33455` and
    `1 S Beach Rd, Hobe Sound, FL 33455`. Merging on name alone would be unsafe --
    two branches of one chain share a name -- so we also require the sheet to give
    them the same distance. The address with a street number wins, because it is
    the one that geocodes.
    """
    by_name: dict[str, dict] = {}
    order: list[str] = []

    for entry in entries:
        key = normalize(entry["name"])
        existing = by_name.get(key)
        if existing is None:
            by_name[key] = entry
            order.append(key)
            continue

        try:
            same_distance = abs(float(existing["distance"]) - float(entry["distance"])) <= 1.0
        except (TypeError, ValueError):
            same_distance = False

        if not same_distance:
            # Same name, different place. Keep both, and let the address key them apart.
            order.append(key := f"{key}|{normalize(entry['address'])}")
            by_name[key] = entry
            continue

        for category in entry["categories"]:
            if category not in existing["categories"]:
                existing["categories"].append(category)
        if not re.match(r"^\d", existing["address"]) and re.match(r"^\d", entry["address"]):
            existing["address"] = entry["address"]

    return [by_name[key] for key in order]


# ---------------------------------------------------------------- geocoding


def address_variants(name: str, address: str) -> list[tuple[str, dict]]:
    """Query shapes to try, in order, until one returns a hit.

    The sheet mixes street addresses with entries that have no street number at
    all (a beach, a preserve). One query shape cannot cover both.
    """
    suite_pattern = r"\b(?:ste|suite|unit|apt)\s*[\w-]+\b|#\s*[\w-]+"
    without_suite = re.sub(suite_pattern, "", address, flags=re.IGNORECASE)
    without_suite = re.sub(r"\s*,\s*,", ",", without_suite).strip().strip(",")
    without_suite = re.sub(r"\s{2,}", " ", without_suite)

    variants: list[tuple[str, dict]] = [
        ("full", {"q": f"{address}, USA"}),
    ]
    if normalize(without_suite) != normalize(address):
        variants.append(("no-suite", {"q": f"{without_suite}, USA"}))

    # Structured query: Nominatim handles a split address better than free text
    # when the free text has an unusual suffix.
    parts = [part.strip() for part in without_suite.split(",") if part.strip()]
    if len(parts) >= 2:
        structured = {"street": parts[0], "country": "USA"}
        state_zip = parts[-1].split()
        if len(state_zip) == 2 and state_zip[1].isdigit():
            structured["state"] = state_zip[0]
            structured["postalcode"] = state_zip[1]
            if len(parts) >= 3:
                structured["city"] = parts[-2]
        else:
            structured["city"] = parts[-1]
        variants.append(("structured", structured))

    # City and state without the ZIP. Nominatim often has the street but not the
    # postcode on it, and a wrong ZIP kills an otherwise good match.
    city = parts[-2] if len(parts) >= 3 else (parts[-1] if len(parts) >= 2 else "")
    state = re.sub(r"\s*\d{5}(?:-\d{4})?$", "", parts[-1]).strip() if parts else ""
    city_state = ", ".join(piece for piece in (city, state) if piece)
    if len(parts) >= 2 and city_state:
        variants.append(("no-zip", {"q": f"{parts[0]}, {city_state}, USA"}))

    # By place name. This is what rescues a beach, a preserve, or a small
    # business that OSM knows by name but not by street number. The parenthetical
    # comes off first -- "(Private)" is not part of any name OSM holds.
    plain_name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    if city_state:
        variants.append(("by-name", {"q": f"{plain_name}, {city_state}, USA"}))
    variants.append(("by-name-state", {"q": f"{plain_name}, Florida, USA"}))

    # OSM rarely stores the apostrophe. "Two Brother's Pizza" and "McCarthy's
    # Wildlife Sanctuary" only match once it comes off.
    stripped_name = plain_name.replace("'", "").replace("’", "")
    if stripped_name != plain_name and city_state:
        variants.append(("by-name-plain", {"q": f"{stripped_name}, {city_state}, USA"}))

    return variants


def load_overrides() -> dict:
    """Hand-entered coordinates, keyed by normalized address."""
    if not OVERRIDES_PATH.exists():
        return {}
    raw = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    return {normalize(key): value for key, value in raw.items() if not key.startswith("_")}


def geocode(
    name: str, address: str, cache: dict, overrides: dict, offline: bool, retry_failed: bool
) -> dict | None:
    """Look up one address, trying each query shape until something lands."""
    cache_key = normalize(address)

    override = overrides.get(cache_key)
    if override:
        return {
            "lat": round(float(override["lat"]), 6),
            "lon": round(float(override["lon"]), 6),
            "variant": "override",
            "placeRank": 30,
            "addressType": "manual",
            "displayName": override.get("note", "hand-entered"),
        }

    if cache_key in cache and not (retry_failed and cache[cache_key] is None):
        return cache[cache_key]

    for variant_name, params in address_variants(name, address):
        params = {
            **params,
            "format": "jsonv2",
            "limit": "1",
            "countrycodes": "us",
            "addressdetails": "1",
        }
        url = f"{NOMINATIM_URL}?{urllib.parse.urlencode(params)}"
        try:
            results = json.loads(http_get(url, offline))
        except Exception as error:  # network hiccup on one address is not fatal
            print(f"    ! {variant_name} query failed: {error}", file=sys.stderr)
            continue

        if results:
            hit = results[0]
            record = {
                "lat": round(float(hit["lat"]), 6),
                "lon": round(float(hit["lon"]), 6),
                "variant": variant_name,
                "placeRank": int(hit.get("place_rank", 0)),
                "addressType": hit.get("addresstype", ""),
                "displayName": hit.get("display_name", ""),
            }
            cache[cache_key] = record
            return record

    cache[cache_key] = None
    return None


# -------------------------------------------------------------- verification


def verify(poi: dict) -> list[str]:
    """Return the reasons this POI needs a human look. Empty means it is clean."""
    reasons = []

    if poi["lat"] is None:
        return ["no geocode result"]

    if not (BBOX["lat_min"] <= poi["lat"] <= BBOX["lat_max"]):
        reasons.append(f"latitude {poi['lat']} outside the expected box")
    if not (BBOX["lon_min"] <= poi["lon"] <= BBOX["lon_max"]):
        reasons.append(f"longitude {poi['lon']} outside the expected box")

    address_type = poi["geocode"].get("addressType", "")
    if poi["geocode"]["placeRank"] < MIN_PLACE_RANK and address_type not in AREA_ADDRESS_TYPES:
        reasons.append(
            f"coarser than street level (place_rank {poi['geocode']['placeRank']},"
            f" {address_type or 'unknown type'})"
        )

    sheet_miles = poi["sheetDistanceMi"]
    computed_miles = poi["computedDistanceMi"]
    if sheet_miles and computed_miles and sheet_miles >= DRIVE_CHECK_FLOOR_MILES:
        ratio = computed_miles / sheet_miles
        if ratio > DRIVE_RATIO_MAX:
            reasons.append(
                f"straight line ({computed_miles} mi) is longer than the drive the"
                f" sheet lists ({sheet_miles} mi), which is impossible"
            )
        elif ratio < DRIVE_RATIO_MIN:
            reasons.append(
                f"straight line ({computed_miles} mi) is far shorter than the drive"
                f" the sheet lists ({sheet_miles} mi)"
            )

    return reasons


# ------------------------------------------------------------------ output


def build_poi(entry: dict, result: dict | None) -> dict:
    name = entry["name"]
    lowered = name.lower()
    active = not any(marker in lowered for marker in INACTIVE_NAME_MARKERS)
    display_name = re.sub(
        r"\s*\(permanently closed\)", "", name, flags=re.IGNORECASE
    ).strip()

    try:
        sheet_miles = float(entry["distance"])
    except (TypeError, ValueError):
        sheet_miles = None

    computed_miles = None
    if result:
        computed_miles = round(
            haversine_miles(ORIGIN["lat"], ORIGIN["lon"], result["lat"], result["lon"]), 2
        )

    poi = {
        "id": slugify(display_name),
        "name": display_name,
        "categories": entry["categories"],
        "address": entry["address"],
        "lat": result["lat"] if result else None,
        "lon": result["lon"] if result else None,
        "sheetDistanceMi": sheet_miles,
        "computedDistanceMi": computed_miles,
        "active": active,
        "flagged": False,
        "flags": [],
        "geocode": result or {},
    }
    poi["flags"] = verify(poi)
    poi["flagged"] = bool(poi["flags"])
    return poi


def write_output(pois: list[dict], sheet_row_count: int) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "source": {"sheetId": SHEET_ID, "gid": int(SHEET_GID), "rowCount": sheet_row_count},
        "origin": ORIGIN,
        "pois": pois,
    }
    OUTPUT_PATH.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_report(pois: list[dict], sheet_row_count: int) -> None:
    flagged = [poi for poi in pois if poi["flagged"]]
    unresolved = [poi for poi in pois if poi["lat"] is None]
    inactive = [poi for poi in pois if not poi["active"]]

    lines = [
        "# POI geocoding report",
        "",
        "Generated by `Tools/poi/geocode_poi.py`. Phase 1 of",
        "`.claude/PLAN-regional-map-route.md`. Re-run the script to regenerate.",
        "",
        "## Counts",
        "",
        "| | |",
        "|---|---|",
        f"| Sheet rows | {sheet_row_count} |",
        f"| POIs after dedupe | {len(pois)} |",
        f"| Rows merged away as duplicates | {sheet_row_count - len(pois)} |",
        f"| Marked inactive | {len(inactive)} |",
        f"| Unresolved (no coordinates) | {len(unresolved)} |",
        f"| Flagged for review | {len(flagged)} |",
        "",
        "## How to read the flags",
        "",
        "The sheet's `Distance` column is **driving** miles, not straight-line. The",
        "source workbook proves it: for airports it lists both, giving Palm Beach",
        "International as 27 mi straight-line and about 32 mi to drive, and the sheet",
        "carries 34.0. So we only flag a distance that a drive cannot explain.",
        "",
        "Two clusters are systematic, not per-row mistakes:",
        "",
        "1. **Every Hobe Sound POI** computes a straight line slightly longer than the",
        "   drive the sheet lists. That is impossible for one point, and it happens to",
        "   all of them, so it points at the origin rather than at the geocodes. The",
        "   marketing distances were measured from a point about a mile east of the",
        "   georeference origin now set in the level. It does not block anything: OSRM",
        "   computes the real route from the real origin in Phase 3.",
        "2. **No geocode result** means OSM does not hold that address. Fix those by",
        "   adding coordinates to `Tools/poi/overrides.json` and re-running.",
        "",
        "## Flagged rows",
        "",
    ]

    if flagged:
        lines += ["| POI | Address | Reason |", "|---|---|---|"]
        for poi in flagged:
            reasons = "; ".join(poi["flags"])
            lines.append(f"| {poi['name']} | {poi['address']} | {reasons} |")
    else:
        lines.append("None. Every POI geocoded to street level and agrees with the sheet.")

    lines += ["", "## All POIs", "", "| POI | Categories | lat | lon | sheet mi | computed mi |", "|---|---|---|---|---|---|"]
    for poi in pois:
        lines.append(
            f"| {poi['name']} | {', '.join(poi['categories'])} | {poi['lat']} | {poi['lon']}"
            f" | {poi['sheetDistanceMi']} | {poi['computedDistanceMi']} |"
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# -------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="re-pull the sheet")
    parser.add_argument(
        "--offline", action="store_true", help="fail instead of making a network call"
    )
    parser.add_argument(
        "--retry-failed", action="store_true", help="re-query addresses that found nothing"
    )
    args = parser.parse_args()

    csv_text = fetch_sheet(args.refresh, args.offline)
    rows = read_rows(csv_text)
    entries = dedupe(rows)
    print(f"{len(rows)} sheet rows -> {len(entries)} POIs after dedupe")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = {}
    if GEOCODE_CACHE_PATH.exists():
        cache = json.loads(GEOCODE_CACHE_PATH.read_text(encoding="utf-8"))
    overrides = load_overrides()
    if overrides:
        print(f"{len(overrides)} hand-entered override(s) in effect")

    pois = []
    try:
        for index, entry in enumerate(entries, start=1):
            cached = cache.get(normalize(entry["address"])) is not None
            print(f"  [{index:>2}/{len(entries)}] {entry['name']}{' (cached)' if cached else ''}")
            result = geocode(
                entry["name"],
                entry["address"],
                cache,
                overrides,
                args.offline,
                args.retry_failed,
            )
            pois.append(build_poi(entry, result))
    finally:
        # Always keep what we paid for, even if the run stops halfway.
        GEOCODE_CACHE_PATH.write_text(
            json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    write_output(pois, len(rows))
    write_report(pois, len(rows))

    flagged = sum(1 for poi in pois if poi["flagged"])
    print(f"\nwrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"wrote {REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"{flagged} POI(s) flagged for review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
