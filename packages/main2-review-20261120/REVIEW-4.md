# 알팡지지 2.0 메인 시안 4차 점검 (2026-11-20, 기술이사)

대상: `packages/main2-preview-20261120/index.html` 25,223B `9b1773ff…`(커밋 `734673c`). 직전본(`740748e`)과 diff 3줄.

## 결론: 필수 잔여 없음 — Pretendard 적용 확인
| 항목 | 결과 |
|---|---|
| body font-family | ✓ `'Pretendard Variable','Pretendard',-apple-system,'Malgun Gothic',sans-serif` (계산 스타일로 확인) |
| 글꼴 서브셋 로드 | ✓ 로컬 서버에서 실제 로드: `document.fonts` 92개 중 **14개 `loaded`**, `document.fonts.status`=loaded (이번에는 외부망 접근이 되어 실증함) |
| preconnect | ✓ `crossorigin` 없는 항목 + 있는 항목, 2줄 (CSS·글꼴 각각 연결) |
| 렌더 차단 CSS | 53,513B(전송 8,189B 압축), `renderBlockingStatus=blocking`. 정적 2,966B보다는 크지만 압축 전송 8KB 수준 |
| 위생 게이트 | cdn-cgi 0 · Analytics 0 · mailto 1 ✓ |
| diff | preconnect 1줄 추가, body font-family 1줄 교체 외 변경 없음 |

## 남은 것(필수 아님)
- 이미지 실물이 올라오면 3회 중앙값 LCP·CLS 측정(히어로 1280w 104.6KB는 상한 95%).
- 모바일 폭 드롭다운 위치(좁은 뷰포트 에뮬레이션 불가).
- 본 빌드 때: head 계승·`hreflang`·위생 게이트 재확인, 수치 빌드 주입, 대만·베트남 홈 적용.
