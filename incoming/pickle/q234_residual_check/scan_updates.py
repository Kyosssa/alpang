import sys, re, json, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, '/workspace/work/map_tmp')
import lib

KEYS = ['옥토퍼스', '믹스골렘', '스톤골렘', '커닝시티 지역', '몬스터 레벨', '몬스터의 레벨']
OUT = '/workspace/work/q234_residual_check/updates.jsonl'


def one(i):
    h = lib.curl(f'https://maplestory.nexon.com/News/Update/{i}', 40)
    if len(h) < 5000:
        return {'id': i, 'err': 'short', 'len': len(h)}
    t = lib.clean_text(h)
    title = ''
    date = ''
    m = re.search(r'\n업데이트\n(.*?)\n', t)
    if m:
        title = m.group(1).strip()
    d = re.search(r'\n(20\d{2}\.\d{2}\.\d{2})\n', t)
    if d:
        date = d.group(1)
    hits = {}
    for k in KEYS:
        idx = [mm.start() for mm in re.finditer(re.escape(k), t)]
        if idx:
            snips = []
            for j in idx[:4]:
                snips.append(t[max(0, j - 160):j + 220].replace('\n', ' '))
            hits[k] = snips
    return {'id': i, 'date': date, 'title': title, 'len': len(t), 'hits': hits}


lo, hi = int(sys.argv[1]), int(sys.argv[2])
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(one, i): i for i in range(lo, hi + 1)}
    for fu in as_completed(futs):
        r = fu.result()
        with open(OUT, 'a') as f:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print(r.get('id'), r.get('date'), r.get('title', '')[:40], list((r.get('hits') or {}).keys()), flush=True)
