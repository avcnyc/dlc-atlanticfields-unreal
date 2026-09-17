# STATE — Regional Map route prototype

Tracks `.claude/PLAN-regional-map-route.md`. Korean plan: `.claude/PLAN-regional-map-route.ko.md`.
Korean version of this file: `.claude/STATE-regional-map-route.ko.md`.

## Phase status

| Phase | Name | Status |
|---|---|---|
| 0 | Setup (origin, ion token, tileset) | **complete** — done in-editor before this plan was written |
| 1 | Addresses → coordinates | **complete 2026-09-17** |
| 2 | POIs on the globe | not started |
| 3 | Fetch 2 routes | not started |
| 4 | Draw the route | not started |
| 5 | Draw-on and wrap up | not started |

## Phase 1 — complete 2026-09-17

**Created**

- `Tools/poi/geocode_poi.py` — pulls the sheet, dedupes, geocodes through Nominatim, verifies, writes
  the JSON and the report. Stdlib only.
- `Tools/poi/overrides.json` — hand-entered coordinates for addresses OSM does not hold. Currently
  holds only its own documentation; 3 real entries are still needed (see Open).
- `Tools/poi/REPORT.md` — generated verification report.
- `Tools/poi/cache/af_poi_raw.csv` — the pulled sheet tab.
- `Tools/poi/cache/geocode_cache.json` — every Nominatim response, so a re-run makes no network call.
- `Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json` — **the Phase 1 deliverable.**

**Modified**

- `.claude/PLAN-regional-map-route.md` / `.ko.md` — corrected the row count and the meaning of the
  sheet's `Distance` column (see Deviations).

**Results**

| | |
|---|---|
| Sheet rows | 46 |
| POIs after dedupe | 40 |
| Resolved with coordinates | 37 |
| Unresolved | 3 |
| Marked inactive (permanently closed) | 3 |
| Flagged for review | 13 |

Both Phase 3 example POIs resolved at building level (`place_rank` 30):
Hobe Sound Social + Coffee `27.059563, -80.128983`, Jupiter Medical Center `26.924122, -80.094573`.

**Verification run**

- Re-run with a warm cache produces a byte-identical `AF_POI.json` (md5 `f71911e2…` before and after)
- `--offline` re-run succeeds, confirming zero network calls on a warm cache
- Origin in the JSON matches the level: `lat 27.064, lon -80.215`

## Deviations from the plan

1. **The sheet has 46 rows, not 62.** The 62 came from a summarizing fetch when the plan was written
   and was wrong. Both plan files are corrected.
2. **The `Distance` column is driving miles, not straight-line.** Proven against the source workbook,
   whose airport tab lists both: Palm Beach International at 27 mi straight-line and about 32 mi to
   drive, against the sheet's 34.0, and our computed straight line of 27.20. The verification rule
   changed from a symmetric ±15% tolerance to a one-sided check, because a drive can never be shorter
   than the straight line. This removed 12 false flags.
3. **Parks and preserves are exempt from the street-level precision check.** A park resolves to its
   polygon centroid at a low `place_rank`, and that centroid is exactly where the marker belongs.
   This removed 2 false flags.
4. **Added a second dedupe pass on name.** Hobe Sound Beach is listed twice under two different
   addresses. Merging on name alone would be unsafe, so it also requires the two rows to give the
   same distance within a mile.
5. **Added `Tools/poi/overrides.json`**, not in the plan. The plan says to fix flagged rows by hand;
   this is where a hand fix lives so that a re-run does not undo it.

## Open — carry into Phase 2

1. **3 addresses OSM does not hold.** Palm City Farm Camp, Treasure Coast Wildlife Center, and Two
   Brother's Pizza have no coordinates. They need a manual lookup into `Tools/poi/overrides.json`.
   None of them is a Phase 3 example POI, so this does not block.
2. **Every Hobe Sound POI computes a straight line slightly longer than the drive the sheet lists** —
   about 1 to 1.4 miles longer, consistently, across all 11 of them. One row like that is a bad
   geocode; all of them is the origin. The marketing distances appear to be measured from a point
   roughly a mile east of the georeference origin currently in the level. The addresses themselves
   geocode correctly, and OSRM will route from the real origin in Phase 3, so nothing is blocked.
   Worth confirming which point the client means.
3. The credits checkbox from Phase 0 is still open: `Show Credits on Screen` is off on the tileset.

## Resume point

**Start Phase 2 — POIs on the globe.** Build `S_POI`, `BP_POIMarker` and `BP_POISet` under
`Content/POI/`, load `Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json`, and place a marker
per active POI with a `CesiumGlobeAnchor` at the fixed marker height. Nothing under `Content/POI/`
may reference Atlantic Fields.
