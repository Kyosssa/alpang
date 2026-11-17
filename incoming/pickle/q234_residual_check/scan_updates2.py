import sys, re, json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, '/workspace/work/map_tmp')
import lib

KEYS = ['옥토퍼스', '믹스골렘', '몬스터 레벨', '몬스터의 레벨', '몬스터의 능력치', '커닝시티 지역']
OUT = '/workspace/work/q234_residual_check/updates2.jsonl'


def one(i):
    h = lib.curl(f'https://maplestory.nexon.com/News/Update/{i}', 40)
    if len(h) < 8000:
        return {'id': i, 'skip': len(h)}
    t = lib.clean_text(h)
    title = ''
    m = re.search(r'<p class="qs_title">(.*?)</p>', h, re.S)
    if m:
        title = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
        title = re.sub(r'\s+', ' ', title)
    d = re.search(r'<p class="last"><img[^>]*>(\d{4}\.\d{2}\.\d{2})</p>', h)
    date = d.group(1) if d else ''
    hits = {}
    for k in KEYS:
        idx = [mm.start() for mm in re.finditer(re.escape(k), t)]
        if idx:
            hits[k] = [t[max(0, j - 200):j + 400].replace('\n', ' ') for j in idx[:3]]
    return {'id': i, 'date': date, 'title': title, 'len': len(t), 'hits': hits}


lo, hi = int(sys.argv[1]), int(sys.argv[2])
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(one, i): i for i in range(lo, hi + 1)}
    rows = []
    for fu in as_completed(futs):
        r = fu.result()
        if r.get('skip'):
            continue
        rows.append(r)
with open(OUT, 'a') as f:
    for r in sorted(rows, key=lambda x: x['id']):
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print(r['id'], r['date'], r['title'][:45], list(r['hits'].keys()), flush=True)
