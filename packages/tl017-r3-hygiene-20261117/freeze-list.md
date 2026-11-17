# 동결 목록 — TL-017 r3 소스 위생 정정 (CF 흔적 재유입 제거, 2026-11-17)

- 동결 일시: 2026-11-17 18:5x KST (타임라인 담당)
- 사유: 클로드 라이브 대조 판정 불통과 (판정서 73aefa03…, 커밋 f0dca8c) — 콘텐츠·자산은 일치하나 HTML 6파일에 CF 흔적 재유입. 원인 실측: 동결 기준본인 라이브 수집본에 Cloudflare가 변환한 형태 (푸터 문의 링크 email-protection href · </body> 앞 빈 Analytics 주석 쌍)가 남아 있었고, 기존 위생 절차 (비콘·email-decode 스크립트 제거만)로는 걷어내지 못했다. 프레임 정본 (data/timeline/frames/*-foot.html)은 mailto 정상 · cdn-cgi 0으로 깨끗함을 실측 확인 — 빌더 산출이 아니라 라이브 수집본 이식이 유입 경로다.
- 정정 범위: 파일당 정확히 2건만 (그 외 바이트 무변경).
  1. 푸터 문의 링크 href="/cdn-cgi/l/email-protection#..." → href="mailto:alpangland@gmail.com" (−43B)
  2. </body> 앞 <!-- Cloudflare Pages Analytics --><!-- Cloudflare Pages Analytics --> 삭제 (−70B)
  합계 파일당 −113B. 정정 후 전 파일 cdn-cgi · Analytics 잔존 0 실측.
- 기준본: 현행 main 세대 (홈 3파일 = r1 동결본, 타임라인 3파일 = r2 동결본).

## 배포 대상 파일 (6건)

| 배포 경로 | 바이트 | SHA-256 |
|---|---|---|
| index.html | 37,542 | e5ae6cad59b153e84ac94bb0d78bb489c922d27906a02079782086a8eac3d944 |
| taiwan/index.html | 37,952 | 3e947b47e6c2a25da9811b8fd3dcf34f5f914f8b0fb689eb466f7b7ee4465251 |
| vietnam/index.html | 41,551 | 675ac6e35f227aba11b2420353830509ce63497e8b5bd716ef47f04116fa621f |
| timeline/index.html | 87,482 | d27dd42ce9e7875f891219bd7890e7e58c2794fcd59a12904d59070aaf5780cd |
| taiwan/timeline/index.html | 81,570 | b10b2cc0c3972eda4b38294fdc680c26e665c516d974b5be373f638d2251c2ea |
| vietnam/timeline/index.html | 98,981 | d629698556c02628b2e9a69ed84f03ca0a1b122fabe1a2abaaca491e0daa74d8 |

동결본 위치: staging-tl017-r3-20261117/ 아래 배포 경로와 같은 구조.

## 재발 방지 제출

1. 소스 정화 단계 신설: ~/workspace/alpang/sanitize_html.py (1,713B) — 위 2규칙 + 비콘·email-decode 제거 + 적용 후 cdn-cgi·Analytics 0 검증 (잔존 시 실패 종료). timeline_build.py 산출 직후 후처리 가드로 연결 완료 (빌드 재실행으로 동작 확인). 이후 동결 제작 시 라이브 수집본에도 같은 스크립트를 적용한다.
2. 타임라인 재생성 금지 표지: 해당 명칭의 표지 파일·문구는 로컬 정본 전역에서 확인되지 않았다 (프레임 head/foot · 빌더 · site 전수 grep). 가장 가까운 실물은 2단 교체 순서표의 "빌더 재생성 금지 구간" 규칙이며 표지 파일 형태가 아니다. 판정서가 특정 파일을 가리키는 것이라면 위치를 알려 주시면 해시를 대조해 제출하겠다. 갈음 실물: 프레임 정본 해시 — ko-foot 0ecb6983ed012e1457ff79615aacb4b7fda1f5db231e9876647ac3e92e6586c9 · zh-TW-foot a2693ac29e5c12513c522277ce210aa401f18ef9ff6c90fbaa95275c692d776f · vi-foot ce965ea4aa5f7a5e4a2e369581d7b06567b8d580e80297138fb3f0b3d165afcb (전부 mailto 정상 · cdn-cgi 0 실측).
3. 등록 때 홈 HTML 변경 줄 기록: TL-017 등록에서 홈 3파일의 변경은 <ul id="dashNews"> 내부 li 3건 교체뿐이다 (신규 li 1건 삽입 + 기존 3번째 li 제거, 그 외 줄 무변경 — 델타 제거 대조로 확인済).

## QA 요청 기준

- 검수 QA 시 소스 내 cdn-cgi · Analytics 0 기준 (기준 ⑨)을 명시 적용해 주세요.
