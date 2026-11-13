import json, os, html, re, unicodedata

DB = os.path.expanduser("~/workspace/alpang/data/db")
SITE = os.path.expanduser("~/workspace/alpang/site")
maps = json.load(open(f"{DB}/maps.json"))["maps"]
mobs = json.load(open(f"{DB}/mobs.json"))["mobs"]
rels = json.load(open(f"{DB}/relations.json"))["relations"]

# 몬스터 확장 스탯 (승인본 alpang-db-20261015-0900, data/db/monster_stats.json)
# mobs.json은 무변경 — 표시는 id 조인으로만 한다. 가드 실패 시 산출 중단 (설계 v1 원칙 계승).
import sys
_stats_doc = json.load(open(f"{DB}/monster_stats.json"))
STAT_FIELDS = ["level", "hp", "mp", "exp", "physical_damage_raw", "magic_damage_raw",
               "physical_defense", "magic_defense", "accuracy", "evasion",
               "movement_speed_raw", "physical_defense_rate_raw", "magic_defense_rate_raw"]
_stats_list = _stats_doc["monsters"]
_errs = []
_extra_ids = {s["id"] for s in _stats_list} - {m["id"] for m in mobs}
if _extra_ids:
    _errs.append(f"monster_stats에만 있는 ID: {sorted(_extra_ids)[:10]}")
for _s in _stats_list:
    for _f in STAT_FIELDS:
        _v = _s["stats"].get(_f)
        if _v is not None and (isinstance(_v, bool) or not isinstance(_v, (int, float))):
            _errs.append(f"타입 오류: {_s['id']}.{_f} = {type(_v).__name__}")
if _errs:
    print("몬스터 스탯 가드 실패 — 산출 중단:")
    for _e in _errs[:20]:
        print(" -", _e)
    sys.exit(1)
# 상세 전체 실패(confirmed 아님·레코드 없음)는 중단하지 않고 카드에 '상세 미확인'으로 분기한다 (기술이사 기준).
stats_by_id = {s["id"]: s["stats"] for s in _stats_list if s.get("detail_status") == "confirmed"}

mob_by_id = {m["id"]: m for m in mobs}
map_by_id = {m["id"]: m for m in maps}

def disp_name(e):
    return e.get("name_ko_candidate") or e.get("name_en") or str(e["id"])

def esc(s):
    return html.escape(str(s), quote=True)

def stat_val(v):
    """확장 스탯 값 렌더링. null(원본 키 부재)은 '미기록' 칩, 실제 0·음수는 원형 그대로 (천 단위 콤마)."""
    if v is None:
        return '<span class="unknown">미기록</span>'
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

# 상세 접기 표시 필드 (확정: 라벨 풀네임, '(원본 수치)'는 이동 속도·방어율만)
DETAIL_FIELDS = [("mp", "MP"), ("physical_damage_raw", "물리 공격력"), ("magic_damage_raw", "마법 공격력"),
                 ("physical_defense", "물리 방어력"), ("magic_defense", "마법 방어력"),
                 ("accuracy", "명중"), ("evasion", "회피"),
                 ("movement_speed_raw", "이동 속도 (원본 수치)"),
                 ("physical_defense_rate_raw", "물리 방어율 (원본 수치)"),
                 ("magic_defense_rate_raw", "마법 방어율 (원본 수치)")]

def norm_name(s):
    """탭 내 검색용 이름 정규화 — 홈 통합 검색(search.js)과 동일 규칙: NFKC·소문자·공백/기호 제거."""
    if not s:
        return ""
    return re.sub(r"[\s\-_·.,'\"!?()\[\]]", "", unicodedata.normalize("NFKC", str(s)).lower())

def data_name(e):
    return esc(norm_name(e.get("name_ko_candidate")) + " " + norm_name(e.get("name_en")))

def filter_bar(fid, placeholder, with_sort=False):
    sort = ''
    if with_sort:
        sort = (f'<label class="flb" for="{fid}Sort">정렬</label>'
                f'<select id="{fid}Sort" class="fsort"><option value="lv">레벨 낮은 순</option>'
                f'<option value="eff">체경비 낮은 순</option></select>')
    return (f'<div class="filterbar"><label class="flb" for="{fid}Filter">이름으로 찾기</label>'
            f'<input type="search" id="{fid}Filter" class="finput" placeholder="{placeholder}" autocomplete="off">'
            f'{sort}'
            f'<span class="fcount" id="{fid}Count" aria-live="polite"></span>'
            f'<button type="button" class="fclear" id="{fid}Clear" hidden>지우기</button></div>'
            f'<p class="fnores" id="{fid}None" hidden>검색 결과가 없습니다.</p>')

MOB_PAGING_SCRIPT = """
<script>
(function () {
  var PAGE = 50, limit = PAGE;
  var more = document.getElementById('mobMore');
  if (!more) return;
  var cards = Array.prototype.slice.call(document.querySelectorAll('.mob'));
  function applyPaging() {
    cards.forEach(function (c) { if (c.getAttribute('data-pg') === '1') { c.style.display = ''; c.removeAttribute('data-pg'); } });
    var passed = cards.filter(function (c) { return c.style.display !== 'none'; });
    var visible = 0;
    passed.forEach(function (c, i) {
      if (i >= limit) { c.style.display = 'none'; c.setAttribute('data-pg', '1'); }
      else visible++;
    });
    if (passed.length <= visible) { more.hidden = true; }
    else { more.hidden = false; more.textContent = '더 보기 (남은 ' + (passed.length - visible).toLocaleString('ko-KR') + '건)'; }
  }
  more.addEventListener('click', function () { limit += PAGE; applyPaging(); });
  document.addEventListener('input', function () { limit = PAGE; setTimeout(applyPaging, 0); });
  document.addEventListener('click', function () { setTimeout(applyPaging, 0); });
  document.addEventListener('change', function () { setTimeout(applyPaging, 0); });
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('mob')) { var ti = cards.indexOf(target); if (ti >= limit) limit = ti + 1; }
  }
  applyPaging();
})();
</script>"""
MOB_SORT_SCRIPT = """<script>(function(){
var sel=document.getElementById('mobSort');if(!sel)return;
var grid=document.querySelector('.grid');if(!grid)return;
function keyEff(c){var v=parseFloat(c.getAttribute('data-eff'));return isNaN(v)?Infinity:v;}
function keyLv(c){var v=parseInt(c.getAttribute('data-lv'),10);return isNaN(v)?9999:v;}
function keyName(c){return c.getAttribute('data-name')||'';}
sel.addEventListener('change',function(){
  var cards=[].slice.call(grid.querySelectorAll('.mob'));
  var mode=sel.value;
  cards.sort(function(a,b){
    if(mode==='eff'){var d=keyEff(a)-keyEff(b);if(d)return d;}
    var dl=keyLv(a)-keyLv(b);if(dl)return dl;
    return keyName(a)<keyName(b)?-1:(keyName(a)>keyName(b)?1:0);
  });
  cards.forEach(function(c){grid.appendChild(c);});
});
})();</script>"""

_FILTER_SCRIPT = """<script>(function(){
var inp=document.getElementById('__FID__Filter');if(!inp)return;
var cards=[].slice.call(document.querySelectorAll('__CARD__'));
var cnt=document.getElementById('__FID__Count');var none=document.getElementById('__FID__None');var clr=document.getElementById('__FID__Clear');
function norm(s){return (s||'').normalize('NFKC').toLowerCase().replace(/[\\s\\-_·.,'"!?()\\[\\]]/g,'');}
function apply(){var q=norm(inp.value);var shown=0;
cards.forEach(function(c){var ok=!q||(c.getAttribute('data-name')||'').indexOf(q)>=0;c.style.display=ok?'':'none';if(ok)shown++;});
__SECTIONS__
if(cnt)cnt.textContent=q?(shown.toLocaleString()+'__UNIT__ 표시 / 전체 '+cards.length.toLocaleString()+'__UNIT__'):('전체 '+cards.length.toLocaleString()+'__UNIT__');
if(none)none.hidden=shown>0;
if(clr)clr.hidden=!q;}
inp.addEventListener('input',apply);
if(clr)clr.addEventListener('click',function(){inp.value='';apply();inp.focus();});
apply();
})();</script>"""
_SECTION_JS = "document.querySelectorAll('.region').forEach(function(sec){var any=false;sec.querySelectorAll('.map').forEach(function(c){if(c.style.display!=='none')any=true;});sec.style.display=any?'':'none';});"

def filter_script(fid, card_sel, unit, with_sections=False):
    s = _FILTER_SCRIPT.replace('__FID__', fid).replace('__CARD__', card_sel).replace('__UNIT__', unit)
    return s.replace('__SECTIONS__', _SECTION_JS if with_sections else '')

def eff_ratio(mid):
    """체경비 = HP ÷ EXP (본진 GMS 95 기준). HP는 상세 수치(stats) 우선·maxHP 폴백, EXP는 두 소스 전수 일치.
    EXP 결측(4종)이면 None — 표기는 '미확인' (확정 조건, 2026-10-16). 정렬 키는 반올림 전 원값을 쓴다."""
    st = stats_by_id.get(mid)
    m = mob_by_id.get(mid)
    hp = st.get("hp") if st else None
    if hp is None and m:
        hp = m.get("maxHP")
    exp = st.get("exp") if st else None
    if exp is None and m:
        exp = m.get("exp")
    if hp is None or not exp:
        return None
    return hp / exp

def detail_block(mid):
    st = stats_by_id.get(mid)
    if st is None:
        # 상세 전체 실패 분기 (레코드 없음·confirmed 아님) — '미기록'과 구분되는 표기 (기술이사 기준, 분기 유지)
        return '<div class="mdetail"><span class="unknown">상세 미확인</span></div>'
    rows = "".join(f'<div class="drow"><dt>{label}</dt><dd>{stat_val(st.get(key))}</dd></div>' for key, label in DETAIL_FIELDS)
    # 핵심 수치 타일 (HP·MP·EXP·체경비) — 체경비는 4번째, 아래에 계산식·기준 라벨 병기 (확정 조건)
    m = mob_by_id.get(mid)
    def tv(v):
        return f"{v:,}" if isinstance(v, int) else '<span class="unknown">미기록</span>'
    hpv = st.get("hp") if st.get("hp") is not None else (m.get("maxHP") if m else None)
    expv = st.get("exp") if st.get("exp") is not None else (m.get("exp") if m else None)
    effv = eff_ratio(mid)
    eff_tile = f"{effv:.1f}" if effv is not None else '<span class="unknown">산출 제외</span>'
    tiles = ('<div class="tiles">'
             f'<div class="tile"><span class="tk">HP</span><b>{tv(hpv)}</b></div>'
             f'<div class="tile"><span class="tk">MP</span><b>{tv(st.get("mp"))}</b></div>'
             f'<div class="tile"><span class="tk">EXP</span><b>{tv(expv)}</b></div>'
             f'<div class="tile eff"><span class="tk">체경비</span><b>{eff_tile}</b></div></div>'
             '<p class="tnote">체경비 = HP ÷ EXP · 본진 GMS 95 기준</p>')
    return ('<details class="mdetail"><summary>상세 수치</summary>'
            '<div class="mbasis">본진 GMS 95 기준 몬스터 기본 수치</div>'
            + tiles +
            f'<dl class="dgrid">{rows}</dl>'
            '<p class="dnote">물리·마법 공격력, 이동 속도·방어율은 모두 원본 수치를 그대로 표시합니다. 이동 속도·방어율은 의미·단위 검증 전이라 백분율이나 계산값이 아닙니다.</p></details>')

IMG_CREDIT = "아이콘·이미지: maplestory.io"
def mob_img(mid):
    return f'<span class="islot"><img class="mimg" src="https://maplestory.io/api/GMS/95/mob/{mid}/icon" alt="" loading="lazy" onerror="this.style.display=\'none\'"></span>'

# relations -> map_id: [(mob, placements)], mob_id: [(map, placements)]
map_mobs, mob_maps = {}, {}
for r in rels:
    mid, bid = r["map_id"], r["mob_id"]
    if bid in mob_by_id and mid in map_by_id:
        map_mobs.setdefault(mid, []).append((mob_by_id[bid], r.get("placements")))
        mob_maps.setdefault(bid, []).append((map_by_id[mid], r.get("placements")))
# fallback: maps.mob_ids for maps with no relations
for mp in maps:
    if mp["id"] not in map_mobs and mp.get("mob_ids"):
        lst = [(mob_by_id[b], None) for b in mp["mob_ids"] if b in mob_by_id]
        if lst:
            map_mobs[mp["id"]] = lst
            for mob, _ in lst:
                mob_maps.setdefault(mob["id"], []).append((mp, None))

DISCLAIMER = "본진 빅뱅 직후(GMS 95) 기준 데이터이며 알팡서버 실서버와 다를 수 있습니다. 한글 이름은 표시명 후보입니다."

THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script>"

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
  .gnb nav a.on{color:var(--accent-dark)}
  @media (max-width:560px){ .gnb .logo{font-size:18px} .gnb nav a{font-size:14px;margin-left:10px} }
  .gnb nav a{display:inline-flex;align-items:center;min-height:44px}
  @media (max-width:768px){.gnb{flex-wrap:nowrap}.gnb nav{flex-wrap:nowrap;overflow-x:auto;flex:1 1 auto;min-width:0;justify-content:flex-start;scrollbar-width:none;-webkit-mask-image:linear-gradient(to right,#000 92%,transparent);mask-image:linear-gradient(to right,#000 92%,transparent)}.gnb nav::-webkit-scrollbar{display:none}}
  .intro{text-align:center;padding:28px 0 16px}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .intro .stats{font-size:13.5px;color:var(--sub);margin-top:8px}
  .notice{font-size:14px;color:var(--sub);background:var(--accent-soft);border-radius:10px;padding:12px 16px;margin-top:16px;text-align:center}
  .notice .small{font-size:12.5px}
  .filterbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--bg);padding:10px 0;margin-top:14px}
   .filterbar{position:sticky;top:73px;z-index:40}
  .flb{font-size:14px;font-weight:800;color:var(--accent-dark)}
  .finput{flex:1;min-width:160px;font-size:16px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text)}
  .fcount{font-size:13px;color:var(--sub)}
  .fsort{font-size:14px;padding:9px 10px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text)}
  .fclear{font-size:13.5px;font-weight:700;padding:8px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer}
  .fnores{font-size:14px;color:var(--sub);text-align:center;padding:18px 0 4px}
  .qmore{display:block;margin:14px auto 4px;font:inherit;font-size:14.5px;font-weight:700;padding:10px 26px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer}
  .xlink{margin-top:14px;text-align:center}
  .xlink a{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 18px;color:var(--accent-dark);font-weight:700;font-size:15px;text-decoration:none}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  a{color:var(--accent-dark)}
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] .mob,[data-theme="dark"] .map{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .islot{background:#26292F}
  [data-theme="dark"] .unknown{background:#26292F}
  [data-theme="dark"] .place,[data-theme="dark"] .chip,[data-theme="dark"] .street{background:#22252B}
  [data-theme="dark"] .place.none,[data-theme="dark"] .chip.none{background:#22252B}
  [data-theme="dark"] .mob .stats,[data-theme="dark"] .map .mobs{border-top-color:var(--line)}

/* 공통 규칙 선행분 — 디렉터 자문 (2026-11-02) */
:root{--card-pad:22px;--card-gap:14px;--slate-bg:rgba(148,163,184,.12);--slate-tx:#94A3B8;--amber:#F59E0B;--amber-lt:#FBBF24}
aside.name-status,.vw-badge,.vw-card-badge{background:var(--slate-bg);color:var(--slate-tx)}
"""

def gnb(active):
    links = [("/", "홈"), ("/timeline/", "타임라인"), ("/faq/", "FAQ"), ("/mobs/", "몬스터 도감"), ("/maps/", "맵 탐색"), ("/items/", "아이템"), ("/npcs/", "NPC·퀘스트")]
    parts = []
    for h, t in links:
        cls = ' class="on"' if h == active else ''
        parts.append('<a href="' + h + '"' + cls + '>' + t + '</a>')
    return '<div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a><nav>' + ''.join(parts) + '</nav>' + THEME_BTN + '</div>'
FOOTER = """<footer>
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95) · 페이지 갱신일: 2026-10-15
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  </footer>"""

def head(title, desc, canon):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 알팡지지</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="{title} — 알팡지지">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://alpang.gg/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{THEME_INIT}
<style>{CSS}
  .dic{{width:1.15em;height:1.15em;image-rendering:pixelated;vertical-align:-.18em}}

  .map{{flex-direction:row}}
  .map .mframe{{width:168px;height:auto;min-height:150px;border-bottom:none;border-right:1px solid var(--line)}}
  .map .mbody{{flex:1;min-width:0}}
  .map .mhead{{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}}
  @media (max-width:640px){{ .map{{flex-direction:column}} .map .mframe{{width:auto;height:150px;border-right:none;border-bottom:1px solid var(--line)}} }}

  .topbtn{{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--accent);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-size:13px;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .18s}}
  .topbtn.on{{opacity:1;pointer-events:auto}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>"""

# ---------- 페이지 1: 몬스터 도감 ----------
sorted_mobs = sorted(mobs, key=lambda m: (m.get("level") if m.get("level") is not None else 9999, disp_name(m)))
cards = ""
for m in sorted_mobs:
    name = esc(disp_name(m))
    en = esc(m.get("name_en") or "")
    sub = f'<span class="en">{en}</span>' if m.get("name_ko_candidate") and en else ""
    lv = m.get("level") if m.get("level") is not None else "?"
    hp = f"{m['maxHP']:,}" if m.get("maxHP") is not None else "미기록"
    if m.get("exp") is not None:
        exp = f"{m['exp']:,}"
    else:
        exp = '<span class="unknown">미기록</span>'
    places = mob_maps.get(m["id"], [])
    if places:
        chips = "".join(f'<span class="place">{esc(disp_name(mp))}</span>' for mp, _ in sorted(places, key=lambda x: disp_name(x[0])))
        where = f'<div class="where"><span class="wlb">출현 맵</span>{chips}</div>'
    else:
        where = '<div class="where"><span class="wlb">출현 맵</span><span class="place none">확인된 출현 맵 없음</span></div>'
    effv = eff_ratio(m["id"])
    eff_chip = f'<span>체경비 <b>{effv:.1f}</b></span>' if effv is not None else '<span>체경비 <span class="unknown">산출 제외</span></span>'
    eff_attr = f"{effv}" if effv is not None else ""
    lv_attr = m.get("level") if m.get("level") is not None else 9999
    cards += f"""<article class="mob" id="mob-{m["id"]}" data-name="{data_name(m)}" data-eff="{eff_attr}" data-lv="{lv_attr}">
      {mob_img(m["id"])}
      <div class="mhead"><h3>{name}</h3>{sub}<span class="lv">Lv.{lv}</span></div>
      <div class="stats"><span>HP <b>{hp}</b></span><span>경험치 <b>{exp}</b></span>{eff_chip}</div>
      {where}
      {detail_block(m["id"])}
    </article>
"""
mobs_css = """
  .live-badge{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:600;color:var(--sub);background:rgba(31,157,85,.08);border:1px solid rgba(31,157,85,.35);border-radius:999px;padding:5px 12px 5px 10px;margin:10px 0 2px}
  .live-dot{flex:none;width:8px;height:8px;border-radius:50%;background:#1F9D55;animation:livePulse 2s ease-out infinite}
  @keyframes livePulse{0%{box-shadow:0 0 0 0 rgba(31,157,85,.45)}70%{box-shadow:0 0 0 7px rgba(31,157,85,0)}100%{box-shadow:0 0 0 0 rgba(31,157,85,0)}}
  @media (prefers-reduced-motion: reduce){.live-dot{animation:none}}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;margin-top:18px}
  .islot{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:#F3F4F6;border-radius:6px;margin:0 auto 8px}
  .islot .mimg{max-width:32px;max-height:32px}
  .mob{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:0 1px 3px rgba(30,25,15,.05);scroll-margin-top:90px}
  .mob:target{outline:2px solid var(--accent);outline-offset:2px}
  .mhead{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
  .mhead h3{font-size:15px;font-weight:700}
  .mhead .en{font-size:12.5px;color:var(--sub)}
  .mhead .lv{margin-left:auto;font-size:11px;font-weight:800;color:var(--accent-dark);background:var(--accent-soft);padding:2px 6px;border-radius:4px}
  .mob .stats{display:flex;gap:16px;font-size:14px;line-height:1.5;color:var(--sub);margin-top:6px;border-top:1px solid #f0ece3;padding-top:8px}
  .mob .stats b{color:var(--text)}
  .unknown{display:inline-block;color:var(--unknown);font-weight:700;font-size:11px;background:#f4f1ea;border-radius:4px;padding:2px 6px}
  .where{margin-top:8px}
  .wlb{font-size:12.5px;font-weight:800;color:var(--accent);display:block;margin-bottom:4px}
  .place{display:inline-block;font-size:13.5px;background:#f7f4ee;border:1px solid var(--line);border-radius:999px;padding:1px 9px;margin:0 4px 4px 0}
  .place.none{color:var(--sub);background:#f4f1ea;border:1px solid var(--line);border-radius:4px;padding:2px 6px;font-size:11px}
  .mdetail{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}
  .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0 6px}
  .tile{background:var(--accent-soft);border-radius:10px;padding:7px 6px;text-align:center}
  .tile .tk{display:block;font-size:11px;font-weight:700;color:var(--sub)}
  .tile b{font-size:15.5px}
  .tile.eff{background:#252A34}
  .tile.eff .tk{color:#B9C0CC}
  .tile.eff b{color:#ECE9E2}
  .tnote{font-size:12px;color:var(--sub);margin:2px 0 8px}
  .mdetail summary{cursor:pointer;font-size:13.5px;font-weight:700;color:var(--accent-dark)}
  .mbasis{font-size:12.5px;color:var(--sub);margin-top:6px}
  .dgrid{display:grid;grid-template-columns:1fr 1fr;gap:3px 14px;margin-top:6px}
  .drow{display:flex;justify-content:space-between;gap:8px;font-size:13.5px}
  .drow dt{color:var(--sub);min-width:0}
  .drow dd{font-weight:600;flex:none;white-space:nowrap}
  .drow .unknown{white-space:nowrap}
  .dnote{font-size:12px;color:var(--sub);line-height:1.55;margin-top:7px}
  @media (max-width:560px){ .grid{grid-template-columns:1fr} .dgrid{grid-template-columns:1fr} }
"""
html_mobs = head("몬스터 도감", "본진 빅뱅 직후(GMS 95) 기준 몬스터 175종의 레벨·HP·경험치와 출현 맵을 정리한 팬 도감입니다.", "https://alpang.gg/mobs/") + f"""
<style>{mobs_css}
  .map{{flex-direction:row}}
  .map .mframe{{width:168px;height:auto;min-height:150px;border-bottom:none;border-right:1px solid var(--line)}}
  .map .mbody{{flex:1;min-width:0}}
  .map .mhead{{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}}
  @media (max-width:640px){{ .map{{flex-direction:column}} .map .mframe{{width:auto;height:150px;border-right:none;border-bottom:1px solid var(--line)}} }}

  .topbtn{{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--accent);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-size:13px;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .18s}}
  .topbtn.on{{opacity:1;pointer-events:auto}}
</style>
<body>
<div class="wrap">
  {gnb('/mobs/')}
  <div class="intro">
    <h1>몬스터 <span>도감</span></h1>
    <p class="live-badge"><span class="live-dot" aria-hidden="true"></span>패치 버전에 맞춰 몬스터 정보가 실시간으로 등록됩니다</p>
    <div class="tag">수집된 맵에 출현하는 몬스터 {len(mobs)}종</div>
    <div class="stats">레벨 오름차순 · 출현 맵은 수집 완료된 맵 기준입니다</div>
  </div>
  <p class="notice">{DISCLAIMER}<br>{IMG_CREDIT}<br>카드의 '상세 수치'는 본진 GMS 95 기준 몬스터 기본 수치입니다.</p>
  <div class="xlink"><a href="/maps/"><img class="dic" src="/assets/icons/icon-worldmap.png" alt="" aria-hidden="true"> 맵 탐색 보러 가기</a></div>
  {filter_bar('mob', '몬스터 이름 입력 (한글·영문)', with_sort=True)}
  <main class="grid">
{cards}  </main>
  <button type="button" class="qmore" id="mobMore" hidden>더 보기</button>
  {FOOTER}
</div>
{THEME_SCRIPT}
{filter_script('mob', '.mob', '종')}
{MOB_PAGING_SCRIPT}
{MOB_SORT_SCRIPT}
<script src="/assets/hit.js?v=2" defer></script>
</body>
</html>"""
os.makedirs(f"{SITE}/mobs", exist_ok=True)
open(f"{SITE}/mobs/index.html", "w").write(html_mobs)

# ---------- 페이지 2: 맵 탐색 ----------
# 맵 이미지 매니페스트 (stage6 편입본): result minimap 333 / icon_fallback 61 / failed 8. 에셋은 site/assets/maps/minimap-{id}.png.
MAP_IMG = {i["map_id"]: i for i in json.load(open(f"{DB}/map_images.json"))}
if set(MAP_IMG) != {m["id"] for m in maps}:
    raise SystemExit("[중단] map_images.json의 맵 ID 집합이 maps.json과 다릅니다.")
for _mid, _info in MAP_IMG.items():
    if _info["result"] in ("minimap", "icon_fallback") and not os.path.exists(f"{SITE}/assets/maps/minimap-{_mid}.png"):
        raise SystemExit(f"[중단] 맵 이미지 에셋 누락: minimap-{_mid}.png (result={_info['result']})")

REG_ORDER = ["Victoria Road", "105-band", "Ludibrium", "Orbis", "Leafre", "Edelstein-area", "Hidden Street", "etc"]
# 권역 라벨 교정 (2026-10-15 확정): 빅토리아 아일랜드 / 슬리피우드 일대 / 에델슈타인 — 표시 라벨만 교체, 분류 키는 무변경.
REG_KO = {"Victoria Road": "빅토리아 아일랜드", "105-band": "슬리피우드 일대", "Ludibrium": "루디브리엄", "Orbis": "오르비스", "Leafre": "리프레", "Edelstein-area": "에델슈타인", "Hidden Street": "히든 스트리트", "etc": "기타 권역"}
# 히든 스트리트 판정 14곳 (데이터 담당 판정, data/stage5-hidden-street/verdict.json: 확정 10 + 이중 근거 1 + 이름 일치 판정 3).
# maps.json 원본은 무변경 — 빌더 오버라이드로만 권역을 바꾼다. 보류 1곳(100040500 무너진 골렘의 성터)은 넣지 않는다.
HIDDEN_STREET_IDS = {200080101, 200081201, 200082301, 220010001, 220011001,
                     240010101, 240010501, 240010901, 240040610, 240040611,
                     910540400, 102030000, 100040000, 100040100}

def eff_region(mp):
    return "Hidden Street" if mp["id"] in HIDDEN_STREET_IDS else (mp.get("region") or "etc")

groups = {}
for mp in maps:
    groups.setdefault(eff_region(mp), []).append(mp)
sections = ""
for reg in REG_ORDER:
    lst = groups.get(reg)
    if not lst:
        continue
    lst = sorted(lst, key=lambda x: (x.get("street_en") or "", disp_name(x)))
    rows = ""
    for mp in lst:
        name = esc(disp_name(mp))
        en = esc(mp.get("name_en") or "")
        sub = f'<span class="en">{en}</span>' if mp.get("name_ko_candidate") and en else ""
        town = '<span class="town">마을</span>' if mp.get("isTown") else ""
        street = esc(mp.get("street_en") or "")
        street_html = f'<span class="street">{street}</span>' if street and street != (mp.get("name_en") or "") else ""
        mlist = map_mobs.get(mp["id"], [])
        if mlist:
            # 도트 칩 (디렉터 공통 규격, 2026-10-16 확정): 24×24 스프라이트 + 이름 13.5px + Lv.
            # 노출 기준은 '최대 2줄' — 빌더는 전 칩을 렌더하고, 줄 측정은 페이지 JS가 해 초과분을 펼침으로 숨긴다 (JS 없으면 전부 보이는 폴백).
            ordered = sorted(mlist, key=lambda x: (x[0].get("level") or 9999, disp_name(x[0])))
            parts = []
            for mob, _ in ordered:
                lv = mob.get("level")
                lv_html = f'<span class="dlv">Lv.{lv}</span>' if isinstance(lv, int) else ''
                parts.append(f'<span class="dchip"><img class="dimg" src="https://maplestory.io/api/GMS/95/mob/{mob["id"]}/icon" alt="" width="24" height="24" loading="lazy" onerror="this.style.display=\'none\'"><span class="dnm">{esc(disp_name(mob))}</span>{lv_html}</span>')
            if len(ordered) >= 3:
                parts.append(f'<button type="button" class="morebtn" aria-expanded="false" hidden>+{len(ordered)}종</button>')
            chips = "".join(parts)
        else:
            chips = '<span class="dchip dnone">출현 몬스터 없음 (수집 기준)</span>'
        # 미니맵 액자 (디렉터 마감 규격): 고정 높이 150px·contain·배경 #0D1014·좌상단 권역 배지, 이름은 액자 아래 본문 첫 줄.
        badge = f'<span class="rbadge">{esc(REG_KO.get(reg, reg))}</span>'
        minfo = MAP_IMG[mp["id"]]
        if minfo["result"] == "minimap":
            frame = f'<div class="mframe">{badge}<img class="mmap" src="/assets/maps/minimap-{mp["id"]}.png" alt="" loading="lazy"></div>'
        elif minfo["result"] == "icon_fallback":
            frame = f'<div class="mframe fb">{badge}<img class="micon" src="/assets/maps/minimap-{mp["id"]}.png" alt="" loading="lazy"></div>'
        else:
            frame = f'<div class="mframe ph">{badge}<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#8A8578" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg><span class="phcap">미니맵 정보 없음</span></div>'
        rows += f"""<article class="map" id="map-{mp["id"]}" data-name="{data_name(mp)}">
      {frame}
      <div class="mbody">
      <div class="mhead"><h3>{name}</h3>{sub}{town}{street_html}</div>
      <div class="mobs">{chips}</div>
      </div>
    </article>
"""
    sections += f"""<section class="region">
    <h2>{REG_KO.get(reg, esc(reg))} <small>{len(lst)}곳</small></h2>
    <div class="list">
{rows}    </div>
  </section>
"""
maps_css = """
  .live-badge{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:600;color:var(--sub);background:rgba(31,157,85,.08);border:1px solid rgba(31,157,85,.35);border-radius:999px;padding:5px 12px 5px 10px;margin:10px 0 2px}
  .live-dot{flex:none;width:8px;height:8px;border-radius:50%;background:#1F9D55;animation:livePulse 2s ease-out infinite}
  @keyframes livePulse{0%{box-shadow:0 0 0 0 rgba(31,157,85,.45)}70%{box-shadow:0 0 0 7px rgba(31,157,85,0)}100%{box-shadow:0 0 0 0 rgba(31,157,85,0)}}
  @media (prefers-reduced-motion: reduce){.live-dot{animation:none}}
  .region{margin-top:26px}
  .region h2{font-size:18px;font-weight:700;border-left:4px solid var(--accent);padding-left:10px;margin-bottom:10px}
  .region h2 small{font-size:13.5px;color:var(--sub);font-weight:600}
  .list{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:10px}
  .map{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:0;overflow:hidden;box-shadow:0 1px 3px rgba(30,25,15,.05);scroll-margin-top:90px;display:flex;flex-direction:column}
  .map:target{outline:2px solid var(--accent);outline-offset:2px}
  .mframe{position:relative;height:150px;background:#0D1014;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:center;padding:10px;box-sizing:border-box;flex:none}
  .mframe .mmap{max-width:100%;max-height:100%;object-fit:contain;display:block}
  .mframe .micon{width:76px;height:76px;object-fit:contain;image-rendering:pixelated}
  .mframe.ph{flex-direction:column;gap:6px}
  .phcap{font-size:12.5px;color:#8A8578}
  .rbadge{position:absolute;top:8px;left:8px;background:rgba(13,16,20,.72);color:#ECE9E2;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;z-index:1}
  .mbody{padding:12px 16px 14px}
  .map .mhead{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
  .map h3{font-size:16px;font-weight:700}
  .map .en{font-size:12.5px;color:var(--sub)}
  .town{font-size:11px;font-weight:800;color:#fff;background:var(--accent);padding:2px 6px;border-radius:4px}
  .street{font-size:11px;color:var(--sub);background:#f7f4ee;border:1px solid var(--line);border-radius:4px;padding:2px 6px}
  .map .mobs{margin-top:8px;border-top:1px solid #f0ece3;padding-top:8px}
  .dchip{display:inline-flex;align-items:center;gap:5px;background:#252A34;border-radius:6px;padding:4px 8px;margin:0 4px 4px 0;color:#ECE9E2;vertical-align:top}
  .dchip[hidden]{display:none}
  .dimg{width:24px;height:24px;object-fit:contain;image-rendering:pixelated;flex:none}
  .dnm{font-size:13.5px}
  .dlv{font-size:12px;font-weight:700;color:#B9C0CC}
  .dchip.dnone{background:var(--accent-soft);color:var(--sub)}
  .morebtn{font-size:12.5px;font-weight:700;padding:6px 10px;border-radius:6px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer;margin:0 4px 4px 0;vertical-align:top}
  @media (max-width:560px){ .list{grid-template-columns:1fr} }
"""
html_maps = head("맵 탐색", "본진 빅뱅 직후(GMS 95) 기준 정상 수집 맵 419곳을 권역별로 정리하고 출현 몬스터를 연결한 팬 탐색 페이지입니다.", "https://alpang.gg/maps/") + f"""
<style>{maps_css}
  .map{{flex-direction:row}}
  .map .mframe{{width:168px;height:auto;min-height:150px;border-bottom:none;border-right:1px solid var(--line)}}
  .map .mbody{{flex:1;min-width:0}}
  .map .mhead{{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}}
  @media (max-width:640px){{ .map{{flex-direction:column}} .map .mframe{{width:auto;height:150px;border-right:none;border-bottom:1px solid var(--line)}} }}

  .topbtn{{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--accent);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-size:13px;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .18s}}
  .topbtn.on{{opacity:1;pointer-events:auto}}
</style>
<body>
<div class="wrap">
  {gnb('/maps/')}
  <div class="intro">
    <h1>맵 <span>탐색</span></h1>
    <p class="live-badge"><span class="live-dot" aria-hidden="true"></span>새로운 지역과 맵 정보가 확인되면 실시간으로 등록됩니다</p>
    <div class="tag">정상 수집된 맵 {len(maps)}곳 · 권역별 정리</div>
    <div class="stats">출현 몬스터는 수집된 출현 관계 기준입니다</div>
  </div>
  <p class="notice">{DISCLAIMER}<br><span class="small">히든 스트리트 권역은 메랜디비(mapledb.kr)의 맵 분류를 대조해 판정한 결과입니다. 미니맵 이미지는 maplestory.io에서 가져왔습니다.</span></p>
  <div class="xlink"><a href="/mobs/">👾 몬스터 도감 보러 가기</a></div>
  {filter_bar('map', '맵 이름 입력 (한글·영문)')}
  <main>
{sections}  </main>
  {FOOTER}
</div>
{THEME_SCRIPT}
{filter_script('map', '.map', '곳', with_sections=True)}
<script>(function(){{
function clampCard(card){{
  if(card.dataset.open==='1')return;
  if(card.offsetParent===null)return;
  var chips=[].slice.call(card.querySelectorAll('.dchip')).filter(function(c){{return !c.classList.contains('dnone');}});
  var btn=card.querySelector('.morebtn');
  chips.forEach(function(c){{c.hidden=false;}});
  var tops=[];var overflow=0;
  chips.forEach(function(c){{var t=Math.round(c.getBoundingClientRect().top);if(tops.indexOf(t)<0)tops.push(t);if(tops.length>2){{c.hidden=true;overflow++;}}}});
  if(btn){{if(overflow>0){{btn.hidden=false;btn.textContent='+'+overflow+'종';btn.setAttribute('aria-expanded','false');}}else{{btn.hidden=true;}}}}
}}
function clampAll(){{document.querySelectorAll('.map').forEach(clampCard);}}
document.addEventListener('click',function(e){{
  var b=e.target.closest?e.target.closest('.morebtn'):null;if(!b)return;
  var card=b.closest('.map');if(!card)return;
  if(card.dataset.open==='1'){{delete card.dataset.open;clampCard(card);}}
  else{{card.dataset.open='1';card.querySelectorAll('.dchip').forEach(function(c){{c.hidden=false;}});b.hidden=false;b.textContent='접기';b.setAttribute('aria-expanded','true');}}
}});
window.addEventListener('load',clampAll);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(clampAll);
var rto;window.addEventListener('resize',function(){{clearTimeout(rto);rto=setTimeout(clampAll,150);}});
var fi=document.getElementById('mapFilter');
if(fi)fi.addEventListener('input',function(){{requestAnimationFrame(clampAll);}});
clampAll();
}})();</script>
<script src="/assets/hit.js?v=2" defer></script>
</body>
</html>"""
os.makedirs(f"{SITE}/maps", exist_ok=True)
open(f"{SITE}/maps/index.html", "w").write(html_maps)

print("mobs page: mobs", len(mobs), "| bytes", len(html_mobs))
print("maps page: maps", len(maps), "| regions", {k: len(v) for k, v in groups.items()}, "| bytes", len(html_maps))
print("mob cards:", html_mobs.count('<article class="mob"'), "| map cards:", html_maps.count('<article class="map"'))
print("unrecorded(null) shown:", html_mobs.count('<span class="unknown">미기록</span>'))
