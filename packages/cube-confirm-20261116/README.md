# 큐브 건 1 확정 재료 제출 (판정 48f5794 후속)

## 동봉 실물
- cube_build.py (현행, mailto 정정 반영): 53,433B · b6c57c8857574e0839db52d28fb4d7ea62eaf60b933a111090d3727956c92d07
  - 정정 전 동결 빌더는 53,476B · 309fbb7f… (백업 보존). 정정으로 −43B (푸터 href 교체분).
  - 저장소 builders/ 사본에도 같은 본이 반영됐습니다 (동결 목록에 명시).
- 빌더 입력 파일 (원본 cube-data.json 12,452,332B · 1a9ff13f…를 분할 제출 — push 한도 때문):
  - inputs/cube-data-core.json: optionPools를 뺀 본체 전 키
  - inputs/pools/<cube>--<부위>.json 30개: optionPools[miracle|suspicious][부위]
  - 재구성: core를 json.load한 dict에 optionPools를 만들어 pools 파일들을 [cube][부위]로 넣으면 원본과 같은 값의 dict가 됩니다 (빌더는 json.load로 읽으므로 직렬화 형식은 무관).
- 동결 목록 2종: 역이식 (49f33cb0…) · mailto 정정 (764b2865…)
- 검수 기록 2종: 역이식 QA (01c4995b…) · mailto 동결 QA (1bd87463… — 재생성본 = 동결본 바이트 일치 재실증 포함)

## 재현 기준
- 건 2 배포 완료: 커밋 0dcd74c9, 정본 = 50,774B · 7f382ebf… (고지 d9e6cc70).
- 격리 실행 재생성본이 7f382ebf…와 바이트 일치하는지, CF 흔적 (cdn-cgi · Analytics · 비컨 내장)이 0인지 확인 부탁드립니다. email-protection은 정정으로 0이 된 상태입니다.
- 확정 판정이 나오면 '큐브 재생성 금지'를 해제하고 기준 해시를 7f382ebf…로 이행하겠습니다.
