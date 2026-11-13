# -*- coding: utf-8 -*-
"""직업·스킬 도감 빌더 — 입력 고정: 도감 모듈 패키지 ZIP (재패키징본).
기준: 개발담당-설계메모-직업스킬도감-20261017 (§0-1 입력 명세 규칙 포함).
원칙: 한글명 전무 → 영문 원본 표시. max_level은 원문 보존+숫자 정규화, master_level과
분리 표기. null 필드는 표기 자체를 만들지 않는다 (0 채움 금지). 스킬북 미확인 직업 4개는
분리 섹션. 차수 보류 3건은 숫자 없이 '차수 확인 중'. 레지스트리 상태는 원본값 그대로만
표기하고 전개값·계산 결과는 붙이지 않는다. 출력은 별도 프리뷰 디렉터리 (배포 묶음과 분리)."""
import hashlib, json, os, re, shutil, sys, zipfile
import html as H

ROOT = os.path.expanduser("~/workspace/alpang")
ZIP_PATH = os.path.join(ROOT, "deliverables/alpang-guide-module-20261017.zip")
OUT = os.path.join(ROOT, "out-jobs-lineage-rev6-20261027")
EXPECTED_ZIP_SHA256 = "05831fce0d55deaa5e08a6e1ed9e00beb8043334b4459af0e5340367b1b960b3"

raw_zip = open(ZIP_PATH, "rb").read()
zsha = hashlib.sha256(raw_zip).hexdigest()
if zsha != EXPECTED_ZIP_SHA256:
    print(f"ZIP 해시 불일치 — 기대 {EXPECTED_ZIP_SHA256[:16]}…, 실제 {zsha[:16]}…. 재패키징 수령 절차부터 다시 확인할 것.")
    sys.exit(1)

zf = zipfile.ZipFile(ZIP_PATH)
def zread(name):
    return zf.read(name)

# 매니페스트 대조 (icons/ 폴더 항목은 icons-manifest가 담당)
man = json.loads(zread("build-manifest.json").decode("utf-8"))
for e in man["files"]:
    if "file" not in e:
        continue
    data = zread(e["file"])
    if len(data) != e["bytes"] or hashlib.sha256(data).hexdigest() != e["sha256"]:
        print(f"매니페스트 불일치: {e['file']}")
        sys.exit(1)

jobs_doc = json.loads(zread("jobs-for-guide.json").decode("utf-8"))
skills_doc = json.loads(zread("skills-for-guide.json").decode("utf-8"))
lineage_doc = json.loads(zread("lineage-for-guide.json").decode("utf-8"))
tier_doc = json.loads(zread("tier-mapping-table.json").decode("utf-8"))
iman = json.loads(zread("icons-manifest.json").decode("utf-8"))

JOBS = jobs_doc["jobs"]
SKILLS = skills_doc["skills"]

# [이름류 반영 2026-10-21] 데이터 담당 실행 산출의 name_ko 58건을 ID 기준으로 오버레이한다 (원본 ZIP 무변경).
_NAMEKO = json.load(open(os.path.join(ROOT, "data/jobskill-name-apply-output/skills-with-nameko-full-rev6-20261027.json"), encoding="utf-8"))
_NAMEKO_MAP = {s["id"]: s["name_ko"] for s in _NAMEKO["skills"] if s.get("name_ko")}
for _s in SKILLS:
    if _s["id"] in _NAMEKO_MAP:
        _s["name_ko"] = _NAMEKO_MAP[_s["id"]]
print(f"이름 오버레이 적용: {len(_NAMEKO_MAP)}건")

# [설명 표시 연결 2026-11-06] 같은 정본의 description.desc_ko · shortDesc_ko를 ID 기준으로 오버레이한다.
# 정본 1809f198… 기준 desc_ko 601 · shortDesc_ko 595 보유, 결측 9종은 오버레이 없음 (표시 없음이 정상).
_DESCKO_MAP = {}
for _r in _NAMEKO["skills"]:
    _d = _r.get("description") or {}
    if _d.get("desc_ko") or _d.get("shortDesc_ko"):
        _DESCKO_MAP[_r["id"]] = (_d.get("desc_ko"), _d.get("shortDesc_ko"))
for _s in SKILLS:
    if _s["id"] in _DESCKO_MAP:
        _s["desc_ko"], _s["short_desc_ko"] = _DESCKO_MAP[_s["id"]]
print(f"설명 오버레이 적용: {len(_DESCKO_MAP)}건")

# [이름류 반영 2026-10-21 · 전직] 전직 이름 6건 오버레이.
_JOBKO = json.load(open(os.path.join(ROOT, "data/jobskill-name-apply-output/jobs-with-nameko-full-rev6-20261027.json"), encoding="utf-8"))
_JOBKO_MAP = {j["id"]: j["name_ko"] for j in _JOBKO["jobs"] if j.get("name_ko")}
for _j in JOBS:
    if _j["id"] in _JOBKO_MAP:
        _j["name_ko"] = _JOBKO_MAP[_j["id"]]
print(f"전직 이름 오버레이 적용: {len(_JOBKO_MAP)}건")

# [영문명 차수 정정 2026-11-12 건B] 410 어쌔신의 원본 영문명 'Assassin (1st)'는 계보상 오기다 —
# 400 Rogue(1차) → 410 → 411 Hermit(3차) 계열이며 병행 420 Bandit은 (2nd)로 정상 표기된다.
# ZIP 원본의 tier도 held(근거 보류)로 표시돼 있던 항목. 원본 · 정본 JSON 무변경, 빌더에서만 정정한다.
_NAMEEN_FIX = {410: "Assassin (2nd)"}
for _j in JOBS:
    if _j["id"] in _NAMEEN_FIX:
        _j["name_en"] = _NAMEEN_FIX[_j["id"]]
print(f"영문명 정정 적용: {len(_NAMEEN_FIX)}건")

# [tier 확정 반영 2026-11-12] 410 어쌔신 tier=2 확정 (기술이사 판정 — GMS 95 보존 직업 목록 ·
# 넥슨 공식 도적 전직표 근거). 원본 jobs tier는 held, 매핑표 행은 verdict '보류' · name_tier 1(오기 파싱)이라
# 교차 대조를 통과하려면 세 지점을 빌더 메모리에서 함께 확정으로 맞춘다. ZIP · 정본 JSON 무변경.
_TIER_CONFIRM = {410: 2}
for _j in JOBS:
    if _j["id"] in _TIER_CONFIRM:
        _j["tier"] = {"status": "confirmed", "tier": _TIER_CONFIRM[_j["id"]]}
for _r in tier_doc["rows"]:
    if _r["job_id"] in _TIER_CONFIRM:
        _r["verdict"] = f"확정: {_TIER_CONFIRM[_r['job_id']]}차"
        _r["name_tier"] = _TIER_CONFIRM[_r["job_id"]]
print(f"tier 확정 적용: {len(_TIER_CONFIRM)}건")

# [계열 카드 개편 2026-10-24] 계열 23 대응표 (기술이사 검수 통과본)를 그대로 쓴다 — 3층 분리 유지.
_MAP23 = json.load(open(os.path.join(ROOT, "data/stage4-jobs-skills/lineage23-mapping-table-20261024.json"), encoding="utf-8"))
LINEAGES23 = _MAP23["lineages"]
assert len(LINEAGES23) == 23

# [세대 정리 이식 2026-11-12 건5] dual-blade 계열의 그룹 라벨은 라이브 세대의 독립 그룹 표기가 정본이다.
# 매핑표 원본 ('모험가(기획안 22종 외 추가 계열)')은 무변경, 빌더 메모리에서만 라벨을 맞춘다.
_GROUP_LABEL_FIX = {"dual-blade": "듀얼블레이드 (모험가 외전)"}
for _ln in LINEAGES23:
    if _ln["lineage_id"] in _GROUP_LABEL_FIX:
        _ln["group"] = _GROUP_LABEL_FIX[_ln["lineage_id"]]
print(f"그룹 라벨 정정 적용: {len(_GROUP_LABEL_FIX)}건")


def job_disp(j):
    en = j.get("name_en") or ""
    ko = j.get("name_ko")
    return f"{ko} ({en})" if ko else en

def skill_disp(s):
    """스킬 표시명 — name_ko가 있으면 한글 + 영문 병기, 없으면 기존 영문 표시."""
    en = s.get("name_en") or f"이름 없는 스킬 (ID {s['id']})"
    ko = s.get("name_ko")
    return f"{ko} ({en})" if ko else en
JOB = {j["id"]: j for j in JOBS}
SKILL = {s["id"]: s for s in SKILLS}
LINES = lineage_doc["lines"]

# tier 교차 대조: jobs-for-guide의 tier와 tier-mapping-table rows가 어긋나면 중단
TIER_ROW = {}
for r in tier_doc["rows"]:
    TIER_ROW[r["job_id"]] = r
for j in JOBS:
    row = TIER_ROW.get(j["id"])
    if row is None:
        print(f"차수표에 없는 직업: {j['id']}")
        sys.exit(1)
    jt = j.get("tier") or {}
    # 차수표의 판정은 verdict가 담당한다 ('보류 — …' / '확정: …'). name_tier는 이름 파싱값이라
    # 보류 행에도 숫자가 들어 있을 수 있으므로, 보류 판정에 name_tier를 쓰지 않는다.
    held_table = str(row.get("verdict") or "").startswith("보류")
    if held_table != (jt.get("status") == "held"):
        print(f"보류 판정 불일치: 직업 {j['id']} jobs={jt.get('status')} table verdict={row.get('verdict')}")
        sys.exit(1)
    if not held_table and jt.get("status") == "confirmed" and isinstance(jt.get("tier"), int):
        if row.get("name_tier") != jt.get("tier"):
            print(f"차수 불일치: 직업 {j['id']} jobs={jt.get('tier')} table={row.get('name_tier')}")
            sys.exit(1)

# §0-1 입력 명세 가드: 두 필드가 레코드에 키로 존재해야 한다 (통과 실패를 표면화)
for s in SKILLS:
    for key in ("required_skill_levels", "elemental_attribute"):
        if key not in s:
            print(f"스킬 {s['id']}: 입력 명세 필드 누락 {key}")
            sys.exit(1)

# 직업별 스킬 목록
from collections import defaultdict
BY_JOB = defaultdict(list)
for s in SKILLS:
    for jid in s.get("job_ids") or []:
        if jid not in JOB:
            print(f"스킬 {s['id']}: 없는 직업 참조 {jid}")
            sys.exit(1)
        BY_JOB[jid].append(s)
for lst in BY_JOB.values():
    lst.sort(key=lambda x: x["id"])

THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script>"

def gnb():
    a = lambda href, label: f'<a href="{href}">{label}</a>'
    return ('<div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a><nav>'
            + a("/", "홈") + a("/timeline/", '타임라인<span class="new-dot" id="tlNewDot" aria-label="새 글 있음"></span>') + a("/faq/", "FAQ") + a("/mobs/", "몬스터 도감") + a("/maps/", "맵 탐색") + a("/items/", "아이템") + a("/npcs/", "NPC·퀘스트") + '<a href="/jobs/" class="on">직업·스킬</a>' + a("/calculator/cube/", "큐브값 계산기") + a("/calculator/onehit/", "한방컷 계산기") + '</nav>' + THEME_BTN + '</div>')

def norm(s):
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def clean_text(t):
    t = (t or "").replace("\\\\n", " ").replace("\\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", t).strip()

def tier_html(j):
    # 표시 규칙 명세 규칙 1: 차수 표기는 tier.status를 먼저 확인하는 가드를 통과해야 한다.
    # held 3건(410·433·434)은 이름에 (1st) 등 표기가 있어도 숫자 배지를 붙이지 않는다.
    t = j.get("tier") or {}
    if j.get("skillbook_status") == "unconfirmed":
        return '<span class="unk-badge">스킬북 미확인</span>'
    if t.get("status") == "held":
        return '<span class="unk-badge">차수 확인 중</span>'
    if t.get("status") == "confirmed" and isinstance(t.get("tier"), int):
        return f'<span class="tier">{t["tier"]}차</span>'
    return ""

def skill_row(s):
    metas = []
    if isinstance(s.get("max_level"), int):
        metas.append(f'최대 레벨 {s["max_level"]}')
    if s.get("master_level") is not None:
        metas.append(f'마스터 레벨 {s["master_level"]}')
    # 속성 표기 적용 명세 (개정3, 2026-10-17 고정): 코드 원형 병기는 화면에서 제거하고
    # 확정 4종은 표기명 배지로 붙인다. 데이터 원본 코드는 검수·추적용으로 그대로 둔다.
    ATTR_BADGE = {"f": "불", "i": "얼음", "l": "번개", "h": "성"}
    attr = s.get("elemental_attribute")
    if attr in ATTR_BADGE:
        metas.append(f'<span class="attr-badge">{ATTR_BADGE[attr]}</span>')
    # s 코드: '독' 배지는 스킬 단위 근거(설명에 독 명시)가 있는 2101005·2111003만 붙이고,
    # 그 외 s 보유 스킬(2121006)은 의미를 추정하지 않고 코드 원형으로 표기한다 (기술이사 판정 2026-10-17).
    if s["id"] in (2101005, 2111003):
        metas.append('<span class="attr-badge">독</span>')
    elif attr == "s":
        metas.append('<span class="attr-code">속성 코드 s (원본)</span>')
    if s.get("weapons"):
        metas.append('사용 가능 무기 코드 ' + '·'.join(str(w) for w in s["weapons"]) + ' (원본 표기)')
    pre = []
    unc_ids = set(s.get("unconfirmed_prerequisite_ids") or [])
    for pid_s, lv in (s.get("required_skill_levels") or {}).items():
        pid = int(pid_s)
        if pid in unc_ids:
            continue  # 미수집 참조는 아래 unconfirmed 경로에서만 렌더 (맵 경로와 중복 방지)
        ps = SKILL.get(pid)
        if ps is not None:
            # 이름 없는 스킬 9개 판정 (원본 자체 이름 없음) — 폴백 라벨은 설계 메모 §3-1 고정안
            pname = skill_disp(ps)
            pre.append(f'<a class="ptag" href="#skill-{pid}">{H.escape(pname)} Lv.{lv} 필요</a>')
        else:
            pre.append(f'<span class="ptag unknown">선행 스킬 {pid} (미확인)</span>')
    req_map = s.get("required_skill_levels") or {}
    for pid in s.get("unconfirmed_prerequisite_ids") or []:
        lv = req_map.get(str(pid))
        lv_txt = f' Lv.{lv} 필요' if isinstance(lv, int) else ''
        pre.append(f'<span class="ptag unknown">선행 스킬 {pid}{lv_txt} (미확인 — 원본 미수집)</span>')
    pre_html = f'<div class="pre"><span class="pre-label">선행 스킬</span>{"".join(pre)}</div>' if pre else ""
    # [세대 정리 이식 2026-11-12 건1] reg 문단 (수식 상태 레지스트리 표기)은 라이브 세대에서 전건 제거된
    # 세대가 정본이다 — 생성하지 않는다. registry_statuses 데이터 자체는 무변경 (표시만 제거).
    reg_html = ""
    desc = clean_text(s.get("desc"))
    short = clean_text(s.get("short_desc"))
    desc_ko = clean_text(s.get("desc_ko"))
    short_ko = clean_text(s.get("short_desc_ko"))
    return (f'<div class="skill" id="skill-{s["id"]}">'
            f'<img class="sicon" src="/assets/skill-icons/{s["id"]}.png" alt="" loading="lazy" width="32" height="32">'
            f'<div class="sbody"><div class="shead"><span class="sname">{H.escape(skill_disp(s))}</span>'
            + (f'<span class="smeta">{" · ".join(metas)}</span>' if metas else "")
            + '</div>'
            + (f'<p class="sdesc">{H.escape(desc)}</p>' if desc else "")
            + (f'<p class="sdesc-ko">{H.escape(desc_ko)}</p>' if desc_ko else "")
            + (f'<p class="sshort">{H.escape(short)}</p>' if short else "")
            + (f'<p class="sshort-ko">{H.escape(short_ko)}</p>' if short_ko else "")
            + pre_html + reg_html + '</div></div>')

def job_card(j, anchor=True):
    jid = j["id"]
    skills = BY_JOB.get(jid, [])
    id_attr = f' id="job-{jid}"' if anchor else ""
    lines_tags = "".join(f'<span class="ltag">{H.escape(x)}</span>' for x in (j.get("lineages") or []))
    base = '<span class="tier base">기본 직업</span>' if j.get("is_base") else ""
    search_txt = (norm(j.get("name_en")) + "|" + "|".join(norm(s.get("name_en")) for s in skills)
                  + "|" + str(jid) + "|" + "|".join(str(s["id"]) for s in skills))
    skills_html = "".join(skill_row(s) for s in skills)
    return (f'<article class="job-card"{id_attr} data-search="{H.escape(search_txt)}">'
            f'<div class="jhead"><h3>{H.escape(job_disp(j))}</h3>{tier_html(j)}{base}'
            f'<span class="jcount">스킬 {len(skills)}개</span></div>'
            + (f'<div class="ltags">{lines_tags}</div>' if lines_tags else "")
            + (f'<details class="skills"><summary>스킬 목록 펼치기</summary>{skills_html}</details>' if skills else "")
            + '</article>')

def build():
    conf = [j for j in JOBS if j.get("skillbook_status") != "unconfirmed"]
    unc = [j for j in JOBS if j.get("skillbook_status") == "unconfirmed"]
    # 계열 섹션: 대응표 23계열을 카드 그리드로 (템플릿 설계 2026-10-24 골격)
    def short_disp(j):
        return j.get("name_ko") or j.get("name_en") or ""
    group_order = []
    for ln in LINEAGES23:
        if ln["group"] not in group_order:
            group_order.append(ln["group"])
    filter_btns = ['<button type="button" data-g="all" aria-pressed="true">전체</button>']
    filter_btns += [f'<button type="button" data-g="{H.escape(g)}" aria-pressed="false">{H.escape(g)}</button>' for g in group_order]
    line_sections = [f'<div class="filterbar" role="group" aria-label="소속 필터">{"".join(filter_btns)}</div>']
    grouped = {g: [ln for ln in LINEAGES23 if ln["group"] == g] for g in group_order}
    for g, lns in grouped.items():
        cards23 = []
        for ln in lns:
            ids = ln["stage_job_ids"]
            steps = []
            for i, jid in enumerate(ids):
                j = JOB.get(jid)
                if j is None:
                    continue
                label = H.escape(short_disp(j))
                if j.get("skillbook_status") == "unconfirmed":
                    label += " (미확인)"
                cls = "step final" if i == len(ids) - 1 else "step"
                steps.append(f'<li><a class="{cls}" href="#job-{jid}">{label}</a></li>')
            last = JOB.get(ids[-1])
            lname = H.escape(short_disp(last)) if last else H.escape(ln["lineage_id"])
            cards23.append(
                f'<article class="lcard" id="lineage-{ln["lineage_id"]}" data-group="{H.escape(g)}">'
                f'<div class="lthumb"><img src="/assets/lineage/{ln["lineage_id"]}.webp" alt="" width="80" height="80" loading="lazy" onerror="this.remove()"></div>'
                f'<div class="lbody"><div class="lhead"><span class="lgroup">{H.escape(g)}</span>'
                f'<span class="lname">{lname}</span></div>'
                f'<ol class="lsteps">{"".join(steps)}</ol></div></article>')
        line_sections.append(f'<h2 class="grp">{H.escape(g)}</h2><div class="lgrid">{"".join(cards23)}</div>')
    # 직업 상세: ID 오름차순, 카드+스킬
    cards = "\n".join(job_card(j) for j in sorted(conf, key=lambda x: x["id"]))
    # A안 (2026-10-17 확정): 실패 스킬북 4직업은 접이식 섹션에 간략 카드로 두고 앵커를 심는다.
    # 간략 카드는 미확인 고지일 뿐 내용 대체가 아니다 — 스킬 목록·상세를 만들지 않는다.
    def unc_card(j):
        tags = "".join(f'<span class="ltag">{H.escape(x)}</span>' for x in (j.get("lineages") or []))
        return (f'<article class="job-card unc-card" id="job-{j["id"]}">'
                f'<div class="jhead"><h3>{H.escape(job_disp(j))}</h3>'
                f'<span class="unk-badge">스킬북 미확인</span><span class="uid">ID {j["id"]}</span></div>'
                + (f'<div class="ltags">{tags}</div>' if tags else "")
                + '</article>')
    unc_items = "\n".join(unc_card(j) for j in sorted(unc, key=lambda x: x["id"]))
    body = f"""
  <div class="intro">
    <h1>직업·스킬 <span>도감</span></h1>
    <div class="tag">직업 {len(JOBS)}개와 스킬 {len(SKILLS)}개의 전직 계열·조건 정리</div>
    <div class="disclaimer">본진 빅뱅 직후(GMS 95) 기준 데이터이며 알팡서버 실서버와 다를 수 있습니다. 한글 이름은 표시명 후보입니다. 알팡서버 공식 오픈 시 해당 버전에 맞춰 상세 정보를 업데이트할 예정입니다. 직업·스킬 이름은 한글 이름과 영문 원본을 함께 표기합니다. 한글 이름에는 대조 출처 표기와 자체 번역이 섞여 있어, 실제 알팡서버의 이름·내용과 다를 수 있어요.<br>아이콘·이미지: maplestory.io</div>
  </div>
  <div class="filters">
    <input type="text" id="jobSearch" placeholder="직업·스킬 이름(영문)·ID 검색" aria-label="직업·스킬 검색" autocomplete="off">
    <p class="fcount" id="jobCount"></p>
  </div>
  <section class="lines">
{chr(10).join(line_sections)}
  </section>
  <h2 class="grp">직업별 스킬</h2>
  <main class="job-list" id="jobList">
{cards}
  </main>
  <p class="empty" id="jobEmpty" hidden>조건에 맞는 직업이 없어요.</p>
  <button type="button" class="qmore" id="jobMore" hidden>더 보기</button>
  <details class="unc-box">
    <summary>스킬북 미확인 직업 {len(unc)}개 (원본에서 수집되지 않은 항목)</summary>
    <p class="unc-note">스킬북 원본 미확인 — 원천 서버 오류로 수집되지 않은 스킬북입니다. 하위 단계 데이터로 대체하지 않습니다.</p>
{unc_items}
  </details>
  <p class="reg cap-note">수식 상태 표기는 수식 문법의 분류일 뿐, 피해 계산 결과나 정확성을 뜻하지 않습니다. 레벨별 전개값은 검증이 끝난 뒤에 단계적으로 붙입니다.</p>
<script>
(function () {{
  var q = '';
  var cards = Array.prototype.slice.call(document.getElementById('jobList').children),
      count = document.getElementById('jobCount'), empty = document.getElementById('jobEmpty');
  function norm(s) {{ return (s || '').normalize('NFKC').toLowerCase().replace(/[^0-9a-z가-힣]/g, ''); }}
  function apply() {{
    var shown = 0;
    cards.forEach(function (c) {{
      var ok = !q || c.getAttribute('data-search').indexOf(q) >= 0;
      c.style.display = ok ? '' : 'none';
      if (ok) shown++;
    }});
    count.textContent = shown.toLocaleString('ko-KR') + '개 직업 표시 중';
    empty.hidden = shown > 0;
  }}
  document.getElementById('jobSearch').addEventListener('input', function () {{ q = norm(this.value); apply(); }});
  apply();
}})();
</script>
<script>
(function () {{
  var PAGE = 50, limit = PAGE;
  var list = document.getElementById('jobList');
  var more = document.getElementById('jobMore');
  if (!list || !more) return;
  var cards = Array.prototype.slice.call(list.children).filter(function (c) {{ return c.classList.contains('job-card'); }});
  function applyPaging() {{
    cards.forEach(function (c) {{ if (c.getAttribute('data-pg') === '1') {{ c.style.display = ''; c.removeAttribute('data-pg'); }} }});
    var passed = cards.filter(function (c) {{ return c.style.display !== 'none'; }});
    var visible = 0;
    passed.forEach(function (c, i) {{
      if (i >= limit) {{ c.style.display = 'none'; c.setAttribute('data-pg', '1'); }}
      else visible++;
    }});
    if (passed.length <= visible) {{ more.hidden = true; }}
    else {{ more.hidden = false; more.textContent = '더 보기 (남은 ' + (passed.length - visible).toLocaleString('ko-KR') + '건)'; }}
  }}
  more.addEventListener('click', function () {{ limit += PAGE; applyPaging(); }});
  document.addEventListener('input', function () {{ limit = PAGE; setTimeout(applyPaging, 0); }});
  document.addEventListener('click', function () {{ setTimeout(applyPaging, 0); }});
  if (location.hash) {{
    var target = document.getElementById(location.hash.slice(1));
    if (target) {{
      var card = target.classList.contains('job-card') ? target : (target.closest ? target.closest('.job-card') : null);
      if (card) {{ var ti = cards.indexOf(card); if (ti >= limit) limit = ti + 1; }}
    }}
  }}
  applyPaging();
}})();
</script>
<script>
(function () {{
  var bar = document.querySelector('.filterbar');
  if (!bar) return;
  var cards = Array.prototype.slice.call(document.querySelectorAll('.lcard'));
  var heads = Array.prototype.slice.call(document.querySelectorAll('section.lines .grp'));
  function setGroup(g) {{
    bar.querySelectorAll('button').forEach(function (b) {{ b.setAttribute('aria-pressed', b.getAttribute('data-g') === g ? 'true' : 'false'); }});
    cards.forEach(function (c) {{ c.style.display = (g === 'all' || c.getAttribute('data-group') === g) ? '' : 'none'; }});
    heads.forEach(function (h) {{ h.style.display = (g === 'all' || h.textContent === g) ? '' : 'none'; }});
    document.querySelectorAll('section.lines .lgrid').forEach(function (gr) {{
      var any = Array.prototype.some.call(gr.children, function (c) {{ return c.style.display !== 'none'; }});
      gr.style.display = any ? '' : 'none';
    }});
  }}
  bar.addEventListener('click', function (e) {{
    var b = e.target.closest('button'); if (!b) return;
    setGroup(b.getAttribute('data-g'));
  }});
  // 딥링크 도착 시 필터가 대상을 가리지 않게 전체로 되돌린다
  function unlock() {{ if (/^#(job|skill|lineage)-/.test(location.hash)) setGroup('all'); }}
  window.addEventListener('hashchange', unlock);
  unlock();
}})();
</script>"""

    return page(body)

def provenance():
    # 입력 식별 기록 (데이터 담당 3 정식 보완 항목): 산출물만으로 입력 패키지와 빌더를 대조할 수 있게 한다.
    import datetime
    self_path = os.path.abspath(__file__)
    self_sha = hashlib.sha256(open(self_path, "rb").read()).hexdigest()
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    return (f"<!-- alpang-build-provenance\n"
            f"  input-package: deliverables/alpang-guide-module-20261017.zip sha256={zsha}\n"
            f"  builder: jobs_skills_build.py sha256={self_sha}\n"
            f"  built-at: {now}\n-->")

def page(body):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
{provenance()}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>직업·스킬 도감 — 알팡지지</title>
<meta name="description" content="알팡서버를 기다리며 정리한 직업·스킬 도감. 직업 90개와 스킬 610개의 전직 계열과 조건을 본진 GMS 95 기준으로 모았습니다.">
<link rel="canonical" href="https://alpang.gg/jobs/">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="직업·스킬 도감 — 알팡지지">
<meta property="og:description" content="알팡서버를 기다리며 정리한 직업·스킬 도감. 직업 90개와 스킬 610개의 전직 계열과 조건을 본진 GMS 95 기준으로 모았습니다.">
<meta property="og:url" content="https://alpang.gg/jobs/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://alpang.gg/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{THEME_INIT}
<style>{CSS}
  /* 타이틀 패턴 (2026-11-04) */
.intro{{background-color:#faf9f6;background-image:image-set(url("/assets/title-bg/title-bg-common.webp") type("image/webp"),url("/assets/title-bg/title-bg-common.png") type("image/png"));background-size:cover;background-position:center;background-repeat:no-repeat}}

/* 패턴 다크 톤다운 (2026-11-04) */
[data-theme="dark"] .intro{{background-image:linear-gradient(rgba(18,19,22,.90),rgba(18,19,22,.90)),image-set(url("/assets/title-bg/title-bg-common.webp") type("image/webp"),url("/assets/title-bg/title-bg-common.png") type("image/png"))}}
@media (max-width:640px){{[data-theme="dark"] .intro{{background-image:linear-gradient(rgba(18,19,22,.90),rgba(18,19,22,.90)),image-set(url("/assets/title-bg/title-bg-common-mobile.webp") type("image/webp"),url("/assets/title-bg/title-bg-common-mobile.png") type("image/png"))}}}}}}@media (max-width:640px){{[data-theme="dark"] .intro{{background-image:linear-gradient(rgba(18,19,22,.90),rgba(18,19,22,.90)),image-set(url("/assets/title-bg/title-bg-common-mobile.webp") type("image/webp"),url("/assets/title-bg/title-bg-common-mobile.png") type("image/png"))}}}}
.new-dot{{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}}
  .new-dot.on{{display:inline-block}}

.sentence-block{{margin:8px 0 4px;padding:10px 12px;background:var(--accent-soft,#FFF1E8);border-radius:8px}}

.sentence-block p{{margin:0 0 4px;font-size:14.5px}}

.sentence-block .rc{{color:var(--accent-dark,#B65100);font-weight:700}}

.sentence-detail{{margin-top:6px}}

.sentence-detail summary{{cursor:pointer;font-size:13px;font-weight:700;color:var(--accent-dark,#B65100)}}

.sentence-detail table{{width:100%;border-collapse:collapse;margin:6px 0 2px;font-size:13px}}

.sentence-detail th,.sentence-detail td{{border-top:1px solid var(--line,#e6e1d8);padding:5px 6px;text-align:left}}

.sentence-detail th{{width:34%;color:var(--sub,#6f6a5e);white-space:nowrap}}

.tscroll{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}}

.tscroll-hint{{display:block;text-align:right;font-size:11px;color:var(--sub);margin-bottom:4px}}

.twrap{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
.twrap>table{{margin:0}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>
<body>
<div class="wrap">
{gnb()}
{body}
  <footer>
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    페이지 갱신일: 2026-10-17
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  </footer>
</div>
{THEME_SCRIPT}
<script src="/assets/hit.js?v=1" defer></script>
<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>
<button type="button" class="topbtn" id="topBtn" aria-label="맨 위로 이동">↑ Top</button><script>(function(){{var b=document.getElementById('topBtn');if(!b)return;addEventListener('scroll',function(){{b.classList.toggle('on',scrollY>600)}},{{passive:true}});b.addEventListener('click',function(){{scrollTo({{top:0,behavior:'smooth'}})}});}})();</script>
</body>
</html>"""

CSS = """
  :root{--bg:#faf9f6;--card:#ffffff;--line:#e6e1d8;--text:#1f1c18;--sub:#6f6a5e;--accent:#FF7E36;--accent-dark:#C25700;--accent-soft:#FFF1E8;--unknown:#6b6250;--slot:#f3f0e9}
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
  /* 모바일: sticky GNB가 nav 줄바꿈으로 높아져(약 118px) 앵커 제목이 가려지는 문제 —
     헤더 실측 최대 높이 + 여유를 반영한 여백 (기술이사 검수 2026-10-17) */

  .intro{text-align:center;padding:28px 0 16px}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .disclaimer{font-size:13.5px;color:var(--sub);text-align:center;margin-top:8px;line-height:1.65}
  .filters{margin-top:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
  .filters input{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text);font-size:15px;outline:none}
  .filters input:focus{border-color:var(--accent)}
  .fcount{font-size:12.5px;color:var(--sub);margin-top:8px}
  .grp{font-size:19px;font-weight:800;margin:22px 0 4px}
  .filterbar{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 6px}
  .filterbar button{font:inherit;font-size:14px;font-weight:700;padding:7px 14px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--text);cursor:pointer}
  .filterbar button[aria-pressed="true"]{background:#FF6B00;border-color:#FF6B00;color:#fff}
  .lgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px}
  @media (max-width:900px){.lgrid{grid-template-columns:repeat(2,1fr)}}
  @media (max-width:560px){.lgrid{grid-template-columns:1fr}}
  .lcard{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;min-height:110px;box-sizing:border-box;scroll-margin-top:90px}
  .lthumb{flex:0 0 80px;width:80px;height:80px;aspect-ratio:1/1;border-radius:10px;background:transparent;border:none;display:flex;align-items:center;justify-content:center;overflow:hidden}
  .lthumb img{width:80px;height:80px;object-fit:contain}
  .lbody{flex:1;min-width:0}
  .lhead{display:flex;align-items:center;gap:8px;margin-bottom:8px}
  .lgroup{font-size:11.5px;font-weight:800;padding:2px 8px;border-radius:999px;background:var(--accent-soft);color:#FF6B00}
  .lname{font-size:16.5px;font-weight:800}
  .lsteps{display:flex;flex-wrap:wrap;gap:5px;list-style:none;margin:0;padding:0}
  .step{display:inline-block;font-size:13px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--bg);border:1px solid var(--line);color:var(--text);text-decoration:none}
  .step.final{background:#FF6B00;border-color:#FF6B00;color:#fff;font-weight:800}
  .line-box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 14px;margin-top:8px}
  .line-name{font-size:15px;font-weight:800;color:var(--accent-dark)}
  .jchips{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:6px;font-size:13px;color:var(--sub)}
  .jchip{background:var(--slot);border-radius:6px;padding:3px 9px;color:var(--text);text-decoration:none;font-weight:600}
  .jchip.unknown{background:transparent;border:1px dashed var(--line);color:var(--sub)}
  .job-list{display:flex;flex-direction:column;gap:10px;margin-top:10px}
  .job-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;scroll-margin-top:90px}
  .job-card:target{outline:2px solid var(--accent);outline-offset:1px}
  .jhead{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  .jhead h3{font-size:17px;font-weight:800}
  .tier{font-size:11.5px;font-weight:800;background:var(--accent);color:#fff;border-radius:4px;padding:2px 7px}
  .tier.base{background:#7A6A53}
  .unk-badge{font-size:10.5px;font-weight:700;color:var(--unknown);background:var(--slot);border-radius:4px;padding:2px 6px;white-space:nowrap}
  .jcount{font-size:12.5px;color:var(--sub);margin-left:auto}
  .ltags{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}
  .ltag{font-size:12px;background:var(--accent-soft);color:var(--accent-dark);border-radius:6px;padding:2px 8px;font-weight:600}
  .skills{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}
  .skills summary{cursor:pointer;font-size:13.5px;font-weight:700;color:var(--accent-dark)}
  .skill{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid var(--line);scroll-margin-top:90px}
  .skill:last-child{border-bottom:none}
  .skill:target{background:var(--accent-soft);border-radius:8px}
  .sicon{width:32px;height:32px;object-fit:contain;image-rendering:pixelated;flex:none}
  .sbody{flex:1;min-width:0}
  .shead{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}
  .sname{font-size:15px;font-weight:800}
  .smeta{font-size:12.5px;color:var(--sub)}
  .attr-badge{font-size:11px;font-weight:800;background:#5B8C5A;color:#fff;border-radius:4px;padding:1px 6px}
  .attr-code{font-size:11px;font-weight:700;background:var(--slot);color:var(--sub);border-radius:4px;padding:1px 6px}
  .sdesc{font-size:13.5px;color:var(--text);line-height:1.6;margin-top:2px}
  .sdesc-ko{font-size:13.5px;color:var(--text);line-height:1.6;margin-top:2px}
  .sshort{font-size:12.5px;color:var(--sub);line-height:1.55}
  .sshort-ko{font-size:12.5px;color:var(--sub);line-height:1.55}
  .pre{display:flex;flex-wrap:wrap;gap:5px;align-items:center;margin-top:5px}
  .pre-label{font-size:11.5px;font-weight:700;color:var(--sub)}
  .ptag{font-size:12px;background:var(--slot);border-radius:6px;padding:2px 8px;color:var(--text);text-decoration:none}
  .ptag.unknown{color:var(--sub);border:1px dashed var(--line);background:transparent}
  .reg{font-size:11.5px;color:var(--unknown);margin-top:4px}
  .cap-note{margin-top:16px}
  .empty{text-align:center;color:var(--sub);padding:30px 0}
  .qmore{display:block;margin:14px auto 4px;font:inherit;font-size:14.5px;font-weight:700;padding:10px 26px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer}
  .unc-box{margin-top:18px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px}
  .unc-box summary{cursor:pointer;font-weight:700;font-size:14.5px}
  .unc-note{font-size:13px;color:var(--sub);margin-top:8px;line-height:1.6}
  .unc-card{margin-top:10px;scroll-margin-top:90px}
  .unc-card:target{outline:2px solid var(--accent);outline-offset:1px}
  .unc-card .uid{color:var(--sub);font-size:11.5px;margin-left:auto}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;--slot:#26292F;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  @media (max-width:720px){ .job-card,.skill,.unc-card{scroll-margin-top:170px} }

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .topbtn{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--accent);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-size:13px;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .18s}
  .topbtn.on{opacity:1;pointer-events:auto}
  .jhead{position:sticky;top:73px;z-index:30;background:var(--card);padding:6px 0}
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "jobs"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/skill-icons"), exist_ok=True)
    html_out = build()
    open(os.path.join(OUT, "jobs/index.html"), "w", encoding="utf-8").write(html_out)
    # 아이콘 복사 + icons-manifest 대조
    icon_bad = []
    for e in iman["files"]:
        fn = os.path.basename(e.get("file") or e.get("name"))
        data = zread(f"icons/{fn}")
        if (e.get("bytes") is not None and len(data) != e["bytes"]) or (e.get("sha256") and hashlib.sha256(data).hexdigest() != e["sha256"]):
            icon_bad.append(fn)
            continue
        open(os.path.join(OUT, "assets/skill-icons", fn), "wb").write(data)
    if icon_bad:
        print("아이콘 해시 불일치:", icon_bad[:5])
        sys.exit(1)
    print("jobs built | bytes:", len(html_out.encode("utf-8")), "| jobs:", len(JOBS), "| skills:", len(SKILLS),
          "| icons copied:", len(iman["files"]), "| 선행 보유:", sum(1 for s in SKILLS if s.get("required_skill_levels")),
          "| 속성 보유:", sum(1 for s in SKILLS if s.get("elemental_attribute") is not None))
