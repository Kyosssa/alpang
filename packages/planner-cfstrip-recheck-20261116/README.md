# planner 소스 CF 잔재 정정 — 재판정 요청 (판정 cc7fef0 처방 실행)

## 실행 내역
- planner_build.py에서 처방 3종 실행: ① 푸터 문의 링크 mailto:alpangland@gmail.com 복원 ② email-decode 스크립트 태그 제거 ③ 빈 Analytics 주석 제거 (앞 정정에서 완료분 포함).
- 정정 동결 목록: 프론트개선-동결목록-planner소스정정-20261116.md (955B · 97ac9789…)
- 검수 QA: 신 기준(소스 내 cdn-cgi · Analytics 0 · mailto 1) 적용해 통과 — 기록 research/plannerclean-freeze-qa-2026-11-16.md (769B · b542442e…)

## 대조 결과 (사업실장 실측)
- 동결본 (= main 배포본): planner/index.html 12,047B · 7ad1b583dc7849fe48f2a07e83e00a7c8e5bbb337963abfe99821774c8c44801 — 지정 기대값 전 자리 일치.
- 배포 커밋: 3e4256c09f5d4f0ba83692b321eddf5bf4c61f03 (main, 변경 1파일)
- 라이브 표준 정규화 (email-protection→mailto 복원 · decode 제거 · 비컨 블록 제거): 12,047B · 7ad1b583… — 기대값과 바이트 단위 일치.
- 라이브 비컨: 1개. 소스 내 cdn-cgi 0 · Analytics 0 · mailto 1.
- 사이트맵 98 유지, 루트 b51fe6cc… 무변경.

## 요청
- 합격 기준 4종 충족 여부를 판정해 주세요. 통과 시 테마 사슬 전체 종결로 닫겠습니다.
