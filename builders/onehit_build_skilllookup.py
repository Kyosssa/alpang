# -*- coding: utf-8 -*-
# 편입 사본 (2026-10-20): 한방컷 페이지에 스킬 수치 조회 층 A(기술이사 r5 승인본)를 편입한 사본. 정본 onehit_build.py는 무변경.
# 편입 데이터·평가기는 skill-lookup/package-r5 동결 실물을 해시 대조 후에만 쓰고, 산출은 staging-skilllookup-deploy로 나간다.
"""한방컷 계산기 (1차 범위) — 승인 몬스터 175종 HP 검색 + 실측 피해 수동 입력 → 조건부 N회 범위.
기술이사 확정 범위(research/onehit-formula-review-2026-10-16.md): 미검증 공식 자동 계산 금지,
임의 상수 채우기 금지. 이 페이지는 사용자가 실측한 1회 총피해 하한/상한으로만 계산한다."""
import json, os, html as H

ROOT = os.path.expanduser("~/workspace/alpang")
SITE = os.path.join(ROOT, "site")
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
  .cta-row{display:flex;flex-direction:column;gap:8px;margin-top:12px}
  .cta-btn{display:flex;align-items:center;justify-content:center;min-height:48px;padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text);font-size:14.5px;font-weight:700;text-decoration:none;cursor:pointer}
  .cta-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
  @media (max-width:640px){.cta-cards{grid-template-columns:1fr}}
  .cta-card{display:block;border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none;color:var(--text);background:var(--card)}
  .cta-card b{display:block;font-size:15.5px;margin-bottom:4px}
  .cta-card span{font-size:13px;color:var(--sub)}
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
  .lk-form{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
  @media (max-width:560px){ .lk-form{grid-template-columns:1fr} }
  .lk-result{display:none;margin-top:16px;border-top:1px dashed var(--line);padding-top:14px;font-size:14.5px;line-height:1.7}
  .lk-result.show{display:block}
  .lk-result .muted{color:var(--sub);font-size:13.5px}
  .lk-result code{background:var(--accent-soft);padding:1px 6px;border-radius:5px;font-size:13.5px}
"""

LOOKUP_DIR = os.path.join(ROOT, "skill-lookup", "package-r5")
LOOKUP_SHA = "17b8b265a378acccbedd36ec7c18503c3e4d705b6c23b4c5438db74157e2dbee"
EVAL_SHA = "71b828dedfb283af001521fdcaf97caf2e71f2739fbee24573dbfb4253cbdfe7"

LK_SECTION = """  <section class="card" data-stage="1" id="skillLookup">
    <h2>스킬 수치 조회<span class="mode-badge">원본 수치 조회</span></h2>
    <p style="font-size:14.5px;line-height:1.75">직업의 <b>전 스킬</b>을 골라 조회합니다. 원본 설명에 데미지 수식이 있는 스킬은 <b>수식과 그 산술값</b>을, 없는 스킬은 이름·최대 레벨·원문 설명만 보여줍니다. 예상 피해를 계산하는 도구가 아니며, 여기서 x는 스킬 레벨입니다. 수치는 본진 GMS 95 기준 자료로 maplestory.io를 경유해 수집됐고, 알팡서버 실서버의 수치와 다를 수 있습니다. 조회 결과는 위 관측 입력칸에 자동으로 들어가지 않습니다.</p>
    <div class="lk-form" style="margin-top:12px">
      <div><label class="fl" for="lkJob" style="margin-top:0">직업</label><select id="lkJob"></select></div>
      <div><label class="fl" for="lkSkill" style="margin-top:0">스킬</label><select id="lkSkill"></select></div>
      <div><label class="fl" for="lkLv" style="margin-top:0">스킬 레벨</label><input type="number" id="lkLv" step="1" value="1" inputmode="numeric"></div>
    </div>
    <button type="button" class="calc-btn" id="lkGo">수치 조회하기</button>
    <div class="lk-result" id="lkResult"></div>
  </section>
"""

LK_LOGIC = """
(function () {
  var ALL = {};
  DATA.labeled.forEach(function (r) { ALL[r.skill_id] = Object.assign({label: true}, r); });
  DATA.unlabeled.forEach(function (r) { ALL[r.skill_id] = Object.assign({label: false}, r); });
  (typeof ALL_SKILLS !== 'undefined' ? ALL_SKILLS : []).forEach(function (s) { if (!ALL[s.id]) { ALL[s.id] = {skill_id: s.id, jobs: s.jobs, plain: true, max_level: s.max_level, desc: s.desc}; } });
  var jobs = [...new Set(Object.values(ALL).flatMap(function (r) { return r.jobs; }))].sort(function (a, b) { return a - b; });
  var jobSel = document.getElementById('lkJob'), skillSel = document.getElementById('lkSkill');
  var lvInput = document.getElementById('lkLv'), resultBox = document.getElementById('lkResult');
  jobs.forEach(function (j) { var o = document.createElement('option'); o.value = j; o.textContent = JOB_NAMES[j] || ('직업 ' + j); jobSel.appendChild(o); });
  function fillSkills() {
    skillSel.innerHTML = '';
    Object.values(ALL).filter(function (r) { return r.jobs.includes(Number(jobSel.value)); }).forEach(function (r) {
      var o = document.createElement('option'); o.value = r.skill_id;
      o.textContent = (SKILL_NAMES[r.skill_id] || r.name || ('스킬 ' + r.skill_id)) + (r.plain ? ' (수식 정보 없음)' : (r.label ? '' : ' (원본 수치·단위 미확인)'));
      skillSel.appendChild(o);
    });
  }
  function invalidate() {
    resultBox.innerHTML = '<p class="muted">선택이 바뀌었습니다. 조회 버튼을 눌러 주세요.</p>';
    resultBox.classList.add('show');
  }
  jobSel.addEventListener('change', function () { fillSkills(); invalidate(); });
  skillSel.addEventListener('change', invalidate);
  lvInput.addEventListener('input', invalidate);
  lvInput.addEventListener('change', invalidate);
  fillSkills();
  document.getElementById('lkGo').addEventListener('click', function () {
    resultBox.innerHTML = '';
    var r = ALL[Number(skillSel.value)];
    var lv = Number(lvInput.value);
    if (r.plain) {
      div.innerHTML = '<b>' + (SKILL_NAMES[r.skill_id] || r.skill_id) + '</b><br>' +
        '<span class="muted">이 스킬은 원본 설명에 데미지 수식이 없어 수치 조회 대상이 아닙니다.' + (r.max_level ? ' 최대 레벨 ' + r.max_level + '.' : '') + (r.desc ? '<br>원문 설명: ' + r.desc : '') + '</span>';
      resultBox.appendChild(div); resultBox.classList.add('show'); return;
    }
    var div = document.createElement('div');
    var src = '<br><span class="muted">스킬 ID ' + r.skill_id + ' · 단위 근거: ' + r.unit_basis +
      '<br>원문 설명: ' + (r.desc_text || r.short_desc || '(원문 설명 없음)') + '</span>';
    if (!r.label) {
      div.innerHTML = '<b>' + (SKILL_NAMES[r.skill_id] || r.name || r.skill_id) + '</b><br>상태: 원본 수치·단위 미확인<br><span class="muted">' +
        r.status_reason + '</span><br>원본 수식: <code>' + r.expression + '</code>' + src;
      resultBox.appendChild(div); resultBox.classList.add('show'); return;
    }
    var res = evaluate(r.expression, lv, r.level_range);
    if (!res.ok) {
      div.innerHTML = '<b>계산 불가</b><br><span style="color:#C0392B">사유: ' + res.reason + '</span><br>원본 수식: <code>' + r.expression + '</code>' + src;
      resultBox.appendChild(div); resultBox.classList.add('show'); return;
    }
    div.innerHTML = '<b>' + (SKILL_NAMES[r.skill_id] || r.name || r.skill_id) + '</b> · 스킬 레벨 ' + lv + '<br>' +
      '원본 설명상 데미지: <b>' + res.value + '%</b><br>' +
      '원본 수식: <code>' + r.expression + '</code> (x = 스킬 레벨)<br>' +
      (r.attack_count != null ? '원본 타수 표기: ' + r.attack_count + ' (조회값에 곱하지 않습니다)<br>' : '') +
      '<span class="muted">이 수치는 원본 설명의 수치이며 실제 피해 배율이 아닙니다. 타수는 원본에 표기가 있는 경우만 표시합니다.</span>' + src;
          '<div class="cta-row"><a class="cta-btn" href="/jobs/">이 스킬의 직업 도감 보기</a><a class="cta-btn" href="/calculator/cube/">큐브값 계산기</a></div>';
        resultBox.appendChild(div); resultBox.classList.add('show');
  });
})();
"""

# ---------- 2단계 계산 블록 (2026-11-11 역이식 + 모드 토글) ----------
S2_CSS = '  .s2-badge{display:inline-block;font-size:11.5px;font-weight:700;color:var(--accent-dark);background:var(--accent-soft);border:1px solid var(--accent);border-radius:999px;padding:2px 9px;margin-left:8px;vertical-align:middle}\n  .s2-tag{display:inline-block;font-size:11px;font-weight:600;color:var(--sub);background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-left:5px;vertical-align:middle}\n  .s2-modes{display:flex;gap:8px;margin:10px 0}\n  .s2-modes button{flex:1;min-height:42px;border:1px solid var(--line);border-radius:10px;background:var(--card);font-size:14px;font-weight:600;cursor:pointer;color:var(--sub)}\n  .s2-modes button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}\n  .s2-cutline{font-size:17px;margin:8px 0;line-height:1.6}\n  .s2-cutline b{color:var(--accent-dark)}\n  .s2-cannot{color:var(--unknown);font-size:15px;line-height:1.7}\n  .s2-slot{border:1.5px dashed var(--line);border-radius:12px;padding:18px;text-align:center;color:var(--sub);font-size:14.5px;line-height:1.7;background:var(--bg)}\n'
S2_SECTIONS = '  <section class="card" data-stage="2" id="stage2">\n    <h2>2단계 계산<span class="s2-badge">GMS 95 기준 · 알팡서버 실제 구현 미확인</span></h2>\n    <p style="font-size:14.5px;line-height:1.75">시전당 피해를 직접 입력하면 방 수를 확정 계산합니다. 범위(최소·최대)로 입력하면 가능 컷과 보장 컷을 나눠 보여줍니다.</p>\n    <h3 style="margin-top:16px">몬스터</h3>\n    <input type="text" id="s2MobSearch" placeholder="몬스터 이름·ID 검색 (예: 주황버섯, 100100)" autocomplete="off" aria-label="2단계 몬스터 검색">\n    <div class="mob-results" id="s2MobResults"></div>\n    <div class="selected" id="s2SelInfo" style="display:none"></div>\n    <label class="fl" style="margin-top:12px">HP 직접 입력 (데이터 HP를 대신합니다)\n      <input type="number" id="s2HpInput" min="1" placeholder="비워 두면 선택한 몬스터의 데이터 HP 사용">\n    </label>\n  </section>\n  <section class="card" data-stage="2">\n    <h2>시전당 피해 입력</h2>\n    <div class="s2-modes" role="group" aria-label="피해 입력 방식">\n      <button type="button" id="s2ModeFixed" aria-pressed="true">고정값</button>\n      <button type="button" id="s2ModeRange" aria-pressed="false">범위 (최소·최대)</button>\n    </div>\n    <div id="s2FixedWrap">\n      <label class="fl">시전당 피해 (고정값)\n        <input type="number" id="s2DmgFixed" min="1" placeholder="예: 1,250">\n      </label>\n    </div>\n    <div id="s2RangeWrap" style="display:none">\n      <div class="grid2">\n        <label class="fl">최소 피해\n          <input type="number" id="s2DmgMin" min="1" placeholder="예: 900">\n        </label>\n        <label class="fl">최대 피해\n          <input type="number" id="s2DmgMax" min="1" placeholder="예: 1,100">\n        </label>\n      </div>\n    </div>\n    <div class="s2-modes" role="group" aria-label="피해 값의 성격" style="max-width:340px">\n      <button type="button" id="s2KindObs" aria-pressed="true">관측값</button>\n      <button type="button" id="s2KindAssume" aria-pressed="false">가정</button>\n    </div>\n    <p style="font-size:13px;color:var(--sub)">직접 때려보고 잰 값이면 \'관측값\', 예상으로 넣는 값이면 \'가정\'을 골라 주세요. 결과에 그대로 표시됩니다.</p>\n    <button type="button" id="s2CalcBtn" style="margin-top:12px">계산하기</button>\n  </section>\n  <section class="card" data-stage="2">\n    <h2>2단계 결과<span class="s2-badge">GMS 95 기준 · 알팡서버 실제 구현 미확인</span></h2>\n    <div id="s2Result"><p class="s2-cannot">몬스터를 선택하고 시전당 피해를 입력하면 결과가 표시됩니다.</p></div>\n  </section>\n  <section class="card" data-stage="2">\n    <h2>스펙 자동 계산</h2>\n    <div class="s2-slot">스펙으로 시전당 피해를 자동 계산하는 기능은 준비 중입니다.<br>지금은 시전당 피해를 직접 입력해 주세요.</div>\n  </section>\n'
S2_JS = '<script>\n(function () {\n  var M = window.MOBS || [];\n  var sel = null, mode = \'fixed\', kind = \'관측값\';\n  var $ = function (id) { return document.getElementById(id); };\n  var search = $(\'s2MobSearch\'), results = $(\'s2MobResults\'), selInfo = $(\'s2SelInfo\');\n  var result = $(\'s2Result\');\n  function fmt(n) { return n.toLocaleString(\'ko-KR\'); }\n  function clearResult(msg) {\n    result.innerHTML = \'<p class="s2-cannot">\' + msg + \'</p>\';\n  }\n  function invalidate() { clearResult(\'조건이 바뀌었습니다. 다시 계산해 주세요.\'); }\n  function norm(s) { return (s || \'\').normalize(\'NFKC\').toLowerCase().replace(/\\s+/g, \'\'); }\n  search.addEventListener(\'input\', function () {\n    var q = norm(search.value);\n    results.innerHTML = \'\';\n    if (!q) { results.classList.remove(\'open\'); return; }\n    var hits = M.filter(function (m) {\n      return norm(m.name).includes(q) || norm(m.nameEn || \'\').includes(q) || String(m.id).includes(q);\n    }).slice(0, 8);\n    hits.forEach(function (m) {\n      var d = document.createElement(\'div\');\n      d.className = \'mob-item\';\n      d.innerHTML = \'<span class="nm">\' + m.name + \'</span> <span class="meta">Lv.\' + m.lv + \' · HP \' + (m.hp != null ? fmt(m.hp) : \'미확인\') + \'</span>\';\n      d.addEventListener(\'click\', function () {\n        sel = m;\n        selInfo.style.display = \'\';\n        selInfo.textContent = m.name + \' (Lv.\' + m.lv + \') · HP \' + (m.hp != null ? fmt(m.hp) : \'미확인\');\n        results.classList.remove(\'open\');\n        invalidate();\n      });\n      results.appendChild(d);\n    });\n    results.classList.toggle(\'open\', hits.length > 0);\n  });\n  function setMode(m) {\n    mode = m;\n    $(\'s2ModeFixed\').setAttribute(\'aria-pressed\', String(m === \'fixed\'));\n    $(\'s2ModeRange\').setAttribute(\'aria-pressed\', String(m === \'range\'));\n    $(\'s2FixedWrap\').style.display = m === \'fixed\' ? \'\' : \'none\';\n    $(\'s2RangeWrap\').style.display = m === \'range\' ? \'\' : \'none\';\n    invalidate();\n  }\n  $(\'s2ModeFixed\').addEventListener(\'click\', function () { setMode(\'fixed\'); });\n  $(\'s2ModeRange\').addEventListener(\'click\', function () { setMode(\'range\'); });\n  function setKind(k, obsBtn, assumeBtn) {\n    kind = k;\n    obsBtn.setAttribute(\'aria-pressed\', String(k === \'관측값\'));\n    assumeBtn.setAttribute(\'aria-pressed\', String(k === \'가정\'));\n    invalidate();\n  }\n  $(\'s2KindObs\').addEventListener(\'click\', function () { setKind(\'관측값\', $(\'s2KindObs\'), $(\'s2KindAssume\')); });\n  $(\'s2KindAssume\').addEventListener(\'click\', function () { setKind(\'가정\', $(\'s2KindObs\'), $(\'s2KindAssume\')); });\n  [\'s2HpInput\', \'s2DmgFixed\', \'s2DmgMin\', \'s2DmgMax\'].forEach(function (id) {\n    $(id).addEventListener(\'input\', invalidate);\n  });\n  $(\'s2CalcBtn\').addEventListener(\'click\', function () {\n    if (!sel) { clearResult(\'계산 불가 — 몬스터를 먼저 선택해 주세요.\'); return; }\n    var hpDirect = parseInt($(\'s2HpInput\').value, 10);\n    var hp, hpTag;\n    if (!isNaN(hpDirect) && hpDirect > 0) { hp = hpDirect; hpTag = \'사용자 입력\'; }\n    else if (sel.hp != null) { hp = sel.hp; hpTag = \'GMS 95 데이터\'; }\n    else { clearResult(\'계산 불가 — 몬스터 HP가 확인되지 않았습니다. HP를 아는 경우 직접 입력해 주세요.\'); return; }\n    var dmgTag = \'<span class="s2-tag">사용자 입력</span><span class="s2-tag">\' + kind + \'</span>\';\n    var hpTagHtml = \'<span class="s2-tag">\' + hpTag + \'</span>\';\n    if (mode === \'fixed\') {\n      var dmg = parseInt($(\'s2DmgFixed\').value, 10);\n      if (isNaN(dmg) || dmg <= 0) { clearResult(\'계산 불가 — 시전당 피해가 필요합니다.\'); return; }\n      var n = Math.ceil(hp / dmg);\n      var rest = hp - dmg * (n - 1);\n      result.innerHTML =\n        \'<p class="s2-cutline"><b>\' + n + \'회</b> 시전으로 처치합니다.</p>\' +\n        \'<p style="font-size:14.5px;line-height:1.75">HP \' + fmt(hp) + hpTagHtml + \' ÷ 시전당 피해 \' + fmt(dmg) + dmgTag + \'<br>\' +\n        \'마지막 1회 직전 잔여 HP는 \' + fmt(rest) + \'이며, 이 잔여분에 시전 1회로 처치합니다.</p>\';\n      result.innerHTML += \'<div class="cta-row"><a class="cta-btn" href="/mobs/#mob-\' + sel.id + \'">\' + (n === 1 ? \'이 몬스터가 나오는 맵 보기\' : \'이 몬스터 도감에서 보기\') + \'</a><a class="cta-btn" href="/calculator/cube/">\' + (n === 1 ? \'큐브값 계산기로 내 무기 값 확인\' : \'부족분을 큐브값으로 가늠하기\') + \'</a></div>\';\n    } else {\n      var mn = parseInt($(\'s2DmgMin\').value, 10), mx = parseInt($(\'s2DmgMax\').value, 10);\n      if (isNaN(mn) || isNaN(mx) || mn <= 0 || mx <= 0) { clearResult(\'계산 불가 — 최소·최대 피해가 모두 필요합니다.\'); return; }\n      if (mn > mx) { clearResult(\'입력 오류 — 최소 피해가 최대 피해보다 큽니다. 값을 확인해 주세요.\'); return; }\n      var possible = Math.ceil(hp / mx), guaranteed = Math.ceil(hp / mn);\n      result.innerHTML =\n        \'<p class="s2-cutline">가능 컷 <b>\' + possible + \'회</b> — 최대 피해 \' + fmt(mx) + dmgTag + \' 가 계속 나올 때의 하한입니다.</p>\' +\n        \'<p class="s2-cutline">보장 컷 <b>\' + guaranteed + \'회</b> — 최소 피해 \' + fmt(mn) + dmgTag + \' 만 나와도 보장되는 상한입니다.</p>\' +\n        \'<p style="font-size:14.5px;line-height:1.75">기준 HP \' + fmt(hp) + hpTagHtml + \'</p>\';\n      result.innerHTML += \'<div class="cta-row"><a class="cta-btn" href="/mobs/#mob-\' + sel.id + \'">\' + (possible === 1 ? \'이 몬스터가 나오는 맵 보기\' : \'이 몬스터 도감에서 보기\') + \'</a><a class="cta-btn" href="/calculator/cube/">\' + (possible === 1 ? \'큐브값 계산기로 내 무기 값 확인\' : \'부족분을 큐브값으로 가늠하기\') + \'</a></div>\';\n    }\n  });\n})();\n</script>\n</body>\n</html>\n<script>\n(function () {\n  var tabs = document.querySelectorAll(\'.mode-tabs button\');\n  tabs.forEach(function (b) {\n    b.addEventListener(\'click\', function () {\n      document.body.dataset.mode = b.dataset.setMode;\n      tabs.forEach(function (x) { x.setAttribute(\'aria-pressed\', x === b ? \'true\' : \'false\'); });\n    });\n  });\n})();\n</script>\n'
MODE_TABS = '  <div class="mode-tabs" role="group" aria-label="계산 모드 전환">\n    <button type="button" data-set-mode="1" aria-pressed="true">1단계 · 관측 피해 계산</button>\n    <button type="button" data-set-mode="2" aria-pressed="false">2단계 · GMS 95 기준 계산</button>\n  </div>\n'

def inject_stage2(html):
    html = html.replace('</style>', S2_CSS + '\n</style>', 1)
    anchor = '  <section class="card" data-stage="1" id="skillLookup">'
    assert anchor in html
    html = html.replace(anchor, S2_SECTIONS + anchor, 1)
    html = html.replace('</body>', S2_JS + '</body>', 1)
    return html

def inject_lookup(html):
    import hashlib
    raw_data = open(os.path.join(LOOKUP_DIR, "lookup-data.json"), "rb").read()
    raw_eval = open(os.path.join(LOOKUP_DIR, "safe-eval.js"), "rb").read()
    if hashlib.sha256(raw_data).hexdigest() != LOOKUP_SHA:
        raise SystemExit("편입 중단 — lookup-data.json 해시가 동결 연결값과 다릅니다")
    if hashlib.sha256(raw_eval).hexdigest() != EVAL_SHA:
        raise SystemExit("편입 중단 — safe-eval.js 해시가 동결 연결값과 다릅니다")
    data = json.loads(raw_data.decode("utf-8"))
    payload = json.dumps({"labeled": data["supported_label"], "unlabeled": data["unlabeled"]}, ensure_ascii=False)
    # 직업 표시명 맵 (2026-11-10 정정): 정본 직업 페이지(jobs)의 카드 표기를 그대로 쓴다 — 한글 단독, 영문 병기 없음.
    job_names = json.load(open(os.path.join(ROOT, "data/job-names-for-lookup.json"), encoding="utf-8"))
    # 스킬 한글명 + 전 스킬 목록 (2026-11-10 A안 확장): 정본 스킬 데이터(rev6) 전 601종을 조회 목록에 편입한다.
    # 수식 보유 스킬은 기존 수치 조회, 없는 스킬은 이름·최대 레벨·원문 설명만 표시한다 (수치 단정 금지 원칙 유지).
    _sk = json.load(open(os.path.join(ROOT, "data/jobskill-name-apply-output/skills-with-nameko-full-rev6-20261027.json"), encoding="utf-8"))["skills"]
    SKILL_NAMES = {}
    ALL_SKILLS = []
    for _s in _sk:
        _ko = (_s.get("name_ko") or "").strip()
        if _ko:
            SKILL_NAMES[str(_s["id"])] = _ko
        _d = _s.get("description") or {}
        _desc = (_d.get("desc") or "") if isinstance(_d, dict) else ""
        try:
            _ml = int(_s.get("max_level") or 0)
        except Exception:
            _ml = 0
        ALL_SKILLS.append({"id": _s["id"], "jobs": [int(b) for b in (_s.get("books") or [])], "max_level": _ml, "desc": _desc})
    _lkids = {r["skill_id"] for r in data["supported_label"] + data["unlabeled"]}
    ALL_SKILLS = [s for s in ALL_SKILLS if s["id"] not in _lkids]
    script = "<script>\n" + raw_eval.decode("utf-8") + "\n</script>\n<script>\nconst DATA = " + payload + ";\nconst JOB_NAMES = " + json.dumps(job_names, ensure_ascii=False) + ";\nconst SKILL_NAMES = " + json.dumps(SKILL_NAMES, ensure_ascii=False) + ";\nconst ALL_SKILLS = " + json.dumps(ALL_SKILLS, ensure_ascii=False) + ";" + LK_LOGIC + "</script>"
    anchor = '  <section class="card" data-stage="1">\n    <h2>계산 방식 안내</h2>'
    assert anchor in html
    html = html.replace(anchor, LK_SECTION + anchor, 1)
    html = html.replace("페이지 갱신일: 2026-10-16", "페이지 갱신일: 2026-10-20", 1)
    sig = '<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>\n'
    html = html.replace("</body>", sig + script + "\n</body>", 1)
    return html

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
  body[data-mode="1"] [data-stage="2"]{{display:none}}
  body[data-mode="2"] [data-stage="1"]{{display:none}}
  .mode-tabs{{display:flex;gap:8px;margin:0 0 14px}}
  .mode-tabs button{{flex:1;min-height:44px;border:1px solid var(--line);border-radius:10px;background:var(--card);font-size:14.5px;font-weight:700;cursor:pointer;color:var(--sub)}}
  .mode-tabs button[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:#fff}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>
<body data-mode="1">
<div class="wrap">
{GNB}
  <div class="intro">
    <h1>한방컷 <span>계산기</span></h1>
    <div class="tag">몬스터 HP와 내 스킬 1회 총피해로 계산하는 N방컷 예상 범위</div>
    <div class="disclaimer">지금은 직접 때려보고 확인한 피해 범위를 넣는 관측 기준 계산만 제공합니다. 내 스탯·장비와 스킬만으로 한방컷 가능 여부를 판정하는 기능은, 알팡서버의 공식과 수치가 확정되지 않은 지금 열면 확인되지 않은 숫자를 단정하게 되어 제공하지 않습니다.<br>알팡서버 공식 오픈 후 실서버 기준으로 더 상세한 계산 기능을 업데이트할 예정입니다. 몬스터 HP는 본진 메이플스토리 GMS 95 기준 수집값이며 실제 알팡서버와 다를 수 있어요.</div>
  </div>
  <main>
{MODE_TABS}  <section class="card" data-stage="1">
    <h2>1. 몬스터 고르기</h2>
    <input type="text" id="mobSearch" placeholder="몬스터 이름·ID 검색 (예: 주황버섯, 100100)" autocomplete="off" aria-label="몬스터 검색">
    <div class="mob-results" id="mobResults" role="listbox"></div>
    <div class="selected" id="mobSelected"></div>
    <label class="fl" for="hpInput">몬스터 HP (몬스터를 고르면 자동 입력, 직접 바꿀 수도 있어요)</label>
    <input type="number" id="hpInput" min="1" inputmode="numeric" placeholder="예: 300">
  </section>
  <section class="card" data-stage="1">
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
  <section class="card" data-stage="1">
    <h2>계산 방식 안내</h2>
    <p style="font-size:14.5px;line-height:1.75">최선 = ⌈HP ÷ 최대 피해⌉, 최악 상한 = ⌈HP ÷ 최소 피해⌉ 로 계산하는 <b>관측 피해 기준 예상 범위</b>입니다. 매 타격이 명중하고 몬스터가 회복하지 않는다는 전제가 붙고, 실제 전투에서는 빗나감·크리티컬 분포·방어 등으로 달라질 수 있어 도달을 보장하는 값은 아니에요.<br>공식으로 자동 계산하는 '검증된 이론 범위'는 본진 GMS 95 기준 공식 검증이 끝나기 전까지 제공하지 않습니다.</p>
  </section>
  <section class="card" data-stage="1">
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
  <section class="card">
    <h2>관련 도구</h2>
    <div class="cta-cards">
      <a class="cta-card" href="/calculator/cube/"><b>큐브값 계산기</b><span>큐브를 돌렸을 때의 기대값을 계산해요</span></a>
      <a class="cta-card" href="/mobs/"><b>몬스터 도감</b><span>몬스터의 레벨·HP와 출현 맵을 확인해요</span></a>
      <a class="cta-card" href="/jobs/"><b>직업·스킬 도감</b><span>직업별 스킬 구성을 확인해요</span></a>
    </div>
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
  var selId = null;
  function ctaRow(oneHit) {{
    var h = '<div class="cta-row">';
    if (selId) h += '<a class="cta-btn" href="/mobs/#mob-' + selId + '">' + (oneHit ? '이 몬스터가 나오는 맵 보기' : '이 몬스터 도감에서 보기') + '</a>';
    h += '<a class="cta-btn" href="/calculator/cube/">' + (oneHit ? '큐브값 계산기로 내 무기 값 확인' : '부족분을 큐브값으로 가늠하기') + '</a>';
    h += '<button type="button" class="cta-btn cta-again">다른 몬스터로 다시 계산</button></div>';
    return h;
  }}
  result.addEventListener('click', function (e) {{ if (e.target && e.target.classList && e.target.classList.contains('cta-again')) {{ window.scrollTo(0, 0); search.focus(); }} }});
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
        selId = m.id;
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
    result.innerHTML = '<p class="big">' + line + '</p>' + ctaRow(best === 1) +
      '<p>HP ' + fmt(hp) + ' ÷ 최대 피해 ' + fmt(b) + ' = 최선 ' + best + '방 · HP ' + fmt(hp) + ' ÷ 최소 피해 ' + fmt(a) + ' = 최악 상한 ' + worst + '방<br>' +
      '이 범위는 입력한 관측 피해가 매번 명중한다는 전제의 예상값입니다. 빗나감·회복·방어가 있으면 실제 방 수는 달라질 수 있어요.</p>';
    result.classList.add('show');
  }});
}})();
</script>
</body>
</html>"""
    html = inject_lookup(html)
    html = inject_stage2(html)
    out_dir = os.path.join(ROOT, "staging-skilllookup-deploy", "calculator", "onehit")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    open(path, "w", encoding="utf-8").write(html)
    print("onehit+skilllookup built | mobs:", len(mobs), "| bytes:", len(html.encode("utf-8")), "| file:", path)

if __name__ == "__main__":
    main()
