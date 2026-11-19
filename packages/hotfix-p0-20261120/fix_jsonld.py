#!/usr/bin/env python3
"""guide/early-quests JSON-LD(ItemList)의 https://alpang.gg/npcs/#quest-N 55건 → https://alpang.gg/quests/lv-*#quest-N
사용: py -3.11 -I -X utf8 fix_jsonld.py <main 체크아웃 경로>
"""
import glob, json, os, re, sys

root = sys.argv[1].rstrip('/\\')
where = {}
for p in sorted(glob.glob(os.path.join(root, 'quests', 'lv-*.html'))):
    t = open(p, encoding='utf-8', newline='').read()
    for qid in re.findall(r'id="quest-(\d+)"', t):
        where.setdefault(qid, []).append(os.path.basename(p)[:-5])
path = os.path.join(root, 'guide', 'early-quests', 'index.html')
s = open(path, encoding='utf-8', newline='').read()
pat = re.compile(r'https://alpang\.gg/npcs/#quest-(\d+)')
ids = pat.findall(s)
assert len(ids) == 55, len(ids)
for q in set(ids):
    assert len(where.get(q, [])) == 1, q
s2 = pat.sub(lambda m: 'https://alpang.gg/quests/%s#quest-%s' % (where[m.group(1)][0], m.group(1)), s)
# JSON-LD가 여전히 유효한 JSON인지 확인
for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S):
    json.loads(blk)
open(path, 'w', encoding='utf-8', newline='').write(s2)
print('JSON-LD 앵커 %d건(고유 %d) 정정, 모든 ld+json 블록 JSON 유효' % (len(ids), len(set(ids))))
