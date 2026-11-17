# Claude 격리 재현 산출 실물 (2026-11-17)

Python 3.11.9 `-I -X utf8`, Windows, HOME·USERPROFILE 격리. 빌더 `7476e178…`(패키지 동봉본과 동일 파일, builder2-as-run.py).
**파일은 Windows 텍스트 모드 산출이라 CRLF 그대로입니다.** LF 비교는 `tr -d '\r'` 후 해시하세요.

| 파일 | 입력 세트 | 바이트 | CRLF 원본 해시 | LF 정규화 해시 |
|---|---|---|---|---|
| run-new/mobs-index.html | inputs (신 정본) | 456,060 | e2cca749… | de860f7d… |
| run-new/maps-index.html | inputs (신 정본) | 576,203 | 8c34120b… | 7059da49… |
| run-base/mobs-index.html | inputs-base 조합 (구 정본) | 415,556 | bda7ec57… | sums.txt 참조 |
| run-base/maps-index.html | inputs-base 조합 | 576,157 | e29d9fe2… | sums.txt 참조 |

주의: 기대값 e2cca749…·8c34120b…은 **신 정본(inputs) 산출의 CRLF 해시**입니다. inputs-base 조합은 구 정본이라 해당 값이 나오지 않는 것이 정상이며, 구 정본 조합의 기대값은 위 표의 run-base 값입니다.
