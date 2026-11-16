# VERDICT — planner 소스 CF 잔재 정정 재판정 (3e4256c0) — **합격 기준 4종 충족 · planner 통과 · 테마 사슬(허브·planner·early-quests) 전건 종결**
- 판정자: Claude (기술이사) · 2026-11-16
- 패키지: `packages/planner-cfstrip-recheck-20261116/` (커밋 `550c70f`, README `898e26d7…` 1,315B)
- 선행: `VERDICT-테마사슬-planner·허브재적용-라이브대조-20261116.md` (`cc7fef0`, planner 불통과·기대 해시 `7ad1b583…` 사전 지정), 고지 정정 `981780e`
- 증거: `plannerclean-verify/` (planner 2cdfd97c / a0e433d0 / 3e4256c0 / main 세대, 판정자 기대 산출 `expected-planner.html`, 홈·허브·early-quests·사이트맵 main본과 라이브 원본, MANIFEST.sha256 `032edb1e…`)

## 1. 커밋 범위 (API)
- `a0e433d0` (부모 `2cdfd97c`): `planner/index.html` +1/−1. 빈 `<!-- Cloudflare Pages Analytics -->` 주석만 제거했다.
- `3e4256c0` (부모 `a0e433d0`): `planner/index.html` +2/−2.
  - 푸터 문의 링크 `/cdn-cgi/l/email-protection#…` → `mailto:alpangland@gmail.com`
  - timeline 줄 앞의 `email-decode.min.js` 태그 제거
- 대조 시점 main HEAD는 `3e4256c0`이다. 두 커밋을 합치면 처방 ①②③과 정확히 같고, 다른 변경은 없다.
- 참고: `a0e433d0`은 따로 고지되지 않았다. README의 "앞 정정에서 완료분 포함"이 이 커밋을 가리킨다. 중간 세대(12,198B `ebe8791b`)는 배포 직후 다음 커밋으로 덮였고, 판정자는 그 시점 라이브를 보지 않았다.

## 2. 합격 기준 4종
| 기준 | 실측 | 결과 |
| :-- | :-- | :-- |
| ① main = 기대 해시 | main = `3e4256c0`본 = 12,047B `7ad1b583dc7849fe…`. 판정자 기대 산출 `expected-planner.html`과 **바이트 일치** | 충족 |
| ② 라이브 표준 정규화 = 기대 해시 | 라이브 원본 12,412B → 정규화 12,047B `7ad1b583…`, **바이트 일치** | 충족 |
| ③ 라이브 비컨 1 | `beacon.min.js` 1(CF 주입분), Analytics 주석 2(그 블록 앞뒤) | 충족 |
| ④ 소스 cdn-cgi 0 · Analytics 0 · mailto 1 | main본: cdn-cgi 0, Analytics 0, beacon 0, mailto 1, 테마 스크립트 1, CR 0 | 충족 |

- 라이브 원본에는 cdn-cgi 2(email-protection 1, decode 1)가 있다. 소스가 mailto이므로 CF가 주입하는 것이 정상이다(③-b 판정과 같은 이치).

## 3. 주변 무변경 (main · 라이브 정규화)
- 홈 37,542B `b51fe6cc`
- 허브 14,741B `776d2518`(ea041141 판정값)
- early-quests 66,812B `fe8dcd2f`
- 사이트맵 15,634B `119e4009`(`<loc>` 98)

## 4. 판정
- **planner 통과.** 처방 3종이 정확히 적용됐고, 기대 해시가 main과 라이브 정규화 양쪽에서 바이트 일치한다.
- **테마 사슬 전건 종결:**
  - 허브(`ea041141`, cc7fef0에서 통과)
  - early-quests(`fe546358`, 4e62853에서 통과)
  - planner(`3e4256c0`, 이 판정)
- 남겨 두는 사항(종결 조건 아님):
  - `planner_build.py` 수정 발췌와 빌더 해시는 패키지에 없다. 원칙 4(빌더 정정)의 이행은 README의 서술로 수용한다. 다음 planner 재생성 산출이 `7ad1b583`(콘텐츠 변화가 없다면)에서 벗어나 CF 주입물이 다시 나타나면 빌더 미정정으로 본다. 다음 planner 고지 때 빌더 해시를 함께 적어 주기 바란다.
  - 동결 목록 `97ac9789…`와 검수 QA 기록 `b542442e…`는 해시만 인용됐고 실물은 미제출이다.
  - 재발 방지 권고(라이브본을 기준으로 역이식할 때 정규화 본문을 쓴다. 동결 QA에 '소스 내 cdn-cgi·Analytics 0' 항목을 둔다)는 QA 신기준으로 이행됐다고 README에 적혀 있다. 다른 빌더 페이지 전수 점검 권고는 그대로 남는다.

## 5. 실제 시험 범위
- 했음: 두 커밋 변경 파일·부모(API), 4개 세대 저장소본 해시·diff, 기대 산출과 바이트 대조, 라이브 수집·표준 정규화 대조, CF 주입물·mailto·테마 스크립트 수 세기, 홈·허브·early-quests·사이트맵 main/라이브 대조
- 안 했음: `planner_build.py` 실물(미제출), 동결 목록·QA 기록 실물(미제출), 브라우저 렌더링, 중간 세대 a0e433d0 시점 라이브, 다른 빌더 페이지 전수 점검
