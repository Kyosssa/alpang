# 알팡지지 2.0 메인 시안 3차 점검 (2026-11-20, 기술이사)

대상: `packages/main2-preview-20261120/index.html` 25,145B `e564d370…`(커밋 `740748e`). 방법: 이전본과 diff, 로컬 서버에서 실제 렌더·시험, jsDelivr의 Pretendard CSS를 직접 받아 대조. 이미지 실물은 없어 용량은 제출값(히어로 1280×427 104.6KB · 768×512 53.2KB 등) 기준입니다.

## 결론
필수 5건 중 **3건은 해결 확인**, **1건(Pretendard)은 교체했지만 글꼴이 실제로 적용되지 않는 결함**이 있어 수정이 필요하고, 1건(히어로 재단)은 상한 안이지만 여유가 작습니다.

| # | 항목 | 판정 |
|---|---|---|
| ① | 드롭다운 클리핑 | ✓ 해결 확인(아래) |
| ② | preload 삭제 | ✓ `rel="preload"` 0건, `<img fetchpriority="high">` 1건이 LCP 발견을 담당 |
| ③ | 히어로 재단 | ✓ 상한 안 — 단 여유 작음 |
| ④ | Pretendard 동적 서브셋 + preconnect | ✗ **글꼴 이름 불일치로 적용 안 됨** (수정 필요) |
| ⑤ | 권고 3건 | ✓ 갱신일 2026-11-20, 월드맵 `width/height` 64×64(실물과 일치), 수치 '빌드 때 주입' 주석 |

## ① 드롭다운 클리핑 — 해결
`.hero-bleed`의 `overflow:hidden`을 제거하고 이미지 전용 `.hero-media{position:absolute;inset:0;overflow:hidden}`로 분리했습니다. 같은 시험(가짜 결과 10건을 `#sbResults.open`에 넣음)에서 결과 상자 하단이 히어로 하단보다 아래(639 대 300)에 있는데도 경계 아래 30px 지점의 요소가 `sb-badge`, 마지막 항목 위치의 요소가 `sb-item`으로 **드롭다운이 온전히 보입니다**. `.hero-bleed`는 `overflow:visible`, `.hero-media`만 `hidden`임을 계산 스타일로 확인했습니다.

## ③ 히어로 재단 — 상한 안
- 1280w: 1280×427, 104.6KB (상한 110KB의 95%). 768w: 768×512, 53.2KB (상한 60KB의 89%).
- 비율: 데스크톱 히어로 상자(약 2.77:1)에 대해 파일 3:1이라 좌우 약 8%만 잘립니다. 모바일 상자는 거의 정사각이라 768×512(3:2)가 높이 기준으로 줄어들어 확대 문제가 사라집니다.
- `<source>`에 `width="768" height="512"`, `<img>`에 `width="1280" height="427"`을 정확히 지정해 CLS 위험이 없습니다.
- 여유가 작은 점(특히 1280w 95%)은 이후 화질을 올릴 때 상한 초과로 이어질 수 있으니 수정 시 재측정하세요.

## ④ Pretendard — 수정 필요 (재현됨)
- **원인:** 교체한 `pretendardvariable-dynamic-subset.min.css`는 글꼴 이름을 **`Pretendard Variable`** 로 등록합니다(92개 `@font-face`, 직접 받아 확인). 그런데 시안의 `body`는 여전히 `font-family:'Pretendard', …`입니다. 이름이 달라 어느 서브셋도 요청되지 않고, 화면은 `Malgun Gothic`·`-apple-system` 대체 글꼴로 그려집니다.
- **시험:** 시안 로드 후 `document.fonts`에 등록된 패밀리는 `Pretendard Variable` 92개뿐이고 상태는 전부 `unloaded`. `document.fonts.load('16px "Pretendard"', '알팡지지')`는 0개를 불러오고 `'Pretendard Variable'`은 3개를 불러옵니다.
- **수정:** `font-family:'Pretendard Variable','Pretendard',-apple-system,'Malgun Gothic',sans-serif`. (`.sb-wrap input` 등은 `font-family:inherit`라 따라옵니다.)
- **참고:** 동적 서브셋 CSS는 53,513B(이전 정적 CSS 2,966B)로 렌더를 막는 외부 CSS가 커졌습니다. 대신 글꼴 파일은 쓰는 글자의 서브셋만 받습니다. `font-display:swap`은 들어 있습니다. 더 줄이려면 이 CSS를 자체 호스팅하거나(제3자 의존 제거) 필요한 가중치만 담은 서브셋을 쓰는 방법이 있으나 필수는 아닙니다. 이 한 건만 고치면 됩니다.
- 선택: `preconnect`는 `crossorigin` 하나만 있습니다. CSS와 글꼴이 같은 호스트(jsDelivr)라 `crossorigin` 없는 `preconnect`를 하나 더 두면 스타일시트 연결도 미리 열립니다(미세 개선).

## 그 외 확인 (이상 없음)
- 소스 위생: `cdn-cgi` 0 · Analytics 0 · beacon 0 · `mailto` 1.
- 이미지: `loading` 속성 8/12(즉시 4: 로고·히어로·첫 행 스프라이트 2), 상대 경로 0, 구 토큰(`--txt`·`--acc`) 잔존 0, 미정의 CSS 변수 0.
- 이번 토큰 통일(`--text`·`--accent`·`--accent-dark`)로 현행 홈 CSS 이름과 같아졌습니다. 앞서 드린 `.sb-*` 조각(`sb-css-for-main2.css`)은 구 이름이라 그대로 붙이면 안 되지만, 시안 안에 이미 반영돼 있어 문제 없습니다.

## 수정 후 재확인 항목
Pretendard 글꼴 이름 수정본에서 `document.fonts`에 `Pretendard Variable` 서브셋이 실제로 `loaded`가 되는지, 렌더 차단 CSS 크기, 실측 LCP(이미지 실물이 올라온 뒤 3회 중앙값).

## 확인하지 못한 것
이미지 실물(화질·실제 용량), 실제 LCP·CLS 수치, 모바일 폭에서의 드롭다운 위치(좁은 뷰포트 에뮬레이션 불가), `search.js` 실제 결과 항목 모양(시안에서는 가짜 항목으로 시험).
