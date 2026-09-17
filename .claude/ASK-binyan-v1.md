# ASK — Binyan, V1 후속 질문/요청 (AVC-5698)

**상태: 팀 내부 확인 대기.** 아래 §2의 영문 메시지를 Binyan에 보내기 전에 Cameron 확인을 받는다.

> 이 문서는 `dlc-atlanticfields-unreal`에 있다 — 폴더·레벨·애셋 네이밍 규칙의 단일 출처가
> 이 저장소 [`README.md`](../README.md)이고, Binyan 빌드의 목적지도 이 트리이기 때문이다.
> 빌드 성능 측정 플랜은 `dlc-atlanticfields-masterplan`에 남아 있다.

---

## 0. 이 개정에서 바뀐 것 (2026-09-09)

[MIGRATION-content-map.md](MIGRATION-content-map.md)의 실측 분류가 이 문서 초안 세 곳을
무효화했다. 셋 다 반영했다.

1. **폴더 구조 요청이 `Maps/` 한 줄이었다.** 그것만 보내면 Binyan은 *무엇을* 그 밑에 넣어야
   하는지 알 수 없고, 더 나쁘게는 **Fab·Megascans·Substance까지 같이 옮길 수 있다.** §2-2를
   목표 트리 + 판별 규칙 + **손대지 말 목록**으로 다시 썼다.
2. **§3 "import sources" 요청은 어메니티를 버리라는 말이었다.** `SourceAssets/`에는 임포트
   중간물이 아니라 **작성 레벨 44개**가 들어 있다(`AMENITY_CH_Health.umap`, `RESI_Avalon.umap`
   …). 제3자 라이브러리는 `ExternalAssets/`(14 GB)이고 성격이 완전히 다르다. 요청을 후자로
   교체했다.
3. **질문 1이 그들이 이미 한 일을 못 본 것처럼 읽혔다.** `BP_OrbitPawn`,
   `BP_BuildingDirector`, `BP_Building_Master`, `E_BuildingLayer`, `S_Layer*`, `BPI_Peelable` —
   오빗 카메라와 건물 레이어/필링 시스템이 이미 있다. "실시간 최적화 했나요?"가 아니라 "어디까지
   갔나요?"로 바꿨다. 우리가 재사용할 수 있는지를 곧바로 묻는 쪽이 훨씬 값있다.

4. **블루프린트·enum·구조체·머티리얼도 `CommunityMap/` 안으로.** 초안은 `BP_OrbitPawn`,
   `E_BuildingLayer`, `S_Layer*`, `BPI_Peelable`, 그리고 공용 마스터 머티리얼을 루트에 남기라고
   했다. 우리 트리 안에서는 맞는 분류지만 **납품 경계로는 틀렸다** — 아래 §1 "경계선은 …" 참조.
   MIGRATION §B도 같이 뒤집었다.

파일 단위 매핑은 **보내지 않는다.** 우리 분류도 폴더명으로 추정한 것이라 틀린 곳이 있다 —
`Meshes/Architecture`와 `Meshes/Art`는 마스터플랜이 아니라 CaraCara 자산이었다. 자기 콘텐츠는
Binyan이 우리보다 잘 안다. 버킷과 규칙만 주고 배치는 그들에게 맡기는 편이 정확하고 짧다.

---

## 1. 내부 노트 (먼저 읽을 것)

### 왜 지금 상세 성능 측정이 아니라 질문인가

AVC-5698은 프레임레이트·로드 시간·카메라 안정성 측정을 요구하지만, **V1은 8/27 알파 납품이고
최종은 아직 앞에 있다.** 이 단계에서 1% low와 밀리초 단위 기능별 비용표를 만들어도 V2가 오면
숫자가 갈리고, 무엇보다 **그 숫자로 답할 수 없는 질문이 먼저 있다**: 이 빌드가 애초에 실시간을
겨냥해 만들어진 것인지, 그리고 우리 프로젝트로 들어올 수 있는 형태인지.

두 질문의 답이 측정 계획 자체를 바꾼다:

- 실시간 최적화가 **안 된** 상태라면, 지금 측정하는 것은 오프라인 렌더 설정의 비용이고 그건
  이미 예측 가능하다(설정 몇 개를 끄면 사라진다). 측정 가치는 V2 이후에 생긴다.
- 지오메트리·머티리얼이 실시간 예산으로 작성**되었다면**, 남은 격차는 설정뿐이고 우리가 하루면
  해결한다. 그러면 이 이슈는 리포트가 아니라 설정 권고 한 장으로 끝난다.

그래서 **이번 패스의 산출물은 성능 리포트가 아니라 이 두 답**으로 두는 것을 제안한다. 하네스와
카메라 경로는 계획대로 만들되(V2·V3에 재사용), 정밀 측정은 V2에 붙인다.

### 폴더 구조 요청의 타이밍

`__ExternalActors__` 트리가 레벨 패키지 경로를 그대로 따라가기 때문에, **레벨 경로는 작성
시점에 맞아야 한다.** V2를 작성한 뒤에 옮기면 일반 애셋 이동보다 훨씬 지저분하다 —
`SITE_SurroundingLandscape` 하나에 딸린 외부 액터가 657 MiB, `RESI_CaraCara_Main`이 621개다.
지금은 Binyan 쪽 비용이 거의 없고, V2 이후에는 소급 작업이 된다. 요청 창이 지금이라는 뜻.

### 요청에서 "옮기지 말 것"이 "옮길 것"보다 중요하다

36 GiB 중 화면 고유 콘텐츠는 약 3 GiB고, **17.5 GiB가 제3자 라이브러리다.** "우리 구조로
루팅해 달라"만 보내면 Binyan이 성실하게 `Fab/Megascans`까지 옮길 수 있는데, 그러면:

- Fab/Bridge·Substance·Dash는 모두 **고정 경로에 재설치한다.** 옮긴 사본은 다음 업데이트 때
  갱신이 아니라 **중복**으로 생긴다.
- RegionalMap이 같은 나무·같은 하늘을 쓰게 되면 화면 밑에 묻힌 사본은 **화면→화면 참조**를
  강제한다. `dlc-atlanticfields-unreal` README가 금지하는 의존 방향이다.
- 리다이렉터 수천 개가 남고 얻는 게 없다.

그래서 §2-2는 트리와 함께 **표로 된 예외 목록**을 같이 보낸다. 근거는
[MIGRATION-content-map.md](MIGRATION-content-map.md) §C·§F.

실측 크기 (2026-09-09, `Content/` 기준):

| 손대지 말 것 | 크기 |
|---|---|
| `ExternalAssets/` | 14 GiB |
| `Fab/Megascans/` | 1.9 GiB |
| `Polygonflow/` | 1.2 GiB |
| `Megaplant_Library/` | 775 MiB |
| `__ExternalActors__/` | 662 MiB |
| `Maps/_GENERATED/` | 20 MiB |
| `__ExternalObjects__/`, `Developers/`, `Collections/` | ~0 |

### 팀이 승인해줘야 하는 것 세 가지

1. **`CommunityMap`이라는 폴더명.** IA PDF 제목이 "Masterplan Information Architecture"이고 그
   안의 한 브랜치가 "Masterplan (Community Map)"이므로, `Masterplan/`은 제품 전체를 뜻하게 되고
   `RegionalMap/`의 형제로 두면 범주가 어긋난다. 뒤집는 것도 합리적이니 판단만 받으면 된다.
2. **이 메시지는 Binyan에게 "당신들 빌드가 우리 프로젝트의 한 화면으로 들어간다"는 사실을
   알리게 된다.** 계약·범위상 지금 알려도 되는지 확인 필요.
3. **수신자.** 8/27 납품 담당은 Jack Arnold로 기록돼 있어 그 앞으로 썼다. 맞는 창구인지 확인.

### 경계선은 "메커니즘 vs 프레젠테이션"이 아니라 "작성 vs 설치"다

초안은 이 저장소 README의 판별 규칙 — *두 번째 DLC 속성이 수정 없이 쓸 수 있으면 메커니즘,
루트로* — 을 그대로 Binyan 요청에 옮겼다. **우리 트리 안에서는 맞지만 납품 경계에는 맞지 않는다.**

- **Binyan은 RegionalMap을 모른다.** 무엇이 화면을 넘어 재사용될지 판단할 근거가 그들에게 없다.
  모르는 기준으로 분류하라고 하면 틀리게 분류한다.
- **우리도 아직 모른다.** `BP_OrbitPawn`이 `Scaffold/Vista`로 승격될지 우리 카메라로 대체될지는
  인터랙션·성능 평가가 끝나야 나오는 답이다. 그 전에 트리를 확정할 이유가 없다.
- **납품은 통째로 교체 가능해야 한다.** V2가 오면 `CommunityMap/` 하나를 갈아끼우는 게 목표다.
  루트에 흩어져 있으면 납품마다 재분류가 붙고, 그때마다 어느 쪽이 최신인지 따져야 한다.
- **승격은 싸다.** 레벨이 아닌 일반 애셋은 에디터 안에서 옮기면 리다이렉터가 처리한다. 비싼 건
  레벨 경로뿐이고 그건 §2-2에서 못박았다.

의존 방향 규칙(README의 `Route/` 조항)은 폐기된 게 아니라 **적용 시점이 다르다.** 지금
`CommunityMap/` 밑에 있는 것은 쓰는 화면이 하나뿐이라 화면→화면 참조가 애초에 성립하지 않는다.
규칙이 구속력을 갖는 순간은 RegionalMap이 그 자산을 쓰겠다고 할 때이고, 그때 승격이 선행되면
된다. 승격 후보 목록은 [MIGRATION-content-map.md](MIGRATION-content-map.md) §B.

### 트리에 `Amenities/`와 `Lots/`를 같이 넣은 이유

`CommunityMap/` 하나만 주면 어메니티 4개(1.54 GiB)와 주거 4종(12.3 GiB)이 갈 곳이 없어 결국
그 밑으로 들어온다. 주거가 실시간 지오메트리인지 사전 렌더 미디어인지는 **아직 우리 제품
결정**이지만(MIGRATION §D), 어느 쪽이든 Community Map 화면 콘텐츠는 아니다. 형제 폴더를 미리
열어 두는 쪽이 나중에 12 GiB를 OFPA째로 옮기는 것보다 싸다. Binyan에게는 이 결정 과정을
설명하지 않고 버킷만 준다.

### 이번에 보류한 요청 두 개

플랜(§통합 목적지)은 나중에 고치기 비싼 항목을 다섯 개로 봤는데, 이번 메시지에는 두 개만 넣었다.
보류한 것은 §3에 그대로 두었다 — **둘 다 지금이 가장 싸고 V2 이후에는 비싸므로**, 내부 확인 때
함께 보낼지 결정하는 게 좋다. 특히 `ExternalAssets` 14 GB는 폴더 구조 요청과 같은 작업이라 한
번에 말하는 편이 자연스럽다.

---

## 2. Binyan에 보낼 메시지 (영문, 검토 후 발송)

> **Subject:** Masterplan V1 — couple of questions
>
> Hi Jack,
>
> Thanks for the V1 drop. We've had it open on 5.7.4 and are working out how it slots into the
> wider sales tool. Two things, both easier to sort now than after V2:
>
> **1. How far did the realtime side get?**
>
> Looking through the project, there's clearly realtime work in there already — `BP_OrbitPawn`,
> `BP_BuildingDirector` / `BP_Building_Master` with `E_BuildingLayer` and the `S_Layer*` structs,
> `BPI_Peelable`, and the HISM conversion tooling. Before we build any of that ourselves, we'd
> rather know what you have:
>
> - How far did the orbit pawn and the building layer / peel system get — proven in engine, or
>   scaffolding for later?
> - The config is maxed out across the board (Substrate at 6 closures, Lumen HWRT, RT shadows,
>   VSMs, path tracing on, `r.RayTracing.Culling=0`), which reads as a stills-and-film setup. Is
>   that where V1 was aimed, with realtime to follow?
> - Were the meshes and materials built to a realtime budget? Settings we can retune in an
>   afternoon, geometry we can't, so it helps to know which side the cost sits on.
> - Did you have a target frame rate or hardware to hit? We're setting ours now and want them to
>   line up.
>
> **2. Could V2 land in our folder structure?**
>
> The masterplan is one screen in a bigger tool, and our project already has the Regional Map at
> `/Game/Sites/AtlanticFields/RegionalMap/`. Yours becomes its sibling, so ideally the content you
> author for V2 is rooted like this:
>
> ```
> /Game/Sites/AtlanticFields/
> ├─ CommunityMap/      the masterplan screen itself
> │  ├─ Maps/           AtlanticFields_Masterplan, the buildings level, the surrounding landscape
> │  ├─ Geometry/       meshes authored for this site
> │  ├─ Materials/      Master/, Instances/, Functions/, Postprocess/ — keep your own split
> │  ├─ Blueprints/     actors — orbit pawn, building director, environment props
> │  │  └─ Sys/         enums, structs, interfaces, function libraries (E_*, S_*, BPI_*, FL_*)
> │  └─ Foliage/        foliage types placed on the site
> ├─ Amenities/         the AMENITY_* levels and their geometry
> └─ Lots/              the RESI_* houses — shells and furnishings
> ```
>
> The line we're drawing is **authored vs installed**: everything you built for this project —
> levels, meshes, materials, blueprints, and the enums, structs and interfaces behind them — goes
> under `Sites/AtlanticFields/`. Anything a tool installed or generated stays exactly where it is
> (table below).
>
> That includes the parts of your library that aren't Atlantic Fields specific — the shared
> material masters, the orbit pawn, the building layer structs. They're already a copy inside this
> project, so moving them under the screen folder costs you nothing, and it means we can swap the
> whole subtree when V2 lands instead of re-sorting the root each time. We're deliberately **not**
> asking you to work out which of it might be reusable beyond this screen — that's our call to
> make later, and it's a cheap move on our end once we know.
>
> **Levels are the part worth getting right at authoring time.** `__ExternalActors__` and
> `__ExternalObjects__` mirror level package paths, so a level that moves later drags its whole
> OFPA tree with it — `SITE_SurroundingLandscape` alone carries 657 MiB of external actors.
> Ordinary assets we can move on our end with redirectors; levels we'd much rather were authored
> in place.
>
> **What we're specifically *not* asking you to move.** Anything a tool owns or generates should
> stay exactly where it is:
>
> | Leave alone | Why |
> |---|---|
> | `/Game/Fab/Megascans/` | Bridge writes to that fixed path — a copy elsewhere becomes a duplicate on the next update, not an update |
> | `/Game/ExternalAssets/` — Substance, Maxtree, UltraDynamicSky, ResidentialHouses, Hillside, … | vendor libraries, reinstalled to their own paths |
> | `/Game/Polygonflow/`, `/Game/Megaplant_Library/` | same story — Dash and Megaplant own these |
> | `__ExternalActors__/`, `__ExternalObjects__/` | follows the levels on its own; moving it by hand is what breaks it |
> | `Maps/_GENERATED/`, `Developers/`, `Collections/` | editor-generated and per-user |
>
> Level names we're easy on. If renaming `AtlanticFields_Masterplan` would upset sequences or
> references, leave them and we'll deal with it.
>
> Happy to hop on a call if that's easier — it's a 15-minute conversation if the tree above
> doesn't fit how you work.
>
> Thanks,
> Yuno

---

## 3. 보류 중인 요청 — 함께 보낼지 내부 결정

발송하기로 하면 위 메시지의 2번 뒤에 3~4번으로 붙인다.

> **3. Third-party libraries and the repo**
>
> `ExternalAssets/` is about 14 GB — Substance, the Maxtree packs, UltraDynamicSky, the
> ResidentialHouses pack, some Hillside carryover — and with `Fab/`, `Polygonflow/` and
> `Megaplant_Library/` on top it's roughly half the delivery. Our repo is on Git LFS, so we'd
> rather not version vendor libraries we can reinstall.
>
> Happy for them to stay exactly where they are (see the table above) — what would help is
> knowing the surface: which ones the build actually depends on at runtime, and at what versions.
> If there's a Fab/Bridge or Substance asset list you can export, that covers it.
>
> **4. The landscape**
>
> `SITE_SurroundingLandscape.umap` is 657 MiB in one file, which loads whole and hurts our load
> time. Splittable? If it has to stay as one file, what's the constraint?

내부 확인용 근거 두 가지:

- **`SourceAssets/`는 요청 대상이 아니다.** 임포트 중간물처럼 보이지만 어메니티 4개와 주거
  4종의 작성 레벨 44개가 거기 있다. 배제해 달라고 하면 어메니티를 버리게 된다.
- **플러그인 질문은 뺐다.** `Electron7ad48aeb5e8aV16`은 Electronic Nodes(블루프린트 배선 스타일
  전용 에디터 플러그인, `CanContainContent: false`, 런타임 영향 0)로 확인됐고,
  `PathTracedPanorama`는 오프라인 파노라마용이다. 물을 게 없다.

---

## 관련

- 콘텐츠 분류 실측: [MIGRATION-content-map.md](MIGRATION-content-map.md)
- 플랜: [PLAN-binyan-build-perf.md](../../dlc-atlanticfields-masterplan/.claude/PLAN-binyan-build-perf.md) · [한글판](../../dlc-atlanticfields-masterplan/.claude/PLAN-binyan-build-perf.ko.md) — `dlc-atlanticfields-masterplan` 저장소에 있다
- 폴더명 근거: 플랜 §Why `CommunityMap` and not `Masterplan`
- 목적지 규칙 원본: [README.md](../README.md) §Folder and Naming Conventions — 이 저장소가 단일 출처
