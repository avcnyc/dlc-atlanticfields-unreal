# PLAN — Regional Map prototype: POI coordinates → Cesium → A→B driving route

**Ticket:** [AVC-5719 — Track A | Cesium](https://linear.app/av-controls/issue/AVC-5719)
**Level:** `Content/Sites/AtlanticFields/RegionalMap/Maps/RegionalMap_Proto.umap`
**Written:** 2026-09-17 · **Korean:** `.claude/PLAN-regional-map-route.ko.md`

---

## Goal

1. Turn the 46 spreadsheet addresses into lon/lat.
2. Show those POIs on the Cesium globe.
3. Pick 2 of them. Draw the real driving route from Atlantic Fields to each one, following real
   roads, like Google Maps.

This is a prototype. Fixed camera. No labels, no camera moves, no CMS.

| AVC-5719 item | Here |
|---|---|
| 1. Environment | Phase 0 (done) |
| 2. Routing | Phases 1–5 |
| 3. Camera pole · 4. Flags · 5. Highlighting | out of scope |

---

## What is already set up

| Item | Value |
|---|---|
| Georeference origin | **lat 27.064, lon -80.215** |
| Cesium ion token | set |
| Tileset | **Google Photorealistic 3D Tiles**, ion asset `2275207`, `Source: From Cesium Ion` |
| In the level | `CesiumGeoreference0`, `CesiumSunSky`, `CesiumCameraManager0`, `CesiumCreditSystemBP0`, `DynamicPawn` |

No Google Maps Platform key is needed. ion serves the Google tiles.

**One thing to fix:** `Show Credits on Screen` is off on the tileset. Google attribution is a
requirement for photoreal tiles. Turn it on, or confirm the Data Attribution panel shows the Google
logo, and check it again in a packaged build.

---

## Services

Both are OpenStreetMap, and neither needs an API key.

| Job | Service | Notes |
|---|---|---|
| Address → lon/lat | **Nominatim** | 1 request/sec. 46 rows → 40 unique addresses ≈ 1 minute. Set a real User-Agent. |
| Driving route | **OSRM** demo server | `router.project-osrm.org/route/v1/driving/{lon},{lat};{lon},{lat}?overview=full&geometries=geojson` |

We call both **once**, from a script, and save the results as JSON in the project. Nothing runs at
runtime. So the demo server having no SLA does not matter.

---

## Three decisions

### 1. Store lon/lat in the JSON, never Unreal coordinates

Convert to Unreal space at construction-script time, through the `CesiumGeoreference`. If we baked
Unreal vectors instead, moving the origin would silently break every point and throw no error.

### 2. Skip terrain height sampling. Use one fixed height.

Photoreal tiles have no bare-ground layer. `SampleHeightMostDetailed` on them returns rooftops and
tree canopy, so it cannot give us road height.

We do not need it. Hobe Sound to Jupiter is flat — the whole route area is within about 15 m of sea
level. So we put the route line at **one fixed height above the ellipsoid** (start at 25 m) and the
POI markers higher (start at 80 m). That removes the async sampling batch, the second tileset, and
all the per-point failure handling.

If a later site has real terrain, height sampling comes back. See §Cut on purpose.

### 3. Route line draws on top (depth test off)

Trees and buildings sit above the road in photoreal tiles. With depth test on, they chop the line
into dashes. There are no hills here to hide it, so depth test buys nothing. Draw on top, the way
Google Maps does.

---

## Phase 0 — Setup ✅ done

Origin, token and tileset are in place (see above). Only open item: the credits checkbox.

---

## Phase 1 — Addresses → coordinates

**Why.** The sheet has text addresses only. Cesium needs numbers, and OSRM only accepts coordinates.
This step runs once and is then cached forever.

**Source:** [AF Regional POI (WIP)](https://docs.google.com/spreadsheets/d/1-I3zf2qSZ97hkE57KKu4sTeJpDbcRftW96A9NEBWUR4/edit?gid=639708013), tab `gid=639708013`.
Header `Category, Name, Address, Distance`. **46 rows.** No lat/lon columns.
`Distance` is **driving** miles, not straight-line. Confirmed against the source workbook, which
lists both for airports: Palm Beach International is 27 mi straight-line and about 32 mi to drive,
and this sheet carries 34.0.

**Make**

- `Tools/poi/geocode_poi.py` — pull sheet → dedupe → geocode → verify → write JSON
- `Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json`

```json
{
  "origin": { "name": "Atlantic Fields", "lat": 27.064, "lon": -80.215 },
  "pois": [
    {
      "id": "hobe-sound-social-coffee",
      "name": "Hobe Sound Social + Coffee",
      "categories": ["Restaurants & Dining"],
      "address": "11844 SE Dixie Hwy Ste A, Hobe Sound, FL 33455",
      "lat": 27.0619, "lon": -80.1387,
      "sheetDistanceMi": 4.6, "computedDistanceMi": 4.5,
      "active": true, "flagged": false
    }
  ]
}
```

**Steps**

1. Pull the sheet tab to CSV. Never hand-edit it.
2. Dedupe on name + address. Some rows appear twice (every hospital, The Marketplace, Witham Field).
   When rows merge, keep both categories — `The Pine School` is filed under two.
3. Set `active: false` for rows marked "Permanently Closed".
4. Geocode each address with Nominatim. Cache every response to disk.
5. Check each result. The sheet lists driving miles, so only two outcomes are impossible: a straight
   line longer than the drive, or one far shorter than any detour could explain. Flag those, plus
   anything outside `lat 26.4–27.7, lon −80.8…−79.9`, plus anything coarser than street level that
   is not a park or preserve.
6. Fix flagged rows by hand and re-run.

**Done when** every POI has lon/lat or is listed as unresolved with a reason, no flags are left
unreviewed, and a re-run with the cache makes zero network calls.

**Expect some hand-fixing.** Addresses with no street number, like `Hobe Sound Beach — Jupiter
Island, FL 33455`, will land on a town centre. That is what step 5 catches.

---

## Phase 2 — POIs on the globe

**Make**

- `Content/POI/Blueprints/Sys/S_POI` — `Id`, `Name`, `Categories`, `Latitude`, `Longitude`, `bActive`
- `Content/POI/Blueprints/BP_POIMarker` — mesh + `CesiumGlobeAnchor`
- `Content/POI/Blueprints/BP_POISet` — reads `AF_POI.json`, spawns one marker per POI

`Content/POI/` is a mechanism folder, so nothing inside it may reference Atlantic Fields. The
property data comes in as an input.

**Steps**

1. Parse the JSON into `TArray<S_POI>`.
2. Spawn a marker per active POI. Place it with `CesiumGlobeAnchor` at lat/lon and the fixed marker
   height.
3. Colour the marker by category, so a wrong category is visible instead of hidden in data.

**Done when** all POIs sit in the right place (spot-check 5 against Google Maps), none are buried
inside photoreal buildings, and they stay put if the origin moves.

---

## Phase 3 — Fetch 2 routes

**The two POIs.** They cover two different problems, instead of the same one twice.

| | POI | Distance | Why this one |
|---|---|---|---|
| **B1** | Hobe Sound Social + Coffee, Hobe Sound | 4.6 mi | short, many turns → does the line follow surface streets? |
| **B2** | Jupiter Medical Center, Jupiter | 14.5 mi | long US-1 / I-95 run → is it readable at regional distance? |

A is the origin, `27.064 / -80.215`.

**Make**

- `Tools/poi/fetch_route.py`
- `Content/Sites/AtlanticFields/RegionalMap/Routes/Route_AF_to_HobeSoundSocial.json`
- `Content/Sites/AtlanticFields/RegionalMap/Routes/Route_AF_to_JupiterMedical.json`

```json
{
  "id": "af-to-jupiter-medical",
  "from": { "id": "atlantic-fields", "lat": 27.064, "lon": -80.215 },
  "to":   { "id": "jupiter-medical-center", "lat": 26.9234, "lon": -80.0975 },
  "travelTimeSeconds": 1320,
  "distanceMeters": 23336,
  "points": [ { "lat": 27.064, "lon": -80.215 }, { "lat": 27.0638, "lon": -80.2149 } ]
}
```

**Steps**

1. Call OSRM with `overview=full`. This is the important part — the default `overview=simplified`
   drops points and the line visibly cuts corners.
2. OSRM GeoJSON gives `[lon, lat]` pairs. Our JSON names the fields, so write them by name and never
   pass raw arrays around. **This is the most likely bug in the whole plan.**
3. Sanity check: `distanceMeters` must be larger than the straight-line distance. If it is smaller,
   the coordinates got swapped.

**Done when** both files parse, their first and last points match A and B within ~50 m, and a re-run
uses the cache.

---

## Phase 4 — Draw the route

**Make**

- `Content/Route/Blueprints/Sys/S_RoutePoint` — `Latitude`, `Longitude`
- `Content/Route/Blueprints/Sys/S_RouteData` — `TArray<S_RoutePoint>`, `TravelTimeSeconds`, `SourceId`
- `Content/Route/Blueprints/BP_Route` — spline + spline mesh chain
- `Content/Route/Materials/M_RouteLine`
- `Content/Sites/AtlanticFields/RegionalMap/Materials/MI_RouteLine_AtlanticFields`

**Steps**

1. `BP_Route` construction script: load the route JSON → convert each point through the georeference
   at the fixed height → add all points to the spline as **Linear** → build the spline mesh chain,
   writing normalized distance-along-route into each segment.
   Linear is enough because `overview=full` already samples the road densely. See §Cut on purpose.
2. `M_RouteLine`: unlit, translucent, **depth test off**. Parameters: colour, width, and `Progress`
   (Phase 5 uses it).
3. `BP_Route` takes width, height and colour as **inputs**. It does not read any Atlantic Fields
   asset. The level passes them in.
4. Tune the fixed height first. Raise it until the line clears the visible road at the fixed camera,
   on both routes.

**Done when**

- The line reads clearly at the fixed camera distance and follows the real roads
- It does not sink under the photoreal ground anywhere along either route
- Moving the origin a few hundred metres and rebuilding puts the route back in the same place

---

## Phase 5 — Draw-on and wrap up

**Steps**

1. Drive `Progress` from 0 to 1 over `DrawDuration`. The material clips the line against it, so the
   route reveals itself from A to B. One parameter per frame, no rebuilding.
2. Add a replay trigger so it can be shown again without restarting PIE.
3. Record both routes drawing. Attach the video to AVC-5719.
4. Check the reference viewer on `Content/Route/` and `Content/POI/`: zero references into `Sites/`.
5. Confirm Git LFS covers the new `.uasset` / `.umap` files, and that `DefaultEngine.ini` commits
   with no `SecurityToken` line.
6. Confirm Google credits are visible in a packaged build.
7. Write the tuned height and width values into this file.

**Definition of done**

> Open `RegionalMap_Proto.umap` on a fresh clone. Atlantic Fields is on Google photoreal tiles, every
> geocoded POI is placed, and two driving routes — one short and twisty, one long — draw themselves
> along the real roads.

---

## Cut on purpose

These were in the earlier draft. We removed them to keep the prototype small. Each one has a trigger
that brings it back.

| Cut | Bring it back when |
|---|---|
| Terrain height sampling (hidden second tileset, async batch, per-point failure flags) | a site has real elevation change, or the fixed height visibly fails somewhere |
| Corner / curve classifier (`E_VertexKind`, `FL_RouteGeo.ClassifyVertices`, corner rounding, 3 tuning dials) | intersections look wrong with plain Linear points at the final camera distance |
| `RouteSplineTest.umap` debug level | the corner classifier comes back |
| `E_RouteState` / `BPI_Route` state machine | something outside `BP_Route` needs to react to route state, e.g. a HUD |
| Depth test on the route line | a site has hills that should hide the line |

---

## Open

| # | Question | Blocks |
|---|---|---|
| 1 | Turn on `Show Credits on Screen`, or confirm the Google logo shows in the attribution panel | Phase 5 |
| 2 | Is the 46-row sheet tab final? Re-pulling is cheap, but only if nobody hand-edited the JSON | Phase 1 |
| 3 | 3 addresses OSM does not hold: Palm City Farm Camp, Treasure Coast Wildlife Center, Two Brother's Pizza. Look them up and add to `Tools/poi/overrides.json` | Phase 2 |
| 4 | Every Hobe Sound POI computes a straight line slightly longer than the drive the sheet lists. The marketing distances look measured from a point about a mile east of the origin now in the level. Which point is right? | not blocking |
