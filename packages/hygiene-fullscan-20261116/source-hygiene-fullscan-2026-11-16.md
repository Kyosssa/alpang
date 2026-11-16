# 빌더 산출 페이지 소스 위생 전수 점검 (저장소 main 전 HTML 119파일, 2026-11-16)

방법: 저장소 전 HTML을 받아 cdn-cgi email-protection · email-decode · Analytics 주석 · 비컨 내장 · mailto를 기계로 셌다. 표본 4파일 (items 허브 · 타임라인 · 대만 FAQ · about)은 GitHub API로 재대조해 스캔 신뢰도를 확인했다 (전건 일치).

## 결과: 결함 72파일 / 정상 47파일

| 그룹 | 파일 수 | 내역 |
|---|---|---|
| items 계열 (equip 42 + 카테고리 쌍 10 + 허브 1) | 53 | 전건 email-protection 1 · Analytics 2~4. 허브 (items/index)는 email-decode 1 · 비컨 1 추가 |
| 타임라인 (한국어 · 대만 · 베트남) | 3 | email-protection 1 · Analytics 13~19 (프레임 구조상 주석 문자열 다수) |
| 다국어 FAQ (대만 · 베트남) | 2 | email-protection 1 · Analytics 10 · 비컨 5 |
| 다국어 quests (대만 · 베트남) | 2 | email-protection 1 · email-decode 1 · Analytics 2 · 비컨 1 |
| 다국어 가이드 (대만 · 베트남 각 3편) | 6 | email-protection 1만 |
| 정적 페이지 | 4 | privacy: email-protection 3 · decode 1 · Analytics 2 · 비컨 1 / data-criteria: 1 · 1 · 2 · 1 / about · terms: Analytics 2 · 비컨 1 (mailto는 정상) |
| market | 1 | email-protection 1만 |
| 큐브 | 1 | email-protection 1 — 정정 진행 중이라 현황만 기록 |

## 정상 (결함 0) 주요 페이지
가이드 본편 22편 + 허브 · early-quests · jobs · mobs · maps · npcs · quests (한국어) · 홈 + 다국어 홈 · 한방컷 · planner (정정 후) · FAQ (한국어) 등 47파일.

## 판정
- 결함의 본체는 빌더 세대에 굳은 라이브 수집 푸터 (email-protection 링크)와 주석 · 비컨 내장이다. 정정은 빌더 단위로 묶어 (items 빌더 · 타임라인 프레임 · faq 빌더 · npc_quest 다국어 출력 등) 소스에서 제거하는 동결 사슬이 필요하다.
