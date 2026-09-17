# STATE — Regional Map 경로 프로토타입

`.claude/PLAN-regional-map-route.ko.md`의 진행 상태를 기록한다.
영문판: `.claude/STATE-regional-map-route.md` (내용 동일)

## Phase 현황

| Phase | 이름 | 상태 |
|---|---|---|
| 0 | 세팅 (원점, ion 토큰, 타일셋) | **완료** — 이 플랜을 쓰기 전에 에디터에서 끝냄 |
| 1 | 주소 → 좌표 | **2026-09-17 완료** |
| 2 | 지구본 위의 POI | 시작 전 |
| 3 | 경로 2개 받아오기 | 시작 전 |
| 4 | 경로 그리기 | 시작 전 |
| 5 | 드로우온 및 마무리 | 시작 전 |

## Phase 1 — 2026-09-17 완료

**새로 만든 파일**

- `Tools/poi/geocode_poi.py` — 시트를 받아서 중복 제거하고, Nominatim으로 지오코딩하고, 검증하고,
  JSON과 리포트를 쓴다. 표준 라이브러리만 쓴다(pip 설치 불필요).
- `Tools/poi/overrides.json` — OSM에 없는 주소의 좌표를 손으로 넣는 곳. 지금은 사용법 설명만 들어
  있다. 실제 항목 3개가 아직 필요하다(아래 미결 참고).
- `Tools/poi/REPORT.md` — 스크립트가 생성하는 검증 리포트.
- `Tools/poi/cache/af_poi_raw.csv` — 받아온 시트 탭.
- `Tools/poi/cache/geocode_cache.json` — Nominatim 응답 전부. 그래서 재실행 시 네트워크 호출이 없다.
- `Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json` — **Phase 1의 산출물.**

**수정한 파일**

- `.claude/PLAN-regional-map-route.md` / `.ko.md` — 행 수와 `Distance` 컬럼의 의미를 바로잡음
  (아래 플랜과 달라진 점 참고).
- `.gitignore` — 파이썬 바이트코드 무시 규칙 추가.

**결과**

| | |
|---|---|
| 시트 행 | 46 |
| 중복 제거 후 POI | 40 |
| 좌표를 얻은 POI | 37 |
| 미해결 | 3 |
| 폐업으로 inactive 처리 | 3 |
| 검토 플래그 | 13 |

Phase 3에서 쓸 예시 POI 2개는 둘 다 건물 수준(`place_rank` 30)으로 해결됐다.
Hobe Sound Social + Coffee `27.059563, -80.128983`, Jupiter Medical Center `26.924122, -80.094573`.

**검증 실행 결과**

- 캐시가 있는 상태로 다시 돌리면 `AF_POI.json`이 바이트 단위로 동일하다
  (md5 `f71911e2…`, 전후 동일)
- `--offline`로 다시 돌려도 성공한다. 캐시만으로 네트워크 호출이 0회라는 뜻이다.
- JSON의 원점이 레벨과 일치한다: `lat 27.064, lon -80.215`

## 플랜과 달라진 점

1. **시트는 62행이 아니라 46행이다.** 62는 플랜을 쓸 때 요약해서 가져온 값이라 틀렸다. 플랜 두
   파일 모두 고쳤다.
2. **`Distance` 컬럼은 직선거리가 아니라 자동차 주행거리다.** 원본 워크북에서 확인했다. 공항 탭에
   둘 다 적혀 있는데, Palm Beach International이 직선 27 mi / 주행 약 32 mi이고, 시트에는 34.0이
   들어가 있으며, 우리가 계산한 직선거리는 27.20이다. 그래서 검증 규칙을 ±15% 양방향 허용에서
   한쪽 방향 검사로 바꿨다. 주행거리는 직선거리보다 짧을 수 없기 때문이다. 이걸로 잘못된 플래그
   12개가 사라졌다.
3. **공원과 보호구역은 도로명 수준 정밀도 검사에서 뺐다.** 공원은 폴리곤 중심점으로 잡혀서
   `place_rank`가 낮게 나오는데, 마커는 바로 그 중심점에 있어야 맞다. 잘못된 플래그 2개가 사라졌다.
4. **이름 기준 중복 제거를 한 번 더 추가했다.** Hobe Sound Beach가 서로 다른 주소 2개로 두 번
   들어가 있다. 이름만으로 합치면 위험하니까, 시트 거리가 1마일 이내로 같을 때만 합치게 했다.
5. **`Tools/poi/overrides.json`을 추가했다.** 플랜에 없던 것이다. 플랜은 "플래그된 행을 손으로
   고친다"고만 했는데, 그 손질을 여기 두어야 재실행해도 지워지지 않는다.

## 미결 — Phase 2로 넘김

1. **OSM에 없는 주소 3개.** Palm City Farm Camp, Treasure Coast Wildlife Center, Two Brother's
   Pizza에 좌표가 없다. 직접 찾아서 `Tools/poi/overrides.json`에 넣어야 한다. 셋 다 Phase 3의 예시
   POI가 아니라서 블로킹은 아니다.
2. **Hobe Sound POI 전부에서 직선거리가 시트의 주행거리보다 조금씩 길게 나온다.** 11개 전부에서
   1~1.4마일 정도 일관되게 길다. 한 행만 그러면 지오코딩이 틀린 것이지만, 전부 그러면 원점 쪽
   문제다. 마케팅 거리가 현재 레벨의 지오레퍼런스 원점보다 약 1마일 동쪽 지점을 기준으로 측정된
   것으로 보인다. 주소 자체는 제대로 지오코딩됐고 Phase 3에서 OSRM이 실제 원점에서 경로를 계산하니
   막히는 건 없다. 다만 클라이언트가 어느 점을 기준으로 삼는지는 확인해 두는 게 좋다.
3. Phase 0에서 남은 크레딧 체크박스. 타일셋의 `Show Credits on Screen`이 아직 꺼져 있다.

## 재개 지점

**Phase 2 — 지구본 위의 POI부터 시작한다.** `Content/POI/` 아래에 `S_POI`, `BP_POIMarker`,
`BP_POISet`을 만들고, `Content/Sites/AtlanticFields/RegionalMap/POI/AF_POI.json`을 로드해서, active
POI마다 `CesiumGlobeAnchor`로 고정 마커 높이에 마커를 배치한다. `Content/POI/` 아래 어떤 것도
Atlantic Fields를 참조하면 안 된다.
