# 저스티스 2단 메르세데스·캐논슈터 신규 58종 — 요청서 4항목 + 판정 필드 층위 적용 편입본

- 생성: 2026-11-20 (KST)
- 데이터 본체: `justice_t2_merc_cannon_extract58_mergefields_20261120.json` (스킬 58건)
- 아이콘: `t2_merc_cannon_icons_20261120/` (PNG 188장 — 원천 세대와 같은 파일 재사용, 복제 없음)
- 계보: `justice_t2_merc_cannon_client_extract_20261120.json`(SHA-256 `ea4098c6dbfb4fc1dd6c54a9d8dada479160f9175a6a4e60f0948695cd478e64`, 337,629 B, 커밋 234d58c)의 **값을 그대로** 옮기고 필드 이름·층위만 정렬한 세대. 데이터 재추출 없음.

## 0. 요청서와 판정

| 구분 | 파일 | SHA-256 | 커밋 |
|---|---|---|---|
| 요청서 | `packages/t2-extract-request-20261120/T2-CANDIDATE-MISSING-AND-EXTRACT-REQUEST-20261120.md` | `ac58cfe2ff98b6ea…` | `ddc39c6` |
| 판정 | `verdicts/VERDICT-2단추출58종-형식·영문명·표기정본-20261120.md` | `454596cd55285cab…` | `3b13e80` |

- 요청 항목: ① 설명문(desc·shortDesc 한글 원문) ② 레벨별 속성(properties — 데미지%·MP·횟수 등, 마스터 레벨 기준) ③ 영문명 ④ 아이콘 PNG(스킬 ID 파일명)
- 판정 요지: 본 세대 생성 직전에 올라온 Claude 판정(재현 12건 · 형식 · 영문명 · 표기 정본). 판정은 원천 추출본만으로 요청 4항목이 충족된다며 재포장 불필요로 결론냈다. 본 파일은 원천 세대를 대체하지 않고, 판정 §2가 배정한 필드명(desc_ko·levels_kms160·name_en_basis·aliases_ko)으로 값을 미리 옮긴 편입용 사본이다.

## 1. 요청 항목별 이행

| # | 요청 | 이행 필드 | 상태 | 내용 |
|---|---|---|---|---|
| ① | 설명문 — desc · shortDesc 한글 원문 | `desc_ko / shortDesc_ko` | 부분 이행 | desc 58/58(한글 원문, KMS 층위). shortDesc는 0/58 — 클라에 필드가 없어 null + 건별 사유. 간략본 pdesc 48/58은 미채택 병기. |
| ② | 레벨별 속성(properties) — 데미지% · MP · 횟수 등, 마스터 레벨 기준 | `levels_kms160 (values_at_master_level / levels / common_raw)` | 이행 | 마스터 레벨 기준 값 58/58 + 레벨 1~M 전 구간 58/58 + 수식 원문(common_raw). field명은 판정 §2에 따라 levels_kms160(GMS95 properties_raw와 층위 분리). |
| ③ | 영문명 | `name_en (+ name_en_basis · verified_2012)` | 이행(보조 필드 규칙 적용) | name_en 58/58 — 현행 GMS 기준 56건, MSEA·MSN 대체 2건. verified_2012는 전건 false(2012 명칭 미검증). 한글명이 화면 정본. |
| ④ | 아이콘 PNG (스킬 ID 파일명) | `icons.base / icons.files` | 이행 | base(<skill_id>_icon.png) 58/58 + 상태별 총 188장. 기존 폴더 t2_merc_cannon_icons_20261120/ 재사용(바이트 동일). |
| 주의 | 클라 값 = '현행 KMS 1.2.160' 층위 · 2012 판정값과 어긋나는 지점은 덮어쓰지 말고 대조 지점 표시 | `대조_지점[] / skills[].판정_대조` | 이행 | 대조 지점 60건 유형화 — 판정값·기존 표기 덮어쓰기 0. |

## 2. 판정 반영

| 건 | 판정 | 이 파일에서의 적용 |
|---|---|---|
| 재현 | 판정값 12건 독립 재현 확인 | 판정값 미변경 · 클라 재계산값 병기(대조_지점 판정값_재현 12건) |
| 1 | 재포장 불필요 · 영문명은 현행 GMS + 출처 라벨 보조 필드 | 별도 스키마를 만들지 않고 요청서 4항목을 그대로 담되, 필드 층위를 판정 §2 규칙(desc_ko·levels_kms160·name_en_basis·verified_2012)으로 정렬 |
| 2 | 4건 채택 · 5311004는 Forty Winks 기각 → Barrel Roulette | name_en 값·basis 라벨 반영(5311004 MSN-직역 라벨, 5301002 MSEA, 23101003 개칭 의심 주석) |
| 3 | 58종 고정 · 5321005·5321006 미노출 | 58건 유지, 두 스킬과 23121008을 대상외[]에 사유와 함께 보존 |
| 4 | 2012 클라 표기를 정본 | name_ko는 클라 표기 그대로, 판정 목록·현행 KMS 표기는 aliases_ko로 보존(검색 별칭) |

## 3. 필드 층위 정렬 (판정 §2)

본 세대 생성 직전에 Claude 판정이 올라와 “원천 추출본만으로 요청 4항목이 충족된다 — 재포장 불필요”로 결론냈다. 원천 세대는 그대로 보존하고, 이 파일은 판정 §2가 배정한 필드명으로 값을 미리 옮긴 **편입용 사본**이다. 아래 층위 규칙만 적용했다.

| 항목 | 원천 세대(추출본) | 판정 규칙 | 편입본 필드 |
|---|---|---|---|
| 한글 설명문 | `desc` · `desc_plain` | 기존 610종 `description`은 GMS 영문 층위 → 한글은 `desc_ko`로 분리, `description`은 null 유지 | `desc_ko` · `desc_ko_source` · `shortDesc_ko`(null) · `pdesc_ko`(미채택) |
| 힌트 | `hint` · `hint_at_master` | 설명문과 같은 KMS 층위 | `hint_ko` · `hint_ko_at_master` · `hint_ko_미치환_토큰` |
| 레벨별 수치 | `common_raw` + `levels[]` | `properties_raw`(GMS95)와 섞지 않고 `levels_kms160`(수식 `common_raw` 포함)으로 분리 | `levels_kms160{master_level, values_at_master_level, common_raw, levels}` |
| 영문명 | `name_en{gms, msea, 확정}` | 보조 필드 — 현행 GMS 명칭 + `name_en_basis` + `verified_2012:false`, 공백 시 MSEA→MSN | `name_en` · `name_en_basis` · `verified_2012` · `name_en_msea` · `name_en_note` |
| 한글 표기 | `name_ko` | 2012 클라 표기를 정본, 기존 표기는 검색 별칭 | `name_ko` · `name_ko_basis` · `aliases_ko` |
| 아이콘 | `icons{}` | 스킬 ID 파일명 | `icons{base, files, 규격}` — base = `<skill_id>_icon.png` |
| 대조 지점 | 분산된 `대조{...}` | 덮어쓰지 말고 병기 | `대조_지점[]` 60건 |

`description`·`properties_raw` 필드는 이 파일에 넣지 않았다(병합 시 null 유지 — GMS 영문·수치 원문은 이번 58종에 없다).

## 4. 스킬 58종 — 마스터 레벨 기준 속성

`MP`·`데미지%`·`대상`·`횟수`는 `levels_kms160.values_at_master_level`의 mpCon·damage·mobCount·attackCount(bulletCount). `—`는 해당 필드가 클라에 없는 스킬(버프·패시브 등), `(탄)`은 타수가 bulletCount로 표기되는 건.

| # | 직업 | 차수 | 스킬(KMS 1.2.160) | skill_id | M | MP | 데미지% | 대상 | 횟수 | name_en (basis) |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 캐논슈터 | 1차 | 캐논 스플래셔 | 5011000 | 20 | 11 | 225 | 3 | — | Cannon Blaster (current-GMS) |
| 2 | 캐논슈터 | 1차 | 기간틱 백스탭 | 5011002 | 15 | 20 | 210 | 3 | — | Blast Back (current-GMS) |
| 3 | 캐논슈터 | 1차 | 빌드업 캐논 | 5010003 | 10 | — | — | — | — | Cannon Boost (current-GMS) |
| 4 | 캐논슈터 | 1차 | 펀칭 캐논 | 5011001 | 20 | 9 | 95 | 1 | 3 | Cannon Strike (current-GMS) |
| 5 | 캐논슈터 | 2차 | 몽키 러쉬붐 | 5301001 | 20 | 28 | 50 | 8 | 3 | Barrel Bomb (current-GMS) |
| 6 | 캐논슈터 | 2차 | 몽키 매직 | 5301003 | 20 | 55 | — | — | — | Monkey Magic (current-GMS) |
| 7 | 캐논슈터 | 2차 | 캐논 마스터리 | 5300005 | 20 | — | — | — | — | Cannon Mastery (current-GMS) |
| 8 | 캐논슈터 | 2차 | 캐논 부스터 | 5301002 | 20 | 11 | — | — | — | Cannon Booster (MSEA) |
| 9 | 캐논슈터 | 2차 | 크리티컬 파이어 | 5300004 | 15 | — | — | — | — | Critical Fire (current-GMS) |
| 10 | 캐논슈터 | 2차 | 파이렛 트레이닝 | 5300008 | 10 | — | — | — | — | Pirate Training (current-GMS) |
| 11 | 캐논슈터 | 2차 | 슬러그 샷 | 5301000 | 20 | 24 | 220 | 4 | 2(탄) | Scatter Shot (current-GMS) |
| 12 | 캐논슈터 | 3차 | 몽키 웨이브 | 5311002 | 20 | 55 | 860 | 8 | — | Monkey Wave (current-GMS) |
| 13 | 캐논슈터 | 3차 | 몽키 파워붐 | 5311001 | 20 | 46 | 280 | 10 | 5 | Monkey Madness (current-GMS) |
| 14 | 캐논슈터 | 3차 | 캐논 스파이크 | 5311000 | 20 | 36 | 240 | 6 | 3 | Cannon Spike (current-GMS) |
| 15 | 캐논슈터 | 3차 | 캐논 점프 | 5311003 | 15 | 35 | 210 | 6 | — | Cannon Jump (current-GMS) |
| 16 | 캐논슈터 | 3차 | 오크통 룰렛 | 5311004 | 10 | 60 | — | — | — | Barrel Roulette (MSN-직역) |
| 17 | 캐논슈터 | 3차 | 럭키 다이스 | 5311005 | 20 | 60 | — | — | — | Roll of the Dice (current-GMS) |
| 18 | 캐논슈터 | 3차 | 리인포스 캐논 | 5310006 | 15 | — | — | — | — | Reinforced Cannon (current-GMS) |
| 19 | 캐논슈터 | 3차 | 바이탈 익스트림 | 5310007 | 20 | — | — | — | — | Pirate Rush (current-GMS) |
| 20 | 캐논슈터 | 3차 | 반격의 슈터 | 5310009 | 15 | — | 160 | — | — | Counter Crush (current-GMS) |
| 21 | 캐논슈터 | 4차 | 캐논 바주카 | 5321000 | 30 | 75 | 500 | 6 | 4 | Cannon Bazooka (current-GMS) |
| 22 | 캐논슈터 | 4차 | 캐논 버스터 | 5321012 | 30 | 63 | 320 | 1 | 5(탄) | Cannon Barrage (current-GMS) |
| 23 | 캐논슈터 | 4차 | 전함 노틸러스 | 5321001 | 30 | 350 | 520 | 15 | 3 | Nautilus Strike (current-GMS) |
| 24 | 캐논슈터 | 4차 | 파이렛 스피릿 | 5321010 | 30 | 80 | — | — | — | Pirate's Spirit (current-GMS) |
| 25 | 캐논슈터 | 4차 | 마그네틱 앵커 | 5321003 | 15 | 86 | 400 | 8 | — | Anchors Aweigh (current-GMS) |
| 26 | 캐논슈터 | 4차 | 서포트 몽키 트윈스 | 5321004 | 15 | 70 | 350 | 1 | — | Support Monkey (current-GMS) |
| 27 | 캐논슈터 | 4차 | 더블 럭키 다이스 | 5320007 | 5 | 60 | — | — | — | Double Down (current-GMS) |
| 28 | 캐논슈터 | 4차 | 하이퍼 몽키 스펠 | 5320008 | 30 | 80 | — | — | — | Mega Monkey Magic (current-GMS) |
| 29 | 캐논슈터 | 4차 | 오버버닝 캐논 | 5320009 | 30 | — | — | — | — | Cannon Overload (current-GMS) |
| 30 | 메르세데스 | 1차 | 스피드 듀얼샷 | 23001000 | 20 | 14 | 115 | 3 | 2(탄) | Swift Dual Shot (current-GMS) |
| 31 | 메르세데스 | 1차 | 샤프 에이밍 | 23000003 | 20 | — | — | — | — | Sharp Aim (current-GMS) |
| 32 | 메르세데스 | 1차 | 아크로바틱 점프 | 23001002 | 10 | 10 | — | — | — | Spirit Jump (current-GMS) |
| 33 | 메르세데스 | 1차 | 포텐셜 파워 | 23000001 | 15 | — | — | — | — | Potential Power (current-GMS) |
| 34 | 메르세데스 | 2차 | 피지컬 트레이닝 | 23100008 | 10 | — | — | — | — | Physical Training (current-GMS) |
| 35 | 메르세데스 | 2차 | 듀얼보우건 마스터리 | 23100005 | 20 | — | — | — | — | Dual Bowguns Mastery (current-GMS) |
| 36 | 메르세데스 | 2차 | 듀얼보우건 부스터 | 23101002 | 20 | 11 | — | — | — | Dual Bowguns Boost (current-GMS) |
| 37 | 메르세데스 | 2차 | 스피릿 인퓨젼 | 23101003 | 15 | 45 | 15 | — | — | Spirit Surge (current-GMS) |
| 38 | 메르세데스 | 2차 | 차지 드라이브 | 23101001 | 15 | 25 | 130 | 8 | — | Rising Rush (current-GMS) |
| 39 | 메르세데스 | 2차 | 파이널 샷 | 23100004 | 5 | 16 | 70 | 8 | 4 | Parting Shot (current-GMS) |
| 40 | 메르세데스 | 2차 | 파이널 어택 : 듀얼보우건 | 23100006 | 20 | — | 75 | 1 | 2 | Final Attack: Dual Bowguns (current-GMS) |
| 41 | 메르세데스 | 4차 | 어드밴스드 파이널 어택 | 23120012 | 30 | — | 105 | 1 | 2 | Advanced Final Attack (current-GMS) |
| 42 | 메르세데스 | 2차 | 크로스 피어싱 | 23101000 | 20 | 24 | 83 | 6 | 4(탄) | Piercing Storm (current-GMS) |
| 43 | 메르세데스 | 3차 | 스트라이크 듀얼샷 | 23111000 | 20 | 35 | 120 | 5 | 4(탄) | Stunning Strikes (current-GMS) |
| 44 | 메르세데스 | 3차 | 리프 토네이도 | 23111001 | 20 | 45 | 135 | 8 | 4 | Leaf Tornado (current-GMS) |
| 45 | 메르세데스 | 3차 | 거스트 다이브 | 23111003 | 20 | 45 | 195 | 6 | 3 | Gust Dive (current-GMS) |
| 46 | 메르세데스 | 3차 | 하이킥 데몰리션 | 23110006 | 15 | 32 | 110 | 8 | 6 | Aerial Barrage (current-GMS) |
| 47 | 메르세데스 | 3차 | 엘리멘탈 나이트 | 23111008 | 20 | 60 | 550 | — | — | Elemental Knights (current-GMS) |
| 48 | 메르세데스 | 3차 | 이그니스 로어 | 23111004 | 20 | 60 | — | — | — | Ignis Roar (current-GMS) |
| 49 | 메르세데스 | 3차 | 유니콘 스파이크 | 23111002 | 20 | 62 | 140 | 8 | 5 | Unicorn Spike (current-GMS) |
| 50 | 메르세데스 | 3차 | 워터 쉴드 | 23111005 | 20 | 100 | — | — | — | Water Shield (current-GMS) |
| 51 | 메르세데스 | 4차 | 디펜스 브레이크 | 23120010 | 20 | — | — | — | — | Defense Break (current-GMS) |
| 52 | 메르세데스 | 4차 | 듀얼보우건 엑스퍼트 | 23120009 | 30 | — | — | — | — | Dual Bowguns Expert (current-GMS) |
| 53 | 메르세데스 | 4차 | 이슈타르의 링 | 23121000 | 30 | 10 | 110 | — | 2 | Ishtar's Ring (current-GMS) |
| 54 | 메르세데스 | 4차 | 레전드리 스피어 | 23121002 | 20 | 60 | 540 | 12 | 2 | Spikes Royale (current-GMS) |
| 55 | 메르세데스 | 4차 | 라이트닝 엣지 | 23121003 | 30 | 74 | 420 | 8 | 3 | Lightning Edge (current-GMS) |
| 56 | 메르세데스 | 4차 | 롤링 문썰트 | 23120011 | 20 | 70 | 180 | 8 | 6 | Rolling Moonsault (current-GMS) |
| 57 | 메르세데스 | 4차 | 앤시언트 스피릿 | 23121004 | 30 | 80 | — | — | — | Ancient Warding (current-GMS) |
| 58 | 메르세데스 | 4차 | 메이플 용사 | 23121005 | 30 | 70 | — | — | — | Maple Warrior (current-GMS) |

### 4.1 설명문·힌트 원문 (58건)

`desc_ko`는 String.wz 원문 그대로. `shortDesc_ko`는 클라에 필드가 없어 전건 null이다(사유는 `shortDesc_ko_사유`). `pdesc_ko`는 desc의 간략본이지만 채택하지 않았다.

#### 캐논슈터 (29종)

**1. 캐논 스플래셔** (`5011000` · 1차 · 501.img · M20)

- desc_ko: 화염탄을 발사하여 다수의 적을 공격한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 화염탄을 발사하여 다수의 적을 공격한다.
- hint_ko(M): MP 11 소비, 225% 데미지로 최대 3명의 적 공격
- common_raw: `{"maxLevel": 20, "mpCon": "6+u(x/4)", "damage": "185+2*x", "mobCount": "3", "range": "450"}`
- name_en: `Cannon Blaster` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5011000_icon.png`

**2. 기간틱 백스탭** (`5011002` · 1차 · 501.img · M15)

- desc_ko: 후방으로 긴급 회피하며 캐논을 발사한다. 일정 확률로 대상의 이동속도를 감소시킬 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 후방으로 긴급 회피하며 캐논을 발사한다. 일정 확률로 대상의 이동속도를 감소시킬 수 있다.
- hint_ko(M): MP 20 소비, 210% 데미지로 3명의 적 공격, 70% 확률로 5초 간 대상의 이동속도 -60
- common_raw: `{"maxLevel": 15, "mpCon": "45-5*d(x/3)", "damage": "150+4*x", "mobCount": "3", "time": "2+d(x/5)", "prop": "25+3*x", "z": "-15-3*x", "x": "250+d(x/4)*70", "y": "260+d(x/4)*30", "range": "450", "hcTime": "1"}`
- name_en: `Blast Back` (current-GMS, verified_2012=false) · aliases_ko: 기간틱 백스텝
- 아이콘: `t2_merc_cannon_icons_20261120/5011002_icon.png`

**3. 빌드업 캐논** (`5010003` · 1차 · 501.img · M10)

- desc_ko: 캐논을 개량하여 영구적으로 공격력과 방어력을 향상시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 공격력 20, 물리 방어력 250, 마법 방어력 250 증가
- common_raw: `{"maxLevel": 10, "padX": "2*x", "pddX": "25*x", "mddX": "25*x"}`
- name_en: `Cannon Boost` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5010003_icon.png`

**4. 펀칭 캐논** (`5011001` · 1차 · 501.img · M20)

- desc_ko: 적 하나에게 강력한 캐논 펀치를 날린다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 적 하나에게 강력한 캐논 펀치를 날린다.
- hint_ko(M): MP 9 소비, 95%로 3번 공격
- common_raw: `{"maxLevel": 20, "mpCon": "5+2*u(x/10)", "damage": "75+x", "attackCount": "3", "mobCount": "1"}`
- name_en: `Cannon Strike` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5011001_icon.png`

**5. 몽키 러쉬붐** (`5301001` · 2차 · 530.img · M20)

- desc_ko: 폭탄이 가득 들어있는 오크통을 굴린다. 오크통은 일정 거리를 굴러가며 적들을 밀어낸 뒤에 폭발한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 폭탄이 가득 들어있는 오크통을 굴린다. 오크통은 일정 거리를 굴러가며 적들을 밀어낸 뒤에 폭발한다. 
- hint_ko(M): MP 28 소비, 50% 데미지로 최대 8명의 적을 3번 공격, 대상은 100%확률로 넉백, 일정 거리 이동 후 300%의 데미지로 폭발
- common_raw: `{"maxLevel": 20, "mpCon": "20+2*d(x/5)", "damage": "30+x", "mobCount": "8", "attackCount": "3", "time": "900", "prop": "50+5*d(x/2)", "w": "240+3*x", "x": "350"}`
- name_en: `Barrel Bomb` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5301001_icon.png`

**6. 몽키 매직** (`5301003` · 2차 · 530.img · M20)

- desc_ko: 몽키의 마법으로 일정 시간동안 주변 파티원들의 HP, MP, 올스텟, 이동속도, 점프력, 명중치, 회피치를 높여준다. 다른 모든 버프 스킬과 중복으로 사용할 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): MP 55 소비, 300초간 HP 300, MP 300, 올스텟 20, 이동속도 10, 점프력 5, 명중치 160, 회피치 160 증가
- common_raw: `{"mpCon": "30+5*d(x/4)", "time": "15*x", "indieMhp": "15*x", "indieMmp": "15*x", "indieAllStat": "x", "indieSpeed": "u(x/2)", "indieJump": "u(x/4)", "indieAcc": "8*x", "indieEva": "8*x", "maxLevel": 20}`
- name_en: `Monkey Magic` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5301003_icon.png`

**7. 캐논 마스터리** (`5300005` · 2차 · 530.img · M20)

- desc_ko: 캐논 계열 무기의 숙련도와 명중치를 증가시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 캐논 계열 무기의 숙련도 50%, 명중치 120 상승
- common_raw: `{"maxLevel": 20, "mastery": "10+2*x", "accX": "6*x"}`
- name_en: `Cannon Mastery` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5300005_icon.png`

**8. 캐논 부스터** (`5301002` · 2차 · 530.img · M20)

- desc_ko: MP를 소비하여 일정시간 동안 캐논의 공격속도를 2단계 상승시킨다.\n필요 스킬 : #c캐논 마스터리 5레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): MP를 소비하여 일정시간 동안 캐논의 공격속도를 2단계 상승시킨다.\n필요 스킬 : #c캐논 마스터리 5레벨 이상#
- hint_ko(M): MP 11 소비, 200초간 공격 속도 향상
- common_raw: `{"maxLevel": 20, "mpCon": "31-1*x", "time": "10*x", "x": "-2"}`
- name_en: `Cannon Booster` (MSEA, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5301002_icon.png`

**9. 크리티컬 파이어** (`5300004` · 2차 · 530.img · M15)

- desc_ko: 영구적으로 크리티컬 확률과 크리티컬 최소 데미지를 증가시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 영구적으로 크리티컬 확률 20%, 크리티컬 최소 데미지 10% 증가
- common_raw: `{"maxLevel": 15, "cr": "5+x", "criticaldamageMin": "5+u(x/3)"}`
- name_en: `Critical Fire` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5300004_icon.png`

**10. 파이렛 트레이닝** (`5300008` · 2차 · 530.img · M10)

- desc_ko: 해적의 비밀 수련을 통해 힘과 민첩성을 향상시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 영구적으로 힘 30, 민첩성 30 증가
- common_raw: `{"strX": "3*x", "dexX": "3*x", "maxLevel": 10}`
- name_en: `Pirate Training` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5300008_icon.png`

**11. 슬러그 샷** (`5301000` · 2차 · 530.img · M20)

- desc_ko: 전방을 향해 여러발의 소형 포탄을 발사하여 다수의 적을 동시에 공격한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방을 향해 여러발의 소형 포탄을 발사하여 다수의 적을 동시에 공격한다.
- hint_ko(M): MP 24소비, 220% 데미지로 최대 4명의 적을 2번 공격
- common_raw: `{"maxLevel": 20, "mpCon": "16+2*d(x/5)", "damage": "160+3*x", "bulletCount": "2", "mobCount": "4", "range": "450", "ballDelay": "240"}`
- name_en: `Scatter Shot` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5301000_icon.png`

**12. 몽키 웨이브** (`5311002` · 3차 · 531.img · M20)

- desc_ko: 소음을 일으켜 주변의 적들을 공격한다. 힘을 모을수록 큰 소음을 낼 수 있으며, 크리티컬 시 최고 출력으로 바로 사용할 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 소음을 일으켜 주변의 적들을 공격한다. 힘을 모을수록 큰 소음을 낼 수 있으며, 크리티컬 시 최고 출력으로 바로 사용할 수 있다.
- hint_ko(M): MP 55 소비, 최대 860% 데미지로 공격, 95% 확률로 기절, 크리티컬 시 20% 확률로 최고 출력으로 사용 가능
- common_raw: `{"maxLevel": 20, "mpCon": "35+5*d(x/5)", "damage": "460+20*x", "mobCount": "8", "prop": "45+5*d(x/2)", "time": "2+d(x/10)", "w": "2*u(x/2)", "hcTime": "1"}`
- name_en: `Monkey Wave` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311002_icon.png`

**13. 몽키 파워붐** (`5311001` · 3차 · 531.img · M20)

- desc_ko: 대량의 특제 폭탄을 동시에 터뜨려 사방의 적 다수를 공격하고 일정 시간동안 기절시킨다. 추가로 몽키 파워붐 스킬을 배우면 몽키 러쉬붐의 데미지가 영구적으로 증가한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 대량의 특제 폭탄을 동시에 터뜨려 사방의 적 다수를 공격하고 일정 시간동안 기절시킨다. 추가로 몽키 파워붐 스킬을 배우면 몽키 러쉬붐의 데미지가 영구적으로 증가한다.
- hint_ko(M): 액티브 효과 : MP 46소비, 280% 데미지로 최대 10명의 적을 5번 공격, 95% 확률로 4초간 기절, 재사용 대기시간 5초 / 패시브 효과 : 영구적으로 몽키 러쉬붐 데미지 30% 증가
- common_raw: `{"maxLevel": 20, "mpCon": "30+4*d(x/5)", "damage": "220+3*x", "attackCount": "5", "mobCount": "10", "prop": "45+5*d(x/2)", "time": "2+d(x/10)", "damR": "3*u(x/2)", "cooltime": "5", "hcTime": "1"}`
- name_en: `Monkey Madness` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311001_icon.png`

**14. 캐논 스파이크** (`5311000` · 3차 · 531.img · M20)

- desc_ko: 적 다수를 관통할 수 있는 날카로운 캐논 포탄을 발사한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 적 다수를 관통할 수 있는 날카로운 캐논 포탄을 발사한다.
- hint_ko(M): MP 36소비, 240% 데미지로 최대 6명의 적을 3번 공격
- common_raw: `{"maxLevel": 20, "mpCon": "28+2*d(x/5)", "damage": "200+2*x", "attackCount": "3", "mobCount": "6"}`
- name_en: `Cannon Spike` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311000_icon.png`

**15. 캐논 점프** (`5311003` · 3차 · 531.img · M15)

- desc_ko: 지면을 향해 캐논을 발사하여 반동으로 높이 뛰어오른다. 뛰어오르는 순간 주변의 적에게 데미지를 줄 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 지면을 향해 캐논을 발사하여 반동으로 높이 뛰어오른다. 뛰어오르는 순간 주변의 적에게 데미지를 줄 수 있다.
- hint_ko(M): MP 35 소비, 210% 데미지로 최대 6명의 적을 공격하며 점프
- common_raw: `{"maxLevel": 15, "mpCon": "60-5*d(x/3)", "damage": "165+3*x", "mobCount": "6", "x": "0", "y": "950+15*x"}`
- name_en: `Cannon Jump` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311003_icon.png`

**16. 오크통 룰렛** (`5311004` · 3차 · 531.img · M10)

- desc_ko: 오크통을 폭발시켜 랜덤 버프를 받는다. 버프 지속 상태에서 적을 공격하면 일정확률로 대상에게 상태이상 효과를 적용 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 오크통을 폭발시켜 랜덤 버프를 받는다. 버프 지속 상태에서 적을 공격하면 일정확률로 대상에게 상태이상 효과를 적용 수 있다.
- hint_ko(M): MP 60 소비, 240초간 버프 적용. 공격 시 30% 확률로 대상에게 암흑, 기절, 결빙, 슬로우 상태이상 중 하나가 5초간 적용 / 재사용 대기시간 30초
- common_raw: `{"maxLevel": 10, "mpCon": "35+5*d(x/2)", "time": "180+6*x", "u": "-6*x", "v": "3+d(x/5)", "w": "3*x", "x": "3*x", "y": "2*x", "z": "3*x", "cooltime": "60-3*x", "hcSubTime": "1+d(x/5)"}`
- name_en: `Barrel Roulette` (MSN-직역, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311004_icon.png`

**17. 럭키 다이스** (`5311005` · 3차 · 531.img · M20)

- desc_ko: 주사위를 던져 자신의 행운을 시험한다. 주사위의 결과에 따라 일정 시간동안 랜덤 버프를 획득할 수 있지만, 1이 나올 경우에는 아무 일도 발생하지 않는다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 주사위를 던져 자신의 행운을 시험한다. 주사위의 결과에 따라 일정 시간동안 랜덤 버프를 획득할 수 있지만, 1이 나올 경우에는 아무 일도 발생하지 않는다.
- hint_ko(M): MP 60 소비, 주사위 버프 지속시간 180초 / 재사용 대기시간 180초
- common_raw: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "time": "60+6*x", "cooltime": "480-30*d(x/2)", "pddR": "30", "mhpR": "20", "mmpR": "20", "cr": "15", "damR": "20", "expR": "30", "u": "17", "v": "17", "w": "15"}`
- name_en: `Roll of the Dice` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5311005_icon.png`

**18. 리인포스 캐논** (`5310006` · 3차 · 531.img · M15)

- desc_ko: 영구적으로 캐논을 강화하여 공격력과 공격속도를 향상시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 영구적으로 공격력 30, 공격속도 1 증가
- common_raw: `{"maxLevel": 15, "padX": "2*x", "actionSpeed": "-1"}`
- name_en: `Reinforced Cannon` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5310006_icon.png`

**19. 바이탈 익스트림** (`5310007` · 3차 · 531.img · M20)

- desc_ko: 영구적으로 체력과 방어력, 상태이상 내성을 강화한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 체력 20%, 방어력 50%, 상태이상 내성 20% 상승
- common_raw: `{"maxLevel": 20, "mhpR": "x", "pddR": "10+2*x", "mddR": "10+2*x", "asrR": "x"}`
- name_en: `Pirate Rush` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5310007_icon.png`

**20. 반격의 슈터** (`5310009` · 3차 · 531.img · M15)

- desc_ko: 피격 시 일정확률로 캐논을 휘둘러 반격한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 20%로 적의 공격을 막아 160% 데미지로 반격 
- common_raw: `{"maxLevel": 15, "prop": "5+x", "damage": "100+4*x"}`
- name_en: `Counter Crush` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5310009_icon.png`

**21. 캐논 바주카** (`5321000` · 4차 · 532.img · M30)

- desc_ko: 전방을 향해 강력한 캐논포를 발사하여 다수의 적을 동시에 공격한다. 
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방을 향해 강력한 캐논포를 발사하여 다수의 적을 동시에 공격한다. 
- hint_ko(M): MP 75소비, 500% 데미지로 최대 6명의 적을 4번 공격
- common_raw: `{"maxLevel": 30, "mpCon": "50+5*d(x/6)", "damage": "320+6*x", "attackCount": "4", "mobCount": "6", "hcCooltime": "5"}`
- name_en: `Cannon Bazooka` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5321000_icon.png`

**22. 캐논 버스터** (`5321012` · 4차 · 532.img · M30)

- desc_ko: 전방의 적 하나를 집중 포격 한다. 추가 크리티컬 확률이 적용된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방의 적 하나를 집중 포격 한다. 추가 크리티컬 확률이 적용된다.
- hint_ko(M): MP 63소비, 320% 데미지로 5번 공격, 추가 크리티컬 확률 15%
- common_raw: `{"maxLevel": 30, "mpCon": "45+3*d(x/5)", "damage": "230+3*x", "mobCount": "1", "range": "450", "cr": "u(x/2)", "bulletCount": "5", "ballDelay": "60", "ballDelay1": "60", "ballDelay2": "60", "ballDelay3": "60", "ballDelay4": "60"}`
- name_en: `Cannon Barrage` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5321012_icon.png`

**23. 전함 노틸러스** (`5321001` · 4차 · 532.img · M30)

- desc_ko: 전함 노틸러스호에 공격 명령을 내려 적 다수를 동시에 공격한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전함 노틸러스호에 공격 명령을 내려 적 다수를 동시에 공격한다.
- hint_ko(M): MP 350소비, 520% 데미지로 최대 15명의 적을 3번 공격 / 재사용 대기시간 30초
- common_raw: `{"maxLevel": 30, "mpCon": "350", "damage": "400+4*x", "attackCount": "3", "mobCount": "15", "cooltime": "60-2*d(x/2)"}`
- name_en: `Nautilus Strike` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5321001_icon.png`

**24. 파이렛 스피릿** (`5321010` · 4차 · 532.img · M30)

- desc_ko: 영구적으로 반격 확률이 상승하며, 스킬 사용 시 일정시간동안 적의 공격에도 뒤로 물러서지 않는상태가 된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 영구적으로 반격 확률이 상승하며, 스킬 사용 시 일정시간동안 적의 공격에도 뒤로 물러서지 않는상태가 된다.
- hint_ko(M): 액티브 효과 : MP 80소비, 300초 동안 피격 시 80% 확률로 스탠스 효과 발동 / 패시브 효과 : 영구적으로 반격확률 15% 증가
- common_raw: `{"maxLevel": 30, "prop": "u(x/2)", "x": "20+2*x", "mpCon": "50+5*d(x/5)", "time": "10*x"}`
- name_en: `Pirate's Spirit` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5321010_icon.png`

**25. 마그네틱 앵커** (`5321003` · 4차 · 532.img · M15)

- desc_ko: 전방에 강한 자기장을 생성하는 마그네틱 앵커를 설치한다. 마그네틱 앵커는 자기장을 이용하여 주변의 적을 지속적으로 끌어당긴다. 또한 지속시간이 끝나면 폭발하며 주변의 적들에게 치명적인 데미지를 준다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방에 강한 자기장을 생성하는 마그네틱 앵커를 설치한다. 마그네틱 앵커는 자기장을 이용하여 주변의 적을 지속적으로 끌어당긴다. 또한 지속시간이 끝나면 폭발하며 주변의 적들에게 치명적인 데미지를 준다.
- hint_ko(M): MP 86 소비, 20초동안 소환, 주기적으로 400%의 데미지를 주며 주변의 적을 끌어당긴다. 지속시간 경과 시 520%의 추가 데미지
- common_raw: `{"maxLevel": 15, "mpCon": "50+12*u(x/5)", "time": "5+x", "damage": "250+10*x", "mobCount": "8", "prop": "30+3*x", "subTime": "2+d(x/5)", "selfDestruction": "400+8*x", "hcCooltime": "5"}`
- name_en: `Anchors Aweigh` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5321003_icon.png`

**26. 서포트 몽키 트윈스** (`5321004` · 4차 · 532.img · M15)

- desc_ko: 전투를 도와줄 정예 포병 몽키 트윈스를 소환한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전투를 도와줄 정예 포병 몽키 트윈스를 소환한다.
- hint_ko(M): MP 70소비, 60초동안 소환, 각각 350% 데미지로 공격 / 재사용 대기시간 10초
- common_raw: `{"maxLevel": 15, "mpCon": "40+10*d(x/5)", "damage": "275+5*x", "time": "30+2*x", "cooltime": "10", "mobCount": "1"}`
- name_en: `Support Monkey` (current-GMS, verified_2012=false) · aliases_ko: 서포트 몽키
- 아이콘: `t2_merc_cannon_icons_20261120/5321004_icon.png`

**27. 더블 럭키 다이스** (`5320007` · 4차 · 532.img · M5)

- desc_ko: 일정 확률로 주사위 2개를 동시에 던져 자신의 행운을 시험한다. 주사위의 눈이 같을 경우에는 보다 강력한 버프 효과가 적용된다.\n필요 스킬 : #c럭키 다이스 20레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 일정 확률로 주사위 2개를 동시에 던져 자신의 행운을 시험한다. 주사위의 눈이 같을 경우에는 보다 강력한 버프 효과가 적용된다.\n필요 스킬 : #c럭키 다이스 20레벨 이상#
- hint_ko(M): MP 60 소비, 50% 확률로 럭키 다이스 사용 시, 더블 럭키 다이스 발동, 주사위 버프 지속시간 200초 / 재사용 대기시간 200초
- common_raw: `{"maxLevel": 5, "mpCon": "60", "time": "180+4*x", "cooltime": "200", "pddR": "30", "mhpR": "20", "mmpR": "20", "cr": "15", "damR": "20", "expR": "30", "u": "15", "v": "17", "w": "17", "x": "17", "prop": "10*x"}`
- name_en: `Double Down` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5320007_icon.png`

**28. 하이퍼 몽키 스펠** (`5320008` · 4차 · 532.img · M30)

- desc_ko: 몽키 매직을 업그레이드 하여 몽키의 마법으로 일정 시간동안 주변 파티원들의 HP, MP, 올스텟, 이동속도, 점프력, 명중치, 회피치를 높여준다. 다른 모든 버프 스킬과 중복으로 사용할 수 있다.\n필요 스킬 : #c몽키 매직 20레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): MP 80 소비, 300초간 HP 700, MP 700, 올스텟 40, 이동속도 15, 점프력 10, 명중치 250, 회피치 250 증가
- common_raw: `{"maxLevel": 30, "mpCon": "55+5*u(x/6)", "time": "300", "indieMhp": "310+13*x", "indieMmp": "310+13*x", "indieAllStat": "25+d(x/2)", "indieSpeed": "10+u(x/6)", "indieJump": "5+u(x/6)", "indieAcc": "160+3*x", "indieEva": "160+3*x"}`
- name_en: `Mega Monkey Magic` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5320008_icon.png`

**29. 오버버닝 캐논** (`5320009` · 4차 · 532.img · M30)

- desc_ko: 캐논의 성능을 극한까지 끌어올려 영구적으로 데미지를 증가시킨다. 또한 공격 시 몬스터의 방어율을 일정 수준 무시할 수 있게 된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): —
- hint_ko(M): 영구적으로 데미지 40% 증가, 몬스터 방어율 20% 무시 효과 추가
- common_raw: `{"maxLevel": 30, "ignoreMobpdpR": "5+d(x/2)", "damR": "10+x"}`
- name_en: `Cannon Overload` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/5320009_icon.png`

#### 메르세데스 (29종)

**1. 스피드 듀얼샷** (`23001000` · 1차 · 2300.img · M20)

- desc_ko: 전방에 있는 다수의 적에게 화살을 발사한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방에 있는 다수의 적에게 화살을 발사한다.
- hint_ko(M): MP 14 소비,최대 3명의 적에게 115% 데미지의 화살 2개 발사
- common_raw: `{"maxLevel": 20, "mpCon": "8+2*d(x/6)", "damage": "95+x", "bulletCount": "2", "mobCount": "3", "range": "400", "ballDelay": "270"}`
- name_en: `Swift Dual Shot` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23001000_icon.png`

**2. 샤프 에이밍** (`23000003` · 1차 · 2300.img · M20)

- desc_ko: 영구적으로 크리티컬 확률을 높인다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 영구적으로 크리티컬 확률을 높인다.
- hint_ko(M): 크리티컬 확률 40% 상승
- common_raw: `{"cr": "2*x", "maxLevel": 20}`
- name_en: `Sharp Aim` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23000003_icon.png`

**3. 아크로바틱 점프** (`23001002` · 1차 · 2300.img · M10)

- desc_ko: 점프 중 진행방향으로 덤블링하여 먼 거리를 날아간다. 스킬레벨이 상승할수록 이동 거리가 증가한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 점프 중 진행방향으로 덤블링하여 먼 거리를 날아간다. 스킬레벨이 상승할수록 이동 거리가 증가한다.
- hint_ko(M): MP 10 소비, 일정거리 점프
- common_raw: `{"maxLevel": 10, "mpCon": "30-2*x", "x": "350+20*x", "y": "250+10*x"}`
- name_en: `Spirit Jump` (current-GMS, verified_2012=false) · aliases_ko: 스피릿 점프
- 아이콘: `t2_merc_cannon_icons_20261120/23001002_icon.png`

**4. 포텐셜 파워** (`23000001` · 1차 · 2300.img · M15)

- desc_ko: 내면에 잠재된 힘을 영구적으로 활성한다. 이동속도와 최대 이동속도 상한이 증가하며 일정확률로 적의 공격을 회피할 수 있게 된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 내면에 잠재된 힘을 영구적으로 활성한다. 이동속도와 최대 이동속도 상한이 증가하며 일정확률로 적의 공격을 회피할 수 있게 된다.
- hint_ko(M): 이동속도 30 증가, 최대 이동속도 상한 165로 증가, 20% 확률로 적의 공격 회피
- common_raw: `{"maxLevel": 15, "er": "5+x", "psdSpeed": "2*x", "speedMax": "10+x", "u": "150+x"}`
- name_en: `Potential Power` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23000001_icon.png`

**5. 피지컬 트레이닝** (`23100008` · 2차 · 2310.img · M10)

- desc_ko: 신체 단련을 통해 영구적으로 힘과 민첩성을 향상시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 신체 단련을 통해 영구적으로 힘과 민첩성을 향상시킨다.
- hint_ko(M): 영구적으로 힘 30, 민첩성 30 증가
- common_raw: `{"strX": "3*x", "dexX": "3*x", "maxLevel": 10}`
- name_en: `Physical Training` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23100008_icon.png`

**6. 듀얼보우건 마스터리** (`23100005` · 2차 · 2310.img · M20)

- desc_ko: 듀얼보우건 계열 무기의 숙련도와 명중치를 향상시킨다. 
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 듀얼보우건 계열 무기의 숙련도와 명중치를 향상시킨다. 
- hint_ko(M): 듀얼보우건 계열 무기의 숙련도 50%, 명중치 120 상승
- common_raw: `{"maxLevel": 20, "mastery": "10+2*x", "accX": "6*x"}`
- name_en: `Dual Bowguns Mastery` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23100005_icon.png`

**7. 듀얼보우건 부스터** (`23101002` · 2차 · 2310.img · M20)

- desc_ko: MP를 소비하여 일정시간 동안 듀얼보우건의 공격속도를 2단계 상승시킨다.\n필요 스킬 : #c듀얼보우건 마스터리 5레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): MP를 소비하여 일정시간 동안 듀얼보우건의 공격속도를 2단계 상승시킨다.\n필요 스킬 : #c듀얼보우건 마스터리 5레벨 이상#
- hint_ko(M): MP 11 소비, 200초간 공격 속도 향상
- common_raw: `{"maxLevel": 20, "mpCon": "31-1*x", "time": "10*x", "x": "-2"}`
- name_en: `Dual Bowguns Boost` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23101002_icon.png`

**8. 스피릿 인퓨젼** (`23101003` · 2차 · 2310.img · M15)

- desc_ko: 일정 시간 동안 데미지와 크리티컬 확률을 증가시키킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 일정 시간 동안 데미지와 크리티컬 확률을 증가시키킨다.
- hint_ko(M): MP 45 소비, 180초 동안 데미지 15%, 크리티컬 확률 15% 증가
- common_raw: `{"maxLevel": 15, "mpCon": "20+5*u(x/3)", "time": "60+8*x", "x": "x", "damage": "x"}`
- name_en: `Spirit Surge` (current-GMS, verified_2012=false) · aliases_ko: 스피릿 인퓨전
- 아이콘: `t2_merc_cannon_icons_20261120/23101003_icon.png`

**9. 차지 드라이브** (`23101001` · 2차 · 2310.img · M15)

- desc_ko: 전방의 적 다수를 빠른 속도로 밀어낸 후 공중에 띄운다. 공중에 뜬 상태의 적을 공격하면 추가 데미지를 줄 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방의 적 다수를 빠른 속도로 밀어낸 후 공중에 띄운다. 공중에 뜬 상태의 적을 공격하면 추가 데미지를 줄 수 있다.
- hint_ko(M): MP 25 소비, 최대 8명의 적을 130% 데미지로 밀며 돌진, 210%의 데미지로 띄움. 띄운 상태 공격 시 추가 데미지 30%
- common_raw: `{"mpCon": "20+d(x/3)", "damage": "100+2*x", "w": "180+2*x", "x": "2*x", "mobCount": "8", "maxLevel": 15, "hcCooltime": "5"}`
- name_en: `Rising Rush` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23101001_icon.png`

**10. 파이널 샷** (`23100004` · 2차 · 2310.img · M5)

- desc_ko: 차지 드라이브로 공중으로 뜬 적들을 향해 화살을 난사한다. 차지 드라이브 사용 후에만 사용할 수 있다.\n필요 스킬 : #c차지 드라이브 1레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 차지 드라이브로 공중으로 뜬 적들을 향해 화살을 난사한다. 차지 드라이브 사용 후에만 사용할 수 있다.\n필요 스킬 : #c차지 드라이브 1레벨 이상#
- hint_ko(M): MP 16 소비, 최대 8명의 적을 70% 데미지로 4번 공격
- common_raw: `{"maxLevel": 5, "mpCon": "12+4*d(x/5)", "damage": "40+6*x", "mobCount": "8", "attackCount": "4"}`
- name_en: `Parting Shot` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23100004_icon.png`

**11. 파이널 어택 : 듀얼보우건** (`23100006` · 2차 · 2310.img · M20)

- desc_ko: 일정확률로 공격 스킬이 사용된 후 추가 데미지가 적용된다. 다만, 반드시 듀얼보우건 계열 무기를 들었을 경우에만 발동이 가능하다.\n필요 스킬 : #c듀얼보우건 마스터리 3레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 일정확률로 공격 스킬이 사용된 후 추가 데미지가 적용된다. 다만, 반드시 듀얼보우건 계열 무기를 들었을 경우에만 발동이 가능하다.\n필요 스킬 : #c듀얼보우건 마스터리 3레벨 이상#
- hint_ko(M): 40% 확률로 2회 파이널 어택 발동, 1타는 75%, 2타는 50%의 데미지 적용
- common_raw: `{"damage": "55+2*d(x/2)", "x": "26+4*d(x/3)", "prop": "2*x", "mobCount": "1", "attackCount": "2", "maxLevel": 20}`
- name_en: `Final Attack: Dual Bowguns` (current-GMS, verified_2012=false) · aliases_ko: 파이널 어택
- 아이콘: `t2_merc_cannon_icons_20261120/23100006_icon.png`

**12. 어드밴스드 파이널 어택** (`23120012` · 4차 · 2312.img · M30)

- desc_ko: 영구적으로 공격력과 명중률이 증가하며 파이널 어택의 발동확률과 데미지가 대폭 상승한다.\n필요 스킬 : #c파이널 어택 20레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 영구적으로 공격력과 명중률이 증가하며 파이널 어택의 발동확률과 데미지가 대폭 상승한다.\n필요 스킬 : #c파이널 어택 20레벨 이상#
- hint_ko(M): 영구적으로 공격력 20, 명중률 10% 증가, 공격 시 70% 확률로 2회 파이널 어택 발동, 1타는 105%, 2타는 70%의 데미지 적용
- common_raw: `{"padX": "5+u(x/2)", "prop": "40+x", "damage": "75+x", "x": "50+2*d(x/3)", "ar": "u(x/3)", "maxLevel": 30, "mobCount": "1", "attackCount": "2"}`
- name_en: `Advanced Final Attack` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23120012_icon.png`

**13. 크로스 피어싱** (`23101000` · 2차 · 2310.img · M20)

- desc_ko: 자연의 힘이 깃든 날카로운 화살을 연속 발사한다. 적 다수를 관통할 수 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 자연의 힘이 깃든 날카로운 화살을 연속 발사한다. 적 다수를 관통할 수 있다.
- hint_ko(M): MP 24 소비, 최대 6명의 적을 83%의 데미지로 4번 관통 공격
- common_raw: `{"maxLevel": 20, "mpCon": "14+d(x/2)", "damage": "63+x", "bulletCount": "4", "mobCount": "6", "range": "400", "ballDelay": "180", "ballDelay1": "180", "ballDelay2": "180"}`
- name_en: `Piercing Storm` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23101000_icon.png`

**14. 스트라이크 듀얼샷** (`23111000` · 3차 · 2311.img · M20)

- desc_ko: 전방에 있는 다수의 적들에게 매우 빠른 속도로 다수의 화살을 날린다. 대상은 일정확률로 기절상태가 된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방에 있는 다수의 적들에게 매우 빠른 속도로 다수의 화살을 날린다. 대상은 일정확률로 기절상태가 된다.
- hint_ko(M): MP 35 소비, 최대 5명의 적에게 120% 데미지의 화살 4개 발사, 80% 확률로 6초간 기절
- common_raw: `{"maxLevel": 20, "mpCon": "20+3*d(x/4)", "damage": "100+x", "mobCount": "5", "bulletCount": "4", "time": "2+d(x/5)", "prop": "20+3*x", "ballDelay": "180", "ballDelay1": "90", "ballDelay2": "90", "ballDelay3": "90", "range": "400", "hcTime": "1"}`
- name_en: `Stunning Strikes` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111000_icon.png`

**15. 리프 토네이도** (`23111001` · 3차 · 2311.img · M20)

- desc_ko: 점프 상태에서 빠르게 몸을 회전하면서 사방에 화살을 난사한다. 공중에서만 사용 가능하며 스킬 사용을 위해서는 반드시 120 이상의 점프력이 필요하다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 점프 상태에서 빠르게 몸을 회전하면서 사방에 화살을 난사한다. 공중에서만 사용 가능하며 스킬 사용을 위해서는 반드시 120 이상의 점프력이 필요하다.
- hint_ko(M): MP 45 소비, 최대 8명의 적을 135% 데미지로 4번 공격
- common_raw: `{"maxLevel": 20, "mpCon": "30+3*u(x/4)", "damage": "95+2*x", "mobCount": "8", "attackCount": "4", "x": "0", "y": "600"}`
- name_en: `Leaf Tornado` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111001_icon.png`

**16. 거스트 다이브** (`23111003` · 3차 · 2311.img · M20)

- desc_ko: 바람의 힘으로 공중에서 빠르게 하강하면서 범위 내의 적 다수를 동시에 공격한다. 스킬 사용을 위해 120이상의 점프력이 필요하다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 바람의 힘으로 공중에서 빠르게 하강하면서 범위 내의 적 다수를 동시에 공격한다. 대상이 약화 상태일 경우 추가 데미지를 받는다. 스킬 사용을 위해 120이상의 점프력이 필요하다.
- hint_ko(M): MP 45 소비, 최대 6명의 적을 195% 데미지로 3번 공격
- common_raw: `{"maxLevel": 20, "mpCon": "25+5*u(x/5)", "damage": "135+3*x", "mobCount": "6", "attackCount": "3", "x": "27+4*u(x/3)", "y": "x", "hcCooltime": "5"}`
- name_en: `Gust Dive` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111003_icon.png`

**17. 하이킥 데몰리션** (`23110006` · 3차 · 2311.img · M15)

- desc_ko: 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다.  공중으로 뜬 적들을 향해 보이지 않을 속도로 빠르게 날아가 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다. 공중으로 뜬 적들을 향해 보이지 않을 속도로 빠르게 날아가 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- hint_ko(M): 액티브 효과 : MP 32 소비, 최대 8명의 적에게 110% 데미지로 6번 공격, 대상은 15% 확률로 즉사 / 패시브 효과 : 차지 드라이브 데미지 20% 상승
- common_raw: `{"maxLevel": 15, "mpCon": "20+4*u(x/5)", "damage": "95+x", "attackCount": "6", "mobCount": "8", "prop": "x", "damR": "5+x"}`
- name_en: `Aerial Barrage` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23110006_icon.png`

**18. 엘리멘탈 나이트** (`23111008` · 3차 · 2311.img · M20)

- desc_ko: 냉기 정령, 화염 정령, 암흑 정령 중 1명을 랜덤으로 소환하여 전투를 돕게 한다. \n냉기 정령 : 공격 시 일정 확률로 대상을 결빙\n화염 정령 : 공격 시 일정 확률로 대상에게 화염 속성의 지속 데미지\n암흑 정령 : 냉기 정령과 화염 정령보다 강력한 데미지
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 냉기 정령, 화염 정령, 암흑 정령 중 1명을 랜덤으로 소환하여 전투를 돕게 한다. \n냉기 정령 : 공격 시 일정 확률로 대상을 결빙\n화염 정령 : 공격 시 일정 확률로 대상에게 화염 속성의 지속 데미지\n암흑 정령 : 냉기 정령과 화염 정령보다 강력한 데미지
- hint_ko(M): MP 60 소비하여 3명의 정령 중 1명을 랜덤으로 160초 동안 소환 / 냉기 정령 : 550%로 공격하여 대상을 90%확률로 5초동안 결빙 / 화염 정령 : 550%로 공격, 대상은 5초 동안 1초 당 110%의 지속 피해 / 암흑 정령 : 625%로 공격 / 재사용 대기시간 120초
- common_raw: `{"maxLevel": 20, "mpCon": "140-8*u(x/2)", "time": "60+5*x", "damage": "350+10*x", "subTime": "3+d(x/10)", "prop": "10+4*x", "cooltime": "200-4*x", "v": "350+10*x", "w": "3+d(x/10)", "x": "1", "y": "50+3*x", "z": "385+12*x", "hcSubTime": "1"}`
- name_en: `Elemental Knights` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111008_icon.png`

**19. 이그니스 로어** (`23111004` · 3차 · 2311.img · M20)

- desc_ko: 영구적으로 적의 공격을 추가 회피할 수 있게 되며, 스킬 사용 시 불의 정령의 힘을 빌어 일정시간 동안 공격력을 대폭 증가시킨다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 영구적으로 적의 공격을 추가 회피할 수 있게 되며, 스킬 사용 시 불의 정령의 힘을 빌어 일정시간 동안 대난투 공격력을 대폭 증가시킨다.
- hint_ko(M): 액티브 효과 : MP 60 소비, 180초동안 공격력 40 상승 /  패시브 효과 : 20% 확률로 추가 회피
- common_raw: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "indiePad": "2*x", "prop": "5+3*d(x/4)", "time": "40+7*x"}`
- name_en: `Ignis Roar` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111004_icon.png`

**20. 유니콘 스파이크** (`23111002` · 3차 · 2311.img · M20)

- desc_ko: 성스러운 유니콘을 소환해 전방의 적 다수를 동시에 공격하고 일정시간 동안 약화시킨다. 약화된 대상은 지정된 횟수만큼 아군의 모든 공격에 추가 피해를 받게되며 보스 몬스터에게는 추가 피해 적용횟수가 2배로 적용된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 성스러운 유니콘을 소환해 전방의 적 다수를 동시에 공격하고 일정시간 동안 약화시킨다. 약화된 대상은 지정된 횟수만큼 아군의 모든 공격에 추가 피해를 받게되며 보스 몬스터에게는 추가 피해 적용횟수가 2배로 적용된다.
- hint_ko(M): MP 62 소비, 최대 8명의 적을 140% 데미지로 5번 크리티컬 공격, 대상은 95% 확률로 15초 동안 15%의 추가 피해를 10번 받는 디버프 효과 적용 / 재사용 대기시간 10초
- common_raw: `{"maxLevel": 20, "mpCon": "30+8*u(x/5)", "damage": "100+2*x", "mobCount": "8", "attackCount": "5", "time": "5+d(x/2)", "x": "5+d(x/2)", "y": "5+d(x/4)", "z": "10+2*d(x/4)", "prop": "15+4*x", "cooltime": "20-d(x/2)", "cr": "100"}`
- name_en: `Unicorn Spike` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23111002_icon.png`

**21. 워터 쉴드** (`23111005` · 3차 · 2311.img · M20)

- desc_ko: 정령의 힘을 빌어 일정시간 동안 자신에게 물의 보호막을 발동시킨다. 보호막은 받는 데미지의 일부를 흡수하고, 상태이상 내성과 모든 속성 내성을 증가시키는 효과가 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 정령의 힘을 빌어 일정시간 동안 자신에게 물의 보호막을 발동시킨다. 보호막은 받는 데미지의 일부를 흡수하고, 상태이상 내성과 모든 속성 내성을 증가시키는 효과가 있다.
- hint_ko(M): MP 100 소비, 180초동안 최대 30%만큼의 피해를 흡수하고 상태이상 내성과 모든 속성 내성을 25% 증가시키는 물의 보호막 발동.
- common_raw: `{"maxLevel": 20, "mpCon": "60+10*d(x/5)", "time": "100+4*x", "x": "10+x", "asrR": "5+x", "terR": "5+x"}`
- name_en: `Water Shield` (current-GMS, verified_2012=false) · aliases_ko: 워터 실드, 워터실드
- 아이콘: `t2_merc_cannon_icons_20261120/23111005_icon.png`

**22. 디펜스 브레이크** (`23120010` · 4차 · 2312.img · M20)

- desc_ko: 공격 시 일정 확률로 적의 방어율 100%를 무시한다. 보스몬스터에게도 동일하게 적용된다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 공격 시 일정 확률로 적의 방어율을 100% 무시한다. 보스몬스터에게도 동일하게 적용된다.
- hint_ko(M): 40% 확률로 적의 방어율 100% 무시
- common_raw: `{"maxLevel": 20, "x": "2*x"}`
- name_en: `Defense Break` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23120010_icon.png`

**23. 듀얼보우건 엑스퍼트** (`23120009` · 4차 · 2312.img · M30)

- desc_ko: 듀얼보우건 계열 무기의 숙련도와 물리 공격력, 크리티컬 최소 데미지를 증가시킨다.\n필요 스킬 : #c듀얼보우건 마스터리 20레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 듀얼보우건 계열 무기의 숙련도와 물리 공격력, 크리티컬 최소 데미지를 증가시킨다.\n필요 스킬 : #c듀얼보우건 마스터리 20레벨 이상#
- hint_ko(M): 듀얼보우건 계열 무기의 숙련도 70%로 상승, 물리 공격력 30, 크리티컬 최소 데미지 15% 증가
- common_raw: `{"maxLevel": 30, "mastery": "55+u(x/2)", "x": "x", "criticaldamageMin": "u(x/2)"}`
- name_en: `Dual Bowguns Expert` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23120009_icon.png`

**24. 이슈타르의 링** (`23121000` · 4차 · 2312.img · M30)

- desc_ko: 전설의 무기 이슈타르의 힘을 빌려 빠른 속도로 화살을 전방의 적에게 발사한다. 스킬 키를 누르고 있으면 지속적으로 화살이 발사된다. 추가로 스트라이크 듀얼샷의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.\n필요 스킬 : #c스트라이크 듀얼샷 20레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전설의 무기 이슈타르의 힘을 빌려 빠른 속도로 화살을 전방의 적에게 발사한다. 스킬 키를 누르고 있으면 지속적으로 화살이 발사된다. 추가로 스트라이크 듀얼샷의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.\n필요 스킬 : #c스트라이크 듀얼샷 20레벨 이상#
- hint_ko(M): 액티브 효과 :MP 10 소비, 전방의 적에게 발 당 110% 데미지로 2번의 공격 / 패시브 효과 : 스트라이크 듀얼샷 데미지 25% 상승
- common_raw: `{"maxLevel": 30, "mpCon": "7+u(x/10)", "damage": "80+x", "attackCount": "2", "damR": "5+2*u(x/3)"}`
- name_en: `Ishtar's Ring` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23121000_icon.png`

**25. 레전드리 스피어** (`23121002` · 4차 · 2312.img · M20)

- desc_ko: 도약과 동시에 전설의 창을 떨어트려 전방의 적 다수를 공격한다. 대상의 방어력을 일정수준 감소시키는 효과와 함께 100% 크리티컬 판정으로 적중한다. 추가로 리프 토네이도의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.\n필요 스킬 : #c리프 토네이도 10레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 도약과 동시에 전설의 창을 떨어트려 전방의 적 다수를 공격한다. 대상의 방어력을 일정수준 감소시키는 효과와 함께 100% 크리티컬 판정으로 적중한다. 추가로 리프 토네이도의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.\n필요 스킬 : #c리프 토네이도 10레벨 이상#
- hint_ko(M): 액티브 효과 : MP 60 소비, 최대 12명의 적을 540%로 2번 크리티컬 공격. 15초 동안 대상의 방어력 -20% 감소 효과 적용 / 재사용 대기시간 5초 / 패시브 효과 : 리프토네이도 데미지 30% 상승
- common_raw: `{"maxLevel": 20, "mpCon": "40+5*d(x/5)", "damage": "420+6*x", "mobCount": "12", "damR": "10+x", "attackCount": "2", "time": "5+d(x/2)", "x": "-x", "cooltime": "10-d(x/4)"}`
- name_en: `Spikes Royale` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23121002_icon.png`

**26. 라이트닝 엣지** (`23121003` · 4차 · 2312.img · M30)

- desc_ko: 전방을 향해 순간적으로 이동하며 경로 내 적 다수를 공격한다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 전방을 향해 순간적으로 이동하며 경로 내 적 다수를 공격한다.
- hint_ko(M): MP 74 소비, 최대 8명의 적에게 420%의 데미지로 3번 공격하며 전방으로 이동 / 재사용 대기시간 5초
- common_raw: `{"maxLevel": 30, "mpCon": "50+4*u(x/5)", "damage": "270+5*x", "attackCount": "3", "mobCount": "8", "cooltime": "10-d(x/6)"}`
- name_en: `Lightning Edge` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23121003_icon.png`

**27. 롤링 문썰트** (`23120011` · 4차 · 2312.img · M20)

- desc_ko: 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다. 공중에 뜬 적들을 빠르게 회전하며 연속 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 차지 드라이브로 적들을 공중으로 띄웠을 때 사용하는 연계 스킬이다. 공중에 뜬 적들을 빠르게 회전하며 연속 공격한다. 추가로 차지 드라이브의 데미지를 영구적으로 증가시키는 패시브 효과가 있다.
- hint_ko(M): 액티브 효과 : MP 70 소비, 최대 8명의 적에게 180%의 데미지로 6번 공격 / 패시브 효과 : 차지 드라이브 데미지 50% 상승
- common_raw: `{"maxLevel": 20, "mpCon": "50+4*u(x/4)", "damage": "140+2*x", "attackCount": "6", "mobCount": "8", "damR": "10+2*x"}`
- name_en: `Rolling Moonsault` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23120011_icon.png`

**28. 앤시언트 스피릿** (`23121004` · 4차 · 2312.img · M30)

- desc_ko: 일정시간동안 고대 정령의 가호를 받아 데미지와 HP를 증가시키며, 영구적으로 이그니스 로어의 회피 확률을 상승시킨다.\n필요 스킬 : #c이그니스 로어 5레벨 이상#
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 일정시간동안 고대 정령의 가호를 받아 데미지와 HP를 증가시키며, 영구적으로 이그니스 로어의 회피 확률을 상승시킨다.\n필요 스킬 : #c이그니스 로어 5레벨 이상#
- hint_ko(M): 액티브 효과 : MP 80 소비, 210초간 데미지 30%, 체력 1500 증가 / 패시브 효과 : 이그니스 로어의 회피 확률 20% 상승
- common_raw: `{"maxLevel": 30, "mpCon": "45+5*d(x/4)", "time": "60+5*x", "prop": "5+u(x/2)", "damR": "x", "x": "1", "emhp": "50*x"}`
- name_en: `Ancient Warding` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23121004_icon.png`

**29. 메이플 용사** (`23121005` · 4차 · 2312.img · M30)

- desc_ko: 일정시간 동안 파티원의 모든 스탯을 일정 퍼센트만큼 상승시켜 준다.
- shortDesc_ko: — (원천부재) · pdesc_ko(간략본, 미채택): 일정시간 동안 팀원의 모든 스탯을 일정 퍼센트만큼 상승시켜 준다.
- hint_ko(M): MP 70 소비, 900초간 모든 스탯 15% 향상
- common_raw: `{"maxLevel": 30, "mpCon": "10+10*d(x/5)", "x": "u(x/2)", "time": "30*x"}`
- name_en: `Maple Warrior` (current-GMS, verified_2012=false) · aliases_ko: —
- 아이콘: `t2_merc_cannon_icons_20261120/23121005_icon.png`

## 5. 영문명 보조 필드 (판정 §2·§3)

화면 정본은 한글명(`name_ko`)이고 `name_en`은 검색·alt 보조 필드다. 현행 GMS 명칭 56건, 대체 2건(MSEA·MSN), 2012 시점 검증은 전건 false.

| skill_id | 한글(2012 클라) | name_en | basis | 비고 |
|---|---|---|---|---|
| 5011002 | 기간틱 백스탭 | Blast Back | current-GMS | 현행 KMS명이 클라(2012)와 달라 개칭 이력 있음 — 영문명은 현행 GMS 값(보조 필드) |
| 5301002 | 캐논 부스터 | Cannon Booster | MSEA | GMS 칸 공백 → MSEA 열 채택 — 판정 §3 |
| 5311004 | 오크통 룰렛 | Barrel Roulette | MSN-직역 | GMS Forty Winks 기각(동일 행 MSN 열 Barrel Roulette가 한글 직역과 일치) — 판정 §3 채택, GMS 2012 명칭 미검증 |
| 5310007 | 바이탈 익스트림 | Pirate Rush | current-GMS | 현행 영문명이 Pirate Rush로 개칭(동일 ID) — 판정 §3 |
| 5321004 | 서포트 몽키 트윈스 | Support Monkey | current-GMS | 현행 KMS명이 클라(2012)와 달라 개칭 이력 있음 — 영문명은 현행 GMS 값(보조 필드) |
| 23001002 | 아크로바틱 점프 | Spirit Jump | current-GMS | 현행 KMS명이 클라(2012)와 달라 개칭 이력 있음 — 영문명은 현행 GMS 값(보조 필드) |
| 23101003 | 스피릿 인퓨젼 | Spirit Surge | current-GMS | 현행명 채택 + 개칭 의심 라벨(JMS는 スピリットインフュージョン=인퓨전 유지) — 판정 §3 |
| 23111004 | 이그니스 로어 | Ignis Roar | current-GMS | 현행 표의 KMS 슬롯이 비어 대응 불확실 — GMS·MSEA 일치 값 채택(판정 §3) |
| 23111005 | 워터 쉴드 | Water Shield | current-GMS | 현행 KMS명이 클라(2012)와 달라 개칭 이력 있음 — 영문명은 현행 GMS 값(보조 필드) |
| 23120011 | 롤링 문썰트 | Rolling Moonsault | current-GMS | 현행 표의 KMS 슬롯이 비어 대응 불확실 — GMS·MSEA 일치 값 채택(판정 §3) |

나머지 56건은 현행 GMS 명칭 그대로(`current-GMS`)다.

## 6. 대조 지점 (60건 — 덮어쓰지 않고 병기)

| 유형 | 건수 | 처리 원칙 |
|---|---:|---|
| 마스터레벨_층위 | 14 | M은 common.maxLevel. 노드 masterLevel(전투명령 상한)을 M으로 쓰지 않음 |
| 현행_최대레벨_차이 | 14 | 2012 세트 B M 유지, 현행 KMS 최대레벨 차이는 참고 병기 |
| 판정값_재현 | 12 | 판정값을 그대로 두고 클라 재계산값을 병기 — 판정에서 12건 재현 확인 |
| 영문명_보조필드 | 10 | 보조 필드로만 수록(verified_2012=false) — 판정 §3 값·라벨 적용 |
| 명칭_표기차 | 7 | 클라(1.2.160) 표기를 화면 정본, 기존 표기는 aliases_ko로 보존 |
| ID_정정 | 2 | 클라 실재 ID 채택, 이전 ID는 기각 표기로 병기 |
| 문안_MP_층위 | 1 | 클라(2012) 값을 정본, 문안 수치는 참고만 |

### 6.1 판정값 재현 12건

| skill_id | 스킬 | 기존 판정값(세트 B) | 클라 재계산(마스터) | 근거등급 |
|---|---|---|---|---|
| 5301001 | 몽키 러쉬붐 | 50% · 8명 3회 + 300% 폭발 | M 20 · damage 50 · mobCount 8 · attackCount 3 · bulletCount — · MP 28 | ✅ 공식 역산(규칙 5·6) |
| 5301000 | 슬러그 샷 | 220% · 최대 4명 2회 | M 20 · damage 220 · mobCount 4 · attackCount — · bulletCount 2 · MP 24 | ✅ 공식 역산(규칙 5·6) |
| 5311002 | 몽키 웨이브 | 860%(최대) · 기절 95% | M 20 · damage 860 · mobCount 8 · attackCount — · bulletCount — · MP 55 | ✅ 공식 역산(규칙 5·6) |
| 5311000 | 캐논 스파이크 | 240% · 6명 3회 | M 20 · damage 240 · mobCount 6 · attackCount 3 · bulletCount — · MP 36 | ✅ 공식 역산(규칙 5·6) |
| 5321000 | 캐논 바주카 | 500% · 6명 4회 | M 30 · damage 500 · mobCount 6 · attackCount 4 · bulletCount — · MP 75 | ✅ 공식 + 본섭 관측 3곳 |
| 5321012 | 캐논 버스터 | 320% · 5회 · 추가 크리 15% (후딜 810ms는 미확보·분리) | M 30 · damage 320 · mobCount 1 · attackCount — · bulletCount 5 · MP 63 | ✅ 공식 역산(규칙 5·6), 후딜 제외 |
| 5321003 | 마그네틱 앵커 | 400% + 지속 종료 시 520% | M 15 · damage 400 · mobCount 8 · attackCount — · bulletCount — · MP 86 | ✅ 공식 역산(규칙 5·6) |
| 23100004 | 파이널 샷 | 70% · 최대 8명 4회 | M 5 · damage 70 · mobCount 8 · attackCount 4 · bulletCount — · MP 16 | ✅ 본섭 독립 2곳 |
| 23110006 | 하이킥 데몰리션 | 110% · 6회 · 즉사 15% | M 15 · damage 110 · mobCount 8 · attackCount 6 · bulletCount — · MP 32 | 🔸 본섭 1곳 (2013년 값 105%·10%·M5와 혼용 금지) |
| 23121002 | 레전드리 스피어 | 540% · 12명 2회 · 방어력 -20%(15초) · 쿨 5초 | M 20 · damage 540 · mobCount 12 · attackCount 2 · bulletCount — · MP 60 | ✅ 공식(2013 변경 전 문안) + 본섭 1곳, 각주 필수 |
| 23121003 | 라이트닝 엣지 | 420% · 8명 3회 · 쿨 5초 | M 30 · damage 420 · mobCount 8 · attackCount 3 · bulletCount — · MP 74 | ✅ 공식(2013 변경 전 문안) + 본섭 1곳, 각주 필수 |
| 23120011 | 롤링 문썰트 | 180% · 6회 | M 20 · damage 180 · mobCount 8 · attackCount 6 · bulletCount — · MP 70 | 🔸 본섭 1곳 |

### 6.2 마스터레벨 층위 14건

| skill_id | 스킬 | 판정 M | 클라 |
|---|---|---:|---|
| 5321000 | 캐논 바주카 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 5321012 | 캐논 버스터 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 5321001 | 전함 노틸러스 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 5321010 | 파이렛 스피릿 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 5320008 | 하이퍼 몽키 스펠 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 5320009 | 오버버닝 캐논 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23120012 | 어드밴스드 파이널 어택 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23120010 | 디펜스 브레이크 | 20 | common.maxLevel 20 / 노드 masterLevel 10 / combatOrders 1 |
| 23120009 | 듀얼보우건 엑스퍼트 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23121000 | 이슈타르의 링 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23121002 | 레전드리 스피어 | 20 | common.maxLevel 20 / 노드 masterLevel 10 / combatOrders 1 |
| 23121003 | 라이트닝 엣지 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23121004 | 앤시언트 스피릿 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |
| 23121005 | 메이플 용사 | 30 | common.maxLevel 30 / 노드 masterLevel 10 / combatOrders 1 |

### 6.3 현행 KMS 최대레벨 차이 14건

| skill_id | 스킬 | 2012 M(판정) | 클라(1.2.160) | 현행 KMS 최대레벨 |
|---|---|---:|---:|---:|
| 5011001 | 펀칭 캐논 | 20 | 20 | 15 |
| 5300005 | 캐논 마스터리 | 20 | 20 | 10 |
| 5300004 | 크리티컬 파이어 | 15 | 15 | 5 |
| 5300008 | 파이렛 트레이닝 | 10 | 10 | 5 |
| 5311004 | 오크통 룰렛 | 10 | 10 | 15 |
| 5310006 | 리인포스 캐논 | 15 | 15 | 10 |
| 5310007 | 바이탈 익스트림 | 20 | 20 | 9 |
| 5310009 | 반격의 슈터 | 15 | 15 | 10 |
| 5321003 | 마그네틱 앵커 | 15 | 15 | 20 |
| 23100008 | 피지컬 트레이닝 | 10 | 10 | 5 |
| 23100005 | 듀얼보우건 마스터리 | 20 | 20 | 10 |
| 23101001 | 차지 드라이브 | 15 | 15 | 10 |
| 23110006 | 하이킥 데몰리션 | 15 | 15 | 5 |
| 23111008 | 엘리멘탈 나이트 | 20 | 20 | 10 |

### 6.4 문안 MP 층위 · ID 정정 · 명칭 표기차

| 유형 | skill_id | 스킬 | 기존 | 클라 | 비고 |
|---|---|---|---|---|---|
| 문안_MP_층위 | 23110006 | 하이킥 데몰리션 | F14 문안: MP 28 · 105% · 6회 · 즉사 10% · M5 (2013-03 테섭 변경 후 문안) | MP 32 · 110% · 6회 · 즉사 15% · M15 (1.2.160) |  |
| 명칭_표기차 | 5011002 | 기간틱 백스탭 | 기간틱 백스텝 (현행 KMS 표기) | 기간틱 백스탭 (클라 표기) | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 명칭_표기차 | 5321004 | 서포트 몽키 트윈스 | 서포트 몽키 (현행 KMS 표기) | 서포트 몽키 트윈스 (클라 표기) | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 명칭_표기차 | 23001002 | 아크로바틱 점프 | 스피릿 점프 (현행 KMS 표기) | 아크로바틱 점프 (클라 표기) | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 명칭_표기차 | 23101003 | 스피릿 인퓨젼 | 스피릿 인퓨전 (판정 목록 표기) | 스피릿 인퓨젼 (클라 표기) | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |
| 명칭_표기차 | 23100006 | 파이널 어택 : 듀얼보우건 | 파이널 어택 (판정 목록 표기) | 파이널 어택 : 듀얼보우건 (클라 표기) | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |
| 명칭_표기차 | 23111005 | 워터 쉴드 | 워터실드 (현행 KMS 표기) | 워터 쉴드 (클라 표기) | 클라이언트(1.2.160) KMS명과 현행 KMS명이 다름 — 개칭 또는 표기차 |
| 명칭_표기차 | 23111005 | 워터 쉴드 | 워터 실드 (판정 목록 표기) | 워터 쉴드 (클라 표기) | 판정 목록 표기와 클라이언트 String.wz 표기가 다름(동일 ID) |
| ID_정정 | 23120011 | 롤링 문썰트 | 이전 표기 ID 23121011 | 클라 실재 ID 23120011 | 23121011은 1.2.160 클라이언트에 존재하지 않음. 2312.img의 23120011이 해당 스킬(M20) |
| ID_정정 | 5321010 | 파이렛 스피릿 | 이전 표기 ID 5320013 | 클라 실재 ID 5321010 | 5320013은 1.2.160 532.img·String.wz에 없음. 5321010이 M30·패시브 반격+액티브 구조로 원문과 일치(Claude 판정 승인) |

### 6.5 영문명 보조 필드 10건

| skill_id | 스킬 | 편입본 name_en (basis) | 기존 사유 |
|---|---|---|---|
| 5011002 | 기간틱 백스탭 | name_en `Blast Back` (basis current-GMS) · MSEA Blast Back | ID는 있으나 현행 KMS명이 클라(2012)과 다름 — 개칭. 2012 시점 GMS 영문명 미확보. |
| 5301002 | 캐논 부스터 | name_en `Cannon Booster` (basis MSEA) · MSEA Cannon Booster | 현행 Papulatus 표에 KMS 명칭이 없거나(개편으로 ID 슬롯 공백) 현행 KMS명이 클라(2012)와 달라 2012 시점 영문명을 확정할 수 없음. |
| 5311004 | 오크통 룰렛 | name_en `Barrel Roulette` (basis MSN-직역) · MSEA Slumber | 현행 Papulatus 표에 KMS 명칭이 없거나(개편으로 ID 슬롯 공백) 현행 KMS명이 클라(2012)와 달라 2012 시점 영문명을 확정할 수 없음. |
| 5310007 | 바이탈 익스트림 | name_en `Pirate Rush` (basis current-GMS) · MSEA Pirate Rush | ID는 있으나 현행 KMS명이 클라(2012)과 다름 — 개칭. 2012 시점 GMS 영문명 미확보. |
| 5321004 | 서포트 몽키 트윈스 | name_en `Support Monkey` (basis current-GMS) · MSEA Monkey Artillery | ID는 있으나 현행 KMS명이 클라(2012)과 다름 — 개칭. 2012 시점 GMS 영문명 미확보. |
| 23001002 | 아크로바틱 점프 | name_en `Spirit Jump` (basis current-GMS) · MSEA Spirit Jump | ID는 있으나 현행 KMS명이 클라(2012)과 다름 — 개칭. 2012 시점 GMS 영문명 미확보. |
| 23101003 | 스피릿 인퓨젼 | name_en `Spirit Surge` (basis current-GMS) · MSEA Spirit Surge | 현행 Papulatus 표에 KMS 명칭이 없거나(개편으로 ID 슬롯 공백) 현행 KMS명이 클라(2012)와 달라 2012 시점 영문명을 확정할 수 없음. |
| 23111004 | 이그니스 로어 | name_en `Ignis Roar` (basis current-GMS) · MSEA Ignis Roar | 현행 Papulatus 표에 KMS 명칭이 없거나(개편으로 ID 슬롯 공백) 현행 KMS명이 클라(2012)와 달라 2012 시점 영문명을 확정할 수 없음. |
| 23111005 | 워터 쉴드 | name_en `Water Shield` (basis current-GMS) · MSEA Water Shield | ID는 있으나 현행 KMS명이 클라(2012)과 다름 — 개칭. 2012 시점 GMS 영문명 미확보. |
| 23120011 | 롤링 문썰트 | name_en `Rolling Moonsault` (basis current-GMS) · MSEA Rolling Moonsault | 현행 Papulatus 표에 KMS 명칭이 없거나(개편으로 ID 슬롯 공백) 현행 KMS명이 클라(2012)와 달라 2012 시점 영문명을 확정할 수 없음. |

## 7. 대상외 (12건 — 판정 §4, 58종 고정)

| skill_id | img | String.wz 명칭 | maxLevel | invisible | 사유 |
|---|---|---|---:|---:|---|
| 23000004 | 2300.img | 네이쳐스 드레인 | 1 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 23101007 | 2310.img | (이름 없음) | 20 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 23111009 | 2311.img | 엘리멘탈 나이트 | 20 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 23111010 | 2311.img | 엘리멘탈 나이트 | 20 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 23121008 | 2312.img | 용사의 의지 | 5 | 1 | 직업 공통 스킬(이번 668 스킬 동결에서는 미노출 — Claude 판정 §4). 클라 invisible=1, 근거 충돌(클라 비표시 ↔ F6 공지 목록)은 임의로 풀지 않음 |
| 5010004 | 501.img | 포춘 어택 | 1 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 5010005 | 501.img | (이름 없음) | 1 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 5300007 | 530.img | (이름 없음) | 20 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 5310008 | 531.img | 몽키 웨이브 | 20 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 5320011 | 532.img | (이름 없음) | 15 | 1 | invisible=1 부속·숨김 노드 — 58종 목록(클라 표시 스킬 58)과 정확히 일치 |
| 5321005 | 532.img | 메이플 용사 | 30 | 1 | 직업 공통 스킬(이번 668 스킬 동결에서는 미노출 — Claude 판정 §4). 클라 invisible=1, 근거 충돌(클라 비표시 ↔ F6 공지 목록)은 임의로 풀지 않음 |
| 5321006 | 532.img | 용사의 의지 | 5 | 1 | 직업 공통 스킬(이번 668 스킬 동결에서는 미노출 — Claude 판정 §4). 클라 invisible=1, 근거 충돌(클라 비표시 ↔ F6 공지 목록)은 임의로 풀지 않음 |

## 7.1 ID 목록 v2 표기 정정 요청 (판정 §5 조건)

화면 정본을 클라 표기로 두면 ID 목록의 `name_ko`도 같은 값이어야 동결 기준과 화면이 어긋나지 않는다. 판정이 지목한 3건이다.

| skill_id | 클라 표기(정본) | 목록 현재 표기 | 요청 |
|---|---|---|---|
| 23101003 | 스피릿 인퓨젼 | 스피릿 인퓨전 | ID 목록 v2(및 사본)의 name_ko를 클라 표기로 갱신 — 판정 §5 조건 |
| 23100006 | 파이널 어택 : 듀얼보우건 | 파이널 어택 | ID 목록 v2(및 사본)의 name_ko를 클라 표기로 갱신 — 판정 §5 조건 |
| 23111005 | 워터 쉴드 | 워터 실드 | ID 목록 v2(및 사본)의 name_ko를 클라 표기로 갱신 — 판정 §5 조건 |

## 8. 남은 확인 (4건)

1. **2012 시점 영문명 (선택)** — S4 GMS v117 목록에서 5311004·23101003의 당시 영문명을 확인하면 verified_2012를 true로 올릴 수 있다. 현재는 전건 false(판정 §3의 선택 요청).
2. **shortDesc 대체 여부 (선택)** — KMS 1.2.160에 shortDesc 필드가 없어 shortDesc_ko는 0/58. desc의 간략본 pdesc_ko(48/58)를 대체로 쓸지 결정 필요 — 본 파일은 미채택(null)으로 두고 값만 병기했다.
3. **공통 스킬 노출 정책 (디렉터 결정)** — 판정 §4의 별건 — 메르 23121005 유지 / 캐논 5321005·5321006·메르 23121008 추가 여부. 정해지기 전에는 58종 고정이 기준.
4. **has_icon·빌더 역이식 (보강 세대)** — 아이콘 경로 58/58 준비됨 — 편입 시 has_icon=true 전환과 기존 610종 무변경 확인은 보강 세대 단계에서 처리.

## 9. 산출 파일·검증

| 파일 | 내용 |
|---|---|
| `justice_t2_merc_cannon_extract58_mergefields_20261120.json` | 스킬 58건 — desc_ko·hint_ko·levels_kms160·name_en(라벨)·aliases_ko·아이콘·판정 대조 + 대상외 12건 + 대조 지점 60건 |
| `justice_t2_merc_cannon_extract58_mergefields_20261120.md` | 본 보고서 |
| `t2_merc_cannon_icons_20261120/` | PNG 188장(원천 세대와 동일 파일 재사용) |
| `justice_t2_merc_cannon_client_extract_20261120.json`·`.md` | 원천 세대 — **수정하지 않고 보존**(판정이 재현한 해시 `ea4098c6…` 유효) |

검증 실측:
- 건수: 58건 (캐논슈터 29 · 메르세데스 29) — 누락 0
- ID 목록 대조(`justice_t2_skill_id_20261119.json`): 캐논슈터 29/29 · 메르세데스 29/29, **순서까지 일치**, 중복 0
- 아이콘: 기대 188장 · 디스크 188장 · 경로 누락 0 · 파일명 중복 0
- 층위 분리: 레코드에 `description`·`properties_raw` 필드 0건(전건 desc_ko·levels_kms160 사용)
- 필수 필드: desc_ko 58 · levels_kms160.master_level 58 · values_at_master_level 58 · name_en 58 · name_en_basis 58 · icons.base 58 · 판정_대조 58
- 값 무변경: desc·hint·common_raw 수식·levels 전 구간·아이콘 파일이 원천 세대와 deep 대조 일치(재추출·재계산 없음)
- M(마스터레벨) 판정 일치 58/58 · 미치환 #토큰 보유 0건 · JSON 파싱 통과

해시:

| 파일 | 바이트 | SHA-256 |
|---|---:|---|
| `justice_t2_merc_cannon_extract58_mergefields_20261120.json` | 398,803 | `f9fdb16b3a55ae32da8c64501cef578364c83a4c66a53fbe5fd582b9df45161a` |
| `justice_t2_merc_cannon_client_extract_20261120.json` | 337,629 | `ea4098c6dbfb4fc1dd6c54a9d8dada479160f9175a6a4e60f0948695cd478e64` |
| `t2_merc_cannon_icons_20261120/` | 160,172 (188장 합계) | 트리 실측 |

## 10. 기준 클라이언트와 규칙

- KMS 1.2.160 (2012-06-03 파일 날짜) · Skill.wz (311,039,146 B) · String.wz (3,717,336 B)
- Skill.wz MD5 `a59db2f0bd6b3c355dbeda862f7763ab` · String.wz MD5 `f2e28dbf2ccc754c9c94eaa4e0e5c573`
- 원본 아카이브: KMS 1.2.160 7z 분할본(part00~06.bin, 합계 2,797,136,045 B) — MD5 5c9608581a444b7bb84445fb3c4e34d1. 기존 ID 목록(justice_t2_skill_id_20261119)이 인용한 MD5가 이 아카이브 값이다(Skill.wz 자체 MD5와 다름).

추출 방법(원천 세대와 동일, 재추출 없음):
- Skill.wz 이미지(501/530/531/532/2300/2310/2311/2312.img)의 skill 하위 노드를 WZ 바이너리 직접 파싱(BMS 키, v160 해시)
- 아이콘 canvas: width/height/format 헤더 → listWz 블록(int32 길이 + WzKey XOR) 복호 → raw deflate → ARGB4444/ARGB8888 → PNG
- 설명문: String.wz Skill.img의 name/desc/h/pdesc/ph 원문 그대로
- 레벨별 수치: common 블록의 수식을 레벨 1~maxLevel까지 평가(클라이언트는 레벨별 값을 저장하지 않고 수식만 보관)

규칙:
- **층위_분리** — 기존 610종의 description·properties_raw는 GMS 95 영문 원문 층위다. 신규 58종은 KMS 1.2.160 한글·수치만 있으므로 desc_ko·shortDesc_ko·hint_ko·levels_kms160으로 분리 수록하고, description·properties_raw는 이 파일에 넣지 않는다(병합 시 null 유지).
- **desc_ko** — String.wz Skill.img/<id>/desc 한글 원문 그대로(이스케이프·치환 없음).
- **shortDesc_ko** — KMS 1.2.160 String.wz Skill.img에는 shortDesc 필드가 없다. 1,998개 스킬 노드 전수 필드 인벤토리: name 1,873 · desc 1,788 · h 1,126 · h1 576 · h2 41 · h3 30 · h4 6 · pdesc 722 · ph 690 · bookName 125. 따라서 전건 null + 사유 기재, pdesc(간략본)는 미채택 병기.
- **levels_kms160** — master_level은 common.maxLevel(2단 판정 M). values_at_master_level은 그 레벨의 평가값, levels는 1~M 전 구간, common_raw는 수식 원문. 클라에 level 블록 원문이 없어 평가값이다.
- **레벨수치_변수** — x=스킬 레벨, d()=내림, u()=올림. #토큰 치환은 동일 레벨의 common 값으로 수행. 치환 후 남은 #토큰은 hint_미치환_토큰에 기록.
- **필드_의미** — `mpCon`=MP 소비, `damage`=데미지%, `mobCount`=대상 수, `attackCount`=공격 횟수, `bulletCount`=발사체 수(이 필드가 타수로 표기되는 스킬이 있다), `time`=지속 초, `cooltime`=재사용 대기 초, `prop`=확률%, `cr`=크리티컬 확률%
- **name_en** — 보조 필드(검색·alt). 값은 현행 GMS 명칭, name_en_basis로 출처 라벨(current-GMS / MSEA / MSN-직역), verified_2012=false. GMS 칸이 비면 MSEA→MSN 순 대체(판정 §2·§3).
- **name_ko** — 화면 정본은 KMS 1.2.160 String.wz 표기(판정 §5). 판정 목록 표기·현행 KMS 표기는 aliases_ko로 보존해 검색에 잡히게 한다.
- **아이콘** — PNG 32×32, fmt1(ARGB4444). 파일명 {skill_id}_{WZ 캔버스 노드명}.png — 기본 아이콘 <skill_id>_icon.png. 상태 변형(icon1~5)이 있는 3종은 전부 포함.
- **대조** — 클라값과 기존 판정값이 어긋나는 지점은 덮어쓰지 않고 대조_지점[]에 병기. 정본은 클라(1.2.160)이며 판정값은 그대로 보존.
