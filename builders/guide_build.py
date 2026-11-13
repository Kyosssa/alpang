import json, os
from collections import defaultdict

BASE = os.path.expanduser("~/workspace/alpang")
DB = f"{BASE}/data/db"
OUT = f"{BASE}/site/guide"

maps = {m["id"]: m for m in json.load(open(f"{DB}/maps.json"))["maps"]}
mobs = {m["id"]: m for m in json.load(open(f"{DB}/mobs.json"))["mobs"]}
rels = json.load(open(f"{DB}/relations.json"))["relations"]

map_mobs = defaultdict(list)   # map_id -> [{mob_id, placements}]
mob_maps = defaultdict(list)   # mob_id -> [{map_id, placements}]
for r in rels:
    map_mobs[r["map_id"]].append(r)
    mob_maps[r["mob_id"]].append(r)

def dname(x):
    return x.get("name_ko_candidate") or x.get("name_en")

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DISCLAIMER = "이 페이지는 본진 빅뱅 직후 기준이며, 알팡 실서버 구현 시 달라질 수 있습니다."
FOOT = """알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95) · 한글 이름은 '표시명 후보'입니다 · 페이지 갱신일: 2026-10-14
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>"""
FOOT_HUNTING = """
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95 수집 데이터) · 한글 이름은 '표시명 후보'입니다 · 페이지 갱신일: 2026-11-03
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  """
FOOT_EDELSTEIN = """
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95 수집 데이터) · 한글 이름은 '표시명 후보'입니다 · 페이지 갱신일: 2026-11-02
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  """
FOOT_ORBIS = """
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95 수집 데이터) · 한글 이름은 '표시명 후보'입니다 · 페이지 갱신일: 2026-11-01
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  """
FOOT_LUDIBRIUM = """
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95) · 한글 이름은 '표시명 후보'입니다 · 페이지 갱신일: 2026-11-02
  <br><span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
"""

THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script>"
NEW_DOT_CSS = "\n  .new-dot{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}\n  .new-dot.on{display:inline-block}"

CSS = """
  :root{--bg:#faf9f6;--card:#ffffff;--line:#e6e1d8;--text:#1f1c18;--sub:#6f6a5e;--accent:#FF7E36;--accent-dark:#C25700;--accent-soft:#FFF1E8;--unknown:#6b6250}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:"Pretendard",-apple-system,BlinkMacSystemFont,"Malgun Gothic","Apple SD Gothic Neo",sans-serif;letter-spacing:-0.025em;line-height:1.7;padding:0 16px 48px}
  button,input,select,textarea{font-family:inherit}
  .wrap{max-width:1280px;margin:0 auto}
  .gnb{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px 10px;padding:14px 6px;background:rgba(250,249,246,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
  .gnb .logo{font-size:20px;font-weight:800;color:var(--text);text-decoration:none}
  .gnb nav{display:flex;flex-wrap:wrap;justify-content:flex-end;row-gap:2px}
  .gnb nav a{color:var(--sub);text-decoration:none;font-size:15px;font-weight:600;margin-left:14px;white-space:nowrap}
  @media (max-width:560px){ .gnb .logo{font-size:18px} .gnb nav a{font-size:14px;margin-left:10px} }
  .gnb nav a{display:inline-flex;align-items:center;min-height:44px}
  @media (max-width:768px){.gnb{flex-wrap:nowrap}.gnb nav{flex-wrap:nowrap;overflow-x:auto;flex:1 1 auto;min-width:0;justify-content:flex-start;scrollbar-width:none;-webkit-mask-image:linear-gradient(to right,#000 92%,transparent);mask-image:linear-gradient(to right,#000 92%,transparent)}.gnb nav::-webkit-scrollbar{display:none}}
  .gnb nav a.on{color:var(--accent-dark)}
  .intro{text-align:center;padding:28px 0 16px}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .disc{background:var(--accent-soft);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:14px;color:var(--text);margin-top:16px;text-align:center}
  section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 3px rgba(30,25,15,.05);padding:20px 22px;margin-top:14px}
  h2{font-size:18px;font-weight:700;margin-bottom:10px}
  p.body{font-size:16px;margin-bottom:8px}
  .legend{font-size:13px;color:var(--sub);margin-top:10px}
  table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;margin-top:6px}
  th{background:var(--accent-soft);color:var(--accent-dark);font-weight:800;text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
  td{padding:8px 10px;border-bottom:1px solid #f0ece3;vertical-align:top}
  tr:last-child td{border-bottom:none}
  td.num, th.num{text-align:right;white-space:nowrap}
  .mname{font-weight:700}
  .men{display:block;font-size:12.5px;color:var(--sub);font-weight:600}
  .glink{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:700;color:var(--sub);text-decoration:none;margin:2px 4px 2px 0;background:var(--card)}
.glink:hover{color:var(--ink)}
.chip{display:inline-block;background:#f7f3ec;border:1px solid var(--line);border-radius:999px;padding:1px 9px;font-size:13.5px;margin:1px 2px 1px 0}
  .chip b{color:var(--accent-dark)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:6px}
  .mob{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(30,25,15,.05)}
  .mob .islot{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:#F3F4F6;border-radius:6px;margin:0 auto 6px}
  .mob .mimg{max-width:32px;max-height:32px}
  .mob .nm{font-size:15px;font-weight:700}
  .mob .en{font-size:12.5px;color:var(--sub);font-weight:600}
  .mob .stat{font-size:14px;line-height:1.5;margin-top:6px}
  .mob .stat b{color:var(--accent-dark)}
  .mob .where{font-size:13.5px;color:var(--sub);margin-top:6px;line-height:1.6}
  .cnt{display:inline-block;background:var(--accent);color:#fff;font-size:11px;font-weight:800;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  @media (max-width:560px){ table{font-size:13.5px} th,td{padding:7px 6px} .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))} }
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] section.card{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .mob{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .chip{background:#22252B}
  [data-theme="dark"] .mob .islot{background:#26292F}
  [data-theme="dark"] td{border-bottom-color:var(--line)}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}
  .tscroll-hint{display:block;text-align:right;font-size:11px;color:var(--sub);margin-bottom:4px}

  .gtable th{background:#F3EDE2;border-bottom:2px solid var(--line)}
  .gtable tbody tr:nth-child(even){background:#FAF6EE}
  .gtable tbody tr:hover{background:#F1E8D8}
  [data-theme="dark"] .gtable th{background:#2A251C}
  [data-theme="dark"] .gtable tbody tr:nth-child(even){background:#211D16}
  [data-theme="dark"] .gtable tbody tr:hover{background:#2E2820}
"""
CSS_LIVE3 = """
  :root{--bg:#faf9f6;--card:#ffffff;--line:#e6e1d8;--text:#1f1c18;--sub:#6f6a5e;--accent:#FF7E36;--accent-dark:#C25700;--accent-soft:#FFF1E8;--unknown:#6b6250}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:"Pretendard",-apple-system,BlinkMacSystemFont,"Malgun Gothic","Apple SD Gothic Neo",sans-serif;letter-spacing:-0.025em;line-height:1.7;padding:0 16px 48px}
  button,input,select,textarea{font-family:inherit}
  .wrap{max-width:1280px;margin:0 auto}
  .gnb{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px 10px;padding:14px 6px;background:rgba(250,249,246,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
  .gnb .logo{font-size:20px;font-weight:800;color:var(--text);text-decoration:none}
  .gnb nav{display:flex;flex-wrap:wrap;justify-content:flex-end;row-gap:2px}
  .gnb nav a{color:var(--sub);text-decoration:none;font-size:15px;font-weight:600;margin-left:14px;white-space:nowrap}
  @media (max-width:560px){ .gnb .logo{font-size:18px} .gnb nav a{font-size:14px;margin-left:10px} }
  .gnb nav a{display:inline-flex;align-items:center;min-height:44px}
  @media (max-width:768px){.gnb{flex-wrap:nowrap}.gnb nav{flex-wrap:nowrap;overflow-x:auto;flex:1 1 auto;min-width:0;justify-content:flex-start;scrollbar-width:none;-webkit-mask-image:linear-gradient(to right,#000 92%,transparent);mask-image:linear-gradient(to right,#000 92%,transparent)}.gnb nav::-webkit-scrollbar{display:none}}
  .gnb nav a.on{color:var(--accent-dark)}
  .intro{text-align:center;padding:28px 0 16px}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .disc{background:var(--accent-soft);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:14px;color:var(--text);margin-top:16px;text-align:center}
  section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 3px rgba(30,25,15,.05);padding:20px 22px;margin-top:14px}
  h2{font-size:18px;font-weight:700;margin-bottom:10px}
  p.body{font-size:16px;margin-bottom:8px}
  .legend{font-size:13px;color:var(--sub);margin-top:10px}
  table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;margin-top:6px}
  th{background:var(--accent-soft);color:var(--accent-dark);font-weight:800;text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
  td{padding:8px 10px;border-bottom:1px solid #f0ece3;vertical-align:top}
  tr:last-child td{border-bottom:none}
  td.num, th.num{text-align:right;white-space:nowrap}
  .mname{font-weight:700}
  .men{display:block;font-size:12.5px;color:var(--sub);font-weight:600}
  .chip{display:inline-block;background:#f7f3ec;border:1px solid var(--line);border-radius:999px;padding:1px 9px;font-size:13.5px;margin:1px 2px 1px 0}
  .chip b{color:var(--accent-dark)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:6px}
  .mob{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(30,25,15,.05)}
  .mob .islot{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:#F3F4F6;border-radius:6px;margin:0 auto 6px}
  .mob .mimg{max-width:32px;max-height:32px}
  .mob .nm{font-size:15px;font-weight:700}
  .mob .en{font-size:12.5px;color:var(--sub);font-weight:600}
  .mob .stat{font-size:14px;line-height:1.5;margin-top:6px}
  .mob .stat b{color:var(--accent-dark)}
  .mob .where{font-size:13.5px;color:var(--sub);margin-top:6px;line-height:1.6}
  .cnt{display:inline-block;background:var(--accent);color:#fff;font-size:11px;font-weight:800;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  @media (max-width:560px){ table{font-size:13.5px} th,td{padding:7px 6px} .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))} }
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] section.card{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .mob{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .chip{background:#22252B}
  [data-theme="dark"] .mob .islot{background:#26292F}
  [data-theme="dark"] td{border-bottom-color:var(--line)}

  .new-dot{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}
  .new-dot.on{display:inline-block}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .gtable th{background:#F3EDE2;border-bottom:2px solid var(--line)}
  .gtable tbody tr:nth-child(even){background:#FAF6EE}
  .gtable tbody tr:hover{background:#F1E8D8}
  [data-theme="dark"] .gtable th{background:#2A251C}
  [data-theme="dark"] .gtable tbody tr:nth-child(even){background:#211D16}
  [data-theme="dark"] .gtable tbody tr:hover{background:#2E2820}
.glink{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:700;color:var(--sub);text-decoration:none;margin:2px 4px 2px 0;background:var(--card)}
.glink:hover{color:var(--ink)}
"""
CSS_LUDI = """
  :root{--bg:#faf9f6;--card:#ffffff;--line:#e6e1d8;--text:#1f1c18;--sub:#6f6a5e;--accent:#FF7E36;--accent-dark:#C25700;--accent-soft:#FFF1E8;--unknown:#6b6250}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:"Pretendard",-apple-system,BlinkMacSystemFont,"Malgun Gothic","Apple SD Gothic Neo",sans-serif;letter-spacing:-0.025em;line-height:1.7;padding:0 16px 48px}
  button,input,select,textarea{font-family:inherit}
  .wrap{max-width:1280px;margin:0 auto}
  .gnb{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px 10px;padding:14px 6px;background:rgba(250,249,246,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
  .gnb .logo{font-size:20px;font-weight:800;color:var(--text);text-decoration:none}
  .gnb nav{display:flex;flex-wrap:wrap;justify-content:flex-end;row-gap:2px}
  .gnb nav a{color:var(--sub);text-decoration:none;font-size:15px;font-weight:600;margin-left:14px;white-space:nowrap}
  @media (max-width:560px){ .gnb .logo{font-size:18px} .gnb nav a{font-size:14px;margin-left:10px} }
  .gnb nav a{display:inline-flex;align-items:center;min-height:44px}
  @media (max-width:768px){.gnb{flex-wrap:nowrap}.gnb nav{flex-wrap:nowrap;overflow-x:auto;flex:1 1 auto;min-width:0;justify-content:flex-start;scrollbar-width:none;-webkit-mask-image:linear-gradient(to right,#000 92%,transparent);mask-image:linear-gradient(to right,#000 92%,transparent)}.gnb nav::-webkit-scrollbar{display:none}}
  .gnb nav a.on{color:var(--accent-dark)}
  .intro{text-align:center;padding:28px 0 16px}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .disc{background:var(--accent-soft);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:14px;color:var(--text);margin-top:16px;text-align:center}
  section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 3px rgba(30,25,15,.05);padding:20px 22px;margin-top:14px}
  h2{font-size:18px;font-weight:700;margin-bottom:10px}
  p.body{font-size:16px;margin-bottom:8px}
  .legend{font-size:13px;color:var(--sub);margin-top:10px}
  table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5;margin-top:6px}
  th{background:var(--accent-soft);color:var(--accent-dark);font-weight:800;text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
  td{padding:8px 10px;border-bottom:1px solid #f0ece3;vertical-align:top}
  tr:last-child td{border-bottom:none}
  td.num, th.num{text-align:right;white-space:nowrap}
  .mname{font-weight:700}
  .men{display:block;font-size:12.5px;color:var(--sub);font-weight:600}
  .chip{display:inline-block;background:#f7f3ec;border:1px solid var(--line);border-radius:999px;padding:1px 9px;font-size:13.5px;margin:1px 2px 1px 0}
  .chip b{color:var(--accent-dark)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:6px}
  .mob{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(30,25,15,.05)}
  .mob .islot{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:#F3F4F6;border-radius:6px;margin:0 auto 6px}
  .mob .mimg{max-width:32px;max-height:32px}
  .mob .nm{font-size:15px;font-weight:700}
  .mob .en{font-size:12.5px;color:var(--sub);font-weight:600}
  .mob .stat{font-size:14px;line-height:1.5;margin-top:6px}
  .mob .stat b{color:var(--accent-dark)}
  .mob .where{font-size:13.5px;color:var(--sub);margin-top:6px;line-height:1.6}
  .cnt{display:inline-block;background:var(--accent);color:#fff;font-size:11px;font-weight:800;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  @media (max-width:560px){ table{font-size:13.5px} th,td{padding:7px 6px} .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))} }
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] section.card{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .mob{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .chip{background:#22252B}
  [data-theme="dark"] .mob .islot{background:#26292F}
  [data-theme="dark"] td{border-bottom-color:var(--line)}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}
  .tscroll-hint{display:block;text-align:right;font-size:11px;color:var(--sub);margin-bottom:4px}

  .gtable th{background:#F3EDE2;border-bottom:2px solid var(--line)}
  .gtable tbody tr:nth-child(even){background:#FAF6EE}
  .gtable tbody tr:hover{background:#F1E8D8}
  [data-theme="dark"] .gtable th{background:#2A251C}
  [data-theme="dark"] .gtable tbody tr:nth-child(even){background:#211D16}
  [data-theme="dark"] .gtable tbody tr:hover{background:#2E2820}

  .new-dot{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}
  .new-dot.on{display:inline-block}
.glink{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:700;color:var(--sub);text-decoration:none;margin:2px 4px 2px 0;background:var(--card)}
.glink:hover{color:var(--ink)}
"""
# CSS_LUDI: ludibrium 라이브 세대 (라이브3 순서 + tscroll 포함 · </style> 앞 glink 분리형)
# CSS_LIVE3: hunting · edelstein · orbis 라이브 세대 (tscroll 없음 · glink 말미 · .new-dot 포함)


# 지역 서사 섹션 상수 (2026-11-05 게재)
# ---------- 지역 서사 5섹션 (2026-11-07 이식 층 흡수) ----------
NARR_ELINIA = """<section class="card">
<h2>지역 이야기 · 엘리니아</h2>
<p class="body">본진 GMS 95의 엘리니아에는 Arwen과 Rowen 같은 요정들이 등장해요. 퀘스트 서술에서도 두 인물을 엘리니아의 요정으로 소개해요. Rowen은 숲 깊은 곳의 좀비루팡이 마을의 안전을 위협한다고 말하며, 관련 퀘스트에는 좀비루팡을 물리치는 이야기가 나와요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""
NARR_KERNING = """<section class="card">
<h2>지역 이야기 · 커닝시티</h2>
<p class="body">본진 GMS 95의 커닝시티에서는 Nella가 주민들에게서 받은 여러 요청을 전해요. Nella는 요청이 많아 일손이 필요하다고 말하고, 퀘스트 서술에서도 일을 찾으려면 Nella를 만나보라고 안내해요. 뒷골목의 제이엠는 커닝시티가 위험한 거래에 알맞은 곳이라고 말하고, Matthias는 뒷골목에 온갖 정보가 떠돈다고 말해요. 한편 Icarus는 건물 위에서 하늘을 바라보며 언젠가 날고 싶다는 바람을 드러내요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""
NARR_LISHANG = """<section class="card">
<h2>지역 이야기 · 리스항</h2>
<p class="body">본진 GMS 95의 리스항에는 선원과 어부로 소개되는 인물들이 등장해요. 퀘스트 서술에서는 Teo를 빅토리아호의 선원으로, John을 어부로 소개해요. Teo는 아름다운 해안을 따라 항해하는 삶이 최고라고 말해요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""
NARR_SLEEPY = """<section class="card">
<h2>지역 이야기 · 슬리피우드</h2>
<p class="body">본진 GMS 95의 슬리피우드에는 호텔과 사우나가 등장해요. 퀘스트 서술에서도 슬리피우드 호텔 앞과 VIP 사우나를 언급해요. 약초 상인 Sabitrama는 이 숲에 약초가 많고 새 약초를 찾는 일이 기쁘다고 말해요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
<h3>지역 이야기 · 발록 사원</h3>
<p class="body">본진 GMS 95의 발록 사원 관련 게임 텍스트에서는 수십 년 전 Tristan이 봉인한 Balrog의 이야기를 다뤄요. 퀘스트 서술에서는 Balrog가 다시 나타나려 한다는 소식과 함께, 이를 막으려는 원정대 이야기가 나와요. 만지의 제자 Mu Young은 사원에 머물며 Balrog의 부활을 반드시 막아야 한다고 말해요. 퀘스트 서술에는 Tristan의 영혼이 Balrog의 부활을 막아내면 그 이를 후계자로 인정하겠다는 이야기도 나와요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""
NARR_PERION = """<section class="card">
<h2>지역 이야기 · 페리온</h2>
<p class="body">본진 GMS 95의 페리온에는 무엇이든 만들 수 있다고 말하는 Mr. Thunder와, 그의 제자라고 자신을 소개하는 Mr. Smith가 등장해요. Mr. Smith는 만들 것이 있으면 자신을 찾아오라고 말해요. Blackbull은 가족이 늘어 집을 넓혀야 한다고 말하고, 퀘스트 서술에서는 사촌들이 페리온으로 이사 올 예정이라 새집을 짓는다는 이야기가 나와요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""

NARR_MUSHROOM = """<section class="card">
    <h2>지역 이야기 · 버섯신사</h2>
    <p class="body">본진 GMS 95의 버섯신사 관련 게임 텍스트에서는 신사의 작은 제단을 돌보는 Kino Konoko가 등장해요. 퀘스트 서술에서는 그녀가 신사에 거주하는 인물로 소개되고, 신사 청소와 벚꽃을 훼손하는 까마귀 이야기가 나와요. Kino Konoko는 신사가 늘 봄이라고 말해요. 당고를 만드는 인물이 등장하고, 다른 인물들은 타코야키와 국수 이야기를 해요. 퀘스트 서술에서는 음식 노점과 식당들이 불너구리의 습격으로 곤란을 겪는 이야기가 나와요.</p>
    <p class="body">이 소개는 maplestory.io를 경유한 본진 GMS 95 게임 텍스트와 정본에 수록된 퀘스트 9493의 한글 서술을 바탕으로 정리했어요. 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">버섯신사에서 만나는 몬스터와 맵은 <a href="/mobs/">몬스터 도감</a> · <a href="/maps/">맵 도감</a>에서 이어서 볼 수 있어요.</p>
</section>"""


ORBIS_SCOPE_NOTE = """
  <section class="card">
    <p class="body">이 페이지에는 오르비스 · 리프레의 몬스터와 함께, 오르비스 권역의 설원 마을 엘나스의 이야기도 실었어요.</p>
  </section>
"""

TRANSFER_NOTE_ELNATH = """
  <section class="card">
    <p class="body">엘나스 이야기는 <a href="/guide/orbis-leafre/">오르비스 · 리프레 가이드</a>로 옮겼어요.</p>
  </section>
"""
TRANSFER_NOTE_MUSHROOM = """
  <section class="card">
    <p class="body">버섯신사 이야기는 <a href="/guide/mushroom-shrine/">버섯신사 가이드</a>로 옮겼어요.</p>
  </section>
"""

NARR_MURUNG = """
  <section class="card">
    <h2>지역 이야기 · 무릉</h2>
    <p class="body">본진 GMS 95의 무릉 관련 게임 텍스트에는 수련 도장이 등장해요. 퀘스트 서술에서 Do Gong은 무릉의 정신 수련 책임자로, No Gong은 신체 트레이너로 소개돼요. So Gong은 무릉 도장에서 수련한다고 말하고, Do Gong은 이곳까지 찾아온 이들을 가르친다고 말해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">무릉에서 만나는 몬스터와 맵은 <a href="/mobs/">몬스터 도감</a> · <a href="/maps/">맵 도감</a>에서 이어서 볼 수 있어요.</p>
</section>"""
NARR_BAEKCHO = """
  <section class="card">
    <h2>지역 이야기 · 백초해안</h2>
    <p class="body">본진 GMS 95의 백초해안 관련 게임 텍스트에서는 약초밭을 가꾸는 Mr. Ku가 등장해요. 퀘스트 서술에서는 그의 약초밭에 도둑이 들고 몬스터가 침입해 곤란을 겪는 이야기가 나와요. Captain Hwang은 이 마을을 지키기 위해 붉은코 해적단과 싸워야 할지도 모른다고 말해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">백초해안은 무릉과 이어지는 약초 마을이에요. 무릉 이야기는 바로 위 무릉 섹션에서 볼 수 있어요.</p>
</section>"""
NARR_AQUA = """
  <section class="card">
    <h2>지역 이야기 · 아쿠아리움</h2>
    <p class="body">본진 GMS 95의 아쿠아리움 관련 게임 텍스트에는 동물원 조련사 Kenta가 등장해요. Kenta는 동물에게 먹이를 주지 말라고 안내해요. 퀘스트 서술에서는 폭풍 이후 동물들의 이상 행동을 걱정하는 모습과, 몬스터를 길들이는 방법을 연구하는 이야기가 나와요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">아쿠아리움에서 만나는 몬스터와 맵은 <a href="/mobs/">몬스터 도감</a> · <a href="/maps/">맵 도감</a>에서 이어서 볼 수 있어요.</p>
</section>"""
NARR_NAUTILUS = """
  <section class="card">
    <h2>지역 이야기 · 노틸러스</h2>
    <p class="body">본진 GMS 95의 노틸러스는 해적 선장 카이린이 이끄는 배예요. 퀘스트 서술에서는 카이린을 노틸러스의 선장으로 소개하고, 해적이 되려면 노틸러스의 카이린을 찾아가라고 안내해요. 카이린은 노틸러스에 온 것을 환영한다고 말해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">해적이 되는 길과 해적 스킬은 <a href="/jobs/">직업·스킬 도감</a>에서 이어서 볼 수 있어요.</p>
</section>"""
NARR_OMEGA = """
  <section class="card">
    <h2>지역 이야기 · 지구방위본부</h2>
    <p class="body">본진 GMS 95의 지구방위본부(오메가 섹터)는 외계인의 공격에 대비하는 곳이에요. General Maestro는 외계인이 언제든 공격할 수 있으니 조심하라고 말하고, 자기 군대가 이곳을 지키고 있다고 말해요. Rice the Medic은 외계인 공격에 대비해 부상자를 돌본다고 말해요. 한편 Dr. Kim은 이 설계도로 가장 튼튼한 로봇을 만들 수 있다고 말하고, Porter는 본부에서 새 로봇 개발을 돕고 있다고 말해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">지구방위본부는 루디브리엄 권역의 공간이에요. 루디브리엄 이야기는 이 페이지의 루디브리엄 섹션에서 볼 수 있어요.</p>
</section>"""

GUIDE_LINKS = [("/guide/hunting/", "초반 사냥터 후보 비교"), ("/guide/orbis-leafre/", "오르비스 & 리프레 몬스터 구경"), ("/guide/edelstein/", "에델슈타인 엿보기"), ("/guide/ludibrium/", "루디브리엄 마을 가이드"), ("/guide/mushroom-shrine/", "버섯신사 엿보기"), ("/guide/scroll-reward-quests/", "주문서 주는 퀘스트 총정리"), ("/guide/return-routes/", "귀환 연결로 읽는 이동 절약법"), ("/guide/hunting-efficiency/", "사냥터 효율 읽는 법")]

def guide_links(path):
    items = "".join(f'<a class="glink" href="{p}">{t}</a>' for p, t in GUIDE_LINKS if p != path)
    return f'''  <section class="card glinks">
    <h2>다른 가이드 보기</h2>
    <div class="glink-row">{items}</div>
  </section>'''

def page(title, desc, path, h1a, h1b, tag, body, css=None, foot_full=None, no_i18n_alt=False):
    body = body + "\n" + guide_links(path)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 알팡지지</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://alpang.gg{path}">
<link rel="alternate" hreflang="ko" href="https://alpang.gg{path}">
{f'<link rel="alternate" hreflang="zh-TW" href="https://alpang.gg/taiwan{path}">' if not no_i18n_alt else ''}
{f'<link rel="alternate" hreflang="vi" href="https://alpang.gg/vietnam{path}">' if not no_i18n_alt else ''}
<link rel="alternate" hreflang="x-default" href="https://alpang.gg{path}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="{title} — 알팡지지">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://alpang.gg{path}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://alpang.gg/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{THEME_INIT}
<style>{css if css is not None else CSS + NEW_DOT_CSS}</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>
<body>
<div class="wrap">
  <div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a><nav><a href="/">홈</a><a href="/timeline/">타임라인<span class="new-dot" id="tlNewDot" aria-label="새 글 있음"></span></a><a href="/faq/">FAQ</a><a href="/mobs/">몬스터 도감</a><a href="/maps/">맵 탐색</a><a href="/items/">아이템</a><a href="/npcs/">NPC·퀘스트</a><a href="/jobs/">직업·스킬</a><a href="/calculator/cube/">큐브값 계산기</a><a href="/calculator/onehit/">한방컷 계산기</a></nav>{THEME_BTN}</div>
  <div class="intro">
    <h1>{h1a} <span>{h1b}</span></h1>
    <div class="tag">{tag}</div>
  </div>
  <div class="disc">⚠️ {DISCLAIMER}</div>
  <p class="hub-link" style="text-align:center;margin:12px 0 0"><a href="/guide/">가이드 전체 보기 →</a></p>
{body}
  <footer>{foot_full if foot_full is not None else "\n    " + FOOT + "\n  "}</footer>
</div>
{THEME_SCRIPT}
<script src="/assets/hit.js?v=2" defer></script>
<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>
</body>
</html>"""

def mob_chips(map_id):
    rs = sorted(map_mobs[map_id], key=lambda r: (mobs[r["mob_id"]].get("level") or 0, dname(mobs[r["mob_id"]])))
    out = ""
    for r in rs:
        mb = mobs[r["mob_id"]]
        out += f'<span class="chip">{esc(dname(mb))} <b>Lv.{mb.get("level")}</b></span>'
    return out

def mob_group_count(mob_ids):
    return len({dname(mobs[i]) for i in mob_ids})
DUP_NOTE = "같은 이름으로 등록된 개체가 2종 있어요. 이름이 같아도 서로 다른 몬스터예요."
COUNT_NOTE = "종수는 데이터에 등록된 개체 기준이에요. 같은 이름의 개체가 여럿인 경우도 각각 셉니다."
NEWT_EXP_NOTE = "일부 개체의 경험치는 원본 자료에서 확인되지 않아 비워 두었어요."

def _stat_key(mb):
    return (mb.get("level"), mb.get("maxHP"), mb.get("exp"))

def mob_cards(mob_ids, region_map_ids=None):
    # 동일명 병합은 스탯(레벨·HP·경험치)까지 전부 같은 쌍으로 한정한다 (후보 4 확정본 2026-11-13).
    # 스탯이 갈리는 동일명 쌍(뉴트주니어 등)은 카드를 나눈다.
    groups = {}
    singles = []
    by_name = {}
    for mid in mob_ids:
        by_name.setdefault(dname(mobs[mid]), []).append(mid)
    for name, ids in by_name.items():
        if len(ids) > 1 and len({_stat_key(mobs[i]) for i in ids}) == 1:
            groups[name] = ids
        elif len(ids) > 1:
            for i in ids:
                groups[dname(mobs[i]) + "#" + str(i)] = [i]
        else:
            groups[name] = ids
    cards = ""
    def gkey(item):
        key, ids = item
        rep = mobs[ids[0]]
        return (rep.get("level") or 0, dname(rep))
    for name, ids in sorted(groups.items(), key=gkey):
        mb = mobs[ids[0]]
        where_ids = set()
        for mid in ids:
            for r in mob_maps[mid]:
                if region_map_ids is None or r["map_id"] in region_map_ids:
                    where_ids.add(r["map_id"])
        names = []
        for map_id in sorted(where_ids, key=lambda i: dname(maps[i])):
            nm = esc(dname(maps[map_id]))
            if nm not in names:
                names.append(nm)
        shown = " · ".join(names[:4])
        if len(names) > 4:
            shown += f" 외 {len(names) - 4}곳"
        en = f'<div class="en">{esc(mb["name_en"])}</div>' if mb.get("name_ko_candidate") and mb["name_en"] != mb["name_ko_candidate"] else ""
        rep_id = ids[0]
        img = f'<span class="islot"><img class="mimg" src="https://maplestory.io/api/GMS/95/mob/{rep_id}/icon" alt="" loading="lazy" onerror="this.style.display=\'none\'" style="max-width:32px;max-height:32px"></span>'
        dup = ""
        if len(ids) > 1:
            dup = f'<div class="stat">ID {(" · ".join(str(i) for i in ids))}</div><div class="where">{DUP_NOTE}</div>'
        elif "#" in name:
            dup = f'<div class="where">{DUP_NOTE}</div>'
        cards += f"""<div class="mob">{img}<div class="nm">{esc(dname(mb))}</div>{en}<div class="stat">레벨 <b>{mb.get("level")}</b> · HP <b>{mb.get("maxHP"):,}</b></div><div class="where">출현: {shown}</div>{dup}</div>\n"""
    return cards


# ---------- 1. 초반 사냥터 후보 비교 (빅토리아 아일랜드 본토: 맵 ID 100~105 대역) ----------
vic = [m for m in maps.values() if 100000000 <= m["id"] < 110000000 and m["id"] in map_mobs]
# ---------- 가는 법 소섹션 (원고 v2, 2026-11-13 게재) ----------
# 행 데이터: 앵커 ID 대조표 확정본 기준 (출발 ID, 도착 ID). 화면 표기는 원고 표기.
ROUTE_NOTICE = "아래 연결은 본진 GMS 95 원본 데이터에 목적지 맵이 기록된 경우만 정리한 거예요. 원본에 기록이 있다는 뜻이지, 실제로 그 길로 이동할 수 있는지를 확인한 건 아니에요. 알팡 실서버의 연결은 이와 다를 수 있고, 실서버에서는 아직 확인되지 않았어요."
ROUTE_CLOSE = "수집 범위 밖의 맵으로 이어지는 기록은 목적지 상세를 확인할 수 없어 보류 상태로 두고 이 표에서 뺐어요. 일부 연결은 도착 포털의 이름이 확인되지 않아 추가 진단이 필요한 상태라, 도착 지점을 단정하지 않고 확정 경로로 다루지 않았어요. 맵 안에서 움직이는 출구는 이 표에 넣지 않았어요."
ROUTE_ONEDIR = "표에 있는 연결은 전부 한쪽 방향만 기록돼 있어요. 반대 방향 기록이 없다는 건 돌아오는 길이 없다는 뜻이 아니라, 기록으로 확인되지 않았다는 뜻이에요."

def _route_rows(pairs):
    out = ""
    for a, b in pairs:
        out += f'<tr><td><a href="/maps/#map-{a}">{esc(dname(maps[a]))}</a></td><td><a href="/maps/#map-{b}">{esc(dname(maps[b]))}</a></td><td>이 방향만 기록됨</td></tr>\n'
    return out

def route_section(title, intro_paras, tables, onedir=None):
    tbl = ""
    for label, pairs in tables:
        if label:
            tbl += f'<p class="body">{label}</p>\n'
        tbl += f"""<div class="twrap"><table class="gtable">
      <tr><th>출발 맵</th><th>도착 맵</th><th>방향 기록</th></tr>
{_route_rows(pairs)}    </table></div>\n"""
    paras = "".join(f'<p class="body">{p}</p>\n' for p in intro_paras)
    return f"""<section class="card">
    <h2>{title}</h2>
    <p class="body">{ROUTE_NOTICE}</p>
{paras}{tbl}    <p class="body">{onedir or ROUTE_ONEDIR}</p>
    <p class="body">{ROUTE_CLOSE}</p>
  </section>
"""


# ---------- 가는 법 — 루디브리엄 (원고 초안 QA 통과, 2026-11-13 게재) ----------
def _route_rows_dir(pairs):
    out = ""
    for a, b, both in pairs:
        label = "양쪽 방향 다 기록됨" if both else "이 방향만 기록됨"
        out += f'<tr><td><a href="/maps/#map-{a}">{esc(dname(maps[a]))}</a></td><td><a href="/maps/#map-{b}">{esc(dname(maps[b]))}</a></td><td>{label}</td></tr>\n'
    return out

def route_section_ludi():
    groups = [
        ("마을 · 공장과 시간의 길", [(220000000,220000005,0),(220000300,220000304,0),(220010800,220010900,0),(220030100,220030200,0),(220030300,220030400,0),(220040200,220050100,0),(220050100,220050200,0),(220060000,220060100,0),(220060200,220060300,0),(220070000,220070100,0)]),
        ("에오스 탑 · 핼리오스 탑", [(221020400,221020500,0),(221020500,221020600,0),(221020700,221020800,0),(221021900,221022000,0),(221022500,221022600,0),(221023100,221023200,1),(222020200,222020300,0)]),
        ("루디브리엄 미로", [(809050001,809050012,0),(809050002,809050013,0),(809050006,809050013,0),(809050007,809050014,0),(809050007,809050010,0),(809050008,809050011,0),(809050008,809050015,0),(809050010,809050013,0)]),
    ]
    tbl = ""
    for label, pairs in groups:
        tbl += f'<p class="body">{label}</p>\n<div class="twrap"><table class="gtable">\n      <tr><th>출발 맵</th><th>도착 맵</th><th>방향 기록</th></tr>\n{_route_rows_dir(pairs)}    </table></div>\n'
    return f"""<section class="card">
    <h2>가는 법 — 기록된 연결</h2>
    <p class="body">{ROUTE_NOTICE}</p>
    <p class="body">루디브리엄에서는 마을과 공장, 시간의 길 일대의 연결, 두 탑의 층 사이 연결, 미로 안 연결이 각각 확인돼요. 성격이 다른 길이라 나눠서 정리했어요.</p>
{tbl}    <p class="body">표에 있는 연결은 한 쌍만 빼고 전부 한쪽 방향만 기록돼 있어요. 반대 방향 기록이 없다는 건 돌아오는 길이 없다는 뜻이 아니라, 기록으로 확인되지 않았다는 뜻이에요.</p>
    <p class="body">{ROUTE_CLOSE}</p>
  </section>
"""

ROUTE_LUDI = route_section_ludi()

ROUTE_HUNTING = route_section("가는 법 — 기록된 연결",
    ["빅토리아 아일랜드 권역에서, 원본에 맵 사이 연결이 기록된 출발 맵은 세 곳이에요. 나머지 맵은 연결 기록 자체가 없어서 아래 표에 넣지 않았어요. 기록이 없다고 길이 없는 건 아니니, 없는 맵은 연결 미확인으로 봐주세요."],
    [("", [(105020000, 105010100), (105030500, 105030400), (105100000, 105030000)])], onedir="세 연결 다 반대 방향의 기록은 확인되지 않았어요. 거꾸로 돌아오는 길이 없다고 단정하는 게 아니라, 기록이 없다는 뜻이에요.")
ROUTE_ORBIS = route_section("가는 법 — 오르비스",
    ["오르비스에서는 정거장 연결 기록이 따로 확인돼요. 지역을 오가는 기록이라, 지역 안 이동과 나눠서 정리했어요.", "이 표에서 정거장 연결과 지역 안 연결의 구분은 출발 맵의 성격 기준이에요. 정거장·정거장통로 맵에서 출발하는 연결을 정거장 연결로 셌어요."],
    [("정거장 연결 기록:", [(200000111, 200000100), (200000121, 200000100), (200000161, 200000100), (200000151, 200000100), (200000170, 200000100), (200000140, 200000100), (200000150, 200000100), (200000130, 200000100), (200000130, 200000131)]),
     ("지역 안 연결 기록:", [(200000200, 200000000), (200010120, 200010100), (200010130, 200010131), (200050001, 200050000), (200080000, 200070000), (200080600, 200080700), (200081500, 200081400), (200081900, 200081800), (200081201, 200081200)])])
ROUTE_LEAFRE = route_section("가는 법 — 리프레", [],
    [("", [(240000100, 240000000), (240010100, 240010200), (240010700, 240010600), (240020000, 240010200), (240020100, 240020000), (240020100, 240020200)])])
ROUTE_EDEL = route_section("가는 법 — 기록된 연결", [],
    [("", [(310010200, 310010010), (310010400, 310010010), (310030310, 310030300), (931000420, 310000000), (931010020, 310000000)])])
def vic_general(m):
    # 일반 몹만: 9xxxxxx 대역은 분신·훈련·퀘스트/이벤트 특수 계열이라 정렬·범위 산정에서 제외 (2026-11-11 건1)
    # 단 수련장처럼 특수 몹만 있는 맵은 전 몹 기준으로 폴백해 표에서 지우지 않는다
    gen = [r for r in map_mobs[m["id"]] if r["mob_id"] < 9000000]
    return gen if gen else list(map_mobs[m["id"]])
def vic_key(m):
    rs = vic_general(m)
    lvls = [mobs[r["mob_id"]].get("level") or 0 for r in rs]
    main = max(rs, key=lambda r: r["placements"])
    return (sum(lvls) / len(lvls), mobs[main["mob_id"]].get("level") or 0, dname(m))
vic.sort(key=vic_key)
rows = ""
for m in vic:
    rs = map_mobs[m["id"]]
    grs = vic_general(m)
    lvls = [mobs[r["mob_id"]].get("level") or 0 for r in grs]
    total = sum(r["placements"] for r in rs)
    en = f'<span class="men">{esc(m["name_en"])}</span>' if m.get("name_ko_candidate") else ""
    rows += f"""<tr><td><span class="mname">{esc(dname(m))}</span>{en}</td><td>{mob_chips(m["id"])}</td><td class="num">{len(rs)}</td><td class="num">Lv.{min(lvls)}~{max(lvls)}</td><td class="num">{total}</td></tr>\n"""


# ---------- 가이드 확충 2차 (2026-11-13): 다음 지역 안내 + 큐브·잠재 안내 ----------
NEXT_REGION_NOTICE = '''<aside class="name-status" id="notice-next-region" data-component="next-region" data-scope="guide">
    <h2 class="sr-only">다음 지역 안내</h2>
    <p>이 표에 실린 사냥터의 몬스터는 Lv.64까지예요. 더 높은 레벨대의 몬스터를 찾는다면 <a href="/guide/orbis-leafre/">오르비스·리프레 가이드</a>도 함께 봐 주세요. 오르비스 몬스터는 Lv.35~66, 리프레 몬스터는 Lv.97~153이라 빅토리아와 겹치는 구간도 있어, 어느 지역이 맞는지는 레벨대에 따라 달라요. Lv.65~96 사이는 오르비스·리프레 두 지역 범위에서는 확인되지 않은 구간이에요.</p>
  </aside>'''
CUBE_GUIDE_NOTICE = '''<aside class="name-status" id="notice-cube-guide" data-component="cube-guide" data-scope="guide">
    <h2 class="sr-only">큐브·잠재능력 안내</h2>
    <p><strong>알팡서버에도 큐브와 잠재능력이 있나요?</strong></p>
    <p>제작진 발언으로 큐브 체계가 있다는 방향은 확인돼요. 팡이요는 레전드리 등급까지 있다고 언급하며, 후반 보스도 나중에 나올 수 있다는 방향으로 길게 가겠다고 했어요 (2026-10-28, TL-013). 다만 알팡서버의 큐브 확률은 아직 공시된 자료가 없어요. 이 사이트의 <a href="/calculator/cube/">큐브값 계산기</a>는 메이플플래닛이 공시한 확률을 기준으로 만든 체험 도구라, 알팡서버의 실제 확률과는 구분해서 봐 주세요. 알팡 기준 확률이 공시되면 그 기준으로 새로 정리할게요.</p>
  </aside>'''

# ---------- 분포 · 관련 퀘스트 복원 상수 (2026-11-07 역이식) ----------
# 온전 세대 게재분 (분포 5종 + 후속 2축 + 관련 퀘스트)을 빌더 상수로 고정한다.
# 원본: staging-final-merged-20261028 (hunting · edelstein) · deploy-20261030-1b (orbis)
DIST_HUNTING = '''<aside class="name-status" id="notice-distribution-attack-defense" data-component="distribution-attack-defense" data-scope="guide">
    <h2 class="sr-only">몬스터 공격·방어 분포</h2>
    <p>몬스터 175종의 원본 수치를 필드별로 구간 나눈 결과입니다. 물리 공격력은 100~499 구간이 85종으로 가장 많고 1,000 이상도 41종 있습니다. 마법 공격력은 값이 0인 종이 7종 있고 100~499 구간이 79종입니다. 물리 방어력은 1~99 구간 62종 · 100~499 구간 67종으로 나뉘고, 마법 방어력은 100~499 구간이 79종으로 가장 많습니다. 이 수치는 원본 기록을 구간으로 나눈 것으로, 몬스터의 강함을 매긴 순위가 아닙니다.</p>
  </aside>
  <aside class="name-status" id="notice-distribution-mob-level-range" data-component="distribution-mob-level-range" data-scope="guide">
    <h2 class="sr-only">맵별 출현 몬스터 레벨 범위 분포</h2>
    <p>몬스터가 출현하는 맵 245곳을 기준으로, 출현 몬스터의 레벨 범위를 세면 범위가 0인 맵(한 가지 레벨의 몬스터만 출현)이 195곳으로 대부분입니다. 범위가 1~5인 맵은 37곳, 6~10인 맵은 9곳, 11~20인 맵은 1곳, 21 이상인 맵은 3곳입니다.</p>
  </aside>
    <aside class="name-status" id="notice-distribution-npc-per-map" data-component="distribution-npc-per-map" data-scope="guide">
    <h2 class="sr-only">맵당 NPC 수 분포</h2>
    <p>맵 402곳을 기준으로, 각 맵에 배치된 NPC가 몇 명인지 셉니다. 배치 기록이 기준이라, NPC가 없다고 해서 마을이 아닌 맵이라는 뜻은 아니에요. NPC가 한 명도 없는 맵이 226곳으로 절반이 넘어요. NPC가 1명 있는 맵이 125곳, 2~3명 있는 맵이 32곳, 4~6명 있는 맵이 6곳, 7명 이상 모여 있는 맵이 13곳 있어, NPC가 있는 맵은 마을이나 거점처럼 사람이 모이는 자리에 몰려 있는 모양이에요.</p>
  </aside>
  <details class="name-status" id="notice-distribution-predecessor" data-component="distribution-predecessor" data-scope="guide">
    <summary>스킬 선행 관계 분포</summary>
    <p>선행 스킬이 있는 스킬 161개를 기준으로 보면, 선행 스킬이 1개인 스킬이 160개로 대부분이고 3개 이상인 스킬은 1개뿐입니다. 선행 스킬이 없는 스킬은 이 집계에 포함하지 않았습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-attr-badge" data-component="distribution-attr-badge" data-scope="guide">
    <summary>스킬 속성 배지 분포</summary>
    <p>속성 코드가 기록된 스킬 48종을 코드별로 보면 f 코드 22종, h 코드 9종, i 코드 8종, l 코드 7종, s 코드 2종입니다. 코드는 원본 데이터의 표기를 그대로 옮긴 것으로, 속성 이름으로 바꿔 표기하지 않습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-return-link" data-component="distribution-return-link" data-scope="guide">
    <summary>맵 귀환 연결 분포</summary>
    <p>귀환 목적지가 되는 맵 41곳을 기준으로, 각 목적지로 돌아오는 출발 맵 수를 세면 1곳에서만 돌아오는 목적지가 13곳, 2~5곳에서 돌아오는 목적지가 16곳, 6~10곳이 5곳, 11곳 이상이 7곳입니다. 귀환 연결이 기록된 맵 402곳의 귀환 연결을 목적지 쪽에서 다시 센 집계입니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-dialogue-length" data-component="distribution-dialogue-length" data-scope="guide">
    <summary>NPC 대사 길이 분포</summary>
    <p>대사가 확인된 NPC 1,234명을 기준으로, 한 NPC가 가진 서로 다른 대사 문장 수를 세면 문장 1개가 303명, 2~3개가 598명, 4~6개가 321명, 7~10개가 5명, 11개 이상이 7명입니다. 같은 문장이 반복되는 경우는 한 번으로 셌습니다.</p>
  </details>
  <aside class="name-status" id="notice-skill-predecessor-count" data-component="skill-predecessor-count" data-scope="guide">
    <p style="margin:0 0 6px"><strong>선행 스킬 개수 분포</strong></p>
    <p style="margin:0 0 6px">선행 스킬이 있는 스킬 161개를 기준으로, 배우기 전에 먼저 배워야 하는 스킬이 몇 개인지 셉니다. 선행 기록이 비어 있는 4건은 세지 않았어요.</p>
    <p style="margin:0 0 6px">선행 스킬이 1개인 스킬이 160개로 대부분이에요. 선행 스킬이 3개 이상인 스킬은 1개뿐이고, 2개인 스킬은 없어요. 배우기 전에 거쳐야 하는 단계가 길게 이어지는 구조보다는, 앞 스킬 하나를 배우면 열리는 구조가 대부분인 셈이에요.</p>
    <p style="margin:0">선행 1개 160개 · 2개 0개 · 3개 이상 1개 (기준 161개)</p>
  </aside>
  <aside class="name-status" id="notice-skill-attr-badge" data-component="skill-attr-badge" data-scope="guide">
    <p style="margin:0 0 6px"><strong>스킬 속성 배지 분포</strong></p>
    <p style="margin:0 0 6px">속성 배지가 붙은 스킬 48종만 기준으로, 배지에 적힌 코드별로 셉니다. 코드는 원본 표기 그대로예요. 코드가 어떤 속성을 뜻하는지는 확정된 자료가 없어, 이 안내에서는 코드에 속성 이름을 붙이지 않아요.</p>
    <p style="margin:0 0 6px">코드가 f인 스킬이 22종으로 가장 많고, h 9종 · i 8종 · l 7종 · s 2종이에요. 배지가 붙은 스킬 자체가 전체 스킬의 일부라, 배지가 없다는 것은 속성이 없다는 뜻이 아니에요 — 원본 기록에 배지가 없는 경우일 뿐이에요.</p>
    <p style="margin:0">코드 f 22종 · h 9종 · i 8종 · l 7종 · s 2종 (기준 48종)</p>
  </aside>
  <aside class="name-status" id="notice-mob-attack-defense" data-component="mob-attack-defense" data-scope="guide">
    <p style="margin:0 0 6px"><strong>몬스터 공격·방어 수치 분포</strong></p>
    <p style="margin:0 0 6px">몬스터 175종 가운데 해당 수치가 기록된 종만 기준으로, 물리·마법 공격과 물리·마법 방어 수치를 자릿수 구간별로 셉니다. 필드마다 기록된 종 수가 달라 기준 종 수도 필드마다 달라요. 수치는 원본 기록 그대로이며, 강하고 약함을 매긴 평가가 아니에요.</p>
    <p style="margin:0 0 6px">물리 공격은 100~499 구간이 85종으로 가장 두텁고, 1,000 이상인 종도 41종이에요. 마법 공격도 비슷한 모양으로 100~499 구간이 79종입니다. 방어는 두 필드 모두 100~499 구간이 중심이고, 물리 방어 1,000 이상은 1종뿐, 마법 방어는 1,000 이상인 종이 없어요. 수치가 0으로 기록된 종도 있어, 없는 값과 0인 값은 구분해서 봐야 해요.</p>
    <p style="margin:0">물리 공격 175종 — 0: 0 · 1~99: 38 · 100~499: 85 · 500~999: 11 · 1,000 이상: 41 / 마법 공격 175종 — 0: 7 · 1~99: 36 · 100~499: 79 · 500~999: 11 · 1,000 이상: 42 / 물리 방어 169종 — 0: 2 · 1~99: 62 · 100~499: 67 · 500~999: 37 · 1,000 이상: 1 / 마법 방어 170종 — 0: 1 · 1~99: 64 · 100~499: 79 · 500~999: 26 · 1,000 이상: 0</p>
  </aside>
  <aside class="name-status" id="notice-map-return-link" data-component="map-return-link" data-scope="guide">
    <p style="margin:0 0 6px"><strong>맵 귀환 연결 분포</strong></p>
    <p style="margin:0 0 6px">귀환 연결이 기록된 맵 402곳의 연결 402건을 기준으로, 귀환 목적지가 되는 맵 41곳을 '몇 개 맵이 여기로 돌아오는지'로 셉니다.</p>
    <p style="margin:0 0 6px">돌아오는 맵이 1곳뿐인 목적지가 13곳, 2~5곳인 목적지가 16곳으로 가장 많아요. 11곳 이상에서 돌아오는 목적지도 7곳 있어, 귀환이 소수 목적지에 몰리는 모양이에요. 목적지가 아닌 맵은 이 셈에 들어가지 않아요.</p>
    <p style="margin:0">피귀환 1곳 13곳 · 2~5곳 16곳 · 6~10곳 5곳 · 11곳 이상 7곳 (기준 목적지 41곳 · 연결 402건)</p>
  </aside>'''
DIST_EDEL_MAIN = '''<aside class="name-status" id="notice-distribution-attack-defense" data-component="distribution-attack-defense" data-scope="guide">
    <h2 class="sr-only">몬스터 공격·방어 분포</h2>
    <p>몬스터 175종의 원본 수치를 필드별로 구간 나눈 결과입니다. 물리 공격력은 100~499 구간이 85종으로 가장 많고 1,000 이상도 41종 있습니다. 마법 공격력은 값이 0인 종이 7종 있고 100~499 구간이 79종입니다. 물리 방어력은 1~99 구간 62종 · 100~499 구간 67종으로 나뉘고, 마법 방어력은 100~499 구간이 79종으로 가장 많습니다. 이 수치는 원본 기록을 구간으로 나눈 것으로, 몬스터의 강함을 매긴 순위가 아닙니다.</p>
  </aside>
  <details class="name-status" id="notice-distribution-predecessor" data-component="distribution-predecessor" data-scope="guide">
    <summary>스킬 선행 관계 분포</summary>
    <p>선행 스킬이 있는 스킬 161개를 기준으로 보면, 선행 스킬이 1개인 스킬이 160개로 대부분이고 3개 이상인 스킬은 1개뿐입니다. 선행 스킬이 없는 스킬은 이 집계에 포함하지 않았습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-attr-badge" data-component="distribution-attr-badge" data-scope="guide">
    <summary>스킬 속성 배지 분포</summary>
    <p>속성 코드가 기록된 스킬 48종을 코드별로 보면 f 코드 22종, h 코드 9종, i 코드 8종, l 코드 7종, s 코드 2종입니다. 코드는 원본 데이터의 표기를 그대로 옮긴 것으로, 속성 이름으로 바꿔 표기하지 않습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-dialogue-length" data-component="distribution-dialogue-length" data-scope="guide">
    <summary>NPC 대사 길이 분포</summary>
    <p>대사가 확인된 NPC 1,234명을 기준으로, 한 NPC가 가진 서로 다른 대사 문장 수를 세면 문장 1개가 303명, 2~3개가 598명, 4~6개가 321명, 7~10개가 5명, 11개 이상이 7명입니다. 같은 문장이 반복되는 경우는 한 번으로 셌습니다.</p>
  </details>
  <aside class="name-status" id="notice-skill-predecessor-count" data-component="skill-predecessor-count" data-scope="guide">
    <p style="margin:0 0 6px"><strong>선행 스킬 개수 분포</strong></p>
    <p style="margin:0 0 6px">선행 스킬이 있는 스킬 161개를 기준으로, 배우기 전에 먼저 배워야 하는 스킬이 몇 개인지 셉니다. 선행 기록이 비어 있는 4건은 세지 않았어요.</p>
    <p style="margin:0 0 6px">선행 스킬이 1개인 스킬이 160개로 대부분이에요. 선행 스킬이 3개 이상인 스킬은 1개뿐이고, 2개인 스킬은 없어요. 배우기 전에 거쳐야 하는 단계가 길게 이어지는 구조보다는, 앞 스킬 하나를 배우면 열리는 구조가 대부분인 셈이에요.</p>
    <p style="margin:0">선행 1개 160개 · 2개 0개 · 3개 이상 1개 (기준 161개)</p>
  </aside>
  <aside class="name-status" id="notice-skill-attr-badge" data-component="skill-attr-badge" data-scope="guide">
    <p style="margin:0 0 6px"><strong>스킬 속성 배지 분포</strong></p>
    <p style="margin:0 0 6px">속성 배지가 붙은 스킬 48종만 기준으로, 배지에 적힌 코드별로 셉니다. 코드는 원본 표기 그대로예요. 코드가 어떤 속성을 뜻하는지는 확정된 자료가 없어, 이 안내에서는 코드에 속성 이름을 붙이지 않아요.</p>
    <p style="margin:0 0 6px">코드가 f인 스킬이 22종으로 가장 많고, h 9종 · i 8종 · l 7종 · s 2종이에요. 배지가 붙은 스킬 자체가 전체 스킬의 일부라, 배지가 없다는 것은 속성이 없다는 뜻이 아니에요 — 원본 기록에 배지가 없는 경우일 뿐이에요.</p>
    <p style="margin:0">코드 f 22종 · h 9종 · i 8종 · l 7종 · s 2종 (기준 48종)</p>
  </aside>
  <aside class="name-status" id="notice-mob-attack-defense" data-component="mob-attack-defense" data-scope="guide">
    <p style="margin:0 0 6px"><strong>몬스터 공격·방어 수치 분포</strong></p>
    <p style="margin:0 0 6px">몬스터 175종 가운데 해당 수치가 기록된 종만 기준으로, 물리·마법 공격과 물리·마법 방어 수치를 자릿수 구간별로 셉니다. 필드마다 기록된 종 수가 달라 기준 종 수도 필드마다 달라요. 수치는 원본 기록 그대로이며, 강하고 약함을 매긴 평가가 아니에요.</p>
    <p style="margin:0 0 6px">물리 공격은 100~499 구간이 85종으로 가장 두텁고, 1,000 이상인 종도 41종이에요. 마법 공격도 비슷한 모양으로 100~499 구간이 79종입니다. 방어는 두 필드 모두 100~499 구간이 중심이고, 물리 방어 1,000 이상은 1종뿐, 마법 방어는 1,000 이상인 종이 없어요. 수치가 0으로 기록된 종도 있어, 없는 값과 0인 값은 구분해서 봐야 해요.</p>
    <p style="margin:0">물리 공격 175종 — 0: 0 · 1~99: 38 · 100~499: 85 · 500~999: 11 · 1,000 이상: 41 / 마법 공격 175종 — 0: 7 · 1~99: 36 · 100~499: 79 · 500~999: 11 · 1,000 이상: 42 / 물리 방어 169종 — 0: 2 · 1~99: 62 · 100~499: 67 · 500~999: 37 · 1,000 이상: 1 / 마법 방어 170종 — 0: 1 · 1~99: 64 · 100~499: 79 · 500~999: 26 · 1,000 이상: 0</p>
  </aside>
  <aside class="name-status" id="notice-map-return-link" data-component="map-return-link" data-scope="guide">
    <p style="margin:0 0 6px"><strong>맵 귀환 연결 분포</strong></p>
    <p style="margin:0 0 6px">귀환 연결이 기록된 맵 402곳의 연결 402건을 기준으로, 귀환 목적지가 되는 맵 41곳을 '몇 개 맵이 여기로 돌아오는지'로 셉니다.</p>
    <p style="margin:0 0 6px">돌아오는 맵이 1곳뿐인 목적지가 13곳, 2~5곳인 목적지가 16곳으로 가장 많아요. 11곳 이상에서 돌아오는 목적지도 7곳 있어, 귀환이 소수 목적지에 몰리는 모양이에요. 목적지가 아닌 맵은 이 셈에 들어가지 않아요.</p>
    <p style="margin:0">피귀환 1곳 13곳 · 2~5곳 16곳 · 6~10곳 5곳 · 11곳 이상 7곳 (기준 목적지 41곳 · 연결 402건)</p>
  </aside>'''
DIST_EDEL_RETURN = '''<details class="name-status" id="notice-distribution-return-link" data-component="distribution-return-link" data-scope="guide">
    <summary>맵 귀환 연결 분포</summary>
    <p>귀환 목적지가 되는 맵 41곳을 기준으로, 각 목적지로 돌아오는 출발 맵 수를 세면 1곳에서만 돌아오는 목적지가 13곳, 2~5곳에서 돌아오는 목적지가 16곳, 6~10곳이 5곳, 11곳 이상이 7곳입니다. 귀환 연결이 기록된 맵 402곳의 귀환 연결을 목적지 쪽에서 다시 센 집계입니다.</p>
  </details>'''
DIST_ORBIS = '''<aside class="name-status" id="notice-distribution-attack-defense" data-component="distribution-attack-defense" data-scope="guide">
    <h2 class="sr-only">몬스터 공격·방어 분포</h2>
    <p>몬스터 175종의 원본 수치를 필드별로 구간 나눈 결과입니다. 물리 공격력은 100~499 구간이 85종으로 가장 많고 1,000 이상도 41종 있습니다. 마법 공격력은 값이 0인 종이 7종 있고 100~499 구간이 79종입니다. 물리 방어력은 1~99 구간 62종 · 100~499 구간 67종으로 나뉘고, 마법 방어력은 100~499 구간이 79종으로 가장 많습니다. 이 수치는 원본 기록을 구간으로 나눈 것으로, 몬스터의 강함을 매긴 순위가 아닙니다.</p>
  </aside>
  <aside class="name-status" id="notice-distribution-return-link" data-component="distribution-return-link" data-scope="guide">
    <h2 class="sr-only">맵 귀환 연결 분포</h2>
    <p>귀환 목적지가 되는 맵 41곳을 기준으로, 각 목적지로 돌아오는 출발 맵 수를 세면 1곳에서만 돌아오는 목적지가 13곳, 2~5곳에서 돌아오는 목적지가 16곳, 6~10곳이 5곳, 11곳 이상이 7곳입니다. 귀환 연결이 기록된 맵 402곳의 귀환 연결을 목적지 쪽에서 다시 센 집계입니다.</p>
  </aside>
  <details class="name-status" id="notice-distribution-predecessor" data-component="distribution-predecessor" data-scope="guide">
    <summary>스킬 선행 관계 분포</summary>
    <p>선행 스킬이 있는 스킬 161개를 기준으로 보면, 선행 스킬이 1개인 스킬이 160개로 대부분이고 3개 이상인 스킬은 1개뿐입니다. 선행 스킬이 없는 스킬은 이 집계에 포함하지 않았습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-attr-badge" data-component="distribution-attr-badge" data-scope="guide">
    <summary>스킬 속성 배지 분포</summary>
    <p>속성 코드가 기록된 스킬 48종을 코드별로 보면 f 코드 22종, h 코드 9종, i 코드 8종, l 코드 7종, s 코드 2종입니다. 코드는 원본 데이터의 표기를 그대로 옮긴 것으로, 속성 이름으로 바꿔 표기하지 않습니다.</p>
  </details>
  <details class="name-status" id="notice-distribution-dialogue-length" data-component="distribution-dialogue-length" data-scope="guide">
    <summary>NPC 대사 길이 분포</summary>
    <p>대사가 확인된 NPC 1,234명을 기준으로, 한 NPC가 가진 서로 다른 대사 문장 수를 세면 문장 1개가 303명, 2~3개가 598명, 4~6개가 321명, 7~10개가 5명, 11개 이상이 7명입니다. 같은 문장이 반복되는 경우는 한 번으로 셌습니다.</p>
  </details>
  <aside class="name-status" id="notice-skill-predecessor-count" data-component="skill-predecessor-count" data-scope="guide">
    <p style="margin:0 0 6px"><strong>선행 스킬 개수 분포</strong></p>
    <p style="margin:0 0 6px">선행 스킬이 있는 스킬 161개를 기준으로, 배우기 전에 먼저 배워야 하는 스킬이 몇 개인지 셉니다. 선행 기록이 비어 있는 4건은 세지 않았어요.</p>
    <p style="margin:0 0 6px">선행 스킬이 1개인 스킬이 160개로 대부분이에요. 선행 스킬이 3개 이상인 스킬은 1개뿐이고, 2개인 스킬은 없어요. 배우기 전에 거쳐야 하는 단계가 길게 이어지는 구조보다는, 앞 스킬 하나를 배우면 열리는 구조가 대부분인 셈이에요.</p>
    <p style="margin:0">선행 1개 160개 · 2개 0개 · 3개 이상 1개 (기준 161개)</p>
  </aside>
  <aside class="name-status" id="notice-skill-attr-badge" data-component="skill-attr-badge" data-scope="guide">
    <p style="margin:0 0 6px"><strong>스킬 속성 배지 분포</strong></p>
    <p style="margin:0 0 6px">속성 배지가 붙은 스킬 48종만 기준으로, 배지에 적힌 코드별로 셉니다. 코드는 원본 표기 그대로예요. 코드가 어떤 속성을 뜻하는지는 확정된 자료가 없어, 이 안내에서는 코드에 속성 이름을 붙이지 않아요.</p>
    <p style="margin:0 0 6px">코드가 f인 스킬이 22종으로 가장 많고, h 9종 · i 8종 · l 7종 · s 2종이에요. 배지가 붙은 스킬 자체가 전체 스킬의 일부라, 배지가 없다는 것은 속성이 없다는 뜻이 아니에요 — 원본 기록에 배지가 없는 경우일 뿐이에요.</p>
    <p style="margin:0">코드 f 22종 · h 9종 · i 8종 · l 7종 · s 2종 (기준 48종)</p>
  </aside>
  <aside class="name-status" id="notice-mob-attack-defense" data-component="mob-attack-defense" data-scope="guide">
    <p style="margin:0 0 6px"><strong>몬스터 공격·방어 수치 분포</strong></p>
    <p style="margin:0 0 6px">몬스터 175종 가운데 해당 수치가 기록된 종만 기준으로, 물리·마법 공격과 물리·마법 방어 수치를 자릿수 구간별로 셉니다. 필드마다 기록된 종 수가 달라 기준 종 수도 필드마다 달라요. 수치는 원본 기록 그대로이며, 강하고 약함을 매긴 평가가 아니에요.</p>
    <p style="margin:0 0 6px">물리 공격은 100~499 구간이 85종으로 가장 두텁고, 1,000 이상인 종도 41종이에요. 마법 공격도 비슷한 모양으로 100~499 구간이 79종입니다. 방어는 두 필드 모두 100~499 구간이 중심이고, 물리 방어 1,000 이상은 1종뿐, 마법 방어는 1,000 이상인 종이 없어요. 수치가 0으로 기록된 종도 있어, 없는 값과 0인 값은 구분해서 봐야 해요.</p>
    <p style="margin:0">물리 공격 175종 — 0: 0 · 1~99: 38 · 100~499: 85 · 500~999: 11 · 1,000 이상: 41 / 마법 공격 175종 — 0: 7 · 1~99: 36 · 100~499: 79 · 500~999: 11 · 1,000 이상: 42 / 물리 방어 169종 — 0: 2 · 1~99: 62 · 100~499: 67 · 500~999: 37 · 1,000 이상: 1 / 마법 방어 170종 — 0: 1 · 1~99: 64 · 100~499: 79 · 500~999: 26 · 1,000 이상: 0</p>
  </aside>
  <aside class="name-status" id="notice-map-return-link" data-component="map-return-link" data-scope="guide">
    <p style="margin:0 0 6px"><strong>맵 귀환 연결 분포</strong></p>
    <p style="margin:0 0 6px">귀환 연결이 기록된 맵 402곳의 연결 402건을 기준으로, 귀환 목적지가 되는 맵 41곳을 '몇 개 맵이 여기로 돌아오는지'로 셉니다.</p>
    <p style="margin:0 0 6px">돌아오는 맵이 1곳뿐인 목적지가 13곳, 2~5곳인 목적지가 16곳으로 가장 많아요. 11곳 이상에서 돌아오는 목적지도 7곳 있어, 귀환이 소수 목적지에 몰리는 모양이에요. 목적지가 아닌 맵은 이 셈에 들어가지 않아요.</p>
    <p style="margin:0">피귀환 1곳 13곳 · 2~5곳 16곳 · 6~10곳 5곳 · 11곳 이상 7곳 (기준 목적지 41곳 · 연결 402건)</p>
  </aside>'''
RQ_ORBIS = '''<aside class="name-status" id="notice-region-quest-orbis" data-component="region-quest-link" data-scope="guide">
    <h2 class="sr-only">관련 퀘스트 — 오르비스</h2>
    <p>오르비스와 이어지는 퀘스트는 <a href="/npcs/">NPC·퀘스트 도감</a>에서 볼 수 있어요.</p>
    <p class="small">집계 기준 — 지표명은 &quot;수록 자료 기준, 해당 권역 전용 NPC가 시작 또는 완료 지점인 퀘스트 고유 ID 수&quot;입니다. 본진 메이플스토리 빅뱅 직후(GMS 95) 수록 자료에서 관측한 값으로, 실제 게임에서 제공·수행 가능한 퀘스트 수를 뜻하지 않습니다.</p>
  </aside>'''
RQ_LEAFRE = '''<aside class="name-status" id="notice-region-quest-leafre" data-component="region-quest-link" data-scope="guide">
    <h2 class="sr-only">관련 퀘스트 — 리프레</h2>
    <p>리프레와 이어지는 퀘스트는 <a href="/npcs/">NPC·퀘스트 도감</a>에서 볼 수 있어요.</p>
    <p class="small">집계 기준 — 지표명은 &quot;수록 자료 기준, 해당 권역 전용 NPC가 시작 또는 완료 지점인 퀘스트 고유 ID 수&quot;입니다. 본진 메이플스토리 빅뱅 직후(GMS 95) 수록 자료에서 관측한 값으로, 실제 게임에서 제공·수행 가능한 퀘스트 수를 뜻하지 않습니다.</p>
  </aside>'''

body1 = f"""
  <section class="card">
    <h2>빅토리아 아일랜드 초반 사냥터 후보<span class="cnt">{len(vic)}곳</span></h2>
    <p class="body">빅토리아 아일랜드 본토(헤네시스·엘리니아·페리온·커닝시티·리스항구·슬리피우드 일대) 맵 가운데 몬스터가 출현하는 맵을 모았습니다. 어느 곳이 가장 좋은지는 캐릭터와 장비에 따라 달라지므로 순위를 매기지 않고, 출현 몬스터와 배치 규모를 나란히 비교할 수 있게 정리했습니다. 출현 몬스터(특수·이벤트 몹 제외)의 평균 레벨이 낮은 맵부터 정렬했습니다.</p>
    <p class="body">본진 GMS 95의 헤네시스 퀘스트에는 밍밍부인이 마을 축제를 준비하는 모습이 담겨 있어요. 밍밍부인은 일손이 부족해 마을 밖 사람들의 도움이 필요하다고 말해요. 마을의 촌장은 장로 스탄이에요. 에반 관련 퀘스트에서 장로 스탄은 여러 마을 몬스터가 이상하게 행동한다는 소문을 들었다고 말하고, Bruce는 헤네시스 근처 주황버섯에게도 비슷한 일이 있었다고 전해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <div class="twrap"><table class="gtable">
      <tr><th>맵</th><th>출현 몬스터</th><th class="num">종류</th><th class="num">레벨 범위</th><th class="num">배치 총량</th></tr>
{rows}    </table></div>
    <p class="legend">배치 총량은 본진 기준 데이터에서 해당 맵에 배치된 몬스터 수의 합계입니다. 실제 사냥 효율은 리젠·지형·직업에 따라 달라질 수 있습니다. 한글 이름은 표시명 후보이며, 후보가 없는 맵은 영문명으로 표기했습니다.</p>
  </section>"""

ELNATH_SECTION = """
  <section class="card">
    <h2>지역 이야기 · 엘나스</h2>
    <p class="body">본진 GMS 95의 퀘스트 서술에서는 Gordon을 엘나스의 인물로 소개해요. Gordon은 이 마을에서 50년 넘게 신발을 만들어 왔다고 말해요. 다른 퀘스트에는 얼어붙은 엘나스의 들판으로 찾아가 Rene에게 책을 건네는 이야기가 나와요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
</section>"""

os.makedirs(f"{OUT}/hunting", exist_ok=True)
open(f"{OUT}/hunting/index.html", "w").write(page(
    "초반 사냥터 후보 비교", "빅토리아 아일랜드 초반 사냥터 후보를 출현 몬스터·레벨 범위·배치 규모로 비교합니다.",
    "/guide/hunting/", "초반 사냥터", "후보 비교", "어디서 사냥할지, 순위가 아니라 비교로 고르기", body1 + "\n  " + DIST_HUNTING + "\n  " + ROUTE_HUNTING + "\n  " + NEXT_REGION_NOTICE + "\n  " + CUBE_GUIDE_NOTICE + "\n" + NARR_ELINIA + "\n" + NARR_KERNING + "\n" + NARR_LISHANG + "\n" + NARR_SLEEPY + "\n" + NARR_PERION + TRANSFER_NOTE_ELNATH + NARR_NAUTILUS + "\n" + TRANSFER_NOTE_MUSHROOM, css=CSS_LIVE3 + "\n.twrap{overflow-x:auto;-webkit-overflow-scrolling:touch}\n.twrap>table{margin:0}\n", foot_full=FOOT_HUNTING))

# ---------- 가이드 확충 2차 (2026-11-13): 오르비스·리프레 출현 맵 표 ----------
def _map_rows(region_maps_sorted):
    out = ""
    for m in region_maps_sorted:
        rs = map_mobs[m["id"]]
        en = f'<span class="men">{esc(m["name_en"])}</span>' if m.get("name_ko_candidate") else ""
        out += f"""<tr><td><span class="mname">{esc(dname(m))}</span>{en}</td><td>{mob_chips(m["id"])}</td><td class="num">{len(rs)}</td></tr>\n"""
    return out

def _by_min_level(region):
    ms = [m for m in maps.values() if m["region"] == region and m["id"] in map_mobs]
    return sorted(ms, key=lambda m: (min((mobs[r["mob_id"]].get("level") or 0) for r in map_mobs[m["id"]]), m["id"]))

_orb_sorted = _by_min_level("Orbis")
_leaf_sorted = _by_min_level("Leafre")
ORBIS_MAP_TABLE = f'''<section class="card">
    <h2>몬스터가 출현하는 맵 — 오르비스<span class="cnt">{len(_orb_sorted)}곳</span></h2>
    <div class="twrap"><table class="gtable">
      <tr><th>맵</th><th>출현 몬스터</th><th class="num">종류</th></tr>
{_map_rows(_orb_sorted)}    </table></div>
  </section>
  <section class="card">
    <h2>몬스터가 출현하는 맵 — 리프레<span class="cnt">{len(_leaf_sorted)}곳</span></h2>
    <div class="twrap"><table class="gtable">
      <tr><th>맵</th><th>출현 몬스터</th><th class="num">종류</th></tr>
{_map_rows(_leaf_sorted)}    </table></div>
  </section>'''

# ---------- 2. 오르비스 & 리프레 몬스터 구경 ----------
orb_maps = {m["id"] for m in maps.values() if m["region"] == "Orbis"}
leaf_maps = {m["id"] for m in maps.values() if m["region"] == "Leafre"}
orb_mobs = {r["mob_id"] for mid in orb_maps for r in map_mobs.get(mid, [])}
orb_with_n = sum(1 for mid in orb_maps if mid in map_mobs)
orb_lv_min = min(mobs[i].get("level") or 0 for i in orb_mobs)
orb_lv_max = max(mobs[i].get("level") or 0 for i in orb_mobs)
leaf_with_n = sum(1 for mid in leaf_maps if mid in map_mobs)
leaf_mobs = {r["mob_id"] for mid in leaf_maps for r in map_mobs.get(mid, [])}
leaf_lv_min = min(mobs[i].get("level") or 0 for i in leaf_mobs)
leaf_lv_max = max(mobs[i].get("level") or 0 for i in leaf_mobs)
body2 = f"""
  <section class="card">
    <h2>오르비스 몬스터<span class="cnt">{mob_group_count(orb_mobs)}종</span></h2>
<p class="body">오르비스 전체 맵 {len(orb_maps)}곳 중, 몬스터가 나오는 맵 {orb_with_n}곳에 출현하는 몬스터를 정리했어요.</p>
    <p class="body">하늘 위 도시 오르비스 일대에 출현하는 몬스터입니다. 구름과 탑 주변을 지키는 몬스터들이 중심입니다.</p>
    <div class="grid">
{mob_cards(orb_mobs, orb_maps)}    </div>
  </section>
  {RQ_ORBIS}
  {ROUTE_ORBIS}
  <p class="body">오르비스 몬스터는 Lv.{orb_lv_min}~{orb_lv_max}, 리프레 몬스터는 Lv.{leaf_lv_min}~{leaf_lv_max}이에요. 그 사이 레벨대의 몬스터는 수집된 두 지역 범위에서는 확인되지 않았어요.</p>
<section class="card">
    <h2>리프레 몬스터<span class="cnt">{mob_group_count(leaf_mobs)}종</span></h2>
<p class="body">본진 GMS 95의 리프레는 하프링들이 사는 마을이에요. 촌장 Tatamo는 하프링이 평화와 사랑을 좋아한다고 말해요. Ito와 다른 주민들의 대사에는 아기 용의 알을 따뜻하게 지키거나 부화를 기다리는 이야기가 나와요. 리프레 정거장의 Corba는, 인간과 엘프는 잊었을지 몰라도 하프링은 시간의 신전을 둘러싼 초록빛 오로라를 기억한다고 말해요.</p>
<p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
<p class="body">리프레 전체 맵 {len(leaf_maps)}곳 중, 몬스터가 나오는 맵 {leaf_with_n}곳에 출현하는 몬스터를 정리했어요.</p>
    <p class="body">용의 숲 리프레 일대에 출현하는 몬스터입니다. 본진 기준 후반부 지역이라 전반적으로 레벨이 높습니다.</p>
    <div class="grid">
{mob_cards(leaf_mobs, leaf_maps)}    </div>
    <p class="legend">출현 맵은 해당 권역 안에서 확인된 맵만 표기했습니다. 레벨·HP는 본진 기준 수집 데이터입니다.<br>{COUNT_NOTE}<br>{NEWT_EXP_NOTE}<br>아이콘·이미지: maplestory.io</p>
  </section>
  {RQ_LEAFRE}
  {ROUTE_LEAFRE}
  {DIST_ORBIS}
  {ORBIS_MAP_TABLE}"""
os.makedirs(f"{OUT}/orbis-leafre", exist_ok=True)
open(f"{OUT}/orbis-leafre/index.html", "w").write(page(
    "오르비스 & 리프레 몬스터 구경", "오르비스와 리프레 일대에 출현하는 몬스터를 레벨·HP·출현 맵과 함께 소개합니다.",
    "/guide/orbis-leafre/", "오르비스 & 리프레", "몬스터 구경", "하늘 도시와 용의 숲에는 누가 살고 있을까", body2 + ORBIS_SCOPE_NOTE + NARR_MURUNG + NARR_BAEKCHO + NARR_AQUA + ELNATH_SECTION, css=CSS_LIVE3, foot_full=FOOT_ORBIS))


# ---------- 3. 에델슈타인 엿보기 ----------
ed_maps = sorted([m for m in maps.values() if m["region"] == "Edelstein-area"], key=lambda m: dname(m))
ed_with = [m for m in ed_maps if m["id"] in map_mobs]
ed_mobs = {r["mob_id"] for m in ed_with for r in map_mobs[m["id"]]}
rows3 = ""
for m in ed_with:
    rs = map_mobs[m["id"]]
    en = f'<span class="men">{esc(m["name_en"])}</span>' if m.get("name_ko_candidate") else ""
    rows3 += f"""<tr><td><span class="mname">{esc(dname(m))}</span>{en}</td><td>{mob_chips(m["id"])}</td><td class="num">{len(rs)}</td></tr>\n"""
ed_only = [m for m in ed_maps if m["id"] not in map_mobs]
town_names = " · ".join(esc(dname(m)) for m in ed_only)
ed_town_n = sum(1 for m in ed_only if m.get("isTown"))
ed_npconly_n = sum(1 for m in ed_only if not m.get("isTown") and m.get("npcs"))
ed_rest_n = len(ed_only) - ed_town_n - ed_npconly_n
ed_lv_min = min(mobs[i].get("level") or 0 for i in ed_mobs)
ed_lv_max = max(mobs[i].get("level") or 0 for i in ed_mobs)
body3 = f"""
  <section class="card">
    <h2>에델슈타인은 어떤 곳?</h2>
    <p class="body">에델슈타인은 빅뱅 이후 개편 시기에 추가된 지역으로, 블랙윙이 점거한 광산 도시를 배경으로 해요. 이 페이지에서는 수집된 에델슈타인 권역 맵 {len(ed_maps)}곳 가운데 몬스터가 출현하는 {len(ed_with)}곳과, 거기서 만날 수 있는 몬스터 {mob_group_count(ed_mobs)}종을 미리 엿봐요.</p>
    <p class="body">본진 GMS 95의 에델슈타인은 블랙윙이 마을을 차지한 상황으로 묘사돼요. 무기·방어구 상인 Bonjasky는 블랙윙이 마을을 점령하고 있는 동안 강력한 무기를 팔 수 없다고 말해요. 배틀메이지 교관 Brighton은 블랙윙을 몰아내고 자유를 되찾을 날까지 싸움이 계속될 거라고 말해요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
  </section>
  <section class="card">
    <h2>몬스터가 출현하는 맵<span class="cnt">{len(ed_with)}곳</span></h2>
<p class="body">에델슈타인 전체 맵 {len(ed_maps)}곳 중, 몬스터가 나오는 맵 {len(ed_with)}곳만 이 표에 정리했어요.</p>
    <table class="gtable">
      <tr><th>맵</th><th>출현 몬스터</th><th class="num">종류</th></tr>
{rows3}    </table>
<p class="body">이 표에 없는 나머지 {len(ed_only)}곳은 몬스터가 나오지 않는 맵이에요. 데이터에서 마을로 분류된 맵이 {ed_town_n}곳, NPC만 있는 맵이 {ed_npconly_n}곳, 어느 쪽으로도 분류되지 않은 맵이 {ed_rest_n}곳이에요.</p>
    <p class="legend">몬스터가 출현하지 않는 맵(마을·실내 등): {town_names}</p>
  {DIST_EDEL_RETURN}
  </section>
  <section class="card">
    <h2>에델슈타인 몬스터<span class="cnt">{len(ed_mobs)}종</span></h2>
<p class="body">이 지역 몬스터 {len(ed_mobs)}종은 Lv.{ed_lv_min}부터 Lv.{ed_lv_max}까지예요.</p>
    <div class="grid">
{mob_cards(ed_mobs, {m["id"] for m in ed_maps})}    </div>
    <p class="legend">레벨·HP와 출현 맵은 본진 기준 수집 데이터입니다.<br>아이콘·이미지: maplestory.io</p>
  </section>
  {ROUTE_EDEL}
  {DIST_EDEL_MAIN}"""
os.makedirs(f"{OUT}/edelstein", exist_ok=True)
open(f"{OUT}/edelstein/index.html", "w").write(page(
    "에델슈타인 엿보기", "빅뱅 이후 개편으로 추가된 지역 에델슈타인의 맵과 출현 몬스터를 미리 살펴봅니다.",
    "/guide/edelstein/", "에델슈타인", "엿보기", "블랙윙의 광산 도시, 미리 구경하기", body3, css=CSS_LIVE3, foot_full=FOOT_EDELSTEIN))


# ---------- 4. 루디브리엄 마을 가이드 (신설 2026-11-05, 에델슈타인 구조 승계) ----------
ludi_maps = sorted([m for m in maps.values() if m["region"] == "Ludibrium"], key=lambda m: dname(m))
ludi_with = [m for m in ludi_maps if m["id"] in map_mobs]
ludi_mobs = {r["mob_id"] for m in ludi_with for r in map_mobs[m["id"]]}
rows4 = ""
for m in ludi_with:
    rs = map_mobs[m["id"]]
    en = f'<span class="men">{esc(m["name_en"])}</span>' if m.get("name_ko_candidate") else ""
    rows4 += f"""<tr><td><span class="mname">{esc(dname(m))}</span>{en}</td><td>{mob_chips(m["id"])}</td><td class="num">{len(rs)}</td></tr>\n"""
ludi_only = [m for m in ludi_maps if m["id"] not in map_mobs]
ludi_town_n = sum(1 for m in ludi_only if m.get("isTown"))
ludi_npconly_n = sum(1 for m in ludi_only if not m.get("isTown") and m.get("npcs"))
ludi_rest_n = len(ludi_only) - ludi_town_n - ludi_npconly_n
ludi_town = " · ".join(esc(dname(m)) for m in ludi_only)
body4 = f"""
  <section class="card">
    <h2>루디브리엄은 어떤 곳?</h2>
    <p class="body">본진 GMS 95의 루디브리엄에서 Marcel은 경비를 맡고 있다고 자신을 소개해요. 그는 에오스 타워를 더럽히는 생물들이 마음에 들지 않는다고 말해요. 퀘스트 서술에는 헬리오스 타워가 개방된 뒤 몬스터가 늘어나 Marcel이 곤란을 겪는다는 이야기가 나와요.</p>
    <p class="body">이 소개는 본진 GMS 95의 게임 텍스트를 바탕으로 자체 번역·요약한 내용이에요. 자료는 maplestory.io를 경유했으며, 알팡서버의 실제 구현은 미확인입니다.</p>
    <p class="body">이 페이지에서는 수집된 루디브리엄 권역 맵 {len(ludi_maps)}곳 가운데 몬스터가 출현하는 {len(ludi_with)}곳과, 거기서 만날 수 있는 몬스터 {mob_group_count(ludi_mobs)}종을 미리 엿봅니다.</p>
</section>
  <section class="card">
    <h2>몬스터가 출현하는 맵<span class="cnt">{len(ludi_with)}곳</span></h2>
    <div class="tscroll"><span class="tscroll-hint" aria-hidden="true">좌우로 밀어 표 전체를 볼 수 있어요</span><table class="gtable">
      <tr><th>맵</th><th>출현 몬스터</th><th class="num">종류</th></tr>
{rows4}    </table></div>
<p class="body">이 표에 없는 나머지 {len(ludi_only)}곳은 몬스터가 나오지 않는 맵이에요. 데이터에서 마을로 분류된 맵이 {ludi_town_n}곳, NPC만 있는 맵이 {ludi_npconly_n}곳, 어느 쪽으로도 분류되지 않은 맵이 {ludi_rest_n}곳이에요.</p>
    <p class="legend">몬스터가 출현하지 않는 맵(마을·실내 등): {ludi_town}</p>
  </section>
  <section class="card">
    <h2>루디브리엄 몬스터<span class="cnt">{len(ludi_mobs)}종</span></h2>
    <div class="grid">
{mob_cards(ludi_mobs, {m["id"] for m in ludi_maps})}    </div>
    <p class="legend">레벨·HP와 출현 맵은 본진 기준 수집 데이터입니다.<br>아이콘·이미지: maplestory.io</p>
  </section>"""
os.makedirs(f"{OUT}/ludibrium", exist_ok=True)
open(f"{OUT}/ludibrium/index.html", "w").write(page(
    "루디브리엄 마을 가이드", "장난감 도시 루디브리엄의 맵과 출현 몬스터를 미리 살펴봅니다.",
    "/guide/ludibrium/", "루디브리엄", "마을 가이드", "장난감 도시와 두 개의 타워, 미리 구경하기", body4 + ROUTE_LUDI + NARR_OMEGA, css=CSS_LUDI, foot_full=FOOT_LUDIBRIUM, no_i18n_alt=True))

# ---------- 5. 버섯신사 가이드 (신설 2026-11-13, 사냥터에서 이관) ----------
body5 = f"""
  <section class="card">
    <h2>버섯신사는 어떤 곳?</h2>
    <p class="body">버섯신사는 지팡구 지역에 있는 마을이에요. 신사를 중심으로 사람들이 모여 사는 곳으로, 이 페이지에서는 본진 게임 텍스트에 남은 버섯신사의 이야기를 미리 엿봐요. 이 이야기는 원래 사냥터 가이드에 실려 있던 섹션을 이 마을만의 페이지로 옮겨 온 거예요.</p>
  </section>
""" + NARR_MUSHROOM
os.makedirs(f"{OUT}/mushroom-shrine", exist_ok=True)
open(f"{OUT}/mushroom-shrine/index.html", "w").write(page(
    "버섯신사 엿보기", "지팡구 지역의 신사 마을 버섯신사의 이야기를 미리 살펴봅니다.",
    "/guide/mushroom-shrine/", "버섯신사", "엿보기", "벚꽃이 지지 않는 신사 마을, 미리 구경하기", body5, css=CSS_LUDI, foot_full=FOOT_LUDIBRIUM))

print("guide built | hunting maps:", len(vic), "| orbis mobs:", len(orb_mobs), "| leafre mobs:", len(leaf_mobs), "| edel maps:", len(ed_with), "edel mobs:", len(ed_mobs))
