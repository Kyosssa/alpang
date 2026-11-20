#!/usr/bin/env python3
"""02·03 채움본(82f62e48/25ee82aa, 구세대)에 피클 현행본의 ID 정정 9건을 반영한다.
사용: py -3.11 -I -X utf8 apply_id_fix.py <repo>  → 출력 02-...-v2.json, 03-...-v2.json (이 스크립트 폴더)
"""
import json, os, sys
repo = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
pk = json.load(open(os.path.join(repo, 'incoming/pickle/justice_t2_skill_id_20261119.json'), encoding='utf-8'))
pdir = os.path.join(repo, 'packages/justice-t2-skillid-20261119')
P = {(j, s['skill']): s for j, L in pk['jobs'].items() for s in L}
fix = [(x['직업'], x['스킬'], x['이전'], x['이후']) for x in pk['갱신_20261119_2140']['정정_목록']]
assert len(fix) == 9
# 02
a = json.load(open(os.path.join(pdir, '02-skill-id-list-filled.json'), encoding='utf-8'))
for j, n, old, new in fix:
    s = next(x for x in a['jobs'][j] if x['skill'] == n)
    assert s['skill_id'] == old, (n, s['skill_id'])
    for k in ('skill_id', 'id_status', 'id_source', 'id_note'):
        s[k] = P[(j, n)][k]
    if 'id_confirm' in P[(j, n)]:
        s['id_confirm'] = P[(j, n)]['id_confirm']
for j, L in a['jobs'].items():
    for s in L:
        assert s['skill_id'] == P[(j, s['skill'])]['skill_id']
ids = [s['skill_id'] for L in a['jobs'].values() for s in L]
assert len(ids) == 149 and len(set(ids)) == 149
json.dump(a, open(os.path.join(here, '02-skill-id-list-filled-v2.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
# 03 (캐논 샘플)
b = json.load(open(os.path.join(pdir, '03-newjob-sample-cannon-filled.json'), encoding='utf-8'))
n3 = 0
for j, n, old, new in fix:
    if j != '캐논슈터':
        continue
    s = next(x for x in b['skills'] if x['name_ko'] == n)
    assert s['skill_id'] == old
    s['skill_id'] = new
    for k in ('id_status', 'id_source', 'id_note'):
        if k in s and k in P[(j, n)]:
            s[k] = P[(j, n)][k]
    n3 += 1
for s in b['skills']:
    assert s['skill_id'] == P[('캐논슈터', s['name_ko'])]['skill_id']
json.dump(b, open(os.path.join(here, '03-newjob-sample-cannon-filled-v2.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
print('02: 9건 정정, 149건 ID 전건 피클 현행본과 일치·중복 0 / 03: 캐논 %d건 정정, 29건 일치' % n3)
