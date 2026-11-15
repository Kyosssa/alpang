# VERDICT — onehit 세대 합치기 재상신 (2차) — **승인**
- 판정자: Claude (기술이사) · 2026-11-16 03:20
- 패키지: `packages/onehit-resubmit-20261116/` (커밋 `c0d53f6`)
- 선행 판정: `VERDICT-onehit-세대합치기-재상신-20261115.md` (반려 — 구 동결본 `2f3cb3b0`에 패치 4층 누락)

## 1. 제출물 해시 — 전건 일치
| 파일 | 실측 SHA-256 | 동결 목록 기재 |
| :-- | :-- | :-- |
| `calculator/onehit/index.html` (288,187B) | `71cd17635385014299ae02d0f02895159a13e32db25a0a1ae41e790e3e7b3d2e` | 일치 |
| `onehit_build_skilllookup.py` (60,219B) | `4055f51ec995d2c99271cbf8559ddfeb116138e6f8c602e9dc559c00975e8c51` | 일치 |
| `lookup-data.json` | `17b8b265…` | 일치 |
| `safe-eval.js` | `71b828de…` | 일치 |
| `mobs.json` | `0a50720c…` | 일치 |
| `job-names-for-lookup.json` | `855df474…` | 일치 |
| `skills-with-nameko-full-rev6-20261027.json` | `1809f198…` | 일치 |

## 2. 격리 재생성 — 동결본과 바이트 일치
- 판정자 격리 홈(`onehit-verify-20261116/home/workspace/alpang/`)에 입력 5개만 두고 빌더 정본을 그대로 실행했다(`python -I`).
- 빌더 출력: "mobs: 175 | bytes: 288187".
- 파일 288,826B는 판정자 Windows 텍스트 모드 쓰기의 CRLF 때문이다(639줄분). LF로 정규화하면 **288,187B · `71cd1763…`로 동결본과 바이트 일치**한다. 동결본에는 CR이 없다.

## 3. 현행 저장소본·라이브 대조 — 차이는 푸터 1줄
- 저장소 main `calculator/onehit/index.html`(API contents): 288,230B · `30872f2d…`. 동결 목록 기재와 일치.
- `diff 저장소본 재생성본` 결과는 **251행 1줄뿐**이다.
  - 저장소본의 문의 링크는 `/cdn-cgi/l/email-protection#3d5c51…`이다. XOR 복호화하면 `alpangland@gmail.com`이다(엣지 변환물이 소스에 굳은 것).
  - 재생성본의 문의 링크는 `mailto:alpangland@gmail.com`(정본 형태)이다.
- 라이브(03:1x 실측 288,444B)와 저장소본의 차이는 Cloudflare Pages Analytics 비컨 주입 1곳뿐이다.
- 패치 4층 흔적(GNB 페이드 84%, `#s2CalcBtn` 44px, `.tag,.disclaimer` 왼쪽 정렬, 스킬 조회 div)은 재생성본과 저장소본에 같은 횟수로 있다. 1줄 외 전 바이트가 같으므로 4층 모두 빌더 산출로 들어 있다.
- 빌더 수정 전·후 해시 표(`fecc744f` → `005e85d6` → `4055f51e`)가 동봉돼, 지난 반려 때의 '기록 없는 +84B' 공백이 닫혔다. 수정 전 백업 실물은 받지 않아 판정자가 확인하지 않았다(기록으로 둔다).

## 4. 판정
- **승인.** 동결본 `71cd1763`을 배포해도 된다. 배포하면 문의 링크 결함(소스에 굳은 CF 변환물)도 함께 고쳐진다.
- 배포 순서: 합의대로 검수 QA → 배포 → 고지(`packages/notices/`) → 판정자 라이브 대조.
- 배포 후 합격 기준: 라이브를 엣지 정규화(email-protection → mailto 복원, decode 스크립트·Analytics 제거)한 결과가 `71cd1763`과 일치해야 한다. 소스가 mailto가 되므로 이번에는 Cloudflare가 decode 스크립트를 주입하는 것이 정상이다.
- 이번 승인 범위 밖: `cube_build.py`의 디렉터 픽스 2차(왼쪽 정렬 + keep-all) 미역이식. 제출 문서도 '미완'으로 적었다. 큐브를 재생성하기 전에 역이식과 동결이 따로 필요하다. **그 전까지 큐브는 재생성하지 않는다.**

## 5. 실제 시험 범위
- 했음: 입력 해시 대조, 격리 재생성, 동결본 바이트 대조, 저장소 main 대조, 라이브 대조, CF 토큰 복호화.
- 안 했음: 계산기 동작 시험(브라우저에서 계산 결과 확인). 이번 재상신은 세대 합치기(바이트 계보) 판정이고, 계산 로직은 바뀌지 않았다(저장소본과 1줄 차이).
- 증거: `onehit-verify-20261116/` (regen-lf.html, repo.html, live-raw.html, MANIFEST.sha256).

## 6. 배포 후 라이브 대조 — **종결** (2026-11-16 04:17)
- 고지: `packages/notices/20261116-0325-onehit.md`. 커밋 `a7b589c2`(main, 1파일), 사이트맵 96 유지.
- 저장소 main `calculator/onehit/index.html`(API contents) = `71cd1763…`. **동결본과 일치.**
- 라이브 실측 288,552B · `32798656…`.
  - 예상대로 Cloudflare가 mailto를 email-protection 링크로 바꾸고 decode 스크립트를 주입했다. 토큰 1개를 복호화하면 `alpangland@gmail.com`이다.
  - 엣지 정규화(링크 복원, decode 스크립트·Analytics 비컨 제거) 결과는 288,187B · `71cd1763…`로 **동결본과 바이트 일치**한다.
- 증거: `onehit-verify-20261116/post/` (live.html, live-norm.html, repo.html, `post-MANIFEST.sha256`).
- **판정: onehit 세대 합치기 재상신 — 종결.** 큐브 빌더 역이식(§4)은 별건으로 남는다.
