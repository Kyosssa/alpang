# 2단 후보본 — 결측 목록 + 피클 추출 요청안 (2026-11-20)

## 후보본 (골격 세대)

| 파일 | 바이트 | SHA-256 |
|---|---|---|
| `obt-prep/t2-candidate-20261120/jobs-candidate.json` | 41,303 | `2306f99ca92c8d37d071750cf6a67342c8fb0a297379af7a4d3f9c1154ff2650` |
| `obt-prep/t2-candidate-20261120/skills-candidate.json` | 3,223,217 | `c6d277e8d9ca1884873fa398dd3e891f8c09d941bb5be73492ce12b5f3d263fb` |

- 책 90 → **98** (신규 8책: 메르 2300 · 2310 · 2311 · 2312 / 캐논 501 · 530 · 531 · 532) · 스킬 610 → **668** (신규 58종).
- 변경 전수 대조: 기존 책 90 · 스킬 610 **전건 무변경** 확인.
- 신규 스킬에 채운 필드: id · name_ko (판정 확정) · max_level (M) · books · has_icon=false. 신규 책에 채운 필드: id · name_ko · skill_count.

## 결측 목록 (원천 부재로 비워 둔 필드)

| 필드 | 대상 | 상태 |
|---|---|---|
| description (desc · shortDesc 영문 원문) | 신규 58종 전건 | 원천 없음 — 피클 확보본 · v2 목록에도 없음 |
| properties_raw (레벨별 수치식) | 신규 58종 전건 | 〃 (판정 확정값은 적용안 · v6_1 층위에 별도 존재) |
| 아이콘 (has_icon) | 신규 58종 전건 | false로 동결 — 추출 뒤 true 전환 |
| 책 name_en · skillbook_sha256 · url | 신규 8책 | GMS 95 원천에 없는 책이라 채울 수 없음 (null + 후보 상태 표기) |
| 스킬 name (영문명) | 신규 58종 | String.wz 영문명 대조로 채울 수 있는 지점 — 추출 요청에 포함 |

## 피클 추출 요청안 (사업실장 경유로 발송)

- 대상: 피클이 보유한 KMS 1.2.160 클라이언트 (work/kms160/)의 Skill.wz · String.wz.
- 요청: 신규 58종 (ID 목록 v2 `b505d3ed…`의 메르세데스 29 + 캐논슈터 29)에 대해 ① 설명문 (desc · shortDesc 한글 원문) ② 레벨별 속성 (properties — 데미지 % · MP · 횟수 등 마스터 레벨 기준) ③ 영문명 ④ 아이콘 PNG (스킬 ID 파일명)를 추출해 claude-exchange `incoming/pickle/`로 반입.
- 주의: 클라이언트 값은 '현행 KMS 1.2.160 값' 층위 — 2012 세트 B 판정값과 어긋나는 지점은 덮어쓰지 말고 대조 지점으로 표시할 것 (소울 어썰트 360% 판정 건과 같은 층위 구분).
