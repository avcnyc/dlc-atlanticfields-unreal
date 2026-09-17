# 플랜 — Regional Map 프로토타입: POI 좌표 → Cesium → A→B 자동차 경로

**티켓:** [AVC-5719 — Track A | Cesium](https://linear.app/av-controls/issue/AVC-5719)
**레벨:** `Content/Sites/AtlanticFields/RegionalMap/Maps/RegionalMap_Proto.umap`
**작성:** 2026-09-17 · **영문판:** `.claude/PLAN-regional-map-route.md`

---

## 목표

1. 스프레드시트의 주소 46개를 lon/lat으로 바꾼다.
2. 그 POI들을 Cesium 지구본에 표시한다.
3. 그중 2개를 고른다. Atlantic Fields에서 각 POI까지 실제 자동차 경로를 그린다. 구글 지도처럼 실제
   도로를 따라간다.

프로토타입이다. 카메라 고정. 라벨 없음, 카메라 이동 없음, CMS 없음.

| AVC-5719 항목 | 여기서는 |
|---|---|
| 1. Environment | Phase 0 (완료) |
| 2. Routing | Phase 1–5 |
| 3. 카메라 pole · 4. Flags · 5. Highlighting | 범위 밖 |

---

## 이미 세팅된 것

| 항목 | 값 |
|---|---|
| 지오레퍼런스 원점 | **lat 27.064, lon -80.215** |
| Cesium ion 토큰 | 설정됨 |
| 타일셋 | **Google Photorealistic 3D Tiles**, ion 애셋 `2275207`, `Source: From Cesium Ion` |
| 레벨에 있는 것 | `CesiumGeoreference0`, `CesiumSunSky`, `CesiumCameraManager0`, `CesiumCreditSystemBP0`, `DynamicPawn` |

Google Maps Platform 키는 필요 없다. ion이 Google 타일을 대신 내려준다.

**하나만 고치면 된다:** 타일셋의 `Show Credits on Screen`이 꺼져 있다. 포토리얼 타일은 저작자 표시가
요구사항이다. 이걸 켜거나, Data Attribution 패널에 Google 로고가 나오는지 확인한다. 패키징 빌드에서도
다시 확인한다.

---

## 사용 서비스

둘 다 OpenStreetMap이고, API 키가 필요 없다.

| 용도 | 서비스 | 참고 |
|---|---|---|
| 주소 → lon/lat | **Nominatim** | 초당 1회. 46행 → 고유 주소 40개, 약 1분. User-Agent를 제대로 넣을 것 |
| 자동차 경로 | **OSRM** 데모 서버 | `router.project-osrm.org/route/v1/driving/{lon},{lat};{lon},{lat}?overview=full&geometries=geojson` |

둘 다 스크립트로 **한 번만** 호출하고, 결과를 JSON으로 프로젝트에 저장한다. 런타임에는 아무것도
호출하지 않는다. 그래서 데모 서버에 SLA가 없다는 점은 문제가 되지 않는다.

---

## 결정 세 가지

### 1. JSON에는 lon/lat만 저장한다. 언리얼 좌표는 저장하지 않는다

언리얼 공간으로의 변환은 컨스트럭션 스크립트 시점에 `CesiumGeoreference`를 통해 한다. 언리얼 벡터를
구워두면, 원점을 옮기는 순간 모든 점이 조용히 틀려진다. 에러도 안 난다.

### 2. 지형 높이 샘플링을 하지 않는다. 고정 높이 하나를 쓴다.

포토리얼 타일에는 맨땅 레이어가 없다. `SampleHeightMostDetailed`를 걸면 옥상과 나무 꼭대기 높이가
나온다. 도로 높이를 알 수 없다.

그런데 필요가 없다. Hobe Sound에서 Jupiter까지는 평지다. 경로 지역 전체가 해수면에서 15 m 이내다.
그래서 경로 선을 **타원체 기준 고정 높이 하나**에 둔다(25 m로 시작). POI 마커는 더 높게 둔다(80 m로
시작). 이것만으로 비동기 샘플링 배치, 두 번째 타일셋, 점별 실패 처리가 전부 사라진다.

나중에 실제로 기복이 있는 사이트를 만나면 높이 샘플링을 되살린다. §의도적으로 뺀 것 참고.

### 3. 경로 선은 맨 위에 그린다 (depth test 끔)

포토리얼 타일에서는 나무와 건물이 도로보다 위에 있다. depth test를 켜면 그것들이 선을 점선처럼
끊는다. 여기는 선을 가릴 언덕이 없으니 켜서 얻는 게 없다. 구글 지도처럼 맨 위에 그린다.

---

## Phase 0 — 세팅 ✅ 완료

원점, 토큰, 타일셋 다 들어가 있다(위 표). 남은 건 크레딧 체크박스 하나뿐이다.

---

## Phase 1 — 주소 → 좌표

**왜 필요한가.** 시트에는 글자 주소밖에 없다. Cesium은 숫자가 필요하고, OSRM은 좌표만 받는다. 이
단계는 한 번만 돌리고 그 결과를 계속 캐싱해서 쓴다.

**소스:** [AF Regional POI (WIP)](https://docs.google.com/spreadsheets/d/1-I3zf2qSZ97hkE57KKu4sTeJpDbcRftW96A9NEBWUR4/edit?gid=639708013)의 `gid=639708013` 탭.
헤더 `Category, Name, Address, Distance`. **46행.** 위경도 컬럼 없음.
`Distance`는 직선거리가 아니라 **자동차 주행거리**다. 원본 워크북에서 확인했다. 공항 탭은 둘 다
적어뒀는데, Palm Beach International이 직선 27 mi / 주행 약 32 mi이고 이 시트에는 34.0이 들어가 있다.

**만들 것**

- `Tools/poi/geocode_poi.py` — 시트 받기 → 중복 제거 → 지오코딩 → 검증 → JSON 작성
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

**작업**

1. 시트 탭을 CSV로 받는다. 손으로 고치지 않는다.
2. 이름 + 주소로 중복을 제거한다. 두 번 들어간 행이 있다(병원 전부, The Marketplace, Witham Field).
   행을 합칠 때 카테고리는 둘 다 남긴다 — `The Pine School`은 두 카테고리에 들어가 있다.
3. "Permanently Closed"가 붙은 행은 `active: false`로 둔다.
4. Nominatim으로 주소를 지오코딩한다. 응답을 전부 디스크에 캐싱한다.
5. 결과를 검사한다. 시트가 주행거리를 적어뒀으니 불가능한 경우는 둘뿐이다. 직선거리가 주행거리보다
   길거나, 어떤 우회로도 설명이 안 될 만큼 짧은 경우다. 그 둘을 플래그한다. 거기에
   `lat 26.4–27.7, lon −80.8…−79.9` 밖으로 나가는 것, 그리고 공원·보호구역이 아닌데 도로명 수준보다
   거친 것도 플래그한다.
6. 플래그된 행을 손으로 고치고 다시 실행한다.

**완료 기준.** 모든 POI가 lon/lat을 갖거나 사유와 함께 미해결로 적혀 있고, 미검토 플래그가 없고,
캐시가 있는 상태에서 다시 실행하면 네트워크 호출이 0회다.

**손으로 고칠 게 몇 개는 나온다.** `Hobe Sound Beach — Jupiter Island, FL 33455`처럼 번지가 없는
주소는 동네 중심점으로 간다. 5번이 그걸 잡으려고 있는 단계다.

---

## Phase 2 — 지구본 위의 POI

**만들 것**

- `Content/POI/Blueprints/Sys/S_POI` — `Id`, `Name`, `Categories`, `Latitude`, `Longitude`, `bActive`
- `Content/POI/Blueprints/BP_POIMarker` — 메시 + `CesiumGlobeAnchor`
- `Content/POI/Blueprints/BP_POISet` — `AF_POI.json`을 읽고 POI마다 마커를 하나씩 스폰

`Content/POI/`는 메커니즘 폴더다. 그래서 그 안의 어떤 것도 Atlantic Fields를 참조하면 안 된다.
프로퍼티 데이터는 입력으로 받는다.

**작업**

1. JSON을 `TArray<S_POI>`로 파싱한다.
2. active POI마다 마커를 스폰한다. `CesiumGlobeAnchor`로 lat/lon과 고정 마커 높이에 배치한다.
3. 카테고리로 마커 색을 정한다. 그래야 카테고리가 틀린 게 데이터에 묻히지 않고 눈에 보인다.

**완료 기준.** 모든 POI가 제자리에 있고(5개를 Google Maps와 대조), 포토리얼 건물 안에 묻힌 게 없고,
원점을 옮겨도 제자리에 남는다.

---

## Phase 3 — 경로 2개 받아오기

**선정한 POI 2개.** 같은 문제를 두 번 보지 않도록, 서로 다른 문제를 하나씩 덮는 조합이다.

| | POI | 거리 | 고른 이유 |
|---|---|---|---|
| **B1** | Hobe Sound Social + Coffee, Hobe Sound | 4.6 mi | 짧고 회전이 많다 → 일반 도로를 제대로 따라가나? |
| **B2** | Jupiter Medical Center, Jupiter | 14.5 mi | US-1 / I-95 장거리 → 지역 줌에서 읽히나? |

A는 원점 `27.064 / -80.215`다.

**만들 것**

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

**작업**

1. OSRM을 `overview=full`로 호출한다. 이게 중요하다. 기본값인 `overview=simplified`는 점을 버려서
   선이 눈에 띄게 코너를 질러버린다.
2. OSRM GeoJSON은 `[lon, lat]` 순서로 준다. 우리 JSON은 필드에 이름이 있으니 이름으로 쓰고, 배열을
   그대로 넘기지 않는다. **이 플랜에서 가장 나기 쉬운 버그다.**
3. 확인: `distanceMeters`가 직선거리보다 커야 한다. 더 작으면 좌표가 뒤집힌 것이다.

**완료 기준.** 두 파일이 파싱되고, 첫 점과 끝 점이 A, B와 약 50 m 이내로 맞고, 다시 실행하면 캐시를
쓴다.

---

## Phase 4 — 경로 그리기

**만들 것**

- `Content/Route/Blueprints/Sys/S_RoutePoint` — `Latitude`, `Longitude`
- `Content/Route/Blueprints/Sys/S_RouteData` — `TArray<S_RoutePoint>`, `TravelTimeSeconds`, `SourceId`
- `Content/Route/Blueprints/BP_Route` — 스플라인 + 스플라인 메시 체인
- `Content/Route/Materials/M_RouteLine`
- `Content/Sites/AtlanticFields/RegionalMap/Materials/MI_RouteLine_AtlanticFields`

**작업**

1. `BP_Route` 컨스트럭션 스크립트: 경로 JSON 로드 → 각 점을 지오레퍼런스로 고정 높이에 변환 → 모든
   점을 **Linear**로 스플라인에 추가 → 스플라인 메시 체인 생성, 각 세그먼트에 정규화된 경로상 거리
   기록.
   Linear로 충분하다. `overview=full`이 이미 도로를 촘촘하게 샘플링해 주기 때문이다.
   §의도적으로 뺀 것 참고.
2. `M_RouteLine`: unlit, translucent, **depth test 끔**. 파라미터는 색상, 폭, 그리고 `Progress`
   (Phase 5에서 쓴다).
3. `BP_Route`는 폭·높이·색상을 **입력으로** 받는다. Atlantic Fields 애셋을 직접 읽지 않는다. 레벨이
   넘겨준다.
4. 고정 높이를 먼저 맞춘다. 고정 카메라에서 선이 보이는 도로 위로 올라올 때까지 올린다. 두 경로
   모두에서 확인한다.

**완료 기준**

- 고정 카메라 거리에서 선이 또렷하게 읽히고, 실제 도로를 따라간다
- 두 경로 어디에서도 선이 포토리얼 지면 아래로 꺼지지 않는다
- 원점을 수백 미터 옮기고 리빌드해도 경로가 같은 자리에 온다

---

## Phase 5 — 드로우온 및 마무리

**작업**

1. `DrawDuration` 동안 `Progress`를 0에서 1로 올린다. 머티리얼이 그 값으로 선을 클립해서, 경로가
   A에서 B로 그려져 나간다. 프레임당 파라미터 1개, 리빌드 없음.
2. PIE 재시작 없이 다시 보여줄 수 있게 리플레이 트리거를 넣는다.
3. 두 경로가 그려지는 걸 녹화한다. AVC-5719에 첨부한다.
4. `Content/Route/`와 `Content/POI/`에 레퍼런스 뷰어를 돌린다. `Sites/`로 나가는 참조가 0건이어야
   한다.
5. 새 `.uasset` / `.umap`이 Git LFS에 잡혔는지, `DefaultEngine.ini`가 `SecurityToken` 줄 없이
   커밋되는지 확인한다.
6. 패키징 빌드에서 Google 크레딧이 보이는지 확인한다.
7. 튜닝된 높이와 폭 값을 이 문서에 적는다.

**완료 정의**

> fresh clone에서 `RegionalMap_Proto.umap`을 연다. Atlantic Fields가 Google 포토리얼 타일 위에
> 보이고, 지오코딩된 POI가 전부 배치되어 있고, 자동차 경로 2개 — 짧고 구불구불한 것 하나, 긴 것
> 하나 — 가 실제 도로를 따라 그려져 나간다.

---

## 의도적으로 뺀 것

아래는 이전 초안에 있던 것들이다. 프로토타입을 작게 유지하려고 뺐다. 각각 되살릴 조건을 적어둔다.

| 뺀 것 | 되살릴 때 |
|---|---|
| 지형 높이 샘플링 (숨긴 두 번째 타일셋, 비동기 배치, 점별 실패 플래그) | 실제로 고도차가 있는 사이트를 하거나, 고정 높이가 어딘가에서 눈에 띄게 실패할 때 |
| 코너/커브 분류기 (`E_VertexKind`, `FL_RouteGeo.ClassifyVertices`, 코너 라운딩, 튜닝 다이얼 3개) | 최종 카메라 거리에서 Linear 점만으로 교차로가 이상하게 보일 때 |
| `RouteSplineTest.umap` 디버그 레벨 | 코너 분류기가 되살아날 때 |
| `E_RouteState` / `BPI_Route` 상태 머신 | `BP_Route` 바깥에서 경로 상태에 반응해야 할 때 (예: HUD) |
| 경로 선의 depth test | 선을 가려야 할 언덕이 있는 사이트를 할 때 |

---

## 미결

| # | 질문 | 막는 곳 |
|---|---|---|
| 1 | `Show Credits on Screen`을 켜거나, 저작자 패널에 Google 로고가 나오는지 확인 | Phase 5 |
| 2 | 46행 시트 탭이 확정본인가? 다시 받는 건 싸지만, 아무도 JSON을 손으로 안 고쳤을 때만 그렇다 | Phase 1 |
| 3 | OSM에 없는 주소 3개: Palm City Farm Camp, Treasure Coast Wildlife Center, Two Brother's Pizza. 찾아서 `Tools/poi/overrides.json`에 넣기 | Phase 2 |
| 4 | Hobe Sound POI 전부에서 직선거리가 시트의 주행거리보다 조금씩 길게 나온다. 마케팅 거리가 현재 원점보다 약 1마일 동쪽 지점 기준으로 측정된 것으로 보인다. 어느 점이 맞는지 확인 | 블로킹 아님 |
