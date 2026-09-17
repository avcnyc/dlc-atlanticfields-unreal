# MIGRATION — Binyan V1 콘텐츠 분류 (무엇이 `CommunityMap/`으로 가고 무엇이 안 가는가)

실측: `D:\Github\dlc-atlanticfields-masterplan\Content\` (2026-09-09, 18,243 엔트리, ~36 GiB).
목적지는 **이 저장소**의 `Content/Sites/AtlanticFields/CommunityMap/`.

> 이 문서는 `dlc-atlanticfields-unreal`에 있다 — 폴더·레벨·애셋 네이밍 규칙의 단일 출처가
> 이 저장소 [`README.md`](../README.md)이고, Binyan 빌드의 목적지도 이 트리이기 때문이다.
> 빌드 성능 측정 플랜은 `dlc-atlanticfields-masterplan`에 남아 있다.

**핵심 수치: 36 GiB 중 실제 CommunityMap 콘텐츠는 약 3–5 GiB다.** 나머지는 제3자 라이브러리
(17.5 GiB), 주거 인테리어(12.3 GiB), 그리고 오프라인 렌더 산출물·에디터 툴·죽은 레벨이다.
"폴더 하나로 옮긴다"가 아니라 **분류 후 1/8만 옮기는** 작업이다.

---

## A. `CommunityMap/` 안으로 — 화면 고유 콘텐츠

| 원본 | 크기 | 목적지 |
|---|---|---|
| `Maps/AtlanticFields_Masterplan.umap` | 0.6 MB | `CommunityMap/Maps/` |
| `Maps/L_AtlanticFields_Masterplan_Buildings.umap` | 9.7 MB | `CommunityMap/Maps/` |
| `Maps/SITE_SurroundingLandscape.umap` | **657 MB** | `CommunityMap/Maps/` — 분할 요청 대상 |
| `Meshes/Masterplan_Datasmith/` | 0.34 GiB (1,856 파일) | `CommunityMap/Geometry/` |
| `Meshes/Environment/`, `Swan/` | 0.18 GiB | `CommunityMap/Geometry/` |
| `SourceAssets/MASTERPLAN/`, `SourceAssets/SITE/` | 0.42 GiB | `CommunityMap/Geometry/` |
| `SourceAssets/AMENITY_*` (4개) | 1.54 GiB | `Sites/AtlanticFields/Amenities/` — PDF상 Community Map의 하위 브랜치지만, 화면 콘텐츠가 아니라 형제 버킷으로 받는다 |
| `Materials/Master/` 전체 | ~0 | `CommunityMap/Materials/Master/` — §B |
| `Materials/Instances/`, `Functions/`, `Postprocess/` | ~0.01 GiB | `CommunityMap/Materials/` — §B |
| `Foliage/Types/` | ~0 | `CommunityMap/Foliage/` |
| `Blueprints/Environment/`, `MASTERPLAN_BP/` | ~0 | `CommunityMap/Blueprints/`, `Sys/` — §B |

**소계 ≈ 3.2 GiB.**

**정정 (2026-09-09):** 이 표의 이전 판은 `Meshes/Architecture/`와 `Meshes/Art/`를
`CommunityMap/Geometry/`로 적었는데, 열어보니 둘 다 CaraCara 자산이다
(`Resi_CaraCara_Door_Ext_005_NoBars`, `SM_CaraCara_Lounge_SlidingDoors_01`, 그리고
`ChamferBox209` 같은 이름 없는 잡물). → §D로 이동. **이 한 건이 Binyan에게 파일 단위 매핑을
보내지 않는 이유다** — 폴더명 추정은 틀린다. 버킷과 판별 규칙만 주고 배치는 그들에게 맡긴다.

`AMENITY_CH_Health`(1.13 GiB)가 어메니티 중 압도적으로 크다 — Clubhouse Health가 PDF의
Fitness Club & Pool / Wellness Centre 계열이라 실제로 콘텐츠가 많은 게 맞지만, 다른 어메니티
3개 합계(0.41 GiB)와의 격차는 확인할 값이다.

---

## B. 메커니즘처럼 보이는 것 — 납품은 `CommunityMap/` 안, 승격은 나중에 우리가

**정정 (2026-09-09).** 이 절의 이전 판은 "여기 넣는 것이 실수다"로 시작해 `BP_OrbitPawn`,
`E_BuildingLayer`, `S_Layer*`, 공용 마스터 머티리얼을 루트로 보냈다. **판단이 바뀌었다 —
블루프린트·enum·구조체·머티리얼은 전부 `CommunityMap/` 밑으로 받는다.** 근거는
[ASK-binyan-v1.md](ASK-binyan-v1.md) §1 "경계선은 …", 요약하면:

납품 경계는 **메커니즘 vs 프레젠테이션**이 아니라 **작성 vs 설치**다. Binyan은 RegionalMap을
모르므로 재사용 여부를 판단할 수 없고, 우리도 평가가 끝나기 전에는 모른다. 그리고 V2가 오면
`CommunityMap/` 하나를 갈아끼우는 것이 목표인데, 루트에 흩어져 있으면 납품마다 재분류가 붙는다.

**의존 방향 규칙이 폐기된 것은 아니다.** 지금은 쓰는 화면이 하나뿐이라 화면→화면 참조가 성립하지
않는다. 규칙이 구속력을 갖는 순간은 RegionalMap이 이 자산을 쓰겠다고 할 때이고, 그때 승격이
선행되면 된다. 레벨이 아닌 일반 애셋의 승격은 에디터 안 이동 + 리다이렉터로 끝난다 — §F의 레벨
이동 비용과 다른 종류의 일이다.

| 원본 | 무엇인가 | 납품 목적지 | 승격 후보 |
|---|---|---|---|
| `Blueprints/MASTERPLAN_BP/BP_OrbitPawn` | 오빗 카메라 폰 | `CommunityMap/Blueprints/` | `Content/Camera/` → `Scaffold/Vista` |
| `BP_BuildingDirector`, `BP_Building_Master` | 건물 레이어 디렉터 | `CommunityMap/Blueprints/` | `Content/Buildings/` 또는 Scaffold |
| `E_BuildingLayer`, `S_LayerActors`, `S_LayerComponents`, `S_LayerInfo`, `S_LayerRule` | 레이어 규칙 enum·구조체 | `CommunityMap/Blueprints/Sys/` | 위와 동일 |
| `BPI_Peelable` | 건물 벗겨내기 인터페이스 | `CommunityMap/Blueprints/Sys/` | 위와 동일 |
| `Blueprints/Environment/` 중 사이트 식생·소품 | 배치용 액터 | `CommunityMap/Blueprints/` | — |
| `Blueprints/Environment/BP_LightFixture_*`, `BP_FramedPicture`, `BP_Couch_Exterior_01`, `BP_Fan` | 주거 인테리어 | `Lots/` (§D) | — |
| `Materials/Master/` 전체 (사이트 전용 + Binyan 공통) | 마스터 머티리얼 33개 | `CommunityMap/Materials/Master/` | 범용분은 평가 후 판단 |
| `Materials/Instances/`, `Functions/`, `Postprocess/` | 인스턴스·함수·포스트프로세스 | `CommunityMap/Materials/` 아래 같은 이름으로 | — |

`Blueprints/Sys/`는 이 저장소 README의 `Route/Blueprints/Sys/` 규약 그대로다 — 구조체·enum·
함수 라이브러리 자리.

**이게 이번 조사에서 가장 값있는 발견이다.** Binyan은 오빗 폰과 건물 레이어/필링 시스템을
이미 만들어 뒀다. 즉 실시간 인터랙션을 어느 정도 작업했다는 증거이고, 우리가 처음부터 만들
필요가 없을 수도 있다는 뜻이다. → §D 하단 "Binyan 질문 수정" 참조.

---

## C. 제3자 라이브러리 — 옮기지 않음 (17.5 GiB, 콘텐츠의 48%)

| 원본 | 크기 | 벤더 |
|---|---|---|
| `ExternalAssets/Substance/` | 4.52 GiB | Adobe Substance |
| `ExternalAssets/ResidentialHouses/` | 4.51 GiB | 마켓플레이스 하우스 팩 |
| `ExternalAssets/Maxtree/` | 2.56 GiB | Maxtree — **summerlin도 `Sites/Astra/ThirdParty/Maxtree` 사용** |
| `Fab/Megascans/` | 1.85 GiB | Quixel / Fab |
| `ExternalAssets/Hillside/` | 1.41 GiB | Binyan 타 프로젝트 캐리오버 |
| `Polygonflow/` (`Assets`, `Materials`, `thebasemesh`) | 1.18 GiB | Polygonflow Dash |
| `Megaplant_Library/` (Black Alder, Goat Willow) | 0.76 GiB | Megaplant |
| `ExternalAssets/UltraDynamicSky/` | 0.50 GiB | UDS — **summerlin도 사용** |
| `ExternalAssets/UltraVolumetrics/`, `3DSky/`, `NiagaraExamples/`, `CustomMotionBlur/`, `RuralAustralia/`, `Adobe/` | 0.15 GiB | 기타 |

### 왜 옮기면 오히려 복잡해지는가

1. **업데이트가 정경로로 재설치된다.** Fab/Bridge, Substance, Dash는 모두 고정 경로에 쓴다
   (`/Game/Fab/Megascans/…`). 옮긴 사본은 다음 업데이트 때 **갱신이 아니라 중복**으로 생긴다.
   리다이렉터가 경로를 이어주더라도 디스크에는 두 벌이 남는다.
2. **화면 간 공유가 깨진다.** RegionalMap이 같은 나무·같은 하늘을 쓰게 되면, `CommunityMap/`
   밑의 사본은 중복 아니면 화면→화면 참조를 강제한다. §B와 같은 문제.
3. **순수 처닝이다.** Megascans/Substance 폴더는 크고 평평하다. 옮겨서 얻는 건 없고 리다이렉터
   수천 개가 남는다.

**목적지 권고:** `Content/ThirdParty/<Vendor>/`를 루트에 두거나, 툴이 쓰는 정경로를 그대로 둔다.
`Fab/`은 후자를 권한다 — Bridge가 거기 쓰기 때문.

**summerlin 선례와 갈리는 지점:** summerlin은 `Sites/Astra/ThirdParty/{Megascans, Maxtree,
UltraDynamicSky, …}`로 **사이트 밑**에 뒀다. 사이트가 독립 앱 하나일 때는 성립하지만, 화면 두
개가 라이브러리를 공유하는 구조에서는 깨진다. 여기서는 선례를 따르지 않는 편이 맞고, 그 판단을
기록으로 남긴다.

---

## D. CommunityMap이 아님 — 별도 결정이 필요한 것 (12.3 GiB)

**주거 모델하우스 인테리어.** 델리버리 자산 수의 다수가 여기다.

| 원본 | 크기 |
|---|---|
| `SourceAssets/RESI_Avalon_Furnishings/` | 3.82 GiB |
| `SourceAssets/RESI_Hamlin_Furnishings/` | 3.66 GiB |
| `SourceAssets/RESI_CaraCara_Furnishings/` | 1.90 GiB |
| `SourceAssets/RESI_Vaccaro_Furnishings/` | 1.43 GiB |
| `SourceAssets/RESI_{Avalon,CaraCara,Vaccaro,Hamlin}/` (셸) | 0.58 GiB |
| `Textures/{Furniture,Books,Art,Produce,Detail}/` | 0.71 GiB |
| `Meshes/Furniture/` | 0.15 GiB |
| `Maps/{Avalon,Hamlin}_Whitecard.umap`, `RESI_*.umap` | 2.4 MB |
| `Blueprints/BP_LightFixture_*`, `BP_FramedPicture`, `BP_Couch_Exterior_01`, `BP_Fan` | ~0 |
| `Dataprep/DPA_Furnishings_*`, `DPAI_RESI_*` | ~0 |

PDF는 이걸 **Lots → Discovery Residences** 브랜치에서 다룬다: *"Renderings of key spaces /
rooms"*, *"Perspective view floor plans and virtual walkthrough"*. 즉 **실시간 지오메트리인지
사전 렌더 미디어인지가 아직 제품 결정이다.** 어느 쪽이든 Community Map 화면 콘텐츠는 아니다 —
`Sites/AtlanticFields/Lots/`로 가거나, 미디어로 빠진다.

이름 대조: PDF의 Discovery Residences는 Avalon·Caracara, Homesites는 Custom·Vacarro·Hamlin·
Clementine. 빌드에는 Avalon·CaraCara·Vaccaro·Hamlin 4종이 있고 **Clementine은 없다** — V2
대상일 가능성.

### 식생 라이브러리 — 경계 사례 (1.74 GiB)

`Textures/{Magnolia 0.88, Adonidia 0.51, Archontopheonix 0.12, OliveTree 0.12, CinnamomumTree
0.09, SyzygiumLeafs 0.02}` + 대응 `BP_Syzygium_*`. **수종 라이브러리**이므로 화면 고유가 아니고,
RegionalMap도 쓸 수 있다. `Content/Vegetation/`에 두는 것을 권하지만, 이 사이트 전용으로
튜닝된 것이라면 A로 넘어간다 — 확인 필요.

---

## E. 안 가져옴

| 원본 | 크기 | 이유 |
|---|---|---|
| `Cinematics/{360, Stills, Prestreaming, Landscape, Misc, Tests}/` | 0.02 GiB | 오프라인 렌더 산출물. 인터랙티브 앱과 무관 |
| `Maps/Archive/`, `*_Backup*`, `*_Old*`, `AtlanticFields_Test`, `SITE_RoughLineup`, `AtlanticFields_InitialSite`, `*_ContextLandscape*` | ~0 | 죽은 레벨 12개. 옮기면 그대로 부채 |
| `Tools/{EditorWidgets, Hillside, PCG}/` | 0.01 GiB | 에디터 툴링. **단 `PCG/PCG_Landscape*`는 랜드스케이프가 PCG 생성이면 필요 — 확인 필요** |
| `Dataprep/` | ~0 | 임포트 자동화, 에디터 전용 |
| `Textures/ReferenceImages/` | 0.15 GiB | 참고 이미지 |
| `Developers/`, `Collections/` | ~0 | 개인 작업물·에디터 메타데이터 |
| `Python/` | ~0 | 우리 하네스가 쓰는 자리. 그들 스크립트는 불필요 |
| `Plugins/Electron7ad48aeb5e8aV16/` | — | **Electronic Nodes** (Hugo Attal) — 블루프린트 배선 스타일만 바꾸는 에디터 플러그인. `CanContainContent: false`, 런타임 영향 0 |
| `Plugins/PathTracedPanorama/` | — | 오프라인 파노라마 렌더용 |

---

## F. 자동으로 따라옴 — 손으로 옮기지 말 것

| 원본 | 크기 |
|---|---|
| `__ExternalActors__/Maps/*` | 0.64 GiB (657 + 하위 레벨별) |
| `__ExternalActors__/SourceAssets/*` | RESI_CaraCara 1,762 · RESI_CaraCara_Furnishings 121 |
| `__ExternalObjects__/` | 43 파일 |
| `Maps/_GENERATED/<user>/` | 20 MiB |

이 트리는 **레벨 패키지 경로를 그대로 미러링한다.** 레벨을 옮기면 따라오고, 따로 옮기면 깨진다.
`Maps/_GENERATED/davidwilliams/`는 에디터가 사용자별로 생성한 것이라 같은 취급이다 — 옮기지
않고, 우리 쪽으로 가져오지도 않는다.
그리고 이것이 Binyan에게 폴더 구조를 *지금* 요청해야 하는 이유다 — 레벨 경로가 작성 시점에
맞아야 한다.

`RESI_CaraCara_Main.umap`이 외부 액터 621개, `__ExternalActors__/SourceAssets/RESI_CaraCara`가
1,762개다. 인테리어가 OFPA로 잘게 쪼개져 있다는 뜻이고, §D 결정이 늦어질수록 이동 비용이 커진다.

---

## 이 조사가 뒤집은 것 — 다른 문서 수정 필요

**1·3·4번은 2026-09-09 `ASK-binyan-v1.md` 개정에 반영 완료** (그 문서 §0 참조). 2·5·6번은
아래 그대로 남아 있다.

1. **`SourceAssets`는 임포트 중간물이 아니다.** 어메니티와 주거의 **작성 레벨**이 들어 있다
   (`AMENITY_AdventurePark.umap`, `AMENITY_FarmHouse.umap`, `AMENITY_CH_Health.umap`,
   `AMENITY_GolfPerformanceCentre.umap`, `RESI_Avalon.umap`, `RESI_CaraCara.umap`, `MASTERPLAN/`).
   → **`ASK-binyan-v1.md` §3의 "import sources" 요청은 어메니티를 버리라는 말이 된다. 발송 전
   수정 필수.** 중간물에 해당하는 건 `ExternalAssets`(제3자)이고, 성격이 다르다.
2. **`ExternalAssets`가 제3자 라이브러리다** — Substance, ResidentialHouses, Maxtree,
   UltraDynamicSky. "28 GB 중간물" 프레이밍은 절반만 맞았고 폴더를 잘못 짚었다.
3. **`Electron7ad48aeb5e8aV16` = Electronic Nodes.** 플랜 §미결 5번 해소. Binyan에 물을 필요
   없음 — 요청 목록에서 빼도 된다.
4. **Binyan은 실시간 인터랙션 기계를 이미 만들었다** — `BP_OrbitPawn`, `BP_BuildingDirector`,
   `BP_Building_Master`, `E_BuildingLayer`, `S_Layer*`, `BPI_Peelable`, 그리고 HISM 최적화 툴링
   (`MeshToHISM`, `WBPU_HISM_Optimization`, `EUW_ConvertHismToFoliage`).
   → **Binyan 질문 1을 수정해야 한다.** "실시간 최적화 됐나요?"가 아니라 "오빗 폰과 건물
   레이어 시스템이 보이는데, 그게 어디까지 갔나요?"가 맞다. 전자는 그들이 이미 한 일을 못 본
   것처럼 읽히고, 후자는 우리가 재사용할 수 있는지를 곧바로 묻는다.
5. **빌드 위치.** 플랜은 `IN/AtlanticFields_Masterplan_V1\`을 작업 사본으로 적었지만 실제로는
   **이 저장소 루트**에 풀려 있다(`Content/`, `Config/`, `Plugins/`… 모두 untracked).
   `.gitignore`가 없으므로 실수로 `git add .` 하면 36 GiB가 들어간다 — **선행 조치 필요.**
6. `SITE_SurroundingLandscape.umap`은 657 MiB(= 689 MB 십진). 같은 값, 단위 표기만 통일.

---

## 관련

- 플랜: [PLAN-binyan-build-perf.md](../../dlc-atlanticfields-masterplan/.claude/PLAN-binyan-build-perf.md) · [한글판](../../dlc-atlanticfields-masterplan/.claude/PLAN-binyan-build-perf.ko.md) — `dlc-atlanticfields-masterplan` 저장소에 있다
- Binyan 요청: [ASK-binyan-v1.md](ASK-binyan-v1.md)
