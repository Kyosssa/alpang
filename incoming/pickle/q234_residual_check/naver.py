import subprocess, json, urllib.parse, time, os, re
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
JAR = "/workspace/work/q234_residual_check/cj.txt"
BASE = "https://section.blog.naver.com/Search/Post.naver"
AJAX = "https://section.blog.naver.com/ajax/SearchList.naver"

def _page_url(q, page=1, s="2011-07-01", e="2012-12-31", order="sim"):
    return (f"{BASE}?pageNo={page}&rangeType=ALL&orderBy={order}&keyword={urllib.parse.quote(q)}"
            f"&startDate={s}&endDate={e}")

def ensure_cookie():
    if os.path.exists(JAR): return
    subprocess.run(["curl","-s","-c",JAR,"-o","/dev/null","-A",UA,_page_url("메이플")],timeout=40)

def search(q, page=1, s="2011-07-01", e="2012-12-31", order="sim", per=30, retries=2):
    ensure_cookie()
    aj = (f"{AJAX}?countPerPage={per}&currentPage={page}&keyword={urllib.parse.quote(q)}"
          f"&orderBy={order}&startDate={s}&endDate={e}&type=post")
    for t in range(retries+1):
        r = subprocess.run(["curl","-s","-b",JAR,"-c",JAR,"-A",UA,"-H","Referer: "+_page_url(q,page,s,e,order),aj],
                           capture_output=True, text=True, timeout=40)
        out = r.stdout
        try:
            data = json.loads(out.split("\n",1)[1] if out.startswith(")]}") else out)
            res = data.get("result") or {}
            return res.get("searchList") or [], res.get("totalCount") or 0
        except Exception:
            time.sleep(1.5)
    return [], 0
