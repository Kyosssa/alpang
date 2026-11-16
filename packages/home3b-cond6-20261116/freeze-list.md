# 프론트개선 동결 목록 — 다국어 홈 라이브 실물 정정 (③-b 경로 변경 · Claude 판정 커밋 aae0260)

- 스테이징: staging-i18nlivefix-20261116/ (taiwan · vietnam 2파일) · MANIFEST.tsv 0eff81b1…
- 기준본: 저장소 main 현행본 (GitHub API contents 수집 · 해시 검증 후 사용).

## 정정 전후 · 기대 해시 대조

| 파일 | 정정 전 | 정정 후 | 기대 해시 | 일치 |
|---|---|---|---|---|
| taiwan/index.html | 38,098B · d170042d35faf70463d2aea1abbe4f40f746d3a993d9c3e43ec51b5fb7160b28 | 37,950B · 83ba628c517877c8d15af6d9609f2a2be03b5cca8daa3b21401f822c7538a398 | 37,950B · 83ba628c… | ✅ |
| vietnam/index.html | 41,700B · 41579a969360ce226fa9ec56ba87c767b5b1e62c3354f94b1768f9ef252d0dfe | 41,552B · 318085a87354f42b68a69fcf785484841de2b4dae4b3bb58794b9d44afe03bc0 | 41,552B · 318085a8… | ✅ |

## diff 전문 (파일당 2 hunk · 그 외 바이트 무변경 · LF 유지)

- hunk 1 (양 파일 공통): 푸터 문의 링크 href `/cdn-cgi/l/email-protection#<토큰>` → `mailto:alpangland@gmail.com` (href 값만).
- hunk 2 (양 파일 공통): `</body>` 앞 빈 `<!-- Cloudflare Pages Analytics -->` 주석 3개 삭제 (−148B = 주석 3개 분량과 정확히 일치).

## 조건 5 · 6 이행

- 재빌드 금지 표지: home_build.py의 build_locale 앞에 가드 주석 3줄 삽입 — 빌더 현행 20,499B · 129217fc95ce9e5512f7db9cde00280b55add5ef97d8592114d92bce5c703f3a (백업 .bak-20261116-pre-guard).
- 별건 등록: 두 홈 푸터 '이용약관' · '사이트 소개' 한국어 미번역을 재구축 체크리스트의 번역 누락 목록에 등록 (체크리스트 현행 256d5fb2…).

## 배포 후 확인 기준

- 두 홈 소스에서 mailto 1 · cdn-cgi 0 · Analytics 잔재 0.
