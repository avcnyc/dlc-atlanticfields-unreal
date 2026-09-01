# PLAN — Regional map A→B route (Phase 01 prototype)

Draw one route line from the Atlantic Fields community (A) to a nearby POI (B) on a fixed camera
angle over Cesium 3D Tiles. No camera movement, no labels, no API — the 8/20 meeting scoped this to
proving the concept and the draw-on presentation only. Everything the final pipeline needs is
hardcoded here, but shaped so the hardcoding is the only thing that gets replaced.

The prototype answers three questions the design mockup cannot: does a road-following polyline read
correctly at regional camera distance, does it stay legible draped over real terrain, and does the
draw-on animation hold up at that scale.

---

## What exists (traced, 2026-09-01)

| Piece | Where | State |
|---|---|---|
| `CesiumForUnreal` | `dlc_atlanticfields.uproject` | Enabled. Win64/Mac/Linux/Android/IOS |
| Cesium ion server asset | `Content/CesiumSettings/CesiumIonServers/CesiumIonSaaS` | Plugin-generated |
| Folder skeleton | `Content/Route/`, `Content/Sites/AtlanticFields/RegionalMap/` | Empty |
| Conventions | `README.md` | Folder / level / prefix rules, reuse path |
| Git LFS | `.gitattributes` | `.uasset` `.umap` + source art. Hooks installed |
| Design reference | Artifact `94740062` | Fixed-cam mockup, pipeline and terrain-drape diagrams |
| Unreal project | — | **Nothing committed yet.** Only `.gitignore` is in history |

**Not present, deliberately:** `Plugins/Scaffold` (the AV&C framework submodule) and `Tools/crate`.
Both sibling projects have them. Adopting them is a separate decision — see Open.

**The load-bearing fact:** the reusable half of this feature already has a home. summerlin's
`Content/Scaffold/Blueprints/BP_RoadLabelSpline` is a spline actor whose construction script places
components along a path, parameterized per site through `DA_Summerlin` / `DA_Astra`, and it belongs to
the Scaffold plugin's **Vista** module ("camera presentation, site management, labels, overlays").
`BP_Route` is its sibling, not a new species. So `Content/Route/` is a staging area, and the only
thing that has to hold is dependency direction: nothing in `Route/` may name Atlantic Fields.

---

## Design

### Cache geographic coordinates, never Unreal coordinates

The routing API returns WGS84 lon/lat. The temptation is to convert once, cache the resulting
vectors, and be done. That breaks the moment the georeference origin moves — an origin edit, or
origin rebasing near the camera, silently invalidates every baked point with no error to catch it.

So the cache stores `lon, lat, height` and conversion happens at spline build time. It costs one
transform per point on a construction-script rebuild, which is nothing, and the cache then survives
an origin change, a level split, and a second property with a different origin.

This also settles where the origin lives: `Sites/AtlanticFields/Data/DA_AtlanticFieldsGeo`, not the
level. Every screen on the property shares one origin, and `Route/` reads it through the data asset
instead of finding a georeference actor by name.

### Height comes from the tileset, not from a trace

A line trace against 3D Tiles hits only what is currently streamed, and tileset LOD is driven by the
render camera — so a trace's answer depends on where the camera happens to be looking.
`Cesium3DTileset` exposes `SampleHeightMostDetailed`, which loads the most detailed tiles covering
the query points regardless of the current view and returns per-point success flags. It is
asynchronous.

That asynchrony is why the drape belongs at bake time, not per frame:

| | Bake (chosen) | Per frame |
|---|---|---|
| Cost | one async batch per route | a sample per point per frame |
| Determinism | same result every run | depends on streaming state |
| Failure mode | visible at author time, per point | pops mid-presentation |

Sampled height plus an offset, so the route floats above the surface rather than z-fighting it. The
offset has to scale with camera distance or it vanishes at regional range; seed it from the fixed
camera's distance and treat it as a dial.

### Straight segments, rounded corners only

A road-following route through a spline set to `Curve` everywhere bulges off the roads between
points. Set every point `Linear`, then build each interior corner explicitly: replace vertex `V` with
two points at distance `r` back along each leg, and give those two points tangents along their legs.
The segment between them is the only curved piece.

This is the mockup's `L … Q … L` construction, and it makes `r` the single shape dial. `r` is in
world units, so a corner whose legs are shorter than `2r` would overshoot — clamp `r` per corner to
half the shorter leg.

### Draw-on by masking, not by rebuilding

The presentation reveals the line from A to B. Two ways, and only one is cheap:

- **Rebuild the spline mesh chain each frame** to the current length — a full component rebuild per
  frame, and the leading edge steps by whole segments.
- **Build the chain once, mask in the material** — bake normalized distance-along-route into each
  spline mesh segment (UV channel or per-instance custom data), then clip where it exceeds a
  `Progress` scalar. One parameter write per frame, sub-segment precision at the leading edge.

The second. It also gives the leading-edge falloff and the endpoint reveal off the same scalar.

---

## Implementation

### 1. `Content/Sites/AtlanticFields/Data/DA_AtlanticFieldsGeo`

Origin `lon / lat / height`, the fixed camera's geographic pose, and the presentation dials
(`RouteWidth`, `SurfaceOffset`, `CornerRadius`, `DrawDuration`). Property-level, shared by every
screen.

### 2. `Content/Sites/AtlanticFields/RegionalMap/Routes/`

One JSON per POI holding the A→B point list as `lon, lat` pairs plus a travel time. The same shape
the routing API will fill later, so the loader written now is the loader used then. Follows hhwv's
`Content/<Feature>/JSON/` precedent.

### 3. `Content/Route/Blueprints/Sys/`

- `S_RoutePoint` — `Longitude`, `Latitude`, `Height`, `bHeightSampled`
- `S_RouteData` — `TArray<S_RoutePoint>`, `TravelTimeSeconds`, `SourceId`
- `E_RouteState` — `Idle`, `Sampling`, `Drawing`, `Complete`, `Failed`
- `FL_RouteGeo` — geo→Unreal conversion, corner insertion, arc-length parameterization. Pure
  functions, no actor references.

### 4. `Content/Route/Blueprints/BP_Route`

Spline component plus a spline mesh chain. Construction script: load `S_RouteData` → convert through
the georeference → insert corner points → set point types → build the chain, writing normalized
distance into each segment. Runtime: drive `Progress` 0→1 over `DrawDuration`, publish state changes
through `BPI_Route`.

Takes its parameters as inputs. It does not read the data asset itself — the level or screen
blueprint passes it in, which is what keeps `Route/` property-clean.

### 5. `Content/Route/Materials/M_RouteLine`

Unlit, translucent, depth test **on** — hills should occlude the route. Clips on `Progress` vs baked
distance. Parameters for colour, width, and leading-edge falloff. The property's brand values live in
`Sites/AtlanticFields/RegionalMap/Materials/MI_RouteLine_AtlanticFields`.

### 6. `Content/Sites/AtlanticFields/RegionalMap/Maps/RegionalMap_Proto.umap`

World Partition **off** — `Cesium3DTileset` runs its own LOD and does not stream as a WP actor.
Contents: `CesiumGeoreference` (origin from the data asset), the tileset, `CesiumSunSky`, a fixed
`CineCameraActor`, one `BP_Route`, and a replay trigger.

---

## Verification

- **Regional legibility** — route readable at the fixed camera distance; line width holds, no aliasing crawl
- **Terrain drape** — fly the editor camera along the route: no point buried in a hill, none floating over a valley
- **Sample failure** — force a miss (query off-tileset) and confirm the point is flagged, not silently placed at height 0
- **Corner shape** — segments stay on the road centreline, only corners curve; legs shorter than `2r` clamp instead of overshooting
- **Draw-on** — leading edge advances smoothly and sub-segment; endpoint reveal lands with the line
- **Origin independence** — move the georeference origin a few hundred metres and rebuild: the route lands in the same geographic place
- **Property cleanliness** — reference viewer on every asset in `Route/`: zero references into `Sites/`
- **Cold start** — fresh clone, empty request cache: the route still bakes as tiles load on demand

---

## Open

1. **Georeference origin.** Needs the actual survey coordinates for Atlantic Fields. Everything else
   here is dial-tuning; this one is a fact to be supplied.
2. **Which tileset.** Cesium World Terrain + imagery, or Google Photorealistic 3D Tiles? The mockup
   implies photoreal context. Google 3D Tiles carries different licensing and has no terrain-only
   mode, which changes both the look and the drape offset.
3. **Route source for the prototype.** Hand-authored points, or one real API response captured to
   JSON now? The second costs about an hour and makes the loader real instead of a placeholder.
4. **How many screens does the app have?** The Figma prototype could not be read (auth-gated). If
   Regional Map is one of several screens, the `Sites/<Property>/<Screen>/` layer earns its keep; if
   it is effectively the whole app, that layer should collapse.
5. **Scaffold submodule timing.** Decided: prototype locally now, migrate later — `README.md`
   §Reuse Path records what the migration costs. Revisit if the camera work starts before the route
   lands.
6. **Nothing is committed.** The project needs a first commit with LFS already in place. Doing it
   after content lands means a `git lfs migrate` and a team-wide reclone.
