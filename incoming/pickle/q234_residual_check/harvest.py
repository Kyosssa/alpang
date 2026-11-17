import sys, json, os, time, re
sys.path.insert(0, '/workspace/work/q234_residual_check')
import naver
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, '/workspace/work/map_tmp')
from lib import postview, parse_post

QUERIES = sys.argv[1].split('|')
PAGES = int(sys.argv[2]) if len(sys.argv) > 2 else 2
OUT = '/workspace/work/q234_residual_check/hits.jsonl'

seen = set()
if os.path.exists(OUT):
    for line in open(OUT):
        try: seen.add(json.loads(line)['url'])
        except: pass

cands = {}
for q in QUERIES:
    for p in range(1, PAGES + 1):
        try:
            res, tot = naver.search(q, p, '2011-01-01', '2013-06-30')
        except Exception as e:
            print('search fail', q, p, e); continue
        for r in res:
            u = r.get('postUrl')
            if not u: continue
            if u in seen: continue
            cands[u] = {'url': u, 'q': q, 'ts': r.get('postdate') or r.get('addDate')}
        print(q, p, tot, len(res), flush=True)
        time.sleep(0.4)

print('cands', len(cands), flush=True)


def work(c):
    m = re.search(r'blog\.naver\.com/([A-Za-z0-9_\-\.]+)/(\d+)', c['url'])
    if not m: return None
    bid, logno = m.group(1), m.group(2)
    try:
        h = postview(bid, logno)
        if len(h) < 3000: return None
        p = parse_post(h)
        body = p['body']
        if '옥토퍼스' not in body and '믹스골렘' not in body: return None
        return {'url': c['url'], 'q': c['q'], 'ts': c['ts'], 'title': p['title'],
                'date': p['date'], 'body': body}
    except Exception:
        return None


n = 0
with open(OUT, 'a') as f, ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(work, c): c for c in cands.values()}
    for fu in as_completed(futs):
        r = fu.result()
        if r:
            f.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
print('saved', n)
