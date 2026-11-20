# 저스티스 2단 메르세데스·캐논슈터 신규 58종 — KMS 1.2.160 클라이언트 추출본

- 생성: 2026-11-20 (KST)
- 데이터 본체: `justice_t2_merc_cannon_client_extract_20261120.json` (레벨별 수치 전량 포함)
- 아이콘: `t2_merc_cannon_icons_20261120/` (PNG 188장)

## 0. 요청서 미확인 고지

- 요청서 지정 파일: `obt-prep/T2-CANDIDATE-MISSING-AND-EXTRACT-REQUEST-20261120.md (SHA-256 앞 8자리 ac58cfe2)`
- 확인 결과: 저장소(claude-exchange·main 전 ref·전 커밋 이력)에 파일·디렉터리 부재. 본 산출물의 형식·경로·명명은 직전 동일 계열 산출물(incoming/pickle/justice_t2_skill_id_20261119.*, justice_2nd_merc_cannon_12_supplement_20261117) 관례를 따랐다. 요청서 확보 시 형식만 맞춰 재포장한다.
- 따라서 아이콘 형식·영문명 출처·파일 경로 규칙은 **요청서 확정안이 아니라** 직전 동일 계열 산출물 관례와 이 문서에 적힌 규칙을 따른다. 요청서가 확보되면 형식만 맞춰 재포장할 수 있다.

## 1. 요약

- **58종 전건 확보** — 캐논슈터 29종(501·530·531·532.img) + 메르세데스 29종(2300·2310·2311·2312.img). 누락 0.
- **완전성**: 두 직업 8개 이미지의 스킬 노드 70개 중 표시(invisible 아님) 스킬 = 58개 전부. 목록 밖 12개는 전부 `invisible=1`(부속·숨김)이라 58종 목록이 클라이언트 표시 스킬과 정확히 일치한다.
- **M(마스터레벨 = `common.maxLevel`) 판정 일치 58/58**, 불일치 0.
- **설명문·힌트 58/58 확보**(String.wz 원문), 마스터레벨 기준 변수 치환 후 미치환 토큰 0.
- **아이콘 188장**: 기본 3종(icon/iconMouseOver/iconDisabled) × 58 = 174 + 상태 아이콘 변형(icon1~5) 14. 전부 32×32, fmt1(ARGB4444), PNG 무결성 검사 통과·손상 0.
- **영문명**: GMS 명칭 그대로 48, 개칭 이력 있음 5, 대응 불확실(현행 표 KMS명 공백) 5. 전부 **현행(2026) 기준**이며 2012 시점 영문명은 요청서 규칙·별도 근거가 없어 검증하지 않았다.
- **기존 판정값 대조**: 수치 불일치 0. 2단 판정 수치 12건 클라이언트 재계산 일치, 공식 문안(F12·F13) MP 9/10 일치 (F14 하이킥 데몰리션은 2013-03 테섭 변경 후 문안으로 2012 수치와 혼용 금지 — 참고만).
- 아이콘 픽셀 검증: 현행 GMS 아이콘과 32×32 픽셀 단위 완전 일치하는 스킬이 다수(예: 5321010·5320007·5321003) — 캔버스 복호 경로가 실물과 일치함을 확인.

## 2. 기준 클라이언트와 추출 방법

- 버전: KMS 1.2.160 (2012-06-03 파일 날짜)
- 파일: Skill.wz (311,039,146 B) · String.wz (3,717,336 B) (Skill.wz MD5 `a59db2f0bd6b3c355dbeda862f7763ab` · String.wz MD5 `f2e28dbf2ccc754c9c94eaa4e0e5c573`)
- 원본 아카이브: KMS 1.2.160 7z 분할본(part00~06.bin, 합계 2,797,136,045 B) — MD5 5c9608581a444b7bb84445fb3c4e34d1. 기존 ID 목록(justice_t2_skill_id_20261119)이 인용한 MD5가 이 아카이브 값이다(Skill.wz 자체 MD5와 다름).
- 경로: `work/kms160/x/KMS_v2.160/` / 출처: archive.org kms-v1.2.160 배포본(11-19 확보)

추출 방법:
- Skill.wz 이미지(501/530/531/532/2300/2310/2311/2312.img)의 skill 하위 노드를 WZ 바이너리 직접 파싱(BMS 키, v160 해시)
- 아이콘 canvas: width/height/format 헤더 → listWz 블록(int32 길이 + WzKey XOR) 복호 → raw deflate → ARGB4444/ARGB8888 → PNG
- 설명문: String.wz Skill.img의 name/desc/h/pdesc/ph 원문 그대로
- 레벨별 수치: common 블록의 수식을 레벨 1~maxLevel까지 평가(클라이언트는 레벨별 값을 저장하지 않고 수식만 보관)

용어:
- `maxLevel` — WZ common.maxLevel — 스킬 마스터레벨(2단 판정의 M과 같은 값). 58/58 판정 M과 일치.
- `wz_masterLevel` — WZ 노드의 masterLevel — 전투명령(combatOrders)으로 올릴 수 있는 상한(4차 스킬 10). 마스터레벨(maxLevel)과 다른 값이므로 혼용 금지.

변수 치환 규칙: x=스킬 레벨, d()=내림, u()=올림. #토큰 치환은 동일 레벨의 common 값으로 수행. 치환 후 남은 #토큰은 hint_미치환_토큰에 기록.

## 3. 스킬 58종 — 식별자·마스터 수치

수치는 클라이언트 `common` 수식을 마스터레벨에서 평가한 값. `MP`·`데미지`·`대상`·`타수`는 각각 mpCon·damage·mobCount·attackCount.

| # | 직업 | 차수 | 스킬(KMS 1.2.160) | skill_id | img | M | MP | 데미지% | 대상 | 타수 | 영문명(현행 GMS) | 영문 상태 |
|---:|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | 캐논슈터 | 1차 | 캐논 스플래셔 | 5011000 | 501.img | 20 | 11 | 225 | 3 | — | Cannon Blaster | 현행_GMS_확보 |
| 2 | 캐논슈터 | 1차 | 기간틱 백스탭 | 5011002 | 501.img | 15 | 20 | 210 | 3 | — | Blast Back | 현행_GMS_개칭(KMS명 변경) |
| 3 | 캐논슈터 | 1차 | 빌드업 캐논 | 5010003 | 501.img | 10 | — | — | — | — | Cannon Boost | 현행_GMS_확보 |
| 4 | 캐논슈터 | 1차 | 펀칭 캐논 | 5011001 | 501.img | 20 | 9 | 95 | 1 | 3 | Cannon Strike | 현행_GMS_확보 |
| 5 | 캐논슈터 | 2차 | 몽키 러쉬붐 | 5301001 | 530.img | 20 | 28 | 50 | 8 | 3 | Barrel Bomb | 현행_GMS_확보 |
| 6 | 캐논슈터 | 2차 | 몽키 매직 | 5301003 | 530.img | 20 | 55 | — | — | — | Monkey Magic | 현행_GMS_확보 |
| 7 | 캐논슈터 | 2차 | 캐논 마스터리 | 5300005 | 530.img | 20 | — | — | — | — | Cannon Mastery | 현행_GMS_확보 |
| 8 | 캐논슈터 | 2차 | 캐논 부스터 | 5301002 | 530.img | 20 | 11 | — | — | — | 미확보 | 대응_불확실(현행 표 KMS명 공백) |
| 9 | 캐논슈터 | 2차 | 크리티컬 파이어 | 5300004 | 530.img | 15 | — | — | — | — | Critical Fire | 현행_GMS_확보 |
| 10 | 캐논슈터 | 2차 | 파이렛 트레이닝 | 5300008 | 530.img | 10 | — | — | — | — | Pirate Training | 현행_GMS_확보 |
| 11 | 캐논슈터 | 2차 | 슬러그 샷 | 5301000 | 530.img | 20 | 24 | 220 | 4 | 2 | Scatter Shot | 현행_GMS_확보 |
| 12 | 캐논슈터 | 3차 | 몽키 웨이브 | 5311002 | 531.img | 20 | 55 | 860 | 8 | — | Monkey Wave | 현행_GMS_확보 |
| 13 | 캐논슈터 | 3차 | 몽키 파워붐 | 5311001 | 531.img | 20 | 46 | 280 | 10 | 5 | Monkey Madness | 현행_GMS_확보 |
| 14 | 캐논슈터 | 3차 | 캐논 스파이크 | 5311000 | 531.img | 20 | 36 | 240 | 6 | 3 | Cannon Spike | 현행_GMS_확보 |
| 15 | 캐논슈터 | 3차 | 캐논 점프 | 5311003 | 531.img | 15 | 35 | 210 | 6 | — | Cannon Jump | 현행_GMS_확보 |
| 16 | 캐논슈터 | 3차 | 오크통 룰렛 | 5311004 | 531.img | 10 | 60 | — | — | — | Forty Winks | 대응_불확실(현행 표 KMS명 공백) |
| 17 | 캐논슈터 | 3차 | 럭키 다이스 | 5311005 | 531.img | 20 | 60 | — | — | — | Roll of the Dice | 현행_GMS_확보 |
| 18 | 캐논슈터 | 3차 | 리인포스 캐논 | 5310006 | 531.img | 15 | — | — | — | — | Reinforced Cannon | 현행_GMS_확보 |
| 19 | 캐논슈터 | 3차 | 바이탈 익스트림 | 5310007 | 531.img | 20 | — | — | — | — | Pirate Rush | 현행_GMS_개칭(영문명 변경) |
| 20 | 캐논슈터 | 3차 | 반격의 슈터 | 5310009 | 531.img | 15 | — | 160 | — | — | Counter Crush | 현행_GMS_확보 |
| 21 | 캐논슈터 | 4차 | 캐논 바주카 | 5321000 | 532.img | 30 | 75 | 500 | 6 | 4 | Cannon Bazooka | 현행_GMS_확보 |
| 22 | 캐논슈터 | 4차 | 캐논 버스터 | 5321012 | 532.img | 30 | 63 | 320 | 1 | 5 | Cannon Barrage | 현행_GMS_확보 |
| 23 | 캐논슈터 | 4차 | 전함 노틸러스 | 5321001 | 532.img | 30 | 350 | 520 | 15 | 3 | Nautilus Strike | 현행_GMS_확보 |
| 24 | 캐논슈터 | 4차 | 파이렛 스피릿 | 5321010 | 532.img | 30 | 80 | — | — | — | Pirate's Spirit | 현행_GMS_확보 |
| 25 | 캐논슈터 | 4차 | 마그네틱 앵커 | 5321003 | 532.img | 15 | 86 | 400 | 8 | — | Anchors Aweigh | 현행_GMS_확보 |
| 26 | 캐논슈터 | 4차 | 서포트 몽키 트윈스 | 5321004 | 532.img | 15 | 70 | 350 | 1 | — | Support Monkey | 현행_GMS_개칭(KMS명 변경) |
| 27 | 캐논슈터 | 4차 | 더블 럭키 다이스 | 5320007 | 532.img | 5 | 60 | — | — | — | Double Down | 현행_GMS_확보 |
| 28 | 캐논슈터 | 4차 | 하이퍼 몽키 스펠 | 5320008 | 532.img | 30 | 80 | — | — | — | Mega Monkey Magic | 현행_GMS_확보 |
| 29 | 캐논슈터 | 4차 | 오버버닝 캐논 | 5320009 | 532.img | 30 | — | — | — | — | Cannon Overload | 현행_GMS_확보 |
| 30 | 메르세데스 | 1차 | 스피드 듀얼샷 | 23001000 | 2300.img | 20 | 14 | 115 | 3 | 2 | Swift Dual Shot | 현행_GMS_확보 |
| 31 | 메르세데스 | 1차 | 샤프 에이밍 | 23000003 | 2300.img | 20 | — | — | — | — | Sharp Aim | 현행_GMS_확보 |
| 32 | 메르세데스 | 1차 | 아크로바틱 점프 | 23001002 | 2300.img | 10 | 10 | — | — | — | Spirit Jump | 현행_GMS_개칭(KMS명 변경) |
| 33 | 메르세데스 | 1차 | 포텐셜 파워 | 23000001 | 2300.img | 15 | — | — | — | — | Potential Power | 현행_GMS_확보 |
| 34 | 메르세데스 | 2차 | 피지컬 트레이닝 | 23100008 | 2310.img | 10 | — | — | — | — | Physical Training | 현행_GMS_확보 |
| 35 | 메르세데스 | 2차 | 듀얼보우건 마스터리 | 23100005 | 2310.img | 20 | — | — | — | — | Dual Bowguns Mastery | 현행_GMS_확보 |
| 36 | 메르세데스 | 2차 | 듀얼보우건 부스터 | 23101002 | 2310.img | 20 | 11 | — | — | — | Dual Bowguns Boost | 현행_GMS_확보 |
| 37 | 메르세데스 | 2차 | 스피릿 인퓨젼 | 23101003 | 2310.img | 15 | 45 | 15 | — | — | Spirit Surge | 대응_불확실(현행 표 KMS명 공백) |
| 38 | 메르세데스 | 2차 | 차지 드라이브 | 23101001 | 2310.img | 15 | 25 | 130 | 8 | — | Rising Rush | 현행_GMS_확보 |
| 39 | 메르세데스 | 2차 | 파이널 샷 | 23100004 | 2310.img | 5 | 16 | 70 | 8 | 4 | Parting Shot | 현행_GMS_확보 |
| 40 | 메르세데스 | 2차 | 파이널 어택 : 듀얼보우건 | 23100006 | 2310.img | 20 | — | 75 | 1 | 2 | Final Attack: Dual Bowguns | 현행_GMS_확보 |
| 41 | 메르세데스 | 4차 | 어드밴스드 파이널 어택 | 23120012 | 2312.img | 30 | — | 105 | 1 | 2 | Advanced Final Attack | 현행_GMS_확보 |
| 42 | 메르세데스 | 2차 | 크로스 피어싱 | 23101000 | 2310.img | 20 | 24 | 83 | 6 | 4 | Piercing Storm | 현행_GMS_확보 |
| 43 | 메르세데스 | 3차 | 스트라이크 듀얼샷 | 23111000 | 2311.img | 20 | 35 | 120 | 5 | 4 | Stunning Strikes | 현행_GMS_확보 |
| 44 | 메르세데스 | 3차 | 리프 토네이도 | 23111001 | 2311.img | 20 | 45 | 135 | 8 | 4 | Leaf Tornado | 현행_GMS_확보 |
| 45 | 메르세데스 | 3차 | 거스트 다이브 | 23111003 | 2311.img | 20 | 45 | 195 | 6 | 3 | Gust Dive | 현행_GMS_확보 |
| 46 | 메르세데스 | 3차 | 하이킥 데몰리션 | 23110006 | 2311.img | 15 | 32 | 110 | 8 | 6 | Aerial Barrage | 현행_GMS_확보 |
| 47 | 메르세데스 | 3차 | 엘리멘탈 나이트 | 23111008 | 2311.img | 20 | 60 | 550 | — | — | Elemental Knights | 현행_GMS_확보 |
| 48 | 메르세데스 | 3차 | 이그니스 로어 | 23111004 | 2311.img | 20 | 60 | — | — | — | Ignis Roar | 대응_불확실(현행 표 KMS명 공백) |
| 49 | 메르세데스 | 3차 | 유니콘 스파이크 | 23111002 | 2311.img | 20 | 62 | 140 | 8 | 5 | Unicorn Spike | 현행_GMS_확보 |
| 50 | 메르세데스 | 3차 | 워터 쉴드 | 23111005 | 2311.img | 20 | 100 | — | — | — | Water Shield | 현행_GMS_개칭(KMS명 변경) |
| 51 | 메르세데스 | 4차 | 디펜스 브레이크 | 23120010 | 2312.img | 20 | — | — | — | — | Defense Break | 현행_GMS_확보 |
| 52 | 메르세데스 | 4차 | 듀얼보우건 엑스퍼트 | 23120009 | 2312.img | 30 | — | — | — | — | Dual Bowguns Expert | 현행_GMS_확보 |
| 53 | 메르세데스 | 4차 | 이슈타르의 링 | 23121000 | 2312.img | 30 | 10 | 110 | — | 2 | Ishtar's Ring | 현행_GMS_확보 |
| 54 | 메르세데스 | 4차 | 레전드리 스피어 | 23121002 | 2312.img | 20 | 60 | 540 | 12 | 2 | Spikes Royale | 현행_GMS_확보 |
| 55 | 메르세데스 | 4차 | 라이트닝 엣지 | 23121003 | 2312.img | 30 | 74 | 420 | 8 | 3 | Lightning Edge | 현행_GMS_확보 |
| 56 | 메르세데스 | 4차 | 롤링 문썰트 | 23120011 | 2312.img | 20 | 70 | 180 | 8 | 6 | Rolling Moonsault | 대응_불확실(현행 표 KMS명 공백) |
| 57 | 메르세데스 | 4차 | 앤시언트 스피릿 | 23121004 | 2312.img | 30 | 80 | — | — | — | Ancient Warding | 현행_GMS_확보 |
| 58 | 메르세데스 | 4차 | 메이플 용사 | 23121005 | 2312.img | 30 | 70 | — | — | — | Maple Warrior | 현행_GMS_확보 |

## 4. 설명문·레벨별 속성 원문 (58종)

각 항목: String.wz 원문(name/desc/hint)과 Skill.wz `common` 수식, 레벨 1·마스터 값. **전 레벨 수치는 JSON의 `levels` 배열**에 있다(1~maxLevel 전 구간).

### 캐논슈터 (29종)

#### 1. 캐논 스플래셔 (`5011000`, 1차, 501.img)

- 설명(원문): 화염탄을 발사하여 다수의 적을 공격한다.
- 힌트(원문): MP #mpCon 소비, #damage% 데미지로 최대 #mobCount명의 적 공격
- 힌트(마스터 치환): MP 11 소비, 225% 데미지로 최대 3명의 적 공격
- common: `{"maxLevel": 20, "mpCon": "6+u(x/4)", "damage": "185+2*x", "mobCount": "3", "range": "450"}`
- Lv1: `{"level": 1, "mpCon": 7, "damage": 187, "mobCount": 3, "range": 450}`
- Lv20(마스터): `{"level": 20, "mpCon": 11, "damage": 225, "mobCount": 3, "range": 450}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Blaster` / MSEA `Cannon Blaster` — 현행_GMS_확보

#### 2. 기간틱 백스탭 (`5011002`, 1차, 501.img)

- 설명(원문): 후방으로 긴급 회피하며 캐논을 발사한다. 일정 확률로 대상의 이동속도를 감소시킬 수 있다.
- 힌트(원문): MP #mpCon 소비, #damage% 데미지로 #mobCount명의 적 공격, #prop% 확률로 #time초 간 대상의 이동속도 #z
- 힌트(마스터 치환): MP 20 소비, 210% 데미지로 3명의 적 공격, 70% 확률로 5초 간 대상의 이동속도 -60
- common: `{"maxLevel": 15, "mpCon": "45-5*d(x/3)", "damage": "150+4*x", "mobCount": "3", "time": "2+d(x/5)", "prop": "25+3*x", "z": "-15-3*x", "x": "250+d(x/4)*70", "y": "260+d(x/4)*30", "range": "450", "hcTime": "1"}`
- Lv1: `{"level": 1, "mpCon": 45, "damage": 154, "mobCount": 3, "time": 2, "hcTime": 1, "prop": 28, "x": 250, "y": 260, "z": -18, "range": 450}`
- Lv15(마스터): `{"level": 15, "mpCon": 20, "damage": 210, "mobCount": 3, "time": 5, "hcTime": 1, "prop": 70, "x": 460, "y": 350, "z": -60, "range": 450}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Blast Back` / MSEA `Blast Back` — 현행_GMS_개칭(KMS명 변경)

#### 3. 빌드업 캐논 (`5010003`, 1차, 501.img)

- 설명(원문): 캐논을 개량하여 영구적으로 공격력과 방어력을 향상시킨다.
- 힌트(원문): 공격력 #padX, 물리 방어력 #pddX, 마법 방어력 #mddX 증가
- 힌트(마스터 치환): 공격력 20, 물리 방어력 250, 마법 방어력 250 증가
- common: `{"maxLevel": 10, "padX": "2*x", "pddX": "25*x", "mddX": "25*x"}`
- Lv1: `{"level": 1, "padX": 2, "pddX": 25, "mddX": 25}`
- Lv10(마스터): `{"level": 10, "padX": 20, "pddX": 250, "mddX": 250}`
- 마스터레벨 10 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Boost` / MSEA `Cannon Boost` — 현행_GMS_확보

#### 4. 펀칭 캐논 (`5011001`, 1차, 501.img)

- 설명(원문): 적 하나에게 강력한 캐논 펀치를 날린다.
- 힌트(원문): MP #mpCon 소비, #damage%로 #attackCount번 공격
- 힌트(마스터 치환): MP 9 소비, 95%로 3번 공격
- common: `{"maxLevel": 20, "mpCon": "5+2*u(x/10)", "damage": "75+x", "attackCount": "3", "mobCount": "1"}`
- Lv1: `{"level": 1, "mpCon": 7, "damage": 76, "attackCount": 3, "mobCount": 1}`
- Lv20(마스터): `{"level": 20, "mpCon": 9, "damage": 95, "attackCount": 3, "mobCount": 1}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Strike` / MSEA `Cannon Strike` — 현행_GMS_확보

#### 5. 몽키 러쉬붐 (`5301001`, 2차, 530.img)

- 설명(원문): 폭탄이 가득 들어있는 오크통을 굴린다. 오크통은 일정 거리를 굴러가며 적들을 밀어낸 뒤에 폭발한다.
- 힌트(원문): MP #mpCon 소비, #damage% 데미지로 최대 #mobCount명의 적을 #attackCount번 공격, 대상은 #prop%확률로 넉백, 일정 거리 이동 후 #w%의 데미지로 폭발
- 힌트(마스터 치환): MP 28 소비, 50% 데미지로 최대 8명의 적을 3번 공격, 대상은 100%확률로 넉백, 일정 거리 이동 후 300%의 데미지로 폭발
- common: `{"maxLevel": 20, "mpCon": "20+2*d(x/5)", "damage": "30+x", "mobCount": "8", "attackCount": "3", "time": "900", "prop": "50+5*d(x/2)", "w": "240+3*x", "x": "350"}`
- Lv1: `{"level": 1, "mpCon": 20, "damage": 31, "attackCount": 3, "mobCount": 8, "time": 900, "prop": 50, "x": 350, "w": 243}`
- Lv20(마스터): `{"level": 20, "mpCon": 28, "damage": 50, "attackCount": 3, "mobCount": 8, "time": 900, "prop": 100, "x": 350, "w": 300}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Barrel Bomb` / MSEA `Barrel Bomb` — 현행_GMS_확보

#### 6. 몽키 매직 (`5301003`, 2차, 530.img)

- 설명(원문): 몽키의 마법으로 일정 시간동안 주변 파티원들의 HP, MP, 올스텟, 이동속도, 점프력, 명중치, 회피치를 높여준다. 다른 모든 버프 스킬과 중복으로 사용할 수 있다.
- 힌트(원문): MP #mpCon 소비, #time초간 HP #indieMhp, MP #indieMmp, 올스텟 #indieAllStat, 이동속도 #indieSpeed, 점프력 #indieJump, 명중치 #indieAcc, 회피치 #indieEva 증가
- 힌트(마스터 치환): MP 55 소비, 300초간 HP 300, MP 300, 올스텟 20, 이동속도 10, 점프력 5, 명중치 160, 회피치 160 증가
- common: `{"mpCon": "30+5*d(x/4)", "time": "15*x", "indieMhp": "15*x", "indieMmp": "15*x", "indieAllStat": "x", "indieSpeed": "u(x/2)", "indieJump": "u(x/4)", "indieAcc": "8*x", "indieEva": "8*x", "maxLevel": 20}`
- Lv1: `{"level": 1, "mpCon": 30, "time": 15, "indieMhp": 15, "indieMmp": 15, "indieAllStat": 1, "indieSpeed": 1, "indieJump": 1, "indieAcc": 8, "indieEva": 8}`
- Lv20(마스터): `{"level": 20, "mpCon": 55, "time": 300, "indieMhp": 300, "indieMmp": 300, "indieAllStat": 20, "indieSpeed": 10, "indieJump": 5, "indieAcc": 160, "indieEva": 160}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Monkey Magic` / MSEA `Monkey Magic` — 현행_GMS_확보

#### 7. 캐논 마스터리 (`5300005`, 2차, 530.img)

- 설명(원문): 캐논 계열 무기의 숙련도와 명중치를 증가시킨다.
- 힌트(원문): 캐논 계열 무기의 숙련도 #mastery%, 명중치 #accX 상승
- 힌트(마스터 치환): 캐논 계열 무기의 숙련도 50%, 명중치 120 상승
- common: `{"maxLevel": 20, "mastery": "10+2*x", "accX": "6*x"}`
- Lv1: `{"level": 1, "mastery": 12, "accX": 6}`
- Lv20(마스터): `{"level": 20, "mastery": 50, "accX": 120}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Mastery` / MSEA `Cannon Mastery` — 현행_GMS_확보

#### 8. 캐논 부스터 (`5301002`, 2차, 530.img)

- 설명(원문): MP를 소비하여 일정시간 동안 캐논의 공격속도를 2단계 상승시킨다. / 필요 스킬 : #c캐논 마스터리 5레벨 이상#
- 힌트(원문): MP #mpCon 소비, #time초간 공격 속도 향상
- 힌트(마스터 치환): MP 11 소비, 200초간 공격 속도 향상
- common: `{"maxLevel": 20, "mpCon": "31-1*x", "time": "10*x", "x": "-2"}`
- Lv1: `{"level": 1, "mpCon": 30, "time": 10, "x": -2}`
- Lv20(마스터): `{"level": 20, "mpCon": 11, "time": 200, "x": -2}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `미확보` / MSEA `Cannon Booster` — 대응_불확실(현행 표 KMS명 공백)

#### 9. 크리티컬 파이어 (`5300004`, 2차, 530.img)

- 설명(원문): 영구적으로 크리티컬 확률과 크리티컬 최소 데미지를 증가시킨다.
- 힌트(원문): 영구적으로 크리티컬 확률 #cr%, 크리티컬 최소 데미지 #criticaldamageMin% 증가
- 힌트(마스터 치환): 영구적으로 크리티컬 확률 20%, 크리티컬 최소 데미지 10% 증가
- common: `{"maxLevel": 15, "cr": "5+x", "criticaldamageMin": "5+u(x/3)"}`
- Lv1: `{"level": 1, "cr": 6, "criticaldamageMin": 6}`
- Lv15(마스터): `{"level": 15, "cr": 20, "criticaldamageMin": 10}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Critical Fire` / MSEA `Critical Fire` — 현행_GMS_확보

#### 10. 파이렛 트레이닝 (`5300008`, 2차, 530.img)

- 설명(원문): 해적의 비밀 수련을 통해 힘과 민첩성을 향상시킨다.
- 힌트(원문): 영구적으로 힘 #strX, 민첩성 #dexX 증가
- 힌트(마스터 치환): 영구적으로 힘 30, 민첩성 30 증가
- common: `{"strX": "3*x", "dexX": "3*x", "maxLevel": 10}`
- Lv1: `{"level": 1, "strX": 3, "dexX": 3}`
- Lv10(마스터): `{"level": 10, "strX": 30, "dexX": 30}`
- 마스터레벨 10 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Pirate Training` / MSEA `Pirate Training` — 현행_GMS_확보

#### 11. 슬러그 샷 (`5301000`, 2차, 530.img)

- 설명(원문): 전방을 향해 여러발의 소형 포탄을 발사하여 다수의 적을 동시에 공격한다.
- 힌트(원문): MP #mpCon소비, #damage% 데미지로 최대 #mobCount명의 적을 #bulletCount번 공격
- 힌트(마스터 치환): MP 24소비, 220% 데미지로 최대 4명의 적을 2번 공격
- common: `{"maxLevel": 20, "mpCon": "16+2*d(x/5)", "damage": "160+3*x", "bulletCount": "2", "mobCount": "4", "range": "450", "ballDelay": "240"}`
- Lv1: `{"level": 1, "mpCon": 16, "damage": 163, "mobCount": 4, "bulletCount": 2, "range": 450, "ballDelay": 240}`
- Lv20(마스터): `{"level": 20, "mpCon": 24, "damage": 220, "mobCount": 4, "bulletCount": 2, "range": 450, "ballDelay": 240}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Scatter Shot` / MSEA `Scatter Shot` — 현행_GMS_확보

#### 12. 몽키 웨이브 (`5311002`, 3차, 531.img)

- 설명(원문): 소음을 일으켜 주변의 적들을 공격한다. 힘을 모을수록 큰 소음을 낼 수 있으며, 크리티컬 시 최고 출력으로 바로 사용할 수 있다.
- 힌트(원문): MP #mpCon 소비, 최대 #damage% 데미지로 공격, #prop% 확률로 기절, 크리티컬 시 #w% 확률로 최고 출력으로 사용 가능
- 힌트(마스터 치환): MP 55 소비, 최대 860% 데미지로 공격, 95% 확률로 기절, 크리티컬 시 20% 확률로 최고 출력으로 사용 가능
- common: `{"maxLevel": 20, "mpCon": "35+5*d(x/5)", "damage": "460+20*x", "mobCount": "8", "prop": "45+5*d(x/2)", "time": "2+d(x/10)", "w": "2*u(x/2)", "hcTime": "1"}`
- Lv1: `{"level": 1, "mpCon": 35, "damage": 480, "mobCount": 8, "time": 2, "hcTime": 1, "prop": 45, "w": 2}`
- Lv20(마스터): `{"level": 20, "mpCon": 55, "damage": 860, "mobCount": 8, "time": 4, "hcTime": 1, "prop": 95, "w": 20}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Monkey Wave` / MSEA `Monkey Wave` — 현행_GMS_확보

#### 13. 몽키 파워붐 (`5311001`, 3차, 531.img)

- 설명(원문): 대량의 특제 폭탄을 동시에 터뜨려 사방의 적 다수를 공격하고 일정 시간동안 기절시킨다. 추가로 몽키 파워붐 스킬을 배우면 몽키 러쉬붐의 데미지가 영구적으로 증가한다.
- 힌트(원문): 액티브 효과 : MP #mpCon소비, #damage% 데미지로 최대 #mobCount명의 적을 #attackCount번 공격, #prop% 확률로 #time초간 기절, 재사용 대기시간 #cooltime초 / 패시브 효과 : 영구적으로 몽키 러쉬붐 데미지 #damR% 증가
- 힌트(마스터 치환): 액티브 효과 : MP 46소비, 280% 데미지로 최대 10명의 적을 5번 공격, 95% 확률로 4초간 기절, 재사용 대기시간 5초 / 패시브 효과 : 영구적으로 몽키 러쉬붐 데미지 30% 증가
- common: `{"maxLevel": 20, "mpCon": "30+4*d(x/5)", "damage": "220+3*x", "attackCount": "5", "mobCount": "10", "prop": "45+5*d(x/2)", "time": "2+d(x/10)", "damR": "3*u(x/2)", "cooltime": "5", "hcTime": "1"}`
- Lv1: `{"level": 1, "mpCon": 30, "damage": 223, "attackCount": 5, "mobCount": 10, "cooltime": 5, "time": 2, "hcTime": 1, "prop": 45, "damR": 3}`
- Lv20(마스터): `{"level": 20, "mpCon": 46, "damage": 280, "attackCount": 5, "mobCount": 10, "cooltime": 5, "time": 4, "hcTime": 1, "prop": 95, "damR": 30}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Monkey Madness` / MSEA `Monkey Madness` — 현행_GMS_확보

#### 14. 캐논 스파이크 (`5311000`, 3차, 531.img)

- 설명(원문): 적 다수를 관통할 수 있는 날카로운 캐논 포탄을 발사한다.
- 힌트(원문): MP #mpCon소비, #damage% 데미지로 최대 #mobCount명의 적을 #attackCount번 공격
- 힌트(마스터 치환): MP 36소비, 240% 데미지로 최대 6명의 적을 3번 공격
- common: `{"maxLevel": 20, "mpCon": "28+2*d(x/5)", "damage": "200+2*x", "attackCount": "3", "mobCount": "6"}`
- Lv1: `{"level": 1, "mpCon": 28, "damage": 202, "attackCount": 3, "mobCount": 6}`
- Lv20(마스터): `{"level": 20, "mpCon": 36, "damage": 240, "attackCount": 3, "mobCount": 6}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Spike` / MSEA `Cannon Spike` — 현행_GMS_확보

#### 15. 캐논 점프 (`5311003`, 3차, 531.img)

- 설명(원문): 지면을 향해 캐논을 발사하여 반동으로 높이 뛰어오른다. 뛰어오르는 순간 주변의 적에게 데미지를 줄 수 있다.
- 힌트(원문): MP #mpCon 소비, #damage% 데미지로 최대 #mobCount명의 적을 공격하며 점프
- 힌트(마스터 치환): MP 35 소비, 210% 데미지로 최대 6명의 적을 공격하며 점프
- common: `{"maxLevel": 15, "mpCon": "60-5*d(x/3)", "damage": "165+3*x", "mobCount": "6", "x": "0", "y": "950+15*x"}`
- Lv1: `{"level": 1, "mpCon": 60, "damage": 168, "mobCount": 6, "x": 0, "y": 965}`
- Lv15(마스터): `{"level": 15, "mpCon": 35, "damage": 210, "mobCount": 6, "x": 0, "y": 1175}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Jump` / MSEA `Cannon Jump` — 현행_GMS_확보

#### 16. 오크통 룰렛 (`5311004`, 3차, 531.img)

- 설명(원문): 오크통을 폭발시켜 랜덤 버프를 받는다. 버프 지속 상태에서 적을 공격하면 일정확률로 대상에게 상태이상 효과를 적용 수 있다.
- 힌트(원문): MP #mpCon 소비, #time초간 버프 적용. 공격 시 #w% 확률로 대상에게 암흑, 기절, 결빙, 슬로우 상태이상 중 하나가 #v초간 적용 / #c재사용 대기시간 #cooltime초#
- 힌트(마스터 치환): MP 60 소비, 240초간 버프 적용. 공격 시 30% 확률로 대상에게 암흑, 기절, 결빙, 슬로우 상태이상 중 하나가 5초간 적용 / 재사용 대기시간 30초
- common: `{"maxLevel": 10, "mpCon": "35+5*d(x/2)", "time": "180+6*x", "u": "-6*x", "v": "3+d(x/5)", "w": "3*x", "x": "3*x", "y": "2*x", "z": "3*x", "cooltime": "60-3*x", "hcSubTime": "1+d(x/5)"}`
- Lv1: `{"level": 1, "mpCon": 35, "cooltime": 57, "time": 186, "hcSubTime": 1, "x": 3, "y": 2, "w": 3, "u": -6, "v": 3, "z": 3}`
- Lv10(마스터): `{"level": 10, "mpCon": 60, "cooltime": 30, "time": 240, "hcSubTime": 3, "x": 30, "y": 20, "w": 30, "u": -60, "v": 5, "z": 30}`
- 마스터레벨 10 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B), icon1(32x32 fmt1 raw2048B), icon2(32x32 fmt1 raw2048B), icon3(32x32 fmt1 raw2048B), icon4(32x32 fmt1 raw2048B)
- 영문명: GMS `Forty Winks` / MSEA `Slumber` — 대응_불확실(현행 표 KMS명 공백)

#### 17. 럭키 다이스 (`5311005`, 3차, 531.img)

- 설명(원문): 주사위를 던져 자신의 행운을 시험한다. 주사위의 결과에 따라 일정 시간동안 랜덤 버프를 획득할 수 있지만, 1이 나올 경우에는 아무 일도 발생하지 않는다.
- 힌트(원문): MP #mpCon 소비, 주사위 버프 지속시간 #time초 / #c재사용 대기시간 #cooltime초#
- 힌트(마스터 치환): MP 60 소비, 주사위 버프 지속시간 180초 / 재사용 대기시간 180초
- common: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "time": "60+6*x", "cooltime": "480-30*d(x/2)", "pddR": "30", "mhpR": "20", "mmpR": "20", "cr": "15", "damR": "20", "expR": "30", "u": "17", "v": "17", "w": "15"}`
- Lv1: `{"level": 1, "mpCon": 40, "cooltime": 480, "time": 66, "cr": 15, "w": 15, "u": 17, "v": 17, "damR": 20, "pddR": 30, "mhpR": 20, "mmpR": 20, "expR": 30}`
- Lv20(마스터): `{"level": 20, "mpCon": 60, "cooltime": 180, "time": 180, "cr": 15, "w": 15, "u": 17, "v": 17, "damR": 20, "pddR": 30, "mhpR": 20, "mmpR": 20, "expR": 30}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B), icon1(32x32 fmt1 raw2048B), icon2(32x32 fmt1 raw2048B), icon3(32x32 fmt1 raw2048B), icon4(32x32 fmt1 raw2048B), icon5(32x32 fmt1 raw2048B)
- 영문명: GMS `Roll of the Dice` / MSEA `Roll of the Dice` — 현행_GMS_확보

#### 18. 리인포스 캐논 (`5310006`, 3차, 531.img)

- 설명(원문): 영구적으로 캐논을 강화하여 공격력과 공격속도를 향상시킨다.
- 힌트(원문): 영구적으로 공격력 #padX, 공격속도 1 증가
- 힌트(마스터 치환): 영구적으로 공격력 30, 공격속도 1 증가
- common: `{"maxLevel": 15, "padX": "2*x", "actionSpeed": "-1"}`
- Lv1: `{"level": 1, "padX": 2, "actionSpeed": -1}`
- Lv15(마스터): `{"level": 15, "padX": 30, "actionSpeed": -1}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Reinforced Cannon` / MSEA `Reinforced Cannon` — 현행_GMS_확보

#### 19. 바이탈 익스트림 (`5310007`, 3차, 531.img)

- 설명(원문): 영구적으로 체력과 방어력, 상태이상 내성을 강화한다.
- 힌트(원문): 체력 #mhpR%, 방어력 #pddR%, 상태이상 내성 #asrR% 상승
- 힌트(마스터 치환): 체력 20%, 방어력 50%, 상태이상 내성 20% 상승
- common: `{"maxLevel": 20, "mhpR": "x", "pddR": "10+2*x", "mddR": "10+2*x", "asrR": "x"}`
- Lv1: `{"level": 1, "pddR": 12, "mddR": 12, "mhpR": 1, "asrR": 1}`
- Lv20(마스터): `{"level": 20, "pddR": 50, "mddR": 50, "mhpR": 20, "asrR": 20}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Pirate Rush` / MSEA `Pirate Rush` — 현행_GMS_개칭(영문명 변경)

#### 20. 반격의 슈터 (`5310009`, 3차, 531.img)

- 설명(원문): 피격 시 일정확률로 캐논을 휘둘러 반격한다.
- 힌트(원문): #prop%로 적의 공격을 막아 #damage% 데미지로 반격 
- 힌트(마스터 치환): 20%로 적의 공격을 막아 160% 데미지로 반격 
- common: `{"maxLevel": 15, "prop": "5+x", "damage": "100+4*x"}`
- Lv1: `{"level": 1, "damage": 104, "prop": 6}`
- Lv15(마스터): `{"level": 15, "damage": 160, "prop": 20}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Counter Crush` / MSEA `Counter Crush` — 현행_GMS_확보

#### 21. 캐논 바주카 (`5321000`, 4차, 532.img)

- 설명(원문): 전방을 향해 강력한 캐논포를 발사하여 다수의 적을 동시에 공격한다. 
- 힌트(원문): MP #mpCon소비, #damage% 데미지로 최대 #mobCount명의 적을 #attackCount번 공격
- 힌트(마스터 치환): MP 75소비, 500% 데미지로 최대 6명의 적을 4번 공격
- common: `{"maxLevel": 30, "mpCon": "50+5*d(x/6)", "damage": "320+6*x", "attackCount": "4", "mobCount": "6", "hcCooltime": "5"}`
- Lv1: `{"level": 1, "mpCon": 50, "damage": 326, "attackCount": 4, "mobCount": 6, "hcCooltime": 5}`
- Lv30(마스터): `{"level": 30, "mpCon": 75, "damage": 500, "attackCount": 4, "mobCount": 6, "hcCooltime": 5}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Bazooka` / MSEA `Cannon Bazooka` — 현행_GMS_확보

#### 22. 캐논 버스터 (`5321012`, 4차, 532.img)

- 설명(원문): 전방의 적 하나를 집중 포격 한다. 추가 크리티컬 확률이 적용된다.
- 힌트(원문): MP #mpCon소비, #damage% 데미지로 #bulletCount번 공격, 추가 크리티컬 확률 #cr%
- 힌트(마스터 치환): MP 63소비, 320% 데미지로 5번 공격, 추가 크리티컬 확률 15%
- common: `{"maxLevel": 30, "mpCon": "45+3*d(x/5)", "damage": "230+3*x", "mobCount": "1", "range": "450", "cr": "u(x/2)", "bulletCount": "5", "ballDelay": "60", "ballDelay1": "60", "ballDelay2": "60", "ballDelay3": "60", "ballDelay4": "60"}`
- Lv1: `{"level": 1, "mpCon": 45, "damage": 233, "mobCount": 1, "bulletCount": 5, "cr": 1, "range": 450, "ballDelay": 60, "ballDelay1": 60, "ballDelay2": 60, "ballDelay3": 60, "ballDelay4": 60}`
- Lv30(마스터): `{"level": 30, "mpCon": 63, "damage": 320, "mobCount": 1, "bulletCount": 5, "cr": 15, "range": 450, "ballDelay": 60, "ballDelay1": 60, "ballDelay2": 60, "ballDelay3": 60, "ballDelay4": 60}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Barrage` / MSEA `Cannon Barrage` — 현행_GMS_확보

#### 23. 전함 노틸러스 (`5321001`, 4차, 532.img)

- 설명(원문): 전함 노틸러스호에 공격 명령을 내려 적 다수를 동시에 공격한다.
- 힌트(원문): MP #mpCon소비, #damage% 데미지로 최대 #mobCount명의 적을 #attackCount번 공격 / #c재사용 대기시간 #cooltime초#
- 힌트(마스터 치환): MP 350소비, 520% 데미지로 최대 15명의 적을 3번 공격 / 재사용 대기시간 30초
- common: `{"maxLevel": 30, "mpCon": "350", "damage": "400+4*x", "attackCount": "3", "mobCount": "15", "cooltime": "60-2*d(x/2)"}`
- Lv1: `{"level": 1, "mpCon": 350, "damage": 404, "attackCount": 3, "mobCount": 15, "cooltime": 60}`
- Lv30(마스터): `{"level": 30, "mpCon": 350, "damage": 520, "attackCount": 3, "mobCount": 15, "cooltime": 30}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Nautilus Strike` / MSEA `Nautilus Strike` — 현행_GMS_확보

#### 24. 파이렛 스피릿 (`5321010`, 4차, 532.img)

- 설명(원문): 영구적으로 반격 확률이 상승하며, 스킬 사용 시 일정시간동안 적의 공격에도 뒤로 물러서지 않는상태가 된다.
- 힌트(원문): 액티브 효과 : MP #mpCon소비, #time초 동안 피격 시 #x% 확률로 스탠스 효과 발동 / 패시브 효과 : 영구적으로 반격확률 #prop% 증가
- 힌트(마스터 치환): 액티브 효과 : MP 80소비, 300초 동안 피격 시 80% 확률로 스탠스 효과 발동 / 패시브 효과 : 영구적으로 반격확률 15% 증가
- common: `{"maxLevel": 30, "prop": "u(x/2)", "x": "20+2*x", "mpCon": "50+5*d(x/5)", "time": "10*x"}`
- Lv1: `{"level": 1, "mpCon": 50, "time": 10, "prop": 1, "x": 22}`
- Lv30(마스터): `{"level": 30, "mpCon": 80, "time": 300, "prop": 15, "x": 80}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Pirate's Spirit` / MSEA `Pirate's Spirit` — 현행_GMS_확보

#### 25. 마그네틱 앵커 (`5321003`, 4차, 532.img)

- 설명(원문): 전방에 강한 자기장을 생성하는 마그네틱 앵커를 설치한다. 마그네틱 앵커는 자기장을 이용하여 주변의 적을 지속적으로 끌어당긴다. 또한 지속시간이 끝나면 폭발하며 주변의 적들에게 치명적인 데미지를 준다.
- 힌트(원문): MP #mpCon 소비, #time초동안 소환, 주기적으로 #damage%의 데미지를 주며 주변의 적을 끌어당긴다. 지속시간 경과 시 #selfDestruction%의 추가 데미지
- 힌트(마스터 치환): MP 86 소비, 20초동안 소환, 주기적으로 400%의 데미지를 주며 주변의 적을 끌어당긴다. 지속시간 경과 시 520%의 추가 데미지
- common: `{"maxLevel": 15, "mpCon": "50+12*u(x/5)", "time": "5+x", "damage": "250+10*x", "mobCount": "8", "prop": "30+3*x", "subTime": "2+d(x/5)", "selfDestruction": "400+8*x", "hcCooltime": "5"}`
- Lv1: `{"level": 1, "mpCon": 62, "damage": 260, "mobCount": 8, "hcCooltime": 5, "time": 6, "subTime": 2, "prop": 33, "selfDestruction": 408}`
- Lv15(마스터): `{"level": 15, "mpCon": 86, "damage": 400, "mobCount": 8, "hcCooltime": 5, "time": 20, "subTime": 5, "prop": 75, "selfDestruction": 520}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Anchors Aweigh` / MSEA `Anchors Away` — 현행_GMS_확보

#### 26. 서포트 몽키 트윈스 (`5321004`, 4차, 532.img)

- 설명(원문): 전투를 도와줄 정예 포병 몽키 트윈스를 소환한다.
- 힌트(원문): MP #mpCon소비, #time초동안 소환, 각각 #damage% 데미지로 공격 / #c재사용 대기시간 #cooltime초#
- 힌트(마스터 치환): MP 70소비, 60초동안 소환, 각각 350% 데미지로 공격 / 재사용 대기시간 10초
- common: `{"maxLevel": 15, "mpCon": "40+10*d(x/5)", "damage": "275+5*x", "time": "30+2*x", "cooltime": "10", "mobCount": "1"}`
- Lv1: `{"level": 1, "mpCon": 40, "damage": 280, "mobCount": 1, "cooltime": 10, "time": 32}`
- Lv15(마스터): `{"level": 15, "mpCon": 70, "damage": 350, "mobCount": 1, "cooltime": 10, "time": 60}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Support Monkey` / MSEA `Monkey Artillery` — 현행_GMS_개칭(KMS명 변경)

#### 27. 더블 럭키 다이스 (`5320007`, 4차, 532.img)

- 설명(원문): 일정 확률로 주사위 2개를 동시에 던져 자신의 행운을 시험한다. 주사위의 눈이 같을 경우에는 보다 강력한 버프 효과가 적용된다. / 필요 스킬 : #c럭키 다이스 20레벨 이상#
- 힌트(원문): MP #mpCon 소비, #prop% 확률로 럭키 다이스 사용 시, 더블 럭키 다이스 발동, 주사위 버프 지속시간 #time초 / #c재사용 대기시간 #cooltime초#
- 힌트(마스터 치환): MP 60 소비, 50% 확률로 럭키 다이스 사용 시, 더블 럭키 다이스 발동, 주사위 버프 지속시간 200초 / 재사용 대기시간 200초
- common: `{"maxLevel": 5, "mpCon": "60", "time": "180+4*x", "cooltime": "200", "pddR": "30", "mhpR": "20", "mmpR": "20", "cr": "15", "damR": "20", "expR": "30", "u": "15", "v": "17", "w": "17", "x": "17", "prop": "10*x"}`
- Lv1: `{"level": 1, "mpCon": 60, "cooltime": 200, "time": 184, "prop": 10, "cr": 15, "x": 17, "w": 17, "u": 15, "v": 17, "damR": 20, "pddR": 30, "mhpR": 20, "mmpR": 20, "expR": 30}`
- Lv5(마스터): `{"level": 5, "mpCon": 60, "cooltime": 200, "time": 200, "prop": 50, "cr": 15, "x": 17, "w": 17, "u": 15, "v": 17, "damR": 20, "pddR": 30, "mhpR": 20, "mmpR": 20, "expR": 30}`
- 마스터레벨 5 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B), icon1(32x32 fmt1 raw2048B), icon2(32x32 fmt1 raw2048B), icon3(32x32 fmt1 raw2048B), icon4(32x32 fmt1 raw2048B), icon5(32x32 fmt1 raw2048B)
- 영문명: GMS `Double Down` / MSEA `Double Down` — 현행_GMS_확보

#### 28. 하이퍼 몽키 스펠 (`5320008`, 4차, 532.img)

- 설명(원문): 몽키 매직을 업그레이드 하여 몽키의 마법으로 일정 시간동안 주변 파티원들의 HP, MP, 올스텟, 이동속도, 점프력, 명중치, 회피치를 높여준다. 다른 모든 버프 스킬과 중복으로 사용할 수 있다. / 필요 스킬 : #c몽키 매직 20레벨 이상#
- 힌트(원문): MP #mpCon 소비, #time초간 HP #indieMhp, MP #indieMmp, 올스텟 #indieAllStat, 이동속도 #indieSpeed, 점프력 #indieJump, 명중치 #indieAcc, 회피치 #indieEva 증가
- 힌트(마스터 치환): MP 80 소비, 300초간 HP 700, MP 700, 올스텟 40, 이동속도 15, 점프력 10, 명중치 250, 회피치 250 증가
- common: `{"maxLevel": 30, "mpCon": "55+5*u(x/6)", "time": "300", "indieMhp": "310+13*x", "indieMmp": "310+13*x", "indieAllStat": "25+d(x/2)", "indieSpeed": "10+u(x/6)", "indieJump": "5+u(x/6)", "indieAcc": "160+3*x", "indieEva": "160+3*x"}`
- Lv1: `{"level": 1, "mpCon": 60, "time": 300, "indieMhp": 323, "indieMmp": 323, "indieAllStat": 25, "indieSpeed": 11, "indieJump": 6, "indieAcc": 163, "indieEva": 163}`
- Lv30(마스터): `{"level": 30, "mpCon": 80, "time": 300, "indieMhp": 700, "indieMmp": 700, "indieAllStat": 40, "indieSpeed": 15, "indieJump": 10, "indieAcc": 250, "indieEva": 250}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Mega Monkey Magic` / MSEA `Mega Monkey Magic` — 현행_GMS_확보

#### 29. 오버버닝 캐논 (`5320009`, 4차, 532.img)

- 설명(원문): 캐논의 성능을 극한까지 끌어올려 영구적으로 데미지를 증가시킨다. 또한 공격 시 몬스터의 방어율을 일정 수준 무시할 수 있게 된다.
- 힌트(원문): 영구적으로 데미지 #damR% 증가, 몬스터 방어율 #ignoreMobpdpR% 무시 효과 추가
- 힌트(마스터 치환): 영구적으로 데미지 40% 증가, 몬스터 방어율 20% 무시 효과 추가
- common: `{"maxLevel": 30, "ignoreMobpdpR": "5+d(x/2)", "damR": "10+x"}`
- Lv1: `{"level": 1, "damR": 11, "ignoreMobpdpR": 5}`
- Lv30(마스터): `{"level": 30, "damR": 40, "ignoreMobpdpR": 20}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Cannon Overload` / MSEA `Cannon Overload` — 현행_GMS_확보

### 메르세데스 (29종)

#### 1. 스피드 듀얼샷 (`23001000`, 1차, 2300.img)

- 설명(원문): 전방에 있는 다수의 적에게 화살을 발사한다.
- 힌트(원문): MP #mpCon 소비,최대 #mobCount명의 적에게 #damage% 데미지의 화살 #bulletCount개 발사
- 힌트(마스터 치환): MP 14 소비,최대 3명의 적에게 115% 데미지의 화살 2개 발사
- common: `{"maxLevel": 20, "mpCon": "8+2*d(x/6)", "damage": "95+x", "bulletCount": "2", "mobCount": "3", "range": "400", "ballDelay": "270"}`
- Lv1: `{"level": 1, "mpCon": 8, "damage": 96, "mobCount": 3, "bulletCount": 2, "range": 400, "ballDelay": 270}`
- Lv20(마스터): `{"level": 20, "mpCon": 14, "damage": 115, "mobCount": 3, "bulletCount": 2, "range": 400, "ballDelay": 270}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Swift Dual Shot` / MSEA `Swift Dual Shot` — 현행_GMS_확보

#### 2. 샤프 에이밍 (`23000003`, 1차, 2300.img)

- 설명(원문): 영구적으로 크리티컬 확률을 높인다.
- 힌트(원문): 크리티컬 확률 #cr% 상승
- 힌트(마스터 치환): 크리티컬 확률 40% 상승
- common: `{"cr": "2*x", "maxLevel": 20}`
- Lv1: `{"level": 1, "cr": 2}`
- Lv20(마스터): `{"level": 20, "cr": 40}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Sharp Aim` / MSEA `Sharp Aim` — 현행_GMS_확보

#### 3. 아크로바틱 점프 (`23001002`, 1차, 2300.img)

- 설명(원문): 점프 중 진행방향으로 덤블링하여 먼 거리를 날아간다. 스킬레벨이 상승할수록 이동 거리가 증가한다.
- 힌트(원문): MP #mpCon 소비, 일정거리 점프
- 힌트(마스터 치환): MP 10 소비, 일정거리 점프
- common: `{"maxLevel": 10, "mpCon": "30-2*x", "x": "350+20*x", "y": "250+10*x"}`
- Lv1: `{"level": 1, "mpCon": 28, "x": 370, "y": 260}`
- Lv10(마스터): `{"level": 10, "mpCon": 10, "x": 550, "y": 350}`
- 마스터레벨 10 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Spirit Jump` / MSEA `Spirit Jump` — 현행_GMS_개칭(KMS명 변경)

#### 4. 포텐셜 파워 (`23000001`, 1차, 2300.img)

- 설명(원문): 내면에 잠재된 힘을 영구적으로 활성한다. 이동속도와 최대 이동속도 상한이 증가하며 일정확률로 적의 공격을 회피할 수 있게 된다.
- 힌트(원문): 이동속도 #psdSpeed 증가, 최대 이동속도 상한 #u로 증가, #er% 확률로 적의 공격 회피
- 힌트(마스터 치환): 이동속도 30 증가, 최대 이동속도 상한 165로 증가, 20% 확률로 적의 공격 회피
- common: `{"maxLevel": 15, "er": "5+x", "psdSpeed": "2*x", "speedMax": "10+x", "u": "150+x"}`
- Lv1: `{"level": 1, "u": 151, "er": 6, "psdSpeed": 2, "speedMax": 11}`
- Lv15(마스터): `{"level": 15, "u": 165, "er": 20, "psdSpeed": 30, "speedMax": 25}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Potential Power` / MSEA `Potential Power` — 현행_GMS_확보

#### 5. 피지컬 트레이닝 (`23100008`, 2차, 2310.img)

- 설명(원문): 신체 단련을 통해 영구적으로 힘과 민첩성을 향상시킨다.
- 힌트(원문): 영구적으로 힘 #strX, 민첩성 #dexX 증가
- 힌트(마스터 치환): 영구적으로 힘 30, 민첩성 30 증가
- common: `{"strX": "3*x", "dexX": "3*x", "maxLevel": 10}`
- Lv1: `{"level": 1, "strX": 3, "dexX": 3}`
- Lv10(마스터): `{"level": 10, "strX": 30, "dexX": 30}`
- 마스터레벨 10 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Physical Training` / MSEA `Physical Training` — 현행_GMS_확보

#### 6. 듀얼보우건 마스터리 (`23100005`, 2차, 2310.img)

- 설명(원문): 듀얼보우건 계열 무기의 숙련도와 명중치를 향상시킨다. 
- 힌트(원문): 듀얼보우건 계열 무기의 숙련도 #mastery%, 명중치 #accX 상승
- 힌트(마스터 치환): 듀얼보우건 계열 무기의 숙련도 50%, 명중치 120 상승
- common: `{"maxLevel": 20, "mastery": "10+2*x", "accX": "6*x"}`
- Lv1: `{"level": 1, "mastery": 12, "accX": 6}`
- Lv20(마스터): `{"level": 20, "mastery": 50, "accX": 120}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Dual Bowguns Mastery` / MSEA `Dual Bowguns Mastery` — 현행_GMS_확보

#### 7. 듀얼보우건 부스터 (`23101002`, 2차, 2310.img)

- 설명(원문): MP를 소비하여 일정시간 동안 듀얼보우건의 공격속도를 2단계 상승시킨다. / 필요 스킬 : #c듀얼보우건 마스터리 5레벨 이상#
- 힌트(원문): MP #mpCon 소비, #time초간 공격 속도 향상
- 힌트(마스터 치환): MP 11 소비, 200초간 공격 속도 향상
- common: `{"maxLevel": 20, "mpCon": "31-1*x", "time": "10*x", "x": "-2"}`
- Lv1: `{"level": 1, "mpCon": 30, "time": 10, "x": -2}`
- Lv20(마스터): `{"level": 20, "mpCon": 11, "time": 200, "x": -2}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Dual Bowguns Boost` / MSEA `Dual Bowguns Boost` — 현행_GMS_확보

#### 8. 스피릿 인퓨젼 (`23101003`, 2차, 2310.img)

- 설명(원문): 일정 시간 동안 데미지와 크리티컬 확률을 증가시키킨다.
- 힌트(원문): MP #mpCon 소비, #time초 동안 데미지 #damage%, 크리티컬 확률 #x% 증가
- 힌트(마스터 치환): MP 45 소비, 180초 동안 데미지 15%, 크리티컬 확률 15% 증가
- common: `{"maxLevel": 15, "mpCon": "20+5*u(x/3)", "time": "60+8*x", "x": "x", "damage": "x"}`
- Lv1: `{"level": 1, "mpCon": 25, "damage": 1, "time": 68, "x": 1}`
- Lv15(마스터): `{"level": 15, "mpCon": 45, "damage": 15, "time": 180, "x": 15}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Spirit Surge` / MSEA `Spirit Surge` — 대응_불확실(현행 표 KMS명 공백)

#### 9. 차지 드라이브 (`23101001`, 2차, 2310.img)

- 설명(원문): 전방의 적 다수를 빠른 속도로 밀어낸 후 공중에 띄운다. 공중에 뜬 상태의 적을 공격하면 추가 데미지를 줄 수 있다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage% 데미지로 밀며 돌진, #w%의 데미지로 띄움. 띄운 상태 공격 시 추가 데미지 #x%
- 힌트(마스터 치환): MP 25 소비, 최대 8명의 적을 130% 데미지로 밀며 돌진, 210%의 데미지로 띄움. 띄운 상태 공격 시 추가 데미지 30%
- common: `{"mpCon": "20+d(x/3)", "damage": "100+2*x", "w": "180+2*x", "x": "2*x", "mobCount": "8", "maxLevel": 15, "hcCooltime": "5"}`
- Lv1: `{"level": 1, "mpCon": 20, "damage": 102, "mobCount": 8, "hcCooltime": 5, "x": 2, "w": 182}`
- Lv15(마스터): `{"level": 15, "mpCon": 25, "damage": 130, "mobCount": 8, "hcCooltime": 5, "x": 30, "w": 210}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Rising Rush` / MSEA `Rising Rush` — 현행_GMS_확보

#### 10. 파이널 샷 (`23100004`, 2차, 2310.img)

- 설명(원문): 차지 드라이브로 공중으로 뜬 적들을 향해 화살을 난사한다. 차지 드라이브 사용 후에만 사용할 수 있다. / 필요 스킬 : #c차지 드라이브 1레벨 이상#
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage% 데미지로 #attackCount번 공격
- 힌트(마스터 치환): MP 16 소비, 최대 8명의 적을 70% 데미지로 4번 공격
- common: `{"maxLevel": 5, "mpCon": "12+4*d(x/5)", "damage": "40+6*x", "mobCount": "8", "attackCount": "4"}`
- Lv1: `{"level": 1, "mpCon": 12, "damage": 46, "attackCount": 4, "mobCount": 8}`
- Lv5(마스터): `{"level": 5, "mpCon": 16, "damage": 70, "attackCount": 4, "mobCount": 8}`
- 마스터레벨 5 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Parting Shot` / MSEA `Parting Shot` — 현행_GMS_확보

#### 11. 파이널 어택 : 듀얼보우건 (`23100006`, 2차, 2310.img)

- 설명(원문): 일정확률로 공격 스킬이 사용된 후 추가 데미지가 적용된다. 다만, 반드시 듀얼보우건 계열 무기를 들었을 경우에만 발동이 가능하다. / 필요 스킬 : #c듀얼보우건 마스터리 3레벨 이상#
- 힌트(원문): #prop% 확률로 #attackCount회 파이널 어택 발동, 1타는 #damage%, 2타는 #x%의 데미지 적용
- 힌트(마스터 치환): 40% 확률로 2회 파이널 어택 발동, 1타는 75%, 2타는 50%의 데미지 적용
- common: `{"damage": "55+2*d(x/2)", "x": "26+4*d(x/3)", "prop": "2*x", "mobCount": "1", "attackCount": "2", "maxLevel": 20}`
- Lv1: `{"level": 1, "damage": 55, "attackCount": 2, "mobCount": 1, "prop": 2, "x": 26}`
- Lv20(마스터): `{"level": 20, "damage": 75, "attackCount": 2, "mobCount": 1, "prop": 40, "x": 50}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Final Attack: Dual Bowguns` / MSEA `Final Attack: Dual Bowguns` — 현행_GMS_확보

#### 12. 어드밴스드 파이널 어택 (`23120012`, 4차, 2312.img)

- 설명(원문): 영구적으로 공격력과 명중률이 증가하며 파이널 어택의 발동확률과 데미지가 대폭 상승한다. / 필요 스킬 : #c파이널 어택 20레벨 이상#
- 힌트(원문): 영구적으로 공격력 #padX, 명중률 #ar% 증가, 공격 시 #prop% 확률로 #attackCount회 파이널 어택 발동, 1타는 #damage%, 2타는 #x%의 데미지 적용
- 힌트(마스터 치환): 영구적으로 공격력 20, 명중률 10% 증가, 공격 시 70% 확률로 2회 파이널 어택 발동, 1타는 105%, 2타는 70%의 데미지 적용
- common: `{"padX": "5+u(x/2)", "prop": "40+x", "damage": "75+x", "x": "50+2*d(x/3)", "ar": "u(x/3)", "maxLevel": 30, "mobCount": "1", "attackCount": "2"}`
- Lv1: `{"level": 1, "damage": 76, "attackCount": 2, "mobCount": 1, "prop": 41, "x": 50, "padX": 6, "ar": 1}`
- Lv30(마스터): `{"level": 30, "damage": 105, "attackCount": 2, "mobCount": 1, "prop": 70, "x": 70, "padX": 20, "ar": 10}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Advanced Final Attack` / MSEA `Advanced Final Attack` — 현행_GMS_확보

#### 13. 크로스 피어싱 (`23101000`, 2차, 2310.img)

- 설명(원문): 자연의 힘이 깃든 날카로운 화살을 연속 발사한다. 적 다수를 관통할 수 있다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage%의 데미지로 #bulletCount번 관통 공격
- 힌트(마스터 치환): MP 24 소비, 최대 6명의 적을 83%의 데미지로 4번 관통 공격
- common: `{"maxLevel": 20, "mpCon": "14+d(x/2)", "damage": "63+x", "bulletCount": "4", "mobCount": "6", "range": "400", "ballDelay": "180", "ballDelay1": "180", "ballDelay2": "180"}`
- Lv1: `{"level": 1, "mpCon": 14, "damage": 64, "mobCount": 6, "bulletCount": 4, "range": 400, "ballDelay": 180, "ballDelay1": 180, "ballDelay2": 180}`
- Lv20(마스터): `{"level": 20, "mpCon": 24, "damage": 83, "mobCount": 6, "bulletCount": 4, "range": 400, "ballDelay": 180, "ballDelay1": 180, "ballDelay2": 180}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Piercing Storm` / MSEA `Piercing Storm` — 현행_GMS_확보

#### 14. 스트라이크 듀얼샷 (`23111000`, 3차, 2311.img)

- 설명(원문): 전방에 있는 다수의 적들에게 매우 빠른 속도로 다수의 화살을 날린다. 대상은 일정확률로 기절상태가 된다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적에게 #damage% 데미지의 화살 #bulletCount개 발사, #prop% 확률로 #time초간 기절
- 힌트(마스터 치환): MP 35 소비, 최대 5명의 적에게 120% 데미지의 화살 4개 발사, 80% 확률로 6초간 기절
- common: `{"maxLevel": 20, "mpCon": "20+3*d(x/4)", "damage": "100+x", "mobCount": "5", "bulletCount": "4", "time": "2+d(x/5)", "prop": "20+3*x", "ballDelay": "180", "ballDelay1": "90", "ballDelay2": "90", "ballDelay3": "90", "range": "400", "hcTime": "1"}`
- Lv1: `{"level": 1, "mpCon": 20, "damage": 101, "mobCount": 5, "bulletCount": 4, "time": 2, "hcTime": 1, "prop": 23, "range": 400, "ballDelay": 180, "ballDelay1": 90, "ballDelay2": 90, "ballDelay3": 90}`
- Lv20(마스터): `{"level": 20, "mpCon": 35, "damage": 120, "mobCount": 5, "bulletCount": 4, "time": 6, "hcTime": 1, "prop": 80, "range": 400, "ballDelay": 180, "ballDelay1": 90, "ballDelay2": 90, "ballDelay3": 90}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Stunning Strikes` / MSEA `Stunning Strikes` — 현행_GMS_확보

#### 15. 리프 토네이도 (`23111001`, 3차, 2311.img)

- 설명(원문): 점프 상태에서 빠르게 몸을 회전하면서 사방에 화살을 난사한다. 공중에서만 사용 가능하며 스킬 사용을 위해서는 반드시 120 이상의 점프력이 필요하다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage% 데미지로 #attackCount번 공격
- 힌트(마스터 치환): MP 45 소비, 최대 8명의 적을 135% 데미지로 4번 공격
- common: `{"maxLevel": 20, "mpCon": "30+3*u(x/4)", "damage": "95+2*x", "mobCount": "8", "attackCount": "4", "x": "0", "y": "600"}`
- Lv1: `{"level": 1, "mpCon": 33, "damage": 97, "attackCount": 4, "mobCount": 8, "x": 0, "y": 600}`
- Lv20(마스터): `{"level": 20, "mpCon": 45, "damage": 135, "attackCount": 4, "mobCount": 8, "x": 0, "y": 600}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Leaf Tornado` / MSEA `Leaf Tornado` — 현행_GMS_확보

#### 16. 거스트 다이브 (`23111003`, 3차, 2311.img)

- 설명(원문): 바람의 힘으로 공중에서 빠르게 하강하면서 범위 내의 적 다수를 동시에 공격한다. 스킬 사용을 위해 120이상의 점프력이 필요하다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage% 데미지로 #attackCount번 공격
- 힌트(마스터 치환): MP 45 소비, 최대 6명의 적을 195% 데미지로 3번 공격
- common: `{"maxLevel": 20, "mpCon": "25+5*u(x/5)", "damage": "135+3*x", "mobCount": "6", "attackCount": "3", "x": "27+4*u(x/3)", "y": "x", "hcCooltime": "5"}`
- Lv1: `{"level": 1, "mpCon": 30, "damage": 138, "attackCount": 3, "mobCount": 6, "hcCooltime": 5, "x": 31, "y": 1}`
- Lv20(마스터): `{"level": 20, "mpCon": 45, "damage": 195, "attackCount": 3, "mobCount": 6, "hcCooltime": 5, "x": 55, "y": 20}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Gust Dive` / MSEA `Gust Dive` — 현행_GMS_확보

#### 17. 하이킥 데몰리션 (`23110006`, 3차, 2311.img)

- 설명(원문): 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다.  공중으로 뜬 적들을 향해 보이지 않을 속도로 빠르게 날아가 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- 힌트(원문): 액티브 효과 : MP #mpCon 소비, 최대 #mobCount명의 적에게 #damage% 데미지로 #attackCount번 공격, 대상은 #prop% 확률로 즉사 / 패시브 효과 : 차지 드라이브 데미지 #damR% 상승
- 힌트(마스터 치환): 액티브 효과 : MP 32 소비, 최대 8명의 적에게 110% 데미지로 6번 공격, 대상은 15% 확률로 즉사 / 패시브 효과 : 차지 드라이브 데미지 20% 상승
- common: `{"maxLevel": 15, "mpCon": "20+4*u(x/5)", "damage": "95+x", "attackCount": "6", "mobCount": "8", "prop": "x", "damR": "5+x"}`
- Lv1: `{"level": 1, "mpCon": 24, "damage": 96, "attackCount": 6, "mobCount": 8, "prop": 1, "damR": 6}`
- Lv15(마스터): `{"level": 15, "mpCon": 32, "damage": 110, "attackCount": 6, "mobCount": 8, "prop": 15, "damR": 20}`
- 마스터레벨 15 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Aerial Barrage` / MSEA `Aerial Barrage` — 현행_GMS_확보

#### 18. 엘리멘탈 나이트 (`23111008`, 3차, 2311.img)

- 설명(원문): 냉기 정령, 화염 정령, 암흑 정령 중 1명을 랜덤으로 소환하여 전투를 돕게 한다.  / 냉기 정령 : 공격 시 일정 확률로 대상을 결빙 / 화염 정령 : 공격 시 일정 확률로 대상에게 화염 속성의 지속 데미지 / 암흑 정령 : 냉기 정령과 화염 정령보다 강력한 데미지
- 힌트(원문): MP #mpCon 소비하여 3명의 정령 중 1명을 랜덤으로 #time초 동안 소환 / 냉기 정령 : #damage%로 공격하여 대상을 #prop%확률로 #subTime초동안 결빙 / 화염 정령 : #v%로 공격, 대상은 #w초 동안 #x초 당 #y%의 지속 피해 / 암흑 정령 : #z%로 공격 / 재사용 대기시간 #cooltime초
- 힌트(마스터 치환): MP 60 소비하여 3명의 정령 중 1명을 랜덤으로 160초 동안 소환 / 냉기 정령 : 550%로 공격하여 대상을 90%확률로 5초동안 결빙 / 화염 정령 : 550%로 공격, 대상은 5초 동안 1초 당 110%의 지속 피해 / 암흑 정령 : 625%로 공격 / 재사용 대기시간 120초
- common: `{"maxLevel": 20, "mpCon": "140-8*u(x/2)", "time": "60+5*x", "damage": "350+10*x", "subTime": "3+d(x/10)", "prop": "10+4*x", "cooltime": "200-4*x", "v": "350+10*x", "w": "3+d(x/10)", "x": "1", "y": "50+3*x", "z": "385+12*x", "hcSubTime": "1"}`
- Lv1: `{"level": 1, "mpCon": 132, "damage": 360, "cooltime": 196, "time": 65, "subTime": 3, "hcSubTime": 1, "prop": 14, "x": 1, "y": 53, "w": 3, "v": 360, "z": 397}`
- Lv20(마스터): `{"level": 20, "mpCon": 60, "damage": 550, "cooltime": 120, "time": 160, "subTime": 5, "hcSubTime": 1, "prop": 90, "x": 1, "y": 110, "w": 5, "v": 550, "z": 625}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Elemental Knights` / MSEA `Elemental Knights` — 현행_GMS_확보

#### 19. 이그니스 로어 (`23111004`, 3차, 2311.img)

- 설명(원문): 영구적으로 적의 공격을 추가 회피할 수 있게 되며, 스킬 사용 시 불의 정령의 힘을 빌어 일정시간 동안 공격력을 대폭 증가시킨다.
- 힌트(원문): 액티브 효과 : MP #mpCon 소비, #time초동안 공격력 #indiePad 상승 /  패시브 효과 : #prop% 확률로 추가 회피
- 힌트(마스터 치환): 액티브 효과 : MP 60 소비, 180초동안 공격력 40 상승 /  패시브 효과 : 20% 확률로 추가 회피
- common: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "indiePad": "2*x", "prop": "5+3*d(x/4)", "time": "40+7*x"}`
- Lv1: `{"level": 1, "mpCon": 40, "time": 47, "prop": 5, "indiePad": 2}`
- Lv20(마스터): `{"level": 20, "mpCon": 60, "time": 180, "prop": 20, "indiePad": 40}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Ignis Roar` / MSEA `Ignis Roar` — 대응_불확실(현행 표 KMS명 공백)

#### 20. 유니콘 스파이크 (`23111002`, 3차, 2311.img)

- 설명(원문): 성스러운 유니콘을 소환해 전방의 적 다수를 동시에 공격하고 일정시간 동안 약화시킨다. 약화된 대상은 지정된 횟수만큼 아군의 모든 공격에 추가 피해를 받게되며 보스 몬스터에게는 추가 피해 적용횟수가 2배로 적용된다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적을 #damage% 데미지로 #attackCount번 크리티컬 공격, 대상은 #prop% 확률로 #time초 동안 #x%의 추가 피해를 #y번 받는 디버프 효과 적용 / 재사용 대기시간 #cooltime초
- 힌트(마스터 치환): MP 62 소비, 최대 8명의 적을 140% 데미지로 5번 크리티컬 공격, 대상은 95% 확률로 15초 동안 15%의 추가 피해를 10번 받는 디버프 효과 적용 / 재사용 대기시간 10초
- common: `{"maxLevel": 20, "mpCon": "30+8*u(x/5)", "damage": "100+2*x", "mobCount": "8", "attackCount": "5", "time": "5+d(x/2)", "x": "5+d(x/2)", "y": "5+d(x/4)", "z": "10+2*d(x/4)", "prop": "15+4*x", "cooltime": "20-d(x/2)", "cr": "100"}`
- Lv1: `{"level": 1, "mpCon": 38, "damage": 102, "attackCount": 5, "mobCount": 8, "cooltime": 20, "time": 5, "prop": 19, "cr": 100, "x": 5, "y": 5, "z": 10}`
- Lv20(마스터): `{"level": 20, "mpCon": 62, "damage": 140, "attackCount": 5, "mobCount": 8, "cooltime": 10, "time": 15, "prop": 95, "cr": 100, "x": 15, "y": 10, "z": 20}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Unicorn Spike` / MSEA `Unicorn Spike` — 현행_GMS_확보

#### 21. 워터 쉴드 (`23111005`, 3차, 2311.img)

- 설명(원문): 정령의 힘을 빌어 일정시간 동안 자신에게 물의 보호막을 발동시킨다. 보호막은 받는 데미지의 일부를 흡수하고, 상태이상 내성과 모든 속성 내성을 증가시키는 효과가 있다.
- 힌트(원문): MP #mpCon 소비, #time초동안 최대 #x%만큼의 피해를 흡수하고 상태이상 내성과 모든 속성 내성을 #terR% 증가시키는 물의 보호막 발동.
- 힌트(마스터 치환): MP 100 소비, 180초동안 최대 30%만큼의 피해를 흡수하고 상태이상 내성과 모든 속성 내성을 25% 증가시키는 물의 보호막 발동.
- common: `{"maxLevel": 20, "mpCon": "60+10*d(x/5)", "time": "100+4*x", "x": "10+x", "asrR": "5+x", "terR": "5+x"}`
- Lv1: `{"level": 1, "mpCon": 60, "time": 104, "x": 11, "asrR": 6, "terR": 6}`
- Lv20(마스터): `{"level": 20, "mpCon": 100, "time": 180, "x": 30, "asrR": 25, "terR": 25}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 없음 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Water Shield` / MSEA `Water Shield` — 현행_GMS_개칭(KMS명 변경)

#### 22. 디펜스 브레이크 (`23120010`, 4차, 2312.img)

- 설명(원문): 공격 시 일정 확률로 적의 방어율 100%를 무시한다. 보스몬스터에게도 동일하게 적용된다.
- 힌트(원문): #x% 확률로 적의 방어율 100% 무시
- 힌트(마스터 치환): 40% 확률로 적의 방어율 100% 무시
- common: `{"maxLevel": 20, "x": "2*x"}`
- Lv1: `{"level": 1, "x": 2}`
- Lv20(마스터): `{"level": 20, "x": 40}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Defense Break` / MSEA `Defense Break` — 현행_GMS_확보

#### 23. 듀얼보우건 엑스퍼트 (`23120009`, 4차, 2312.img)

- 설명(원문): 듀얼보우건 계열 무기의 숙련도와 물리 공격력, 크리티컬 최소 데미지를 증가시킨다. / 필요 스킬 : #c듀얼보우건 마스터리 20레벨 이상#
- 힌트(원문): 듀얼보우건 계열 무기의 숙련도 #mastery%로 상승, 물리 공격력 #x, 크리티컬 최소 데미지 #criticaldamageMin% 증가
- 힌트(마스터 치환): 듀얼보우건 계열 무기의 숙련도 70%로 상승, 물리 공격력 30, 크리티컬 최소 데미지 15% 증가
- common: `{"maxLevel": 30, "mastery": "55+u(x/2)", "x": "x", "criticaldamageMin": "u(x/2)"}`
- Lv1: `{"level": 1, "x": 1, "mastery": 56, "criticaldamageMin": 1}`
- Lv30(마스터): `{"level": 30, "x": 30, "mastery": 70, "criticaldamageMin": 15}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Dual Bowguns Expert` / MSEA `Dual Bowguns Expert` — 현행_GMS_확보

#### 24. 이슈타르의 링 (`23121000`, 4차, 2312.img)

- 설명(원문): 전설의 무기 이슈타르의 힘을 빌려 빠른 속도로 화살을 전방의 적에게 발사한다. 스킬 키를 누르고 있으면 지속적으로 화살이 발사된다. 추가로 스트라이크 듀얼샷의 데미지를 영구적으로 증가시키는 패시브 효과가 있다. / 필요 스킬 : #c스트라이크 듀얼샷 20레벨 이상#
- 힌트(원문): 액티브 효과 :MP #mpCon 소비, 전방의 적에게 발 당 #damage% 데미지로 #attackCount번의 공격 / 패시브 효과 : 스트라이크 듀얼샷 데미지 #damR% 상승
- 힌트(마스터 치환): 액티브 효과 :MP 10 소비, 전방의 적에게 발 당 110% 데미지로 2번의 공격 / 패시브 효과 : 스트라이크 듀얼샷 데미지 25% 상승
- common: `{"maxLevel": 30, "mpCon": "7+u(x/10)", "damage": "80+x", "attackCount": "2", "damR": "5+2*u(x/3)"}`
- Lv1: `{"level": 1, "mpCon": 8, "damage": 81, "attackCount": 2, "damR": 7}`
- Lv30(마스터): `{"level": 30, "mpCon": 10, "damage": 110, "attackCount": 2, "damR": 25}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Ishtar's Ring` / MSEA `Ishtar's Ring` — 현행_GMS_확보

#### 25. 레전드리 스피어 (`23121002`, 4차, 2312.img)

- 설명(원문): 도약과 동시에 전설의 창을 떨어트려 전방의 적 다수를 공격한다. 대상의 방어력을 일정수준 감소시키는 효과와 함께 100% 크리티컬 판정으로 적중한다. 추가로 리프 토네이도의 데미지를 영구적으로 증가시키는 패시브 효과가 있다. / 필요 스킬 : #c리프 토네이도 10레벨 이상#
- 힌트(원문): 액티브 효과 : MP #mpCon 소비, 최대 #mobCount명의 적을 #damage%로 #attackCount번 크리티컬 공격. #time초 동안 대상의 방어력 #x% 감소 효과 적용 / 재사용 대기시간 #cooltime초 / 패시브 효과 : 리프토네이도 데미지 #damR% 상승
- 힌트(마스터 치환): 액티브 효과 : MP 60 소비, 최대 12명의 적을 540%로 2번 크리티컬 공격. 15초 동안 대상의 방어력 -20% 감소 효과 적용 / 재사용 대기시간 5초 / 패시브 효과 : 리프토네이도 데미지 30% 상승
- common: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "damage": "420+6*x", "mobCount": "12", "damR": "10+x", "attackCount": "2", "time": "5+d(x/2)", "x": "-x", "cooltime": "10-d(x/4)"}`
- Lv1: `{"level": 1, "mpCon": 40, "damage": 426, "attackCount": 2, "mobCount": 12, "cooltime": 10, "time": 5, "x": -1, "damR": 11}`
- Lv20(마스터): `{"level": 20, "mpCon": 60, "damage": 540, "attackCount": 2, "mobCount": 12, "cooltime": 5, "time": 15, "x": -20, "damR": 30}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Spikes Royale` / MSEA `Spikes Royale` — 현행_GMS_확보

#### 26. 라이트닝 엣지 (`23121003`, 4차, 2312.img)

- 설명(원문): 전방을 향해 순간적으로 이동하며 경로 내 적 다수를 공격한다.
- 힌트(원문): MP #mpCon 소비, 최대 #mobCount명의 적에게 #damage%의 데미지로 #attackCount번 공격하며 전방으로 이동 / 재사용 대기시간 #cooltime초
- 힌트(마스터 치환): MP 74 소비, 최대 8명의 적에게 420%의 데미지로 3번 공격하며 전방으로 이동 / 재사용 대기시간 5초
- common: `{"maxLevel": 30, "mpCon": "50+4*u(x/5)", "damage": "270+5*x", "attackCount": "3", "mobCount": "8", "cooltime": "10-d(x/6)"}`
- Lv1: `{"level": 1, "mpCon": 54, "damage": 275, "attackCount": 3, "mobCount": 8, "cooltime": 10}`
- Lv30(마스터): `{"level": 30, "mpCon": 74, "damage": 420, "attackCount": 3, "mobCount": 8, "cooltime": 5}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Lightning Edge` / MSEA `Lightning Edge` — 현행_GMS_확보

#### 27. 롤링 문썰트 (`23120011`, 4차, 2312.img)

- 설명(원문): 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다. 공중에 뜬 적들을 빠르게 회전하며 연속 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- 힌트(원문): 액티브 효과 : MP #mpCon 소비, 최대 #mobCount명의 적에게 #damage%의 데미지로 #attackCount번 공격 / 패시브 효과 : 차지 드라이브 데미지 #damR% 상승
- 힌트(마스터 치환): 액티브 효과 : MP 70 소비, 최대 8명의 적에게 180%의 데미지로 6번 공격 / 패시브 효과 : 차지 드라이브 데미지 50% 상승
- common: `{"maxLevel": 20, "mpCon": "50+4*u(x/4)", "damage": "140+2*x", "attackCount": "6", "mobCount": "8", "damR": "10+2*x"}`
- Lv1: `{"level": 1, "mpCon": 54, "damage": 142, "attackCount": 6, "mobCount": 8, "damR": 12}`
- Lv20(마스터): `{"level": 20, "mpCon": 70, "damage": 180, "attackCount": 6, "mobCount": 8, "damR": 50}`
- 마스터레벨 20 / WZ masterLevel(전투명령 상한) 없음 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Rolling Moonsault` / MSEA `Rolling Moonsault` — 대응_불확실(현행 표 KMS명 공백)

#### 28. 앤시언트 스피릿 (`23121004`, 4차, 2312.img)

- 설명(원문): 일정시간동안 고대 정령의 가호를 받아 데미지와 HP를 증가시키며, 영구적으로 이그니스 로어의 회피 확률을 상승시킨다. / 필요 스킬 : #c이그니스 로어 5레벨 이상#
- 힌트(원문): 액티브 효과 : MP #mpCon 소비, #time초간 데미지 #damR%, 체력 #emhp 증가 / 패시브 효과 : 이그니스 로어의 회피 확률 #prop% 상승
- 힌트(마스터 치환): 액티브 효과 : MP 80 소비, 210초간 데미지 30%, 체력 1500 증가 / 패시브 효과 : 이그니스 로어의 회피 확률 20% 상승
- common: `{"maxLevel": 30, "mpCon": "45+5*d(x/4)", "time": "60+5*x", "prop": "5+u(x/2)", "damR": "x", "x": "1", "emhp": "50*x"}`
- Lv1: `{"level": 1, "mpCon": 45, "time": 65, "prop": 6, "x": 1, "damR": 1, "emhp": 50}`
- Lv30(마스터): `{"level": 30, "mpCon": 80, "time": 210, "prop": 20, "x": 1, "damR": 30, "emhp": 1500}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Ancient Warding` / MSEA `Ancient Warding` — 현행_GMS_확보

#### 29. 메이플 용사 (`23121005`, 4차, 2312.img)

- 설명(원문): 일정시간 동안 파티원의 모든 스탯을 일정 퍼센트만큼 상승시켜 준다.
- 힌트(원문): MP #mpCon 소비, #time초간 모든 스탯 #x% 향상
- 힌트(마스터 치환): MP 70 소비, 900초간 모든 스탯 15% 향상
- common: `{"maxLevel": 30, "mpCon": "10+10*d(x/5)", "x": "u(x/2)", "time": "30*x"}`
- Lv1: `{"level": 1, "mpCon": 10, "time": 30, "x": 1}`
- Lv30(마스터): `{"level": 30, "mpCon": 70, "time": 900, "x": 15}`
- 마스터레벨 30 / WZ masterLevel(전투명령 상한) 10 / combatOrders 1 / invisible 없음
- 아이콘: icon(32x32 fmt1 raw2048B), iconMouseOver(32x32 fmt1 raw2048B), iconDisabled(32x32 fmt1 raw2048B)
- 영문명: GMS `Maple Warrior` / MSEA `Maple Warrior` — 현행_GMS_확보

## 5. 기존 판정값과의 대조 지점

규칙: 클라이언트 값과 기존 판정값이 어긋나면 **덮어쓰지 않고** 아래에 병기한다.

### 5.1 M(마스터레벨)
- 판정 M ↔ 클라이언트 `common.maxLevel`: **58/58 일치**, 불일치 0.
- 주의: `Skill.wz` 노드의 `masterLevel`(4차 스킬 10)은 전투명령 상한으로, 판정의 M(=maxLevel, 4차 30)과 **다른 값**이다. 혼용 금지.

### 5.2 2단 판정 수치 12건 재계산

| skill_id | 스킬 | 판정값(value_setB) | 클라 재계산(M) | 판정 |
|---|---|---|---|---|
| 5301001 | 몽키 러쉬붐 | 50% · 8명 3회 + 300% 폭발 | damage 50 · mob 8 · atk 3 · MP 28 | 클라 재계산값(위 문안과 대조) |
| 5301000 | 슬러그 샷 | 220% · 최대 4명 2회 | damage 220 · mob 4 · atk 타수미기재/탄수 2 · MP 24 | 클라 재계산값(위 문안과 대조) |
| 5311002 | 몽키 웨이브 | 860%(최대) · 기절 95% | damage 860 · mob 8 · atk 타수미기재/탄수 None · MP 55 | 클라 재계산값(위 문안과 대조) |
| 5311000 | 캐논 스파이크 | 240% · 6명 3회 | damage 240 · mob 6 · atk 3 · MP 36 | 클라 재계산값(위 문안과 대조) |
| 5321000 | 캐논 바주카 | 500% · 6명 4회 | damage 500 · mob 6 · atk 4 · MP 75 | 클라 재계산값(위 문안과 대조) |
| 5321012 | 캐논 버스터 | 320% · 5회 · 추가 크리 15% (후딜 810ms는 미확보·분리) | damage 320 · mob 1 · atk 타수미기재/탄수 5 · MP 63 | 클라 재계산값(위 문안과 대조) |
| 5321003 | 마그네틱 앵커 | 400% + 지속 종료 시 520% | damage 400 · mob 8 · atk 타수미기재/탄수 None · MP 86 | 클라 재계산값(위 문안과 대조) |
| 23100004 | 파이널 샷 | 70% · 최대 8명 4회 | damage 70 · mob 8 · atk 4 · MP 16 | 클라 재계산값(위 문안과 대조) |
| 23110006 | 하이킥 데몰리션 | 110% · 6회 · 즉사 15% | damage 110 · mob 8 · atk 6 · MP 32 | 클라 재계산값(위 문안과 대조) |
| 23121002 | 레전드리 스피어 | 540% · 12명 2회 · 방어력 -20%(15초) · 쿨 5초 | damage 540 · mob 12 · atk 2 · MP 60 | 클라 재계산값(위 문안과 대조) |
| 23121003 | 라이트닝 엣지 | 420% · 8명 3회 · 쿨 5초 | damage 420 · mob 8 · atk 3 · MP 74 | 클라 재계산값(위 문안과 대조) |
| 23120011 | 롤링 문썰트 | 180% · 6회 | damage 180 · mob 8 · atk 6 · MP 70 | 클라 재계산값(위 문안과 대조) |

- 불일치 목록: 없음(0건)

### 5.3 공식 문안 MP 대조

| 출처 | 스킬 | 공식 문안 MP | 클라 MP(M) | 일치 |
|---|---|---:|---:|---|
| F12 | 슬러그 샷 | 24 | 24 | 일치 |
| F12 | 몽키 러쉬붐 | 28 | 28 | 일치 |
| F12 | 캐논 스파이크 | 36 | 36 | 일치 |
| F12 | 몽키 웨이브 | 55 | 55 | 일치 |
| F12 | 캐논 버스터 | 63 | 63 | 일치 |
| F12 | 마그네틱 앵커 | 86 | 86 | 일치 |
| F12 | 캐논 바주카 | 75 | 75 | 일치 |
| F13 | 라이트닝 엣지 | 74 | 74 | 일치 |
| F13 | 레전드리 스피어 | 60 | 60 | 일치 |
| F14 | 하이킥 데몰리션 | 28 | 32 | **불일치** |

- 9/10 일치 (F14 하이킥 데몰리션은 2013-03 테섭 변경 후 문안으로 2012 수치와 혼용 금지 — 참고만)
- F14(하이킥 데몰리션 MP 28·105%·10%·M5)는 2013-03 테스트서버 변경 후 문안이라 2012 세트 값(MP 32, 110%, 15%, M15)과 혼용하지 않는다. 클라이언트 값이 세트 기준이다.

### 5.4 명칭 표기차 (덮어쓰지 않음)

| skill_id | 클라(1.2.160) | 비교 대상 | 비고 |
|---|---|---|---|
| 5011002 | 기간틱 백스탭 | 현행 KMS: 기간틱 백스텝 | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 5321004 | 서포트 몽키 트윈스 | 현행 KMS: 서포트 몽키 | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 23001002 | 아크로바틱 점프 | 현행 KMS: 스피릿 점프 | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 23101003 | 스피릿 인퓨젼 | 판정 목록: 스피릿 인퓨전 | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |
| 23100006 | 파이널 어택 : 듀얼보우건 | 판정 목록: 파이널 어택 | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |
| 23111005 | 워터 쉴드 | 현행 KMS: 워터실드 | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 23111005 | 워터 쉴드 | 판정 목록: 워터 실드 | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |

사이트 표기는 **클라이언트(2012) String.wz 표기**를 정본으로 두고, 위 표기차는 참고로만 남긴다.

### 5.5 영문명 주의 10건

| skill_id | 스킬 | 상태 | GMS 참고 | MSEA 참고 |
|---|---|---|---|---|
| 5011002 | 기간틱 백스탭 | 현행_GMS_개칭(KMS명 변경) | Blast Back | Blast Back |
| 5301002 | 캐논 부스터 | 대응_불확실(현행 표 KMS명 공백) | — | Cannon Booster |
| 5311004 | 오크통 룰렛 | 대응_불확실(현행 표 KMS명 공백) | Forty Winks | Slumber |
| 5310007 | 바이탈 익스트림 | 현행_GMS_개칭(영문명 변경) | Pirate Rush | Pirate Rush |
| 5321004 | 서포트 몽키 트윈스 | 현행_GMS_개칭(KMS명 변경) | Support Monkey | Monkey Artillery |
| 23001002 | 아크로바틱 점프 | 현행_GMS_개칭(KMS명 변경) | Spirit Jump | Spirit Jump |
| 23101003 | 스피릿 인퓨젼 | 대응_불확실(현행 표 KMS명 공백) | Spirit Surge | Spirit Surge |
| 23111004 | 이그니스 로어 | 대응_불확실(현행 표 KMS명 공백) | Ignis Roar | Ignis Roar |
| 23111005 | 워터 쉴드 | 현행_GMS_개칭(KMS명 변경) | Water Shield | Water Shield |
| 23120011 | 롤링 문썰트 | 대응_불확실(현행 표 KMS명 공백) | Rolling Moonsault | Rolling Moonsault |

- 영문명 값은 전부 현행(2026) GMS/MSEA 명칭이다. 2012년 시점 GMS 명칭은 별도 근거가 없어 **미검증**으로 두며, 개칭 이력이 확인된 건은 상태에 표시했다.
- `5310007 바이탈 익스트림` → 현행 GMS `Pirate Rush`: 기존 ID 목록의 id_note에 "현행 영문명 Pirate Rush로 개칭(동일 ID)"로 기록된 건.
- `5311004 오크통 룰렛`: 현행 표에 KMS 명칭이 비어 있고 GMS 열은 `Forty Winks`(수면 계열 명칭)로, 오크통 룰렛과 의미가 맞지 않는다. **채택 보류**(추정 금지).
- `5301002 캐논 부스터`는 GMS 공백·MSEA `Cannon Booster`만 있어 확정하지 않았다.
- 나머지 3건(23101003 스피릿 인퓨젼·23111004 이그니스 로어·23120011 롤링 문썰트)은 현행 GMS 표기가 있으나 KMS 슬롯이 공백이라 대응을 확정하지 않았다.

## 6. 대상 58종 밖 클라이언트 항목 (12건, 전부 invisible=1)

| skill_id | img | String.wz 명칭 | maxLevel | 비고 |
|---|---|---|---:|---|
| 23000004 | 2300.img | 네이쳐스 드레인 | 1 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 23101007 | 2310.img | (이름 없음) | 20 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 23111009 | 2311.img | 엘리멘탈 나이트 | 20 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 23111010 | 2311.img | 엘리멘탈 나이트 | 20 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 23121008 | 2312.img | 용사의 의지 | 5 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5010004 | 501.img | 포춘 어택 | 1 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5010005 | 501.img | (이름 없음) | 1 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5300007 | 530.img | (이름 없음) | 20 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5310008 | 531.img | 몽키 웨이브 | 20 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5320011 | 532.img | (이름 없음) | 15 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5321005 | 532.img | 메이플 용사 | 30 | 숨김(invisible=1) — 58종 목록 제외 근거 |
| 5321006 | 532.img | 용사의 의지 | 5 | 숨김(invisible=1) — 58종 목록 제외 근거 |

## 7. 산출 파일과 검증

- `justice_t2_merc_cannon_client_extract_20261120.json` — 58종 전량(설명문·힌트·common 수식·레벨별 수치·아이콘 경로·영문명·판정 대조)
- `t2_merc_cannon_icons_20261120/` — PNG 188장(파일명 `{skill_id}_{icon|iconMouseOver|iconDisabled|icon1..5}.png`)

검증:
- JSON 파싱·스키마: 통과(58건, 각 항목 필수 필드 존재)
- 아이콘: 188장 전부 32×32, fmt1(ARGB4444), PIL 검증 통과, 0바이트/손상 0
- 설명문·힌트 누락 0, 미치환 토큰 0
- 아이콘 픽셀 대조: 현행 GMS 아이콘과 완전 일치 다수 확인
