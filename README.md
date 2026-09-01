# DLC Atlantic Fields

Atlantic Fields regional map. Renders the route from the community (A) to a
nearby POI (B) on top of the Cesium for Unreal 3D Tiles georeferenced world.

## Requirements

| Item | Version |
|------|---------|
| Unreal Engine | 5.7 |
| Cesium for Unreal | plugin must be enabled |
| Git LFS | 2.x+ |

## Current Phase

**Phase 01 -- prototype.** Draws only the A->B route line from a fixed camera
angle. Camera movement (pole system), ground labels, and CMS/routing API
integration come later.

- Prototype level: `Content/Sites/AtlanticFields/RegionalMap/Maps/RegionalMap_Proto.umap`
- Design doc: 2026-08-20 meeting "Regional Map -- Camera System and Routing", §3

## Folder and Naming Conventions

Follows the conventions used in `hhwv-unreal` and `summerlin-unreal`.
(`natlanding-unreal` is an inherited outsourced structure and is excluded.)

The DLC work is treated as an ongoing platform, not a one-off delivery. The tree
splits on **mechanism vs presentation**, which is not the same as feature vs
property:

- **Mechanism** -- a capability named after what it does (`Route`), reusable by
  any DLC property unchanged. Lives at `Content/` root, the same slot as hhwv's
  `CameraCapture`, `MultiWorld`, and `Drone`.
- **Presentation** -- a screen from the app design, plus the property data that
  fills it. Lives under `Content/Sites/<Property>/<Screen>/`, the same slot as
  summerlin's `Sites/Summerlin/MasterPlan/`.

"Regional Map" is a screen in the Figma design, not a mechanism -- so it sits
under the property, and the reusable half is `Route`.

### Folder Structure

```
Plugins/
└─ Scaffold/                        AV&C framework submodule       (planned)
Tools/
└─ crate/                           shared tooling submodule       (planned)
Content/
├─ AtlanticFields.umap              property entry level           (planned)
├─ CesiumSettings/                  plugin-generated -- do not edit
├─ Route/                           MECHANISM -- georeferenced route splines
│  ├─ Blueprints/
│  │  └─ Sys/                       structs, enums, function libraries
│  ├─ Materials/                    base materials only (M_RouteLine)
│  └─ Maps/
│     └─ Debug/                     mechanism tests in isolation
└─ Sites/
   └─ AtlanticFields/               PROPERTY
      ├─ Data/                      DA_AtlanticFieldsGeo -- shared by every screen
      ├─ Geometry/                  masterplan meshes
      └─ RegionalMap/               SCREEN
         ├─ Maps/                   RegionalMap_Proto.umap
         ├─ Materials/              MI_RouteLine_AtlanticFields
         └─ Routes/                 cached routing API responses
```

Camera work (the Phase 02 pole system) becomes a sibling mechanism folder, not a
subfolder of a screen.

The split rule: if a second DLC property could use it unchanged, it is a
mechanism. If it names Atlantic Fields, or if it is a screen from the design,
it belongs under `Sites/AtlanticFields/`.

`Sites/` is the house term for this slot (summerlin ships `Sites/Summerlin` and
`Sites/Astra` in one repo). "Property" in the DLC hierarchy fills the same slot --
one word, not two.

### Reuse Path

The camera / spline-label / POI domain already belongs to the **Vista** module of
the `Scaffold` plugin, which summerlin consumes as a git submodule from
`avcnyc/scaffold`. Its closest existing siblings are
`Content/Scaffold/Blueprints/BP_RoadLabelSpline`, `BP_POI`, and `BP_VistaPOI`,
with per-site parameterization via `Content/Scaffold/DA_Summerlin` / `DA_Astra`.

`Content/Route/` is therefore a **staging area, not a destination.** It stays in
the project while the mechanism is prototyped, then splits two ways:

| What | Goes to | Why |
|------|---------|-----|
| C++ classes | `Plugins/Scaffold/Source/Vista/` | ships with the submodule |
| Blueprints, materials | `Content/Scaffold/Blueprints/` | `Scaffold.uplugin` sets `CanContainContent: false`, so content stays in the project |
| `DA_AtlanticFieldsGeo` | `Content/Scaffold/DA_AtlanticFields` | matches `DA_Summerlin` / `DA_Astra` |

That migration is a folder move plus a base-class reparent -- not a rewrite --
**as long as the dependency direction stays clean.** The path is the cheap part;
UE redirectors handle a move. What is expensive is a reference pointing the wrong
way, so:

- Nothing under `Route/` may reference anything under `Sites/AtlanticFields/`.
- Nothing under `Route/` may reference project-specific GameMode, GameInstance,
  or player classes.
- Parameterize through the data asset and `BPI_Route` only.

### Level Names

| Level | Purpose |
|-------|---------|
| `Sites/AtlanticFields/RegionalMap/Maps/RegionalMap_Proto.umap` | Prototype -- fixed cam, hardcoded A->B |
| `Sites/AtlanticFields/RegionalMap/Maps/RegionalMap.umap` | Final screen level (planned) |
| `Route/Maps/Debug/RouteSplineTest.umap` | Corner rounding in isolation |
| `Content/AtlanticFields.umap` | App entry (planned) |

- The screen folder carries the identity, so level names stay unprefixed
  (summerlin does the same with `Sites/Summerlin/Maps/Summerlin.umap`)
- Sublevels use `<Base>_1` ... `<Base>_4` (hhwv `CameraCapture_Block_N_1`)
- World Partition levels take the `_WP` suffix
- `Maps/Debug/` is for internal tools only. Demo levels sit directly in `Maps/`.

### Asset Prefixes

| Prefix | Type | Example |
|--------|------|---------|
| `BP_` | Actor Blueprint | `BP_Route` |
| `BPI_` | Blueprint Interface | `BPI_Route` |
| `WB_` | Widget Blueprint | `WB_RouteHUD` |
| `M_` / `MI_` | Material / Instance | `M_RouteLine`, `MI_RouteLine_AtlanticFields` |
| `DA_` | Data Asset | `DA_AtlanticFieldsGeo` |
| `S_` | Struct | `S_RoutePoint` |
| `E_` | Enum | `E_RouteState` |
| `FL_` | Function Library | `FL_RouteGeo` |
| `C_` | Curve | `C_Ease` |
| `FMS_` | Media Source | `FMS_Drone` |

Property-specific assets carry the property name as a suffix
(`MI_RouteLine_AtlanticFields`), matching summerlin's `MI_RoadLabel_Summerlin`.

## Cesium Notes

- **Start with World Partition off.** `Cesium3DTileset` does not stream as a WP
  actor -- it runs its own LOD. WP buys nothing for a fixed-cam prototype.
- **Keep the CesiumGeoreference origin in data, not in the level.** Put the
  origin lat/lon in `Sites/AtlanticFields/Data/DA_AtlanticFieldsGeo` so every
  screen shares one origin, and so the `Route` blueprints never name a property
  (the summerlin `DA_Summerlin` pattern).
- **Never commit `cesium-request-cache.sqlite*`** -- covered by `.gitignore`.
- **The ion token** lives in project settings, so check `Config/DefaultEngine.ini`
  before committing.

## Version Control

UE binaries (`.uasset`, `.umap`, and friends) plus source textures, 3D files,
fonts, and media all go through Git LFS. See `.gitattributes` for the rules.

Once per fresh clone:

```
git lfs install
git lfs pull
git config filter.strip-secrets.clean "sed '/^SecurityToken=/d'"
git config filter.strip-secrets.smudge cat
```

### Git LFS

`.gitattributes` has to be in place **before the first commit**. Binaries that
already landed as plain blobs will not move to LFS when a rule is added later --
that requires rewriting history with `git lfs migrate`.

### The strip-secrets filter

`Config/DefaultEngine.ini` carries `SecurityToken` under
`[/Script/AndroidFileServerEditor.AndroidFileServerRuntimeSettings]` -- the shared
secret the Android File Server uses to authenticate a device connection. The
editor regenerates it per machine, and it has no use in a Windows installation.

`.gitignore` cannot exclude a single line, so `.gitattributes` routes the file
through a `strip-secrets` clean filter instead: the line is removed on the way
into the index, so it never reaches a commit while staying in the working copy
for the editor.

Git will not configure a filter from `.gitattributes` alone, which is why the two
`git config` lines above are part of clone setup. Without them the token gets
committed again -- nothing breaks, but the secret lands in history and every
machine shows a spurious diff on the file.
