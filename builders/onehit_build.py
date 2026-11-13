# -*- coding: utf-8 -*-
"""한방컷 계산기 (1차 범위) — 승인 몬스터 175종 HP 검색 + 실측 피해 수동 입력 → 조건부 N회 범위.
기술이사 확정 범위(research/onehit-formula-review-2026-10-16.md): 미검증 공식 자동 계산 금지,
임의 상수 채우기 금지. 이 페이지는 사용자가 실측한 1회 총피해 하한/상한으로만 계산한다."""
import json, os, html as H

ROOT = os.path.expanduser("~/workspace/alpang")
SITE = os.environ.get("ALPANG_OUT", os.path.join(ROOT, "site"))
THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script>"

GNB = ('<div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a>'
       '<nav><a href="/">홈</a><a href="/timeline/">타임라인<span class="new-dot" id="tlNewDot" aria-label="새 글 있음"></span></a><a href="/faq/">FAQ</a><a href="/mobs/">몬스터 도감</a><a href="/maps/">맵 탐색</a><a href="/items/">아이템</a><a href="/npcs/">NPC·퀘스트</a><a href="/jobs/">직업·스킬</a><a href="/calculator/cube/">큐브값 계산기</a><a href="/calculator/onehit/" class="on">한방컷 계산기</a></nav>' + THEME_BTN + '</div>')
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
  .disclaimer{font-size:13.5px;color:var(--sub);text-align:center;margin-top:8px;line-height:1.65}
  section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 3px rgba(30,25,15,.05);padding:20px 22px;margin-top:14px}
  h2{font-size:17px;font-weight:800;margin-bottom:10px}
  .mode-badge{display:inline-block;font-size:12px;font-weight:800;color:#7A3E00;background:#FFE7C7;border-radius:5px;padding:2px 8px;vertical-align:2px;margin-left:8px}
  label.fl{display:block;font-size:13.5px;font-weight:700;color:var(--sub);margin:12px 0 5px}
  input[type=text],input[type=number]{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text);font-size:15.5px;outline:none}
  input:focus{border-color:var(--accent)}
  .mob-results{margin-top:8px;border:1px solid var(--line);border-radius:10px;overflow:hidden;display:none}
  .mob-results.open{display:block}
  .mob-item{display:flex;align-items:center;gap:10px;width:100%;padding:8px 12px;background:var(--card);border:none;border-bottom:1px solid var(--line);cursor:pointer;text-align:left;color:var(--text)}
  .mob-item:last-child{border-bottom:none}
  .mob-item:hover{background:var(--accent-soft)}
  .mob-item img{width:40px;height:40px;object-fit:contain;image-rendering:pixelated}
  .mob-item .nm{font-weight:700;font-size:15px}
  .mob-item .meta{font-size:12.5px;color:var(--sub)}
  .selected{display:none;align-items:center;gap:12px;flex-wrap:wrap;background:var(--accent-soft);border:1px solid var(--accent);border-radius:12px;padding:10px 14px;margin-top:10px}
  .selected .nm{word-break:keep-all}
  .mob-item .nm{word-break:keep-all}
  .mob-item .meta{word-break:keep-all}
  .selected.show{display:flex}
  .selected img{width:48px;height:48px;object-fit:contain;image-rendering:pixelated}
  .selected .nm{font-weight:800;font-size:16.5px}
  .selected .meta{font-size:13px;color:var(--sub)}
  .selected button{margin-left:auto;background:none;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;color:var(--sub);font-size:13px}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  @media (max-width:560px){ .grid2{grid-template-columns:1fr} }
  .calc-btn{width:100%;margin-top:16px;padding:13px;border:none;border-radius:11px;background:var(--accent);color:#fff;font-size:16.5px;font-weight:800;cursor:pointer}
  .result{display:none;margin-top:16px;border-top:1px dashed var(--line);padding-top:14px}
  .result.show{display:block}
  .result .big{font-size:19px;font-weight:800;line-height:1.5}
  .result .big b{color:var(--accent-dark)}
  .result p{font-size:13.5px;color:var(--sub);margin-top:6px;line-height:1.65}
  .err{color:#C0392B;font-size:13.5px;margin-top:8px;display:none}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] section.card{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .mode-badge{background:#3A2A10;color:#FFC94D}
  [data-theme="dark"] .result .big b{color:#FF9E57}
  [data-theme="dark"] .err{color:#FF9B9B}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}
"""

def load_mobs():
    mobs = json.load(open(os.path.join(ROOT, "data/db/mobs.json"), encoding="utf-8"))["mobs"]
    out = []
    for m in mobs:
        if not isinstance(m.get("maxHP"), int) or m["maxHP"] <= 0:
            continue
        out.append({
            "id": m["id"],
            "name": (m.get("name_ko_candidate") or m.get("name_en") or "").strip(),
            "nameEn": (m.get("name_en") or "").strip(),
            "lv": m.get("level"), "hp": m["maxHP"],
        })
    out.sort(key=lambda x: (x["lv"] if isinstance(x["lv"], int) else 999, x["id"]))
    return out

def main():
    mobs = load_mobs()
    data_js = json.dumps(mobs, ensure_ascii=False)
    title = "한방컷 계산기 — 몬스터 HP별 N방컷 예상 범위 | 알팡지지"
    desc = "몬스터 HP와 내가 실제로 때려본 스킬 1회 총피해(최소~최대)를 넣으면 몇 방에 잡을 수 있는지의 예상 범위를 계산합니다. 관측 피해 기준이며, 미검증 공식으로 자동 계산하지 않습니다."
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://alpang.gg/calculator/onehit/">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://alpang.gg/calculator/onehit/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://alpang.gg/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{THEME_INIT}
<style>{CSS}
  .new-dot{{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}}
  .new-dot.on{{display:inline-block}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>
<body>
<div class="wrap">
{GNB}
  <div class="intro">
    <h1>한방컷 <span>계산기</span></h1>
    <div class="tag">몬스터 HP와 내 스킬 1회 총피해로 계산하는 N방컷 예상 범위</div>
    <div class="disclaimer">지금은 직접 때려보고 확인한 피해 범위를 넣는 관측 기준 계산만 제공합니다. 내 스탯·장비와 스킬만으로 한방컷 가능 여부를 판정하는 기능은, 알팡서버의 공식과 수치가 확정되지 않은 지금 열면 확인되지 않은 숫자를 단정하게 되어 제공하지 않습니다.<br>알팡서버 공식 오픈 후 실서버 기준으로 더 상세한 계산 기능을 업데이트할 예정입니다. 몬스터 HP는 본진 메이플스토리 GMS 95 기준 수집값이며 실제 알팡서버와 다를 수 있어요.</div>
  </div>
  <main>
  <section class="card">
    <h2>1. 몬스터 고르기</h2>
    <input type="text" id="mobSearch" placeholder="몬스터 이름·ID 검색 (예: 주황버섯, 100100)" autocomplete="off" aria-label="몬스터 검색">
    <div class="mob-results" id="mobResults" role="listbox"></div>
    <div class="selected" id="mobSelected"></div>
    <label class="fl" for="hpInput">몬스터 HP (몬스터를 고르면 자동 입력, 직접 바꿀 수도 있어요)</label>
    <input type="number" id="hpInput" min="1" inputmode="numeric" placeholder="예: 300">
  </section>
  <section class="card">
    <h2>2. 내 스킬 1회 총피해 입력<span class="mode-badge">관측 피해 기준</span></h2>
    <div class="grid2">
      <div><label class="fl" for="dmgMin" style="margin-top:0">최소 피해 (제일 약하게 들어간 한 방)</label><input type="number" id="dmgMin" min="1" inputmode="numeric" placeholder="예: 120"></div>
      <div><label class="fl" for="dmgMax" style="margin-top:0">최대 피해 (제일 세게 들어간 한 방)</label><input type="number" id="dmgMax" min="1" inputmode="numeric" placeholder="예: 210"></div>
    </div>
    <p style="font-size:13.5px;color:var(--sub);margin-top:10px">여러 번 때려보고 관측한 1회 총피해의 하한과 상한을 넣으세요. 다단히트 스킬은 한 번 시전의 총합 기준입니다. 크리티컬이 섞인 관측값이면 결과도 크리티컬이 섞인 기준이 됩니다.</p>
    <button type="button" class="calc-btn" id="calcBtn">몇 방인지 계산하기</button>
    <p class="err" id="calcErr"></p>
    <div class="result" id="calcResult"></div>
  </section>
  <section class="card">
    <h2>계산 방식 안내</h2>
    <p style="font-size:14.5px;line-height:1.75">최선 = ⌈HP ÷ 최대 피해⌉, 최악 상한 = ⌈HP ÷ 최소 피해⌉ 로 계산하는 <b>관측 피해 기준 예상 범위</b>입니다. 매 타격이 명중하고 몬스터가 회복하지 않는다는 전제가 붙고, 실제 전투에서는 빗나감·크리티컬 분포·방어 등으로 달라질 수 있어 도달을 보장하는 값은 아니에요.<br>공식으로 자동 계산하는 '검증된 이론 범위'는 본진 GMS 95 기준 공식 검증이 끝나기 전까지 제공하지 않습니다.</p>
  </section>
  <section class="card">
    <h2>사용 예시와 한계</h2>
    <h3>이 계산기는 무엇을 계산하나요</h3>
    <p style="font-size:14.5px;line-height:1.75">이 계산기는 스펙으로 피해를 예측하는 도구가 아니에요. 직접 때려 보고 확인한 피해 범위를 넣으면, 몬스터 HP 기준으로 몇 방에 잡을 수 있는지를 범위로 알려 주는 '관측 피해 기준' 계산기예요. 공식을 검증해 자동으로 피해를 계산하는 기능은 제공하지 않습니다.</p>
    <h3>사용 예시 — 결과를 이렇게 읽으세요</h3>
    <p style="font-size:14.5px;line-height:1.75">몬스터를 고르면 그 몬스터의 HP가 자동으로 입력돼요. HP는 본진 GMS 95 기준 수집값이고, 직접 바꿔 넣을 수도 있어요. 여러 번 때려 보고 관측한, 스킬 1회 총피해의 가장 약했던 값(최소)과 가장 셌던 값(최대)을 넣으세요. 결과는 하나의 숫자가 아니라 범위로 나와요. 예를 들어 HP 10,000인 몬스터에 관측 피해가 2,000~3,000이면, 결과는 '4방 ~ 5방'으로 읽어요. HP ÷ 최대 피해 = 최선(10,000 ÷ 3,000 → 4방), HP ÷ 최소 피해 = 최악 상한(10,000 ÷ 2,000 → 5방)이라는 뜻입니다. 가장 세게 들어가는 타격만 이어지면 최선 쪽에 가깝고, 가장 약하게 들어가는 타격만 이어지면 상한 쪽에 가까워요. 최대 피해가 몬스터 HP 이상이면 '한 방(1방)'으로 표시돼요. 이때도 최소 피해 기준으로는 몇 방까지 걸릴 수 있는지를 함께 보여 줍니다.</p>
    <h3>입력할 때의 기준</h3>
    <p style="font-size:14.5px;line-height:1.75"><b>다단히트 스킬</b>은 타격 하나하나가 아니라, 한 번 시전했을 때의 총합 피해가 기준이에요. <b>크리티컬은 별도 입력 칸이 없어요.</b> 크리티컬이 섞인 관측이면, 최대값에 크리티컬 피해를 포함해 넣는 것이 이 도구의 기준입니다. <b>빗나간 타격은 관측값에 넣지 마세요.</b> 이 계산기는 넣은 피해가 매번 명중한다는 전제로 계산합니다.</p>
    <h3>결과의 한계 — 실제와 달라질 수 있는 이유</h3>
    <p style="font-size:14.5px;line-height:1.75">이 범위는 매 타격이 명중하고 몬스터가 회복하지 않는다는 전제의 예상값이에요. 실제 전투에서는 빗나감, 크리티컬 분포, 방어 같은 요소로 실제 방 수가 범위 밖으로 달라질 수 있어요. 결과를 도달 보장으로 읽지 마세요. 계산에 쓰이는 몬스터 HP는 본진 GMS 95 기준값이에요. 알팡 서버의 실제 HP와 다르면 결과도 그만큼 달라집니다. 최소와 최대를 좁게 넣을수록 결과 범위도 좁아지지만, 관측 횟수가 적으면 실제 피해 분포를 다 담지 못할 수 있어요.</p>
    <h3>'미확인' 표시가 보이면</h3>
    <p style="font-size:14.5px;line-height:1.75">몬스터 정보에 '미확인'이라고 표시된 항목은 원본 데이터에서 그 값이 확인되지 않았다는 뜻이에요. 비어 있는 값을 0으로 읽거나, 확인된 값처럼 계산에 기대지 마세요. 확인되지 않은 구간을 이 계산기가 추정으로 메우지는 않아요. 미확인인 몬스터는 HP를 직접 아는 경우에만 직접 입력해서 참고용으로만 쓰세요.</p>
  </section>
  </main>
  <footer>
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    페이지 갱신일: 2026-10-16
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span> <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  </footer>
</div>
{THEME_SCRIPT}
<script src="/assets/hit.js?v=2" defer></script>
<script>
var MOBS = {data_js};
(function () {{
  function norm(s) {{ return (s || '').normalize('NFKC').toLowerCase().replace(/[^0-9a-z가-힣]/g, ''); }}
  var search = document.getElementById('mobSearch'), results = document.getElementById('mobResults'),
      selected = document.getElementById('mobSelected'), hpInput = document.getElementById('hpInput'),
      dmgMin = document.getElementById('dmgMin'), dmgMax = document.getElementById('dmgMax'),
      err = document.getElementById('calcErr'), result = document.getElementById('calcResult');
  function fmt(n) {{ return n.toLocaleString('ko-KR'); }}
  document.addEventListener('error', function (e) {{ if (e.target && e.target.tagName === 'IMG') e.target.style.visibility = 'hidden'; }}, true);
  function icon(id) {{ return 'https://maplestory.io/api/GMS/95/mob/' + id + '/icon'; }}
  function renderList() {{
    var q = norm(search.value);
    if (!q) {{ results.classList.remove('open'); results.innerHTML = ''; return; }}
    var rawQ = search.value.trim();
    var hits;
    if (/^[0-9]+$/.test(rawQ)) {{
      // 숫자 질의: ID 정확 일치 최우선 (통합 검색과 같은 원칙), 뒤이어 ID 접두·이름 일치
      var qNum = parseInt(rawQ, 10);
      var exact = MOBS.filter(function (m) {{ return m.id === qNum; }});
      var rest = MOBS.filter(function (m) {{ return m.id !== qNum && (String(m.id).indexOf(rawQ) === 0 || norm(m.name).indexOf(q) >= 0 || norm(m.nameEn).indexOf(q) >= 0); }});
      hits = exact.concat(rest).slice(0, 12);
    }} else {{
      hits = MOBS.filter(function (m) {{ return norm(m.name).indexOf(q) >= 0 || norm(m.nameEn).indexOf(q) >= 0; }}).slice(0, 12);
    }}
    if (!hits.length) {{ results.innerHTML = '<div style="padding:10px 12px;font-size:14px;color:var(--sub)">찾는 몬스터가 없어요. HP를 직접 입력해도 계산할 수 있습니다.</div>'; results.classList.add('open'); return; }}
    results.innerHTML = hits.map(function (m) {{
      return '<button type="button" class="mob-item" data-id="' + m.id + '"><img src="' + icon(m.id) + '" alt="" loading="lazy"><span><span class="nm">' + m.name + '</span><br><span class="meta">Lv.' + (m.lv != null ? m.lv : '미확인') + ' · HP ' + fmt(m.hp) + ' · ID ' + m.id + '</span></span></button>';
    }}).join('');
    results.classList.add('open');
    Array.prototype.forEach.call(results.querySelectorAll('.mob-item'), function (btn) {{
      btn.addEventListener('click', function () {{
        var m = MOBS.filter(function (x) {{ return x.id === Number(btn.getAttribute('data-id')); }})[0];
        if (!m) return;
        hpInput.value = m.hp;
        selected.innerHTML = '<img src="' + icon(m.id) + '" alt=""><span><span class="nm">' + m.name + '</span><br><span class="meta">Lv.' + (m.lv != null ? m.lv : '미확인') + ' · HP ' + fmt(m.hp) + ' (본진 GMS 95 기준)</span></span><button type="button" id="mobClear">다시 고르기</button>';
        selected.classList.add('show');
        results.classList.remove('open');
        search.value = m.name;
        document.getElementById('mobClear').addEventListener('click', function () {{ selected.classList.remove('show'); selected.innerHTML = ''; search.value = ''; search.focus(); }});
      }});
    }});
  }}
  search.addEventListener('input', renderList);
  document.getElementById('calcBtn').addEventListener('click', function () {{
    var hp = Number(hpInput.value), a = Number(dmgMin.value), b = Number(dmgMax.value);
    function fail(msg) {{ err.textContent = msg; err.style.display = 'block'; result.classList.remove('show'); }}
    function valid(v) {{ return Number.isSafeInteger(v) && v > 0; }}
    if (!valid(hp)) return fail('몬스터 HP는 1 이상의 정수로 입력해 주세요. (비어 있거나 소수·0·음수는 계산할 수 없어요)');
    if (!valid(a) || !valid(b)) return fail('1회 총피해의 최소와 최대는 1 이상의 정수로 입력해 주세요. (소수·0·음수는 계산할 수 없어요)');
    if (b < a) return fail('최대 피해가 최소 피해보다 작아요. 두 값을 바꿔서 확인해 주세요.');
    err.style.display = 'none';
    var best = Math.ceil(hp / b), worst = Math.ceil(hp / a);
    var line = best === worst
      ? '관측한 피해 범위 안에서는 항상 <b>' + best + '방</b>에 잡을 수 있어요.'
      : '관측한 피해 기준 <b>' + best + '방 ~ ' + worst + '방</b> 사이에서 잡을 수 있어요.';
    if (best === 1) line = '관측한 최대 피해 기준 <b>한 방(1방)</b>에 잡을 수 있어요. 최소 피해 기준으로는 <b>' + worst + '방</b>까지 걸릴 수 있어요.';
    result.innerHTML = '<p class="big">' + line + '</p>' +
      '<p>HP ' + fmt(hp) + ' ÷ 최대 피해 ' + fmt(b) + ' = 최선 ' + best + '방 · HP ' + fmt(hp) + ' ÷ 최소 피해 ' + fmt(a) + ' = 최악 상한 ' + worst + '방<br>' +
      '이 범위는 입력한 관측 피해가 매번 명중한다는 전제의 예상값입니다. 빗나감·회복·방어가 있으면 실제 방 수는 달라질 수 있어요.</p>';
    result.classList.add('show');
  }});
}})();
</script>
<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>
</body>
</html>"""
    os.makedirs(os.path.join(SITE, "calculator/onehit"), exist_ok=True)
    path = os.path.join(SITE, "calculator/onehit/index.html")
    open(path, "w", encoding="utf-8").write(html)
    print("onehit built | mobs:", len(mobs), "| bytes:", len(html.encode("utf-8")), "| file:", path)

if __name__ == "__main__":
    main()
