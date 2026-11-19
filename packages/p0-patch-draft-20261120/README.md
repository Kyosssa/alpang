# P0 패치 초안 (2026-11-20, 기술이사) — 기준 main `b89b7b6`

디렉터 지시 6건을 한 번에 적용하는 스크립트와 검증 결과입니다. **이 패치는 main에 직접 반영하지 않았습니다**(초안). 적용은 기획실장 쪽 반영 사슬(동결 → 배포 → 사후 대조)로 하세요.

## 적용
```
py -3.11 -I -X utf8 apply_p0.py <main 체크아웃 경로> 2026-11-20
```
바이트 단위로 읽고 써서 CRLF/LF를 보존하며, 모든 치환은 기대 횟수와 정확히 같을 때만 일어나고 아니면 즉시 중단합니다. 개정일(두 번째 인자)은 실제 배포일로 바꾸세요.

## 반영 내용 (제 환경에서 b89b7b6 사본에 적용해 검증)
| # | 내용 | 결과 |
|---|---|---|
| ① | `market/index.html` noindex 복원 | +39B, `<meta name="robots" content="noindex">` |
| ② | 중복 5쌍: 구 세대 `items/{cash,equip,etc,setup,use}/index.html` 삭제 + `_redirects` 301 | 5개 삭제 · 이 5쪽은 내부 링크·사이트맵 참조 0건 확인 |
| ③ | 개인정보처리방침 보강 | 3항 익명 방문 통계 신설(수집 항목 = `functions/api/hit.js` 실제 코드 기준), 4항 광고 쿠키 고지 + Google 링크 3개, 번호 재정렬, 푸터 중복 링크 정리 |
| ④ | 제목·메타 '후보' 삭제 | items 54쪽의 description·og:description에서 "목록 후보"·"표시명 후보" 삭제. **`guide/hunting`의 "초반 사냥터 후보 비교"는 가이드 고유 제목이라 손대지 않음(결정 필요)** |
| ⑤ | **`sitemap.xml` 고아 태그 제거** | 477~478행 `</url>` 바깥 `<changefreq>·<priority>` 2줄 삭제. 검증: `<urlset>` 직속 자식 98개 전부 `<url>`, 각 `<url>`은 loc 1개와 허용 태그뿐, loc 중복 0 |
| ⑥ | 내부 링크 `.html` 제거 | 6,381건 / 60개 페이지(대상 전부 실재). 적용 후 `.html` 내부 href 0건 |
| ⑦ | 404 5건 정리 | 아래 표 |

변경 파일 목록과 전/후 해시: `CHANGED-FILES.tsv`(삭제 5 · 수정 다수 · 신규 `_redirects`), 대표 diff: `p0-modified.diff`. 적용 후 소스 위생 게이트 `cdn-cgi` 0 · Analytics 0 · beacon 0 (전체 HTML).

## 디렉터 지시와 실측이 다른 점
1. **사이트맵에는 `.html` URL이 처음부터 0개입니다.** 98개 `<loc>` 전부 확장자 없는 URL입니다. GSC의 65건 이상 리디렉션은 **내부 링크의 `.html` 6,423건**(quests 간 선행·후행 링크가 대부분, items 허브 링크) 때문으로 보이며 ⑥이 이를 제거합니다.
2. **`<priority>` 고아 태그는 XML이 깨진 것이 아니라 스키마 위반입니다.** 일반 XML 파서는 통과합니다. '가이드 21장·`/mobs/` 색인이 막혔다'는 인과는 제가 확인할 수 없습니다. 구문 오류는 확실히 제거됩니다.

## 404 5건 처리
| 경로 | 참조 | 처리 |
|---|---|---|
| `/quests/lv-11-30.html` | 검색 인덱스 옛 세대 9개에만 존재(현행 -10·-12에는 0건) | `/quests/`로 301 (`.html` 포함 2행). 현재 11~20·21~30으로 분할된 퀘스트 허브 |
| `/taiwan/guide/ludibrium/` · `/vietnam/guide/ludibrium/` | 저장소 내 참조 0건(번역 페이지가 없음) | 각 언어 홈으로 301. 번역본이 생기면 규칙 삭제 |
| `/assets/cube-data/` | 큐브 계산기 스크립트의 fetch 경로 접두 문자열(`'/assets/cube-data/'+…`)이 URL로 추출된 것으로 보임 | `/calculator/cube/`로 301(디렉터리 요청에만 해당, 하위 JSON fetch는 영향 없음) |
| `/status/` | 저장소 내 참조 0건 | **처리하지 않음(404 유지).** 존재하지 않는 페이지의 정상 응답이며, 무관한 페이지로 보내면 소프트 404로 취급될 수 있습니다. 필요하면 `_redirects`에 한 줄 추가 |

## 적용하지 않은 것 · 후속
- **검색 인덱스 href(`.html`)**: 라이브 -10·-12 및 옛 세대의 17,989건이 `.html`을 가리킵니다. GSC 리디렉션 목록의 원인은 아니지만 클릭 때마다 308을 한 번 거칩니다. 기존 세대를 덮어쓰지 않고 **새 세대(-13) 생성 때** `fix_index_hrefs.py <입력> <출력>`을 적용하세요(변환 시험: 21,250건 중 17,989건 변경, 다른 필드 동일, `.html` 잔존 0).
- `guide/hunting` '후보' 제목: 유지/변경 결정.
- 홈·2.0 메인의 '준비 중' 문구는 디렉터 방침대로 2.0 전환 때 정리.

## 배포 전후 확인 (제가 확인하지 못한 부분)
`_redirects` 301이 Cloudflare Pages에서 의도대로 동작하는지는 **배포 전에는 확인할 수 없습니다**(이 환경에 스테이징 없음). 배포 직후 아래를 확인하세요.
```
curl -sI https://alpang.gg/items/cash/        # 301, Location: /items/cash
curl -sI https://alpang.gg/items/cash         # 200 (cash.html)
curl -sI https://alpang.gg/quests/lv-11-30    # 301, Location: /quests/
curl -sI https://alpang.gg/quests/lv-1-10     # 200
curl -s https://alpang.gg/market/ | grep -c 'name="robots" content="noindex"'   # 1
curl -s https://alpang.gg/sitemap.xml | grep -c '<url>'                        # 98
```
리다이렉트 루프가 생기면 `_redirects`만 되돌리면 됩니다(다른 변경과 독립).
그리고 사이트맵은 배포 뒤 GSC에서 다시 제출·검증하세요. 개인정보처리방침은 **90일 보관(삭제는 운영자 수동 수행, `functions/manage-…`)** 과 Cloudflare 이용 문장이 운영 실제와 맞는지 운영 측 확인이 필요합니다.

## 확인 정보 (참고)
- 삭제한 구 세대 `items/*/index.html`은 신판 `items/*.html`과 canonical만 다른 것이 아니라 내용도 구 세대(크기 작음)였습니다. 삭제로 사라지는 신규 정보는 없습니다(내부·사이트맵 참조 0, 검색 인덱스는 `.html` 형태만 가리킴).
- 총 변경: 파일 삭제 5, 수정 다수, 신규 1, 전체 바이트 −2.47MB (대부분 삭제분).
