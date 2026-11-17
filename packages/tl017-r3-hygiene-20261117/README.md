# TL-017 r3 소스 위생 정정 — 제출 패키지 (2026-11-17)

판정서 `VERDICT-TL017-라이브대조-소스위생회귀-20261117.md` (73aefa03…)에 대한 정정 제출입니다.
정정은 이미 배포까지 끝난 상태입니다 — 배포 커밋 `c618d987` (main, 6파일), 사이트맵 98 유지.
사업실장이 저장소 main 6파일 해시가 정정 후 기대값과 전건 일치함을 실측했습니다.

## 세대 기준에 대한 답

판정서의 기대 해시는 r1 세대 기준이 맞습니다. 정정 기준 세대는 현행 main 세대입니다:
- 홈 3파일 = r1 동결본 (r2에서 무변경)
- 타임라인 3파일 = r2 동결본 (r2에서 본문 변경: TL-017 카드에 유튜브 커뮤니티 동일 공지 링크 rel 1줄 추가 — 그 외 무변경)

## 정정 전 → 정정 후 (파일당 −113B 전건 일치)

정정 2건만 적용: ① 푸터 문의 링크 href를 mailto:alpangland@gmail.com으로 복원 (−43B) ② </body> 앞 빈 Analytics 주석 쌍 삭제 (−70B). 그 외 바이트 무변경.

| 파일 | 정정 전 | 정정 후 |
|---|---|---|
| index.html | 37,655B · 01da20ab509c3108757b740421dd4441bac2afef396bcaa73f2e5abc90b2fcfb | 37,542B · e5ae6cad59b153e84ac94bb0d78bb489c922d27906a02079782086a8eac3d944 |
| taiwan/index.html | 38,065B · ec430ca14405b6f020fee7d9372287996ee34e0ed69668c4ef9838d659d094b8 | 37,952B · 3e947b47e6c2a25da9811b8fd3dcf34f5f914f8b0fb689eb466f7b7ee4465251 |
| vietnam/index.html | 41,664B · a40d131c5d528f58bb5461290b0589c670946d8b3bf0a36854d22941a0795a87 | 41,551B · 675ac6e35f227aba11b2420353830509ce63497e8b5bd716ef47f04116fa621f |
| timeline/index.html | 87,595B · 239e8fec85741ac3f4c298dc1f0cd46a70c179e52fd2f2da7704bbe6da67a7e9 | 87,482B · d27dd42ce9e7875f891219bd7890e7e58c2794fcd59a12904d59070aaf5780cd |
| taiwan/timeline/index.html | 81,683B · c5ab6ecb8b9b1115102e61cd8590146f74a7251b1779a5a11d6b5041ce5fa4ba | 81,570B · b10b2cc0c3972eda4b38294fdc680c26e665c516d974b5be373f638d2251c2ea |
| vietnam/timeline/index.html | 99,094B · a0120831d05bad234337c4fe095a49ae32cd2585e9bbfaf1313652efad4c8a2b | 98,981B · d629698556c02628b2e9a69ed84f03ca0a1b122fabe1a2abaaca491e0daa74d8 |

홈 3파일의 정정 후 해시는 판정서 기대값과 우연히 일치합니다 (r1 기준 정정과 같은 파일이라 그렇습니다). 타임라인 3파일은 r2 세대라 판정서 기대값과 다릅니다 — 위 표가 새 기준입니다.

실물: before/ (정정 전 6파일), after/ (정정 후 6파일), freeze-list.md (동결 목록 원본).

## 재발 방지 4건

1. 파이프라인 정화 단계: sanitize_html.py (1,713B · 963cfaad…)를 만들어 timeline_build.py 산출 직후 후처리 가드로 연결 (빌드 재실행으로 동작 확인). 동결 제작 시 라이브 수집본에도 같은 스크립트를 적용합니다. 원인 실측: 유입 경로는 빌더가 아니라 동결 기준본인 라이브 수집본이었습니다 (프레임 정본은 mailto 정상 · cdn-cgi 0).
2. 동결 QA 기준 ⑨ (소스 내 cdn-cgi·Analytics 0 · mailto 1) — 이번 r3 동결 QA에서 명시 적용해 전건 통과했습니다 (검수 기록 tl017-r3-freeze-qa-2026-11-17.md).
3. 재생성 금지 표지: 해당 명칭의 표지 파일·문구는 로컬 정본 전역 (프레임 head/foot · 빌더 · site 전수 grep)에서 확인되지 않았습니다. 판정서가 특정 파일을 가리키는 것이면 위치를 알려 주세요 — 해시를 대조해 제출하겠습니다. 갈음 실물로 프레임 정본 해시를 동결 목록에 적었습니다 (ko-foot 0ecb6983… · zh-TW-foot a2693ac2… · vi-foot ce965ea4…).
4. 홈 변경 줄 기록: TL-017 등록에서 홈 3파일의 변경은 dashNews li 3건 교체뿐임을 동결 목록에 기록했습니다.
