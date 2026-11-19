#!/usr/bin/env python3
"""검색 인덱스 JSON의 href에서 .html 확장자를 제거한다 (다음 인덱스 세대 생성 단계용).

사용: py -3.11 -I -X utf8 fix_index_hrefs.py <입력.json> <출력.json>
- 값만 바꾸고 레코드 순서·다른 필드는 그대로 둔다. 출력 파일명은 새 세대 이름으로 만들 것(기존 세대 덮어쓰기 금지).
- 변환 규칙: "/items/use.html#it1" -> "/items/use#it1", "/quests/lv-1-10.html#quest-5" -> "/quests/lv-1-10#quest-5"
"""
import json, re, sys

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
n = 0
for r in d['records']:
    h = r.get('href', '')
    h2 = re.sub(r'\.html(?=[#?]|$)', '', h)
    if h2 != h:
        r['href'] = h2
        n += 1
json.dump(d, open(dst, 'w', encoding='utf-8', newline=''), ensure_ascii=False, separators=(',', ':'))
print('변경 %d건 / 전체 %d건' % (n, len(d['records'])))
