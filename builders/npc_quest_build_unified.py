# -*- coding: utf-8 -*-
# 본 빌드 사본 (2026-10-20): 합본(채택 19 + [Unknown] 7) 기준 + NPC 로딩 개선 확정 규칙 — 분할 200장 정적 + 나머지 분리 파일, 첫 상호작용(더 보기·검색·필터·딥링크)에 전량 삽입, 표시는 200 단위, 초기 카운트 총수는 빌드 상수(TOTAL_ALL)로 표기.
"""NPC·퀘스트 도감 빌더 — 입력 고정: 0700 승인본 (stage2-npc-quest/out).
기준표: data/data2-expansion/qa-baseline-0700 (입력 해시·필터 수치·dangling 109).
앵커 기준 (정정본): NPC 1,968 (본 목록 1,836 + 상세 미확인 섹션 132) + 퀘스트 3,412 = 5,380.
원칙: 상세 미확인 NPC 132는 카드를 만들지 않되 접이식 섹션 항목에 npc-{id} 앵커는 부여한다
(계획-003 A안, anchors.json 정정). 관련 퀘스트 정의는 퀘스트 상세의 requirement npcId
역참조 (기준표 649 정의). dangling 참조와 자기 참조는 링크 없이 미확인·자기 참조로 표기."""
import json, os, re, html as H

ROOT = os.path.expanduser("~/workspace/alpang")
SITE = os.path.join(ROOT, os.environ.get("ALPANG_OUT", "site"))
SRC = os.path.join(ROOT, "data/stage2-npc-quest/out")

THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script><script>function imgRetry(el){el.onerror=function(){imgHide(el)};el.src=el.src}function imgHide(el){el.style.visibility='hidden'}</script>"

def gnb(active):
    def a(href, label):
        return f'<a href="{href}"' + (' class="on"' if href == active else '') + f'>{label}</a>'
    return ('<div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a><nav>'
            + a("/", "홈") + a("/timeline/", '타임라인<span class="new-dot" id="tlNewDot" aria-label="새 글 있음"></span>') + a("/faq/", "FAQ") + a("/mobs/", "몬스터 도감") + a("/maps/", "맵 탐색") + a("/items/", "아이템") + a("/npcs/", "NPC·퀘스트") + a("/jobs/", "직업·스킬") + a("/calculator/cube/", "큐브값 계산기") + a("/calculator/onehit/", "한방컷 계산기") + '</nav>' + THEME_BTN + '</div>')

def norm(s):
    s = (s or "").lower()
    return re.sub(r"[^0-9a-z가-힣]", "", s)

UNKNOWN_NAME = "[이름 미확인]"
# [Unknown] 7자리 표시 수정안 (기술이사 반영 승인 2026-10-20) — 승인 원본은 보존하고 표시용 파생에만 적용.
# 자리 지정 오버라이드: (NPC id, 슬롯, 토큰 종류, 대상 id) -> 표시값. 지정 자리 밖은 건드리지 않는다.
NAME_OVERRIDES_CLOSED = {
    (2040018, "d1", "o", 4230116): "Barnard Gray",
    (1012102, "d0", "o", 2220100): "파란버섯",
    (1012102, "d1", "o", 2220100): "파란버섯",
    (1032100, "d1", "o", 3210100): "[Unknown]",
    (1032101, "d1", "o", 4230101): "[Unknown]",
    (2103, "d0", "m", 1010000): "[Unknown]",
}
# 불완전 토큰(닫는 '#' 없음) 자리 — 닫힌 토큰 치환과 겹쳐 처리하지 않고 이 자리에서만 확정한다.
NAME_OVERRIDES_INCOMPLETE = {
    (1010100, "d1", "p", 1012102): "피아",
}
CLEANSE_PROTECT = "\u0001"
# 조사 문장 단위 예외 (JOSA-DECISION-FINAL 확정 5건 — 치환된 이름 바로 뒤에 해당 조사가 붙은 경우만 고친다.
# 현행 원문은 영문이라 적용 자리가 없고, 한글 대사가 들어오면 같은 표로 걸린다)
JOSA_EXCEPTIONS = {
    (2102, "d1"): ("센", "를", "을"),
    (1040001, "d0"): ("얼음 조각", "는", "은"),
    (1040001, "d1"): ("얼음 조각", "는", "은"),
    (2010000, "d1"): ("고대문서 조각", "는", "은"),
    (2030001, "d1"): ("고대문서 조각", "는", "은"),
}

def _ref_name(kind, rid):
    """참조 토큰 치환 소스 (확정본: 승인본 전량 치환). 없거나 이름이 비면 None."""
    if kind == "p":
        n = NPC.get(rid)
        return npc_display(n)[0] if n is not None else None
    if kind == "m":
        return MAP_NAME_FULL.get(rid) or None
    if kind == "o":
        return MOB_NAME.get(rid) or None
    if kind == "t":
        return ITEM_NAME.get(rid) or None
    return None

def clean_dialogue(text, npc_id=None, dkey=None, stats=None):
    # 확정 처리 순서 (DIALOGUE-CLEANSE-RULES-FINAL — 데이터 순서 정본):
    # 1 참조 토큰(#p/#m/#o/#t) 치환 (불완전 토큰 포함) → 2 ## 보호 → 3 제어 문자 위치 무관 제거 → 4 ## 복원.
    # 변수 토큰(#h #)은 전 단계에서 건드리지 않는다. stats를 주면 게이트 A 집계에 쓴다.
    t = text or ""
    def sub_ref(m):
        kind, rid = m.group(1), int(m.group(2))
        override = NAME_OVERRIDES_CLOSED.get((npc_id, dkey, kind, rid))
        if override is not None:
            if stats is not None:
                stats["total"] += 1
                stats.setdefault("override", []).append(f"#{kind}{rid}→{override}")
            return override
        name = _ref_name(kind, rid)
        if stats is not None:
            stats["total"] += 1
            if name:
                stats["ok"] += 1
            else:
                stats["fail"].append(f"#{kind}{rid}")
        return name if name else UNKNOWN_NAME
    t = re.sub(r"#([pmot])(\d+)#", sub_ref, t)
    def sub_incomplete(m):
        # 닫는 '#'가 없는 토큰: 확정본 §4대로 [이름 미확인] 처리하고 원본 결함으로 별도 집계
        # 단, 자리 지정 오버라이드가 있는 불완전 자리는 그 자리에서만 확정값으로 표시한다
        override = NAME_OVERRIDES_INCOMPLETE.get((npc_id, dkey, m.group(1), int(m.group(2))))
        if override is not None:
            if stats is not None:
                stats["incomplete"].append(f"#{m.group(1)}{m.group(2)}")
                stats.setdefault("override", []).append(f"#{m.group(1)}{m.group(2)}(불완전)→{override}")
            return override
        if stats is not None:
            stats["incomplete"].append(f"#{m.group(1)}{m.group(2)}")
        return UNKNOWN_NAME
    t = re.sub(r"#([pmot])(\d+)(?![#\d])", sub_incomplete, t)
    t = t.replace("##", CLEANSE_PROTECT)
    t = re.sub(r"#[bkrgenc]", "", t)
    if stats is not None:
        for m in re.finditer(r"#([a-zA-Z])", t):
            if m.group(1) != "h":
                stats["unknown"].append("#" + m.group(1))
    t = t.replace(CLEANSE_PROTECT, "#")
    t = t.replace("\\n", " ").replace("\r", " ")
    t = re.sub(r"\s+", " ", t).strip()
    exc = JOSA_EXCEPTIONS.get((npc_id, dkey))
    if exc:
        nm, wrong, right = exc
        if nm + wrong in t:
            t = t.replace(nm + wrong, nm + right, 1)
    return t

# ---------- 데이터 로드 ----------
npcs_raw = json.load(open(os.path.join(SRC, "npcs.json"), encoding="utf-8"))["npcs"]

# ── 대사 한글화 정본 우선안 A 병합 — 재적용 시범 사본 (2026-10-20, 데이터 담당) ──
# 본 빌드(로딩 분할) 구조 위에 정본 파생 파일 병합만 얹은 시범. 원본 빌더 무변경.
import copy as _copy
_dlg_apply = json.load(open(os.path.join(ROOT, os.environ.get("ALPANG_DIALOGUE_IN", "localization/dialogue-ko-apply.json")), encoding="utf-8"))["npcs"]
_dlg_merged = 0
for _n in npcs_raw:
    _a = _dlg_apply.get(str(_n["id"]))
    if _a is not None:
        _n["dialogue"] = _copy.deepcopy(_a.get("dialogue") or {})
        _dlg_merged += 1
print("dialogue A-merge (loadfinal pilot) | merged NPCs:", _dlg_merged)
quests_raw = json.load(open(os.path.join(ROOT, os.environ["ALPANG_QUESTS_IN"]), encoding="utf-8"))["quests"] if os.environ.get("ALPANG_QUESTS_IN") else json.load(open(os.path.join(SRC, "quests.json"), encoding="utf-8"))["quests"]
maps_db = json.load(open(os.path.join(ROOT, "data/db/maps.json"), encoding="utf-8"))["maps"]
items_db = json.load(open(os.path.join(ROOT, "data/db/items.json"), encoding="utf-8"))["items"]
mobs_db = json.load(open(os.path.join(ROOT, "data/db/mobs.json"), encoding="utf-8"))["mobs"]
jobs_db = json.load(open(os.path.join(ROOT, "data/stage4-jobs-skills/out/jobs.json"), encoding="utf-8"))["jobs"]

NPC = {n["id"]: n for n in npcs_raw}
# 채택 표시명 오버라이드 (잔존 1건) (대표 채택 확정 2026-10-20, 준비본 NPC-NAME-ADOPTED-19-PREP.json be046f35…)
# 9270013 '쇼와 메이플TV'는 정본 채택 완료 (자체 구성 표기 — 기술이사 게이트 채택 2026-11-03)로 2026-11-03 정식 정리에서 제외 — 정본 status를 빌더가 덮지 않는다.
# 출처: 플래닛헬퍼 표시명 (건별 조회 2026-10-20). '공식 이름'·'실측 검증 완료'가 아닌 채택 표시명으로 반영한다.
# 영문명·기존 상태 필드는 원본 그대로 두고 표시용 이름 필드만 이 19건에 채운다. 동결 132건·기존 한글명 NPC는 대상이 아니다.
# 잔존분 전체 정리 (2026-11-05, 정본 a26f7f95… 대조): 정본 채택값과 일치하는 17건은 제거 (정본이 기준, 제거해도 화면 불변).
# 잔존 1건 9110106은 오버라이드 '안즈'와 정본 채택값 '안즈 공주'가 달라 판단 지점으로 유지한다.
ADOPT_RESIDUAL = {9110106: '안즈'}
for _nid, _ko in ADOPT_RESIDUAL.items():
    if _nid in NPC:
        # 재발 방지 가드 (2026-11-03): 정본 status가 이미 게이트 채택 계열이면 오버라이드로 덮지 않는다
        if "게이트 채택" in (NPC[_nid].get("name_ko_status") or ""):
            continue
        NPC[_nid]["name_ko_candidate"] = _ko
        NPC[_nid]["name_ko_status"] = "candidate"
QUEST = {q["id"]: q for q in quests_raw}

# ── 퀘스트 NPC display override (명세 e14c6c41… · 대장 data/quest-npc-display-override.json)
# 원본 quests.json은 수정하지 않는다 — 로드된 표시용 사본의 지정 fieldpath만 치환한다.
# 기대 토큰이 실제 값에 없으면 그 건은 적용하지 않고 불일치로 수집한다 (추측 치환 금지).
import copy as _copy, re as _re
OVERRIDE_WARNINGS = []
def _apply_quest_display_override(_quests):
    try:
        _spec = json.load(open(os.path.join(ROOT, "data/quest-npc-display-override.json"), encoding="utf-8"))
    except Exception:
        return
    _by_id = {q["id"]: q for q in _quests}
    for _row in _spec["rows"]:
        _q = _by_id.get(_row["quest"])
        if _q is None:
            OVERRIDE_WARNINGS.append(f"override 대상 퀘스트 부재: {_row['quest']}")
            continue
        _tok, _disp = _row["token"], _row["display"]
        # 단어 경계 + 소유격 + 서식 토큰(#b · #k) 경계를 이름 경계로 취급한다 (명세 규칙)
        _pat = _re.compile(r"(^|[^A-Za-z]|#[A-Za-z])(" + _re.escape(_tok) + r")(?![A-Za-z])")
        def _sub(_val):
            if not isinstance(_val, str) or not _pat.search(_val):
                return None
            return _pat.sub(lambda m: m.group(1) + _disp, _val)
        for _path in _row["paths"]:
            if _path == "name":
                for _key in ("name_en",):
                    _new = _sub(_q.get(_key))
                    if _new is None:
                        OVERRIDE_WARNINGS.append(f"override 불일치: {_row['quest']} name — 기대 토큰 '{_tok}' 없음")
                    else:
                        _q[_key] = _new
                _d = _q.get("detail") or {}
                if isinstance(_d.get("name"), str):
                    _new = _sub(_d["name"])
                    if _new is not None:
                        _d["name"] = _new
            else:
                _idx = int(_path[len("messages["):-1])
                _msgs = (_q.get("detail") or {}).get("messages") or []
                if _idx < len(_msgs):
                    _new = _sub(_msgs[_idx])
                    if _new is None:
                        OVERRIDE_WARNINGS.append(f"override 불일치: {_row['quest']} messages[{_idx}] — 기대 토큰 '{_tok}' 없음")
                    else:
                        _msgs[_idx] = _new
                else:
                    OVERRIDE_WARNINGS.append(f"override 불일치: {_row['quest']} messages[{_idx}] — 항목 부재")
_apply_quest_display_override(quests_raw)
if OVERRIDE_WARNINGS:
    print("[override] 불일치 " + str(len(OVERRIDE_WARNINGS)) + "건:", *OVERRIDE_WARNINGS, sep="\n  ")
CONFIRMED = {i for i, n in NPC.items() if n.get("detail_status") == "confirmed"}
UNCONFIRMED = {i for i, n in NPC.items() if n.get("detail_status") != "confirmed"}
MAP_NAME = {m["id"]: ((m.get("name_ko_candidate") or "").strip(), (m.get("street_ko_candidate") or "").strip()) for m in maps_db}
MAP_NAME_FULL = {m["id"]: ((m.get("name_ko_candidate") or "").strip() or (m.get("name_en") or "").strip()) for m in maps_db}
ITEM_NAME = {i["id"]: ((i.get("name_ko_candidate") or "").strip() or (i.get("name_en") or "").strip()) for i in items_db}
MOB_NAME = {m["id"]: ((m.get("name_ko_candidate") or "").strip() or (m.get("name_en") or "").strip()) for m in mobs_db}
JOB_NAME = {j["id"]: (j.get("name_en") or "").strip() for j in jobs_db}
# 퀘스트 조건 직업 한글 표기 (데이터 담당 매핑표 2026-10-28 · 사업실장 표기 결정 반영)
JOB_KO = {r["job_id"]: (r.get("name_ko") or "").strip() for r in json.load(open(os.path.join(ROOT, "data/QUEST-JOB-ID-MAPPING-20261028.json"), encoding="utf-8"))["rows"]}
EVAN_STEP_IDS = {2210, 2212, 2213, 2215, 2216, 2218}

# 관련 퀘스트: 퀘스트 상세 requirement npcId 역참조 (기준표 649 정의)
from collections import defaultdict
RELATED = defaultdict(list)
for q in quests_raw:
    d = q.get("detail") or {}
    ids = set()
    for part in ("requirementToStart", "requirementToComplete"):
        nid = (d.get(part) or {}).get("npcId")
        if isinstance(nid, int):
            ids.add(nid)
    for nid in ids:
        RELATED[nid].append(q["id"])
# 선행 퀘스트 역참조 (후속 목록에서 계산)
PREV = defaultdict(set)
for q in quests_raw:
    for nxt in (q.get("detail") or {}).get("questsAvailableOnComplete") or []:
        if isinstance(nxt.get("id"), int) and nxt["id"] != q["id"]:
            PREV[nxt["id"]].add(q["id"])

def npc_sprite(nid):
    return f"https://maplestory.io/api/GMS/95/npc/{nid}/icon"

def item_icon(iid):
    return f"https://maplestory.io/api/GMS/95/item/{iid}/icon"

def mob_icon(mid):
    return f"https://maplestory.io/api/GMS/95/mob/{mid}/icon"

# 표시 분기 판정 반전 (2026-10-30 사업실장 채택 — 안 2): 한글 후보가 있으면 기본으로 한글 표시.
# 영문으로 강제할 상태만 아래 집합에 명시한다. 현재 정본 교차표 (status × 후보 보유) 기준 해당 상태 없음 —
# 후보 보유 상태는 candidate · kms389 · 자체 번역/음차뿐이고, 후보 없는 상태는 후보가 없어 영문 경로가 유지된다.
NAME_DISPLAY_FORCE_EN = frozenset()
_NAME_LABELS = {"kms389_id_name_matched": "KMS389 이름대조", "id_overlap_no_name": "이름 후보 (ID 대조)"}
def _name_label(st):
    if st in _NAME_LABELS:
        return _NAME_LABELS[st]
    if isinstance(st, str):
        if st.startswith("자체 표기"):
            return "자체 표기"
        if st.startswith("자체 음차"):
            return "자체 음차"
        if st.startswith("자체 번역"):
            return "자체 번역"
    return None

def npc_display(n):
    """이름 상태 3분류 표기: (표시명, 상태 라벨 or None, 영문 병기 여부)"""
    ko = (n.get("name_ko_candidate") or "").strip()
    en = (n.get("name_en") or "").strip()
    st = n.get("name_ko_status")
    if st == "id_overlap_no_name":
        return (ko or en), "이름 후보 (ID 대조)", en
    if ko and st not in NAME_DISPLAY_FORCE_EN:
        return ko, _name_label(st), en
    return en, "영문원본", None

def npc_ref_html(nid, link=True):
    """퀘스트 안에서 NPC 참조 렌더링. 미확인·부재는 링크 없이 미확인 표기 (기준표)."""
    n = NPC.get(nid)
    if n is None:
        return f'<span class="npc-ref unknown">NPC {nid} (미확인)</span>'
    name, label, _ = npc_display(n)
    img = f'<img class="dot" src="{npc_sprite(nid)}" alt="" loading="lazy" onerror="imgHide(this)">'
    if nid in UNCONFIRMED:
        return f'<span class="npc-ref unknown">{img}{H.escape(name)} <span class="unk-badge">상세 미확인</span></span>'
    inner = f'{img}{H.escape(name)}'
    if label:
        inner += f' <span class="unk-badge">{label}</span>'
    if link:
        return f'<a class="npc-ref" href="/npcs/#npc-{nid}">{inner}</a>'
    return f'<span class="npc-ref">{inner}</span>'

# ---------- NPC 페이지 ----------
REGION_KO = {"Victoria Road": "빅토리아", "Orbis": "오르비스", "Ludibrium": "루디브리엄", "Leafre": "리프레", "Edelstein-area": "에델슈타인"}
MAP_REGION_TOWN = {m["id"]: (REGION_KO.get(m.get("region"), "기타"), (m.get("name_ko_candidate") or "").strip() if m.get("isTown") else "") for m in maps_db}

def npc_filter_attrs(n):
    """지역 · 마을 · 기능 속성 산출 (프론트 동결 규칙과 동일 — 200개 렌더분 전수 대조로 검증)."""
    regs, towns = set(), set()
    for loc in n.get("map_locations") or []:
        rt = MAP_REGION_TOWN.get(loc["map_id"])
        if not rt: continue
        regs.add(rt[0])
        if rt[1]: towns.add(rt[1])
    f = (n.get("function") or "").strip()
    if not f: func = ""
    elif f == "Storage Keeper": func = "storage"
    elif f in ("Item Maker", "Item Creator"): func = "craft"
    elif f == "Merchant" or f.endswith("Seller"): func = "shop"
    else: func = "etc"
    return "|".join(sorted(regs)), "|".join(sorted(towns)), func

def npc_card(n):
    nid = n["id"]
    name, label, en = npc_display(n)
    rel = RELATED.get(nid, [])
    locs = n.get("map_locations") or []
    dlg = ""
    d = n.get("dialogue") or {}
    if isinstance(d, dict):
        dkey = "d0" if d.get("d0") else next((k for k, v in d.items() if v), None)
        dlg = clean_dialogue(d.get(dkey) if dkey else "", nid, dkey)
    tags = []
    for loc in locs[:3]:
        mid = loc["map_id"]
        mn, street = MAP_NAME.get(mid, ("", ""))
        label_txt = (f"{street} · " if street else "") + (mn or f"맵 {mid}")
        tags.append(f'<a class="tag" href="/maps/#map-{mid}"><img class="dic" src="/assets/icons/icon-worldmap.png" alt="" aria-hidden="true" onerror="imgHide(this)"> {H.escape(label_txt)}</a>')
    if len(locs) > 3:
        tags.append(f'<span class="tag more">외 {len(locs) - 3}곳</span>')
    rel_html = ""
    if rel:
        chips = []
        for qid in rel[:3]:
            q = QUEST[qid]
            qn = (q.get("name_ko_candidate") or q.get("name_en") or "").strip()
            chips.append(f'<a class="qtag" href="{quest_href(qid)}">{H.escape(qn)}</a>')
        # 역방향 전건화 (2026-11-13): 4건째부터는 접이식으로 전건 링크한다 (총수 라벨만 있던 절단 해소)
        if len(rel) > 3:
            more = []
            for qid in rel[3:]:
                q = QUEST[qid]
                qn = (q.get("name_ko_candidate") or q.get("name_en") or "").strip()
                more.append(f'<a class="qtag" href="{quest_href(qid)}">{H.escape(qn)}</a>')
            chips.append(f'<details class="rel-more"><summary>외 {len(rel) - 3}건 더 보기</summary>' + "".join(more) + "</details>")
        rel_html = (f'<div class="rel"><span class="rel-label"><img class="dic" src="/assets/icons/icon-quest.png" alt="" aria-hidden="true" onerror="imgHide(this)"> 관련 퀘스트 {len(rel)}건</span>'
                    + "".join(chips) + "</div>")
    badge = f' <span class="unk-badge">{label}</span>' if label else ""
    en_html = f'<span class="en">{H.escape(en)}</span>' if en else ""
    _tcls = "t-ko" if name and name == (n.get("name_ko_candidate") or "").strip() else "t-en"
    dlg_html = f'<p class="dlg">“{H.escape(dlg)}”</p>' if dlg else ""
    search_txt = norm(name) + "|" + norm(n.get("name_en") or "") + "|" + str(nid)
    _fr, _ft, _ff = npc_filter_attrs(n)
    return (f'<article class="npc-card" id="npc-{nid}" data-quests="{1 if rel else 0}" data-maps="{1 if locs else 0}" '
            f'data-namestate="{n.get("name_ko_status") or ""}" data-search="{H.escape(search_txt)}" data-region="{H.escape(_fr)}" data-town="{H.escape(_ft)}" data-func="{_ff}">'
            f'<div class="nc-head"><img class="sprite" src="{npc_sprite(nid)}" alt="" loading="lazy" width="64" height="64" onerror="imgRetry(this)">'
            f'<div class="nc-title {_tcls}"><h3>{H.escape(name)}{badge}</h3>{en_html}</div></div>'
            f'{dlg_html}'
            + (f'<div class="tags">{"".join(tags)}</div>' if tags else "")
            + rel_html + "</article>")

def build_npcs():
    conf = sorted((n for n in npcs_raw if n["id"] in CONFIRMED), key=lambda x: x["id"])
    unc = sorted((n for n in npcs_raw if n["id"] in UNCONFIRMED), key=lambda x: x["id"])
    n_rel = sum(1 for n in conf if RELATED.get(n["id"]))
    n_map = sum(1 for n in conf if n.get("map_locations"))
    _all_cards = [npc_card(n) for n in conf]
    FIRST = 200
    cards = "\n".join(_all_cards[:FIRST])
    import json as _json
    _rest_path = os.path.join(SITE, "assets", "npcs-rest.json")
    os.makedirs(os.path.dirname(_rest_path), exist_ok=True)
    open(_rest_path, "w", encoding="utf-8").write(_json.dumps(_all_cards[FIRST:], ensure_ascii=False, separators=(",", ":")))
    def unc_label(n):
        en = H.escape((n.get("name_en") or "").strip())
        cand = (n.get("name_ko_candidate") or "").strip()
        return f'{en} ({H.escape(cand)})' if cand else en
    unc_items = "".join(
        f'<li id="npc-{n["id"]}">{unc_label(n)} <span class="uid">ID {n["id"]}</span></li>' for n in unc)
    body = f"""
  <div class="intro">
    <h1>NPC <span>도감</span></h1>
    <p class="live-badge"><span class="live-dot" aria-hidden="true"></span>NPC 정보가 확인되는 대로 실시간으로 등록됩니다</p>
    <div class="tag">마을과 필드의 NPC {len(conf):,}명의 위치·대사·관련 퀘스트</div>
    <div class="disclaimer">본진 메이플스토리 GMS 95 기준으로 수집한 정보예요. 한글 이름은 확인된 후보 표기이며, 실제 알팡서버의 배치·내용과는 다를 수 있어요. 알팡서버가 공식 오픈하면 해당 버전에 맞춰 상세 정보를 업데이트할 예정이에요.</div>
  </div>
  <div class="seg" role="tablist" aria-label="도감 전환">
    <a class="seg-on" href="/npcs/" role="tab" aria-selected="true">NPC</a><a href="/quests/" role="tab" aria-selected="false">퀘스트</a>
  </div>
  <div class="filters">
    <div class="fbtns" id="npcMainFilters">
      <button type="button" class="fbtn on" data-f="all">전체 {len(conf):,}</button>
      <button type="button" class="fbtn" data-f="quests">관련 퀘스트 있음</button>
      <button type="button" class="fbtn" data-f="maps">출현 맵 있음</button>
    </div>

<div class="nf-bar" id="nfBar">
  <div class="nf-row"><span class="nf-lb">지역</span><span class="nf-chips" id="nfRegion"><button type="button" data-r="빅토리아">빅토리아</button><button type="button" data-r="오르비스">오르비스</button><button type="button" data-r="루디브리엄">루디브리엄</button><button type="button" data-r="리프레">리프레</button><button type="button" data-r="에델슈타인">에델슈타인</button><button type="button" data-r="기타">기타</button></span></div>
  <div class="nf-row"><span class="nf-lb">기능</span><span class="nf-chips" id="nfFunc"><button type="button" data-u="shop">상점</button><button type="button" data-u="storage">창고</button><button type="button" data-u="craft">제작</button></span></div>
  <p class="nf-note" id="nfNote" hidden></p>
</div>
<details class="nf-rest" id="nfRest" hidden><summary id="nfRestSummary"></summary><div class="nf-rest-grid" id="nfRestGrid"></div></details>
    <details class="nf-name"><summary>이름 확인 상태로 찾기</summary>
    <p class="nf-note">이름 표기의 확인 상태로 좁혀요. 지역 · 기능 필터와 함께 쓸 수 있어요.</p>
    <div class="fbtns" id="npcNameFilters">
      <button type="button" class="fbtn on" data-n="all">이름 전체</button>
      <button type="button" class="fbtn" data-n="candidate">한글명 후보</button>
      <button type="button" class="fbtn" data-n="id_overlap_no_name">이름 후보 (ID 대조)</button>
      <button type="button" class="fbtn" data-n="unmapped">영문 원본</button>
    </div>
    </details>
    <input type="text" id="npcSearch" placeholder="NPC 이름·영문·ID 검색" aria-label="NPC 검색" autocomplete="off">
    <p class="fcount" id="npcRestNote">나머지 NPC는 더 보기 · 검색 · 필터 · 링크로 진입할 때 이어서 불러옵니다.</p>
    <p class="fcount" id="npcCount"></p>
  </div>
  <main class="npc-grid" id="npcGrid">
{cards}
  </main>
  <p class="empty" id="npcEmpty" hidden>조건에 맞는 NPC가 없어요.</p>
  <button type="button" class="more-btn" id="npcMore" hidden>더 보기</button>
  <details class="unc-box">
    <summary>상세 미확인 NPC {len(unc)}명 (원본에서 상세를 확인할 수 없었던 항목)</summary>
    <p class="unc-note">아래 NPC는 원본 데이터에서 상세 응답이 없어 위치·대사를 확인하지 못했습니다. 확인되지 않은 정보를 채우지 않고 이름만 남깁니다.</p>
    <ul class="unc-list">{unc_items}</ul>
  </details>
<script>
(function () {{
  var main = 'all', nameF = 'all', q = '', region = '', func = '';
  var restBox = document.getElementById('nfRest'), restGrid = document.getElementById('nfRestGrid'),
      restSummary = document.getElementById('nfRestSummary'), nfNote = document.getElementById('nfNote');
  var PAGE = 50, revealed = PAGE;
  var TOTAL_ALL = {len(conf)};
  var grid = document.getElementById('npcGrid'), cards = Array.prototype.slice.call(grid.children),
      restLoaded = false, restLoading = null,
      count = document.getElementById('npcCount'), empty = document.getElementById('npcEmpty'),
      moreBtn = document.getElementById('npcMore');
  // 스프라이트 빈 이미지 판정 → 플레이스홀더 전환 (핫픽스 ④: 1x1 투명 응답·로드 오류를 판정 후에만 교체)
  function spritePh(img) {{
    if (img.dataset.ph) return; img.dataset.ph = '1';
    var s = document.createElement('span');
    s.className = 'sprite-ph'; s.textContent = '📜'; s.setAttribute('aria-hidden', 'true');
    img.replaceWith(s);
  }}
  cards.forEach(function (c, i) {{
    c._nfIdx = i;
    var img = c.querySelector('img.sprite'); if (!img) return;
    img.addEventListener('load', function () {{ if (img.naturalWidth <= 1) spritePh(img); }});
    img.addEventListener('error', function () {{ spritePh(img); }});
    if (img.complete && img.naturalWidth <= 1) spritePh(img);
  }});
  function norm(s) {{ return (s || '').normalize('NFKC').toLowerCase().replace(/[^0-9a-z가-힣]/g, ''); }}
  function paging() {{ return main === 'all' && nameF === 'all' && !q && !region && !func; }}
  function rfActive() {{ return !!(region || func); }}
  function restoreRest() {{
    if (!restGrid || !restGrid.children.length) return;
    Array.prototype.slice.call(restGrid.children).forEach(function (c) {{ grid.appendChild(c); }});
    Array.prototype.slice.call(grid.children).sort(function (a, b) {{ return (a._nfIdx || 0) - (b._nfIdx || 0); }}).forEach(function (c) {{ grid.appendChild(c); }});
    restBox.hidden = true;
  }}
  function loadRest() {{
    if (restLoaded) return Promise.resolve();
    if (restLoading) return restLoading;
    restLoading = fetch('/assets/npcs-rest.json').then(function (r) {{ return r.json(); }}).then(function (arr) {{
      arr.forEach(function (html) {{
        var t = document.createElement('template'); t.innerHTML = html;
        var card = t.content.firstElementChild;
        bindSprite(card); card._nfIdx = cards.length; grid.appendChild(card); cards.push(card);
      }});
      restLoaded = true;
      var note = document.getElementById('npcRestNote'); if (note) note.hidden = true;
    }}).catch(function () {{ restLoading = null; }});
    return restLoading;
  }}
  function bindSprite(c) {{
    var img = c.querySelector('img.sprite'); if (!img) return;
    img.addEventListener('load', function () {{ if (img.naturalWidth <= 1) spritePh(img); }});
    img.addEventListener('error', function () {{ spritePh(img); }});
    if (img.complete && img.naturalWidth <= 1) spritePh(img);
  }}
  function apply() {{
    if (!restLoaded && (q || main !== 'all' || nameF !== 'all' || rfActive())) {{ loadRest().then(function () {{ apply(); }}); }}
    restoreRest();
    var shown = 0, stayed = 0, pg = paging(), rf = rfActive();
    cards.forEach(function (c, i) {{
      var base = (main === 'all' || c.getAttribute('data-' + main) === '1')
        && (nameF === 'all' || c.getAttribute('data-namestate') === nameF)
        && (!q || c.getAttribute('data-search').indexOf(q) >= 0);
      if (!rf) {{
        var ok0 = base && (!pg || i < revealed);
        c.style.display = ok0 ? '' : 'none';
        if (ok0) shown++;
        return;
      }}
      var regs = (c.getAttribute('data-region') || '').split('|');
      var missR = region && regs.indexOf(region) < 0;
      var missF = func && c.getAttribute('data-func') !== func;
      var noInfo = (region && !c.getAttribute('data-region')) || (func && !c.getAttribute('data-func'));
      if (!base) {{ c.style.display = 'none'; return; }}
      if ((missR || missF) && noInfo) {{ restGrid.appendChild(c); stayed++; return; }}
      if (missR || missF) {{ c.style.display = 'none'; return; }}
      c.style.display = ''; shown++;
    }});
    if (rf && stayed > 0) {{
      restBox.hidden = false;
      restSummary.textContent = (region ? '지역' : '') + (region && func ? ' · ' : '') + (func ? '기능' : '') + ' 정보가 확인되지 않은 NPC ' + stayed + '명 (펼치면 볼 수 있어요)';
    }}
    nfNote.hidden = !rf;
    if (rf) nfNote.textContent = '지역은 출현 맵이 확인된 NPC만, 기능은 기능 값이 확인된 NPC만 좁혀집니다. 정보가 없는 NPC는 아래 묶음에 남아 있어요.';
    count.textContent = pg
      ? '전체 ' + TOTAL_ALL.toLocaleString('ko-KR') + '명 중 ' + shown.toLocaleString('ko-KR') + '명 표시 중'
      : shown.toLocaleString('ko-KR') + '명 표시 중';
    empty.hidden = (shown + stayed) > 0;
    moreBtn.hidden = !(pg && revealed < TOTAL_ALL);
    moreBtn.textContent = '더 보기 (남은 ' + (TOTAL_ALL - revealed).toLocaleString('ko-KR') + '명)';
  }}
  function grow() {{ loadRest().then(function () {{ revealed += PAGE; apply(); }}); }}
  moreBtn.addEventListener('click', grow);
  function bind(id, attr, set) {{
    var box = document.getElementById(id);
    box.addEventListener('click', function (e) {{
      var b = e.target.closest('button'); if (!b) return;
      box.querySelectorAll('.fbtn').forEach(function (x) {{ x.classList.remove('on'); }});
      b.classList.add('on'); set(b.getAttribute(attr)); apply();
    }});
  }}
  function bindChips(id, attr, set) {{
    var box = document.getElementById(id); if (!box) return;
    box.addEventListener('click', function (e) {{
      var b = e.target.closest('button'); if (!b) return;
      var v = b.getAttribute(attr);
      set(v); paintChips(); apply();
    }});
  }}
  function paintChips() {{
    Array.prototype.forEach.call(document.getElementById('nfRegion').children, function (b) {{ b.classList.toggle('on', b.getAttribute('data-r') === region); }});
    Array.prototype.forEach.call(document.getElementById('nfFunc').children, function (b) {{ b.classList.toggle('on', b.getAttribute('data-u') === func); }});
  }}
  bindChips('nfRegion', 'data-r', function (v) {{ region = (region === v ? '' : v); }});
  bindChips('nfFunc', 'data-u', function (v) {{ func = (func === v ? '' : v); }});
  bind('npcMainFilters', 'data-f', function (v) {{ main = v; }});
  bind('npcNameFilters', 'data-n', function (v) {{ nameF = v; }});
  document.getElementById('npcSearch').addEventListener('input', function () {{ q = norm(this.value); apply(); }});
  function goHash() {{
    if (!location.hash) return;
    var t = document.querySelector(location.hash);
    if (!t) {{ loadRest().then(function () {{ goHash(); }}); return; }}
    var idx = cards.indexOf(t);
    if (idx >= 0) {{
      // 직접 링크로 들어온 카드가 페이징 범위 밖이면 그 지점까지 확장
      if (idx >= revealed) {{ revealed = Math.ceil((idx + 1) / PAGE) * PAGE; apply(); }}
    }} else if (t.tagName === 'LI') {{
      var box = t.closest('details'); if (box) box.open = true;
    }}
    t.scrollIntoView();
  }}
  window.addEventListener('hashchange', goHash);
  apply();
  goHash();
}})();
</script>"""
    return page("NPC 도감 — 알팡지지", "알팡서버를 기다리며 정리한 NPC 도감. NPC 1,836명의 출현 위치·대사·관련 퀘스트를 본진 GMS 95 기준으로 모았습니다.", "https://alpang.gg/npcs/", "/npcs/", body, pattern=True)

# ---------- 페이지 공통 ----------
# 타이틀 패턴 정본 블록 (저장소 현행 인덱스 페이지의 적용 형태 그대로 — 2026-11-08 역이식).
# 적용 방식: 인덱스 페이지에서만 .intro 기본 규칙 바로 뒤에 삽입하고, 구간 페이지에는 넣지 않는다.
TITLE_PATTERN_BLOCK = """/* 타이틀 패턴 (2026-11-04) */
.intro{background-color:#faf9f6;background-image:image-set(url("/assets/title-bg/title-bg-common.webp") type("image/webp"),url("/assets/title-bg/title-bg-common.png") type("image/png"));background-size:cover;background-position:center;background-repeat:no-repeat}

/* 패턴 다크 톤다운 (2026-11-04) */
[data-theme="dark"] .intro{background-image:linear-gradient(rgba(18,19,22,.90),rgba(18,19,22,.90)),image-set(url("/assets/title-bg/title-bg-common.webp") type("image/webp"),url("/assets/title-bg/title-bg-common.png") type("image/png"))}
@media (max-width:640px){[data-theme="dark"] .intro{background-image:linear-gradient(rgba(18,19,22,.90),rgba(18,19,22,.90)),image-set(url("/assets/title-bg/title-bg-common-mobile.webp") type("image/webp"),url("/assets/title-bg/title-bg-common-mobile.png") type("image/png"))}}"""

def page(title, desc, canonical, active, body, pattern=False):
    css = CSS
    if pattern:
        anchor = ".intro{text-align:center;padding:28px 0 16px}\n"
        assert anchor in css, "타이틀 패턴 삽입 앵커(.intro 기본 규칙)를 CSS에서 찾지 못함"
        css = css.replace(anchor, anchor + TITLE_PATTERN_BLOCK + "\n", 1)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://alpang.gg/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{THEME_INIT}
<style>{css}
  .new-dot{{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}}
  .new-dot.on{{display:inline-block}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"https://alpang.gg/#website","url":"https://alpang.gg/","name":"알팡지지","inLanguage":"ko"}},{{"@type":"Organization","@id":"https://alpang.gg/#organization","name":"알팡지지","url":"https://alpang.gg/","logo":"https://alpang.gg/assets/logo.png","sameAs":["https://t.me/alpang_gg","https://www.threads.net/@maplestoryworld_"]}}]}}
</script>
</head>
<body>
<div class="wrap">
{gnb(active)}
{body}
  <footer>
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    페이지 갱신일: 2026-10-16
  <br><span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
</footer>
</div>
{THEME_SCRIPT}
<script src="/assets/hit.js?v=1" defer></script>
<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>
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
  @media (max-width:560px){ .gnb .logo{font-size:18px} .gnb nav a{font-size:14px;margin-left:10px} }
  .gnb nav a{display:inline-flex;align-items:center;min-height:44px}
  @media (max-width:768px){.gnb{flex-wrap:nowrap}.gnb nav{flex-wrap:nowrap;overflow-x:auto;flex:1 1 auto;min-width:0;justify-content:flex-start;scrollbar-width:none;-webkit-mask-image:linear-gradient(to right,#000 92%,transparent);mask-image:linear-gradient(to right,#000 92%,transparent)}.gnb nav::-webkit-scrollbar{display:none}}
  .gnb nav a.on{color:var(--accent-dark)}
  .intro{text-align:center;padding:28px 0 16px}
  .live-badge{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:600;color:var(--sub);background:rgba(31,157,85,.08);border:1px solid rgba(31,157,85,.35);border-radius:999px;padding:5px 12px 5px 10px;margin:10px 0 2px}
  .live-dot{flex:none;width:8px;height:8px;border-radius:50%;background:#1F9D55;animation:livePulse 2s ease-out infinite}
  @keyframes livePulse{0%{box-shadow:0 0 0 0 rgba(31,157,85,.45)}70%{box-shadow:0 0 0 7px rgba(31,157,85,0)}100%{box-shadow:0 0 0 0 rgba(31,157,85,0)}}
  @media (prefers-reduced-motion: reduce){.live-dot{animation:none}}
  .intro h1{font-size:28px;font-weight:800} .intro h1 span{color:var(--accent)}
  .intro .tag{color:var(--sub);font-size:15px;margin-top:6px}
  .disclaimer{font-size:13.5px;color:var(--sub);text-align:center;margin-top:8px;line-height:1.65}
  .seg{display:flex;gap:4px;justify-content:center;margin-top:18px}
  .seg a{padding:8px 22px;border:1px solid var(--line);background:var(--card);color:var(--sub);font-weight:700;font-size:15px;text-decoration:none;border-radius:999px}
  .seg a.seg-on{background:var(--accent);border-color:var(--accent);color:#fff}
  .filters{margin-top:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
  .nf-bar{margin:10px 0;padding:10px 12px;background:var(--card);border:1px solid var(--line);border-radius:10px}
  .nf-row{display:flex;gap:8px;align-items:flex-start;margin:4px 0}
  .nf-lb{flex:none;font-weight:700;font-size:13px;padding-top:5px}
  .nf-chips{display:flex;flex-wrap:wrap;gap:6px}
  .nf-chips button{padding:5px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--text);cursor:pointer;font-size:13px;min-height:32px}
  .nf-chips button.on{background:#FF6B00;border-color:#FF6B00;color:#fff;font-weight:700}
  .nf-note{font-size:12.5px;color:var(--sub);margin:6px 0 0}
  .nf-rest{margin:12px 0}
  .nf-rest summary{cursor:pointer;font-weight:700;font-size:14px;color:var(--sub)}
  .nf-rest-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:10px}
  .nf-name{margin:8px 0}
  .nf-name summary{cursor:pointer;font-weight:600;font-size:13.5px;color:var(--sub)}
  .fbtns{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
  .fbtn{padding:6px 13px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--sub);font-size:13.5px;font-weight:600;cursor:pointer}
  .fbtn.on{background:var(--accent);border-color:var(--accent);color:#fff}
  .filters input{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text);font-size:15px;outline:none;margin-top:4px}
  .filters input:focus{border-color:var(--accent)}
  .fcount{font-size:12.5px;color:var(--sub);margin-top:8px}
  .npc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px;margin-top:14px}
  .npc-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;scroll-margin-top:90px}
  .npc-card:target{outline:2px solid var(--accent);outline-offset:1px}
  .nc-head{display:flex;gap:12px;align-items:center}
  .sprite{width:64px;height:64px;object-fit:contain;image-rendering:pixelated;flex:none}
  .sprite-ph{width:64px;height:64px;flex:none;display:inline-flex;align-items:center;justify-content:center;font-size:28px;background:var(--slot);border-radius:8px}
  .nc-title h3{font-size:16px;font-weight:800;line-height:1.35}
  .nc-title .en{display:block;font-size:12px;color:var(--sub)}
  .unk-badge{font-size:10.5px;font-weight:700;color:var(--unknown);background:var(--slot);border-radius:4px;padding:1px 5px;vertical-align:2px;white-space:nowrap}
  .dlg{position:relative;font-size:13.5px;color:var(--text);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:9px 12px;margin-top:12px;line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.dlg::before{content:"";position:absolute;top:-6px;left:18px;width:12px;height:12px;background:var(--card);border-left:1px solid var(--line);border-top:1px solid var(--line);transform:rotate(45deg)}
  .tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:10px}
  .tag{font-size:12px;background:var(--slot);border-radius:6px;padding:3px 8px;color:var(--text);text-decoration:none}
  .tag.more{color:var(--sub)}
  .rel{border-top:1px dashed var(--line);margin-top:11px;padding-top:9px;display:flex;flex-wrap:wrap;gap:5px;align-items:center}
  .rel-label{font-size:12.5px;font-weight:700;color:var(--accent-dark)}
  .qtag{font-size:12px;background:var(--accent-soft);color:var(--accent-dark);border-radius:6px;padding:3px 8px;text-decoration:none}
  .rel-more{display:inline}
  .rel-more summary{display:inline;cursor:pointer;font-size:12px;font-weight:700;color:var(--accent-dark)}
  .rel-more .qtag{margin-top:4px}
  .empty{text-align:center;color:var(--sub);padding:30px 0}
  .qmore{display:block;margin:14px auto 4px;font:inherit;font-size:14.5px;font-weight:700;padding:10px 26px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer}
  .more-btn{display:block;margin:16px auto 4px;padding:11px 34px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--accent-dark);font-size:15px;font-weight:800;cursor:pointer}
  .more-btn:hover{border-color:var(--accent)}
  .unc-box{margin-top:18px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px}
  .unc-box summary{cursor:pointer;font-weight:700;font-size:14.5px}
  .unc-note{font-size:13px;color:var(--sub);margin-top:8px;line-height:1.6}
  .unc-list{columns:3;font-size:13px;margin-top:10px;list-style:none}
  @media (max-width:760px){ .unc-list{columns:2} }
  .unc-list li{padding:2px 0;break-inside:avoid;scroll-margin-top:90px}
  .unc-list li:target{background:var(--accent-soft);border-radius:4px}
  .unc-list .uid{color:var(--sub);font-size:11.5px}
  .band-nav{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:14px}
  .band-nav a{padding:7px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--sub);font-size:13.5px;font-weight:700;text-decoration:none}
  .band-nav a.on{background:var(--accent);border-color:var(--accent);color:#fff}
  .band-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-top:16px}
  .band-card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 16px;text-decoration:none;color:var(--text)}
  .band-card b{display:block;font-size:17px;font-weight:800}
  .band-card span{font-size:13px;color:var(--sub)}
  .qlist{margin-top:14px;display:flex;flex-direction:column;gap:8px}
  .qrow{background:var(--card);border:1px solid var(--line);border-radius:12px;scroll-margin-top:90px}
  .qrow:target{outline:2px solid var(--accent);outline-offset:1px}
  .qdet summary{list-style:none}
  .qdet summary::-webkit-details-marker{display:none}
  .qsum{display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;flex-wrap:wrap}
  .qvis{display:inline-flex;flex:none}
  .qvis img{width:48px;height:48px;object-fit:contain;image-rendering:pixelated}
  .qvis.fallback{width:48px;height:48px;align-items:center;justify-content:center;font-size:24px;background:var(--slot);border-radius:8px}
  .qarrow{color:var(--sub);font-size:14px;flex:none}
  .qmain{flex:1;min-width:200px}
  .qname{font-size:16px;font-weight:800;line-height:1.35}
  .qmain .en{font-size:12px;color:var(--sub);margin-left:7px}
  .qmeta{display:block;font-size:12.5px;color:var(--sub);margin-top:1px}
  .qmeta .rep{color:var(--accent-dark);font-weight:700}
  .qrew{font-size:12.5px;color:var(--accent-dark);font-weight:700;flex:none;display:inline-flex;align-items:center;gap:6px}
  .rew-icons{display:inline-flex;align-items:center;gap:3px}
  .rew-ic{width:24px;height:24px;object-fit:contain;image-rendering:pixelated}
  .rew-more{font-size:12px}
  .qbody{border-top:1px dashed var(--line);padding:12px 16px 14px}
  .ph{margin-bottom:12px}
  .ph h4{font-size:13.5px;font-weight:800;color:var(--accent-dark);margin-bottom:6px}
  .steps{list-style:none;display:flex;flex-direction:column;gap:5px}
  .step{display:flex;gap:8px;align-items:flex-start;font-size:14px;line-height:1.55}
  .snum{flex:none;width:18px;height:18px;border-radius:50%;background:var(--accent-dark);color:#fff;font-size:11px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;margin-top:3px}
  .skind{flex:none;font-size:11px;font-weight:700;background:var(--slot);border-radius:4px;padding:2px 6px;color:var(--sub);margin-top:2px;white-space:nowrap}
  .sbody{flex:1}
  .npc-ref{display:inline-flex;align-items:center;gap:5px;color:var(--accent-dark);text-decoration:none;font-weight:600}
  .npc-ref.unknown{color:var(--sub)}
  .npc-ref .dot,.mchip .dot{width:28px;height:28px;object-fit:contain;image-rendering:pixelated;vertical-align:-8px}
  .slots{display:flex;flex-wrap:wrap;gap:6px}
  .slot{display:inline-flex;align-items:center;gap:6px;background:#241B12;color:#F3E9D2;border-radius:8px;padding:5px 10px;font-size:13px;font-weight:600}
  .slot img{width:34px;height:34px;object-fit:contain;image-rendering:pixelated}
  .slot .cnt{color:#FFC94D}
  .slot.exp{background:#17301F;color:#BFE8C9}
  .slot.meso{background:#3A2E08;color:#FFE08A}
  .mchip{display:inline-flex;align-items:center;gap:5px;background:var(--slot);border-radius:6px;padding:3px 8px;color:var(--text);text-decoration:none;font-size:13.5px}
  .qdesc{font-size:13.5px;color:var(--sub);line-height:1.65}
  .cap{font-size:12px;color:var(--unknown);line-height:1.6}
  .qtag.unknown{background:var(--slot);color:var(--sub)}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;--slot:#26292F;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .dic{width:1.15em;height:1.15em;image-rendering:pixelated;vertical-align:-.18em}

/* 공통 규칙 선행분 — 디렉터 자문 (2026-11-02) */
:root{--card-pad:22px;--card-gap:14px;--slate-bg:rgba(148,163,184,.12);--slate-tx:#94A3B8;--amber:#F59E0B;--amber-lt:#FBBF24}
aside.name-status,.vw-badge,.vw-card-badge{background:var(--slate-bg);color:var(--slate-tx)}
"""

# ---------- 퀘스트 페이지 ----------

BANDS = [("lv-1-10", "Lv.1~10", 1, 10), ("lv-11-20", "Lv.11~20", 11, 20), ("lv-21-30", "Lv.21~30", 21, 30), ("lv-31-40", "Lv.31~40", 31, 40),
         ("lv-41-50", "Lv.41~50", 41, 50), ("lv-51-60", "Lv.51~60", 51, 60), ("lv-61-70", "Lv.61~70", 61, 70), ("lv-71-100", "Lv.71~100", 71, 100), ("lv-101", "Lv.101~", 101, None),
         ("lv-none", "레벨 조건 없음", None, None)]

def quest_band(q):
    lv = (q.get("detail") or {}).get("requirementToStart") or {}
    lv = lv.get("levelMinimum")
    if not isinstance(lv, int):
        return BANDS[-1]
    for b in BANDS:
        if b[2] is not None and lv >= b[2] and (b[3] is None or lv <= b[3]):
            return b
    return BANDS[-1]

def quest_href(qid):
    q = QUEST.get(qid)
    if q is None:
        return None
    return f"/quests/{quest_band(q)[0]}.html#quest-{qid}"

def quest_name(q):
    ko = (q.get("name_ko_candidate") or "").strip()
    en = (q.get("name_en") or "").strip()
    _st = q.get("name_ko_status")
    if _st == "id_overlap_no_name":
        return (ko or en), en, "이름 후보 (ID 대조)"
    if ko and _st not in NAME_DISPLAY_FORCE_EN:
        return ko, en, _name_label(_st)
    return en, None, "영문원본"

def item_slot(iid, count=None):
    name = ITEM_NAME.get(iid, "")
    label = H.escape(name) if name else f"아이템 {iid} (이름 미확인)"
    cnt = f' <span class="cnt">×{count}</span>' if isinstance(count, int) and count > 0 else ""
    return (f'<span class="slot"><img src="{item_icon(iid)}" alt="" loading="lazy">{label}{cnt}</span>')

def mob_chip(mid, count=None):
    name = MOB_NAME.get(mid, "")
    label = H.escape(name) if name else f"몬스터 {mid} (이름 미확인)"
    cnt = f' {count}마리' if isinstance(count, int) and count > 0 else ""
    # 이름 미확인 몬스터는 아이콘 참조가 404라 img를 만들지 않는다 (A안 · 특정표 8d4cb6af…)
    _img = f'<img class="dot" src="{mob_icon(mid)}" alt="" loading="lazy" onerror="imgHide(this)">' if name else ""
    inner = f'{_img}{label}{cnt}'
    if mid in {m["id"] for m in mobs_db}:
        return f'<a class="mchip" href="/mobs/#mob-{mid}">{inner}</a>'
    return f'<span class="mchip">{inner}</span>'

def step(num, kind, content):
    return f'<li class="step"><span class="snum">{num}</span><span class="skind">{kind}</span><span class="sbody">{content}</span></li>'

# 퀘스트 설명 인게임 태그 파싱 (렌더 공통 — 원문 · 번역본 모두 이 함수를 거친다)
SKILL_NAME = {x["id"]: ((x.get("name_ko") or "").strip() or (x.get("name") or "").strip()) for x in json.load(open(os.path.join(ROOT, "data/jobskill-name-apply-output/skills-with-nameko-full-rev6-20261027.json"), encoding="utf-8"))["skills"]}

DESC_UNKNOWN = "[확인 중]"

def parse_desc_tags(text):
    t = text or ""
    def sub_ref(m):
        kind, rid = m.group(1), int(m.group(2))
        if kind == "q":
            name = SKILL_NAME.get(rid) or None
        elif kind == "a":
            # #a는 GMS 전체 몬스터 참조라 정본 175종에 없는 종이 대부분 — 이름이 없으면 토큰을 비운다
            return MOB_NAME.get(rid) or MOB_NAME.get(int(str(rid).zfill(7))) or DESC_UNKNOWN
        else:
            name = _ref_name(kind, rid)
        return name if name else DESC_UNKNOWN
    t = re.sub(r"#@(\d+):", lambda m: _ref_name("p", int(m.group(1))) or DESC_UNKNOWN, t)
    def sub_icon(m):
        rid = int(m.group(1))
        return "" if re.match(r"#t" + str(rid) + r"#", t[m.end():]) else (_ref_name("t", rid) or DESC_UNKNOWN)
    t = re.sub(r"#i(\d+)#", sub_icon, t)
    t = re.sub(r"#c\d+#", "", t)
    t = re.sub(r"#y(\d+)#", lambda m: ((QUEST[int(m.group(1))].get("name_ko_candidate") or QUEST[int(m.group(1))].get("name_en") or "").strip() if int(m.group(1)) in QUEST else ""), t)
    t = re.sub(r"#u\d+#", DESC_UNKNOWN, t)
    t = re.sub(r"#t([^#\d][^#]*)#", lambda m: m.group(1), t)
    t = re.sub(r"#([pmotqa])(\d+)#", sub_ref, t)
    t = re.sub(r"#([pmotqa])(\d+)(?![#\d])", lambda m: DESC_UNKNOWN, t)
    t = re.sub(r"#i(\d+)(?![#\d])", lambda m: _ref_name("t", int(m.group(1))) or DESC_UNKNOWN, t)
    t = t.replace("##", CLEANSE_PROTECT)
    t = re.sub(r"#[bkrgenc]", "", t)
    t = t.replace(CLEANSE_PROTECT, "#")
    t = re.sub(r"#[bkrgenc]", "", t)
    t = re.sub(r"#(?=[A-Z])", "", t)
    t = t.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\r", "\n")
    return "\n".join(re.sub(r"\s+", " ", ln).strip() for ln in t.split("\n")).strip()

def job_label(jid):
    if jid in EVAN_STEP_IDS:
        return "에반"
    nm = JOB_KO.get(jid) or JOB_NAME.get(jid)
    return f"{H.escape(nm)}" if nm else f"직업 ID {jid} (대응 이름 미확인)"

def job_list_label(jids):
    labels = [job_label(j) for j in jids]
    seen_evan = False
    out = []
    for lb in labels:
        if lb == "에반":
            if seen_evan:
                continue
            seen_evan = True
        out.append(lb)
    return " / ".join(out)

def quest_detail_html(q):
    d = q.get("detail") or {}
    rs = d.get("requirementToStart") or {}
    rc = d.get("requirementToComplete") or {}
    rw = d.get("rewardOnComplete") or {}
    parts = []
    # 시작 조건 단계
    steps = []
    n = 0
    if isinstance(rs.get("npcId"), int):
        n += 1; steps.append(step(n, "대화", npc_ref_html(rs["npcId"]) + " 에게서 시작"))
    if isinstance(rs.get("levelMinimum"), int) or isinstance(rs.get("levelMaximum"), int):
        n += 1
        lv = []
        if isinstance(rs.get("levelMinimum"), int): lv.append(f"Lv.{rs['levelMinimum']} 이상")
        if isinstance(rs.get("levelMaximum"), int): lv.append(f"Lv.{rs['levelMaximum']} 이하")
        steps.append(step(n, "레벨", " · ".join(lv)))
    if rs.get("jobs"):
        n += 1; steps.append(step(n, "직업", job_list_label(rs["jobs"])))
    for pq in rs.get("quests") or []:
        pid = pq.get("id")
        if not isinstance(pid, int): continue
        n += 1
        if pid == q["id"]:
            pn = (q.get("name_ko_candidate") or q.get("name_en") or "").strip()
            steps.append(step(n, "선행 퀘스트", f'{H.escape(pn)} <span class="unk-badge">자기 참조 (원본 표기)</span>'))
        elif pid in QUEST:
            pn = (QUEST[pid].get("name_ko_candidate") or QUEST[pid].get("name_en") or "").strip()
            steps.append(step(n, "선행 퀘스트", f'<a href="{quest_href(pid)}">{H.escape(pn)}</a> 완료'))
        else:
            steps.append(step(n, "선행 퀘스트", f"퀘스트 {pid} (미확인 — 상세 없음)"))
    if isinstance(rs.get("fame"), int):
        n += 1; steps.append(step(n, "인기도", f"인기도 {rs['fame']} 이상 (원본 표기)"))
    if isinstance(rs.get("repeatInterval"), int):
        n += 1; steps.append(step(n, "반복", f"완료 후 반복 가능 (원본 간격 표기: {rs['repeatInterval']})"))
    if steps:
        parts.append(f'<div class="ph"><h4>시작 조건</h4><ol class="steps">{"".join(steps)}</ol></div>')
    # 완료 조건 단계
    steps = []
    n = 0
    start_npc = rs.get("npcId")
    if isinstance(rc.get("npcId"), int):
        n += 1; steps.append(step(n, "대화", npc_ref_html(rc["npcId"]) + " 에게 완료"))
    for it in rc.get("items") or []:
        if isinstance(it.get("id"), int):
            n += 1; steps.append(step(n, "필요 아이템", item_slot(it["id"], it.get("count"))))
    for mb in rc.get("mobs") or []:
        if isinstance(mb.get("id"), int):
            n += 1; steps.append(step(n, "처치", mob_chip(mb["id"], mb.get("count"))))
    if isinstance(rc.get("levelMinimum"), int):
        n += 1; steps.append(step(n, "레벨", f"Lv.{rc['levelMinimum']} 이상"))
    if steps:
        parts.append(f'<div class="ph"><h4>완료 조건</h4><ol class="steps">{"".join(steps)}</ol></div>')
    cond_type = "조건 있음" if parts else ""
    # 보상
    rewards = []
    if isinstance(rw.get("exp"), int) and rw["exp"]:
        rewards.append('<span class="slot exp">EXP ' + f'{rw["exp"]:,}' + '</span>')
    if isinstance(rw.get("meso"), int) and rw["meso"]:
        rewards.append('<span class="slot meso">메소 ' + f'{rw["meso"]:,}' + '</span>')
    if isinstance(rw.get("fame"), int) and rw["fame"]:
        rewards.append(f'<span class="slot">인기도 {rw["fame"]:,}</span>')
    for it in rw.get("items") or []:
        if isinstance(it.get("id"), int):
            rewards.append(item_slot(it["id"], it.get("count")))
    for sk in rw.get("skills") or []:
        rewards.append(f'<span class="slot">스킬 {H.escape(str(sk))} (원본 표기)</span>')
    if isinstance(rw.get("buffItemId"), int):
        rewards.append(item_slot(rw["buffItemId"]))
    if rewards:
        parts.append(f'<div class="ph"><h4>보상</h4><div class="slots">{"".join(rewards)}</div></div>')
    # 후속 퀘스트
    nxt = []
    for a in d.get("questsAvailableOnComplete") or []:
        nid2 = a.get("id")
        if not isinstance(nid2, int): continue
        if nid2 == q["id"]:
            nn = (q.get("name_ko_candidate") or q.get("name_en") or "").strip()
            nxt.append(f'<span class="qtag unknown">{H.escape(nn)} (자기 참조)</span>')
        elif nid2 in QUEST:
            nn = (QUEST[nid2].get("name_ko_candidate") or QUEST[nid2].get("name_en") or "").strip()
            nxt.append(f'<a class="qtag" href="{quest_href(nid2)}">{H.escape(nn)}</a>')
        else:
            nxt.append(f'<span class="qtag unknown">퀘스트 {nid2} (미확인)</span>')
    if nxt:
        parts.append(f'<div class="ph"><h4>후속 퀘스트</h4><div class="slots">{"".join(nxt)}</div></div>')
    # 게임 내 설명 (messages 첫 항목)
    msgs = d.get("messages") or []
    msg0 = ""
    if isinstance(msgs, list) and msgs and isinstance(msgs[0], str):
        msg0 = msgs[0]
    if msg0:
        if os.environ.get("ALPANG_QUESTS_IN"):
            msgs_ko = d.get("messages_ko") or []
            ko0 = ""
            if isinstance(msgs_ko, list) and msgs_ko and isinstance(msgs_ko[0], str):
                ko0 = msgs_ko[0].strip()
            if ko0:
                parts.append(f'<div class="ph"><h4>퀘스트 설명 (한국어 · 자체 번역)</h4><p class="qdesc">{H.escape(parse_desc_tags(ko0)).replace(chr(10), "<br>")}</p></div>')
        parts.append(f'<div class="ph"><h4>퀘스트 설명 (영문 원문)</h4><p class="qdesc">{H.escape(parse_desc_tags(msg0)).replace(chr(10), "<br>")}</p></div>')
    if not parts:
        parts.append('<p class="qdesc">표시할 조건·보상 상세가 원본에 없습니다.</p>')
    caps = ('<p class="cap">필요 아이템 및 조건 — 복수 조건의 적용 방식(전부 충족인지 일부인​지)은 확인되지 않았습니다.</p>'
            '<p class="cap">보상 목록 — 확정 지급인지, 선택·확률 보상인지 여부는 확인되지 않았습니다.</p>')
    return "".join(parts) + caps, cond_type

def quest_row(q):
    d = q.get("detail") or {}
    rs = d.get("requirementToStart") or {}
    rc = d.get("requirementToComplete") or {}
    rw = d.get("rewardOnComplete") or {}
    name, en, label = quest_name(q)
    sn = rs.get("npcId") if isinstance(rs.get("npcId"), int) else None
    cn = rc.get("npcId") if isinstance(rc.get("npcId"), int) else None
    # 대표 비주얼: 시작 NPC 도트, 완료가 다르면 ➔ 완료 도트
    vis = ""
    if sn is not None and sn in NPC and sn not in UNCONFIRMED:
        vis = f'<a class="qvis" href="/npcs/#npc-{sn}"><img src="{npc_sprite(sn)}" alt="" loading="lazy" width="48" height="48" onerror="imgHide(this)"></a>'
        if cn is not None and cn != sn and cn in NPC and cn not in UNCONFIRMED:
            vis += f'<span class="qarrow">➔</span><a class="qvis" href="/npcs/#npc-{cn}"><img src="{npc_sprite(cn)}" alt="" loading="lazy" width="48" height="48" onerror="imgHide(this)"></a>'
    elif sn is not None:
        vis = '<span class="qvis fallback" title="시작 NPC 상세 미확인">📜</span>'
    else:
        vis = '<span class="qvis fallback">📜</span>'
    metas = []
    if isinstance(rs.get("levelMinimum"), int):
        metas.append(f"Lv.{rs['levelMinimum']}~")
    if rs.get("jobs"):
        metas.append("직업 조건")
    if isinstance(rs.get("repeatInterval"), int):
        metas.append('<span class="rep">반복 가능</span>')
    pre = PREV.get(q["id"], set())
    if pre:
        metas.append(f"선행 퀘스트 {len(pre)}개 필요")
    sname = ""
    if sn is not None and sn in NPC:
        sname = npc_display(NPC[sn])[0]
        comp = ""
        if cn is not None and cn != sn and cn in NPC:
            comp = f' · 완료: {H.escape(npc_display(NPC[cn])[0])}'
        sname = f'시작: {H.escape(sname)}{comp}'
    elif sn is not None:
        sname = "시작 NPC 미확인"
    if sname:
        metas.append(sname)
    rw_sum = []
    if isinstance(rw.get("exp"), int) and rw["exp"]:
        rw_sum.append(f"EXP {rw['exp']:,}")
    if rw.get("items"):
        rw_sum.append(f"보상 아이템 {len(rw['items'])}개")
    # ⑤ summary 보상 아이콘 (A안): 최대 4개 + 초과분 '+N개'. EXP·메소만 있으면 아이콘 영역을 만들지 않는다
    rw_items = [it["id"] for it in rw.get("items") or [] if isinstance(it.get("id"), int)]
    qrew_icons = ""
    if rw_items:
        imgs = "".join(f'<img class="rew-ic" src="{item_icon(iid)}" alt="" loading="lazy" width="24" height="24">' for iid in rw_items[:4])
        more = f'<span class="rew-more">+{len(rw_items) - 4}개</span>' if len(rw_items) > 4 else ""
        qrew_icons = f'<span class="rew-icons">{imgs}{more}</span>'
    qrew_html = (f'<span class="qrew">{" · ".join(rw_sum)}{qrew_icons}</span>' if rw_sum
                 else (f'<span class="qrew">{qrew_icons}</span>' if qrew_icons else ""))
    badge = f' <span class="unk-badge">{label}</span>' if label else ""
    en_html = f'<span class="en">{H.escape(en)}</span>' if en and en != name else ""
    detail, _ct = quest_detail_html(q)
    lvmin = rs.get("levelMinimum") if isinstance(rs.get("levelMinimum"), int) else 0
    band = "1" if lvmin <= 10 else "2" if lvmin <= 30 else "3" if lvmin <= 50 else "4" if lvmin <= 70 else "5" if lvmin <= 100 else "6"
    search_txt = norm(name) + "|" + norm(q.get("name_en") or "") + "|" + str(q["id"])
    attrs = (f'data-band="{band}" data-jobs="{1 if rs.get("jobs") else 0}" data-rep="{1 if isinstance(rs.get("repeatInterval"), int) else 0}" '
             f'data-rwexp="{1 if (isinstance(rw.get("exp"), int) and rw["exp"]) else 0}" data-rwmeso="{1 if (isinstance(rw.get("meso"), int) and rw["meso"]) else 0}" '
             f'data-rwitem="{1 if rw.get("items") else 0}" data-search="{H.escape(search_txt)}"')
    return (f'<div class="qrow" id="quest-{q["id"]}" {attrs}>'
            f'<details class="qdet"><summary class="qsum">{vis}'
            f'<span class="qmain"><span class="qname {"t-ko" if en_html else "t-en"}">{H.escape(name)}{badge}</span>{en_html}'
            f'<span class="qmeta">{" · ".join(metas) if metas else "별도 조건 없음"}</span></span>'
            + qrew_html
            + f'</summary><div class="qbody">{detail}</div></details></div>')

def band_nav(active_slug):
    links = []
    for slug, label, _lo, _hi in BANDS:
        links.append(f'<a href="/quests/{slug}.html"' + (' class="on"' if slug == active_slug else '') + f'>{label}</a>')
    return '<nav class="band-nav" aria-label="레벨 구간">' + "".join(links) + '</nav>'

def build_quests_index(band_counts):
    cards = "".join(
        f'<a class="band-card" href="/quests/{slug}.html"><b>{label}</b><span>퀘스트 {cnt}건</span></a>'
        for (slug, label, _lo, _hi), cnt in zip(BANDS, band_counts))
    body = f"""
  <div class="intro">
    <h1>퀘스트 <span>도감</span></h1>
    <p class="live-badge"><span class="live-dot" aria-hidden="true"></span>퀘스트 정보가 확인되는 대로 실시간으로 등록됩니다</p>
    <div class="tag">퀘스트 {len(quests_raw):,}건의 시작·완료 조건과 보상을 한눈에</div>
    <div class="disclaimer">본진 메이플스토리 GMS 95 기준으로 수집한 정보예요. 한글 이름은 확인된 후보 표기이며, 실제 알팡서버의 배치·내용과는 다를 수 있어요. 알팡서버가 공식 오픈하면 해당 버전에 맞춰 상세 정보를 업데이트할 예정이에요. 페이지가 무거워지지 않게 레벨 구간별로 나눠 두었어요.</div>
  </div>
  <div class="seg" role="tablist" aria-label="도감 전환">
    <a href="/npcs/" role="tab" aria-selected="false">NPC</a><a class="seg-on" href="/quests/" role="tab" aria-selected="true">퀘스트</a>
  </div>
  <div class="band-grid">
{cards}
  </div>"""
    return page("퀘스트 도감 — 알팡지지", "알팡서버를 기다리며 정리한 퀘스트 도감. 퀘스트 3,412건의 시작·완료 NPC, 조건, 보상을 본진 GMS 95 기준으로 모았습니다.", "https://alpang.gg/quests/", "/npcs/", body, pattern=True)

def build_quests_band(band, quests):
    slug, label, _lo, _hi = band
    rows = "\n".join(quest_row(q) for q in sorted(quests, key=lambda x: x["id"]))
    body = f"""
  <div class="intro">
    <h1>퀘스트 <span>도감</span></h1>
    <p class="live-badge"><span class="live-dot" aria-hidden="true"></span>퀘스트 정보가 확인되는 대로 실시간으로 등록됩니다</p>
    <div class="tag">{label} 구간 퀘스트 {len(quests)}건</div>
    <div class="disclaimer">본진 메이플스토리 GMS 95 기준으로 수집한 정보예요. 한글 이름은 확인된 후보 표기이며, 실제 알팡서버의 배치·내용과는 다를 수 있어요. 알팡서버가 공식 오픈하면 해당 버전에 맞춰 상세 정보를 업데이트할 예정이에요.</div>
  </div>
  <div class="seg" role="tablist" aria-label="도감 전환">
    <a href="/npcs/" role="tab" aria-selected="false">NPC</a><a class="seg-on" href="/quests/" role="tab" aria-selected="true">퀘스트</a>
  </div>
{band_nav(slug)}
  <div class="filters">
    <div class="fbtns" id="qFlags">
      <button type="button" class="fbtn" data-v="jobs">직업 조건</button>
      <button type="button" class="fbtn" data-v="rep">반복 가능</button>
      <button type="button" class="fbtn" data-v="rwexp">EXP 보상</button>
      <button type="button" class="fbtn" data-v="rwmeso">메소 보상</button>
      <button type="button" class="fbtn" data-v="rwitem">아이템 보상</button>
    </div>
    <input type="text" id="qSearch" placeholder="퀘스트 이름·영문·ID 검색" aria-label="퀘스트 검색" autocomplete="off">
    <p class="fcount" id="qCount"></p>
  </div>
  <main class="qlist" id="qList">
{rows}
  </main>
  <p class="empty" id="qEmpty" hidden>조건에 맞는 퀘스트가 없어요.</p>
  <button type="button" class="qmore" id="qMore" hidden>더 보기</button>
<script>
(function () {{
  var flags = {{}}, q = '';
  var rows = Array.prototype.slice.call(document.getElementById('qList').children),
      count = document.getElementById('qCount'), empty = document.getElementById('qEmpty');
  function norm(s) {{ return (s || '').normalize('NFKC').toLowerCase().replace(/[^0-9a-z가-힣]/g, ''); }}
  var PAGE = 50, limit = PAGE;
  var more = document.getElementById('qMore');
  function filtering() {{ return !!q || Object.keys(flags).length > 0; }}
  function apply() {{
    var shown = 0, visible = 0, filt = filtering();
    rows.forEach(function (r, i) {{
      var ok = Object.keys(flags).every(function (k) {{ return r.getAttribute('data-' + k) === '1'; }})
        && (!q || r.getAttribute('data-search').indexOf(q) >= 0);
      var vis = ok && (filt || i < limit);
      r.style.display = vis ? '' : 'none';
      if (ok) shown++;
      if (vis) visible++;
    }});
    count.textContent = shown.toLocaleString('ko-KR') + '건 표시 중';
    empty.hidden = shown > 0;
    if (filt || shown <= visible) {{ more.hidden = true; }}
    else {{ more.hidden = false; more.textContent = '더 보기 (남은 ' + (shown - visible).toLocaleString('ko-KR') + '건)'; }}
  }}
  document.getElementById('qFlags').addEventListener('click', function (e) {{
    var b = e.target.closest('button'); if (!b) return;
    var k = b.getAttribute('data-v');
    if (flags[k]) {{ delete flags[k]; b.classList.remove('on'); }} else {{ flags[k] = 1; b.classList.add('on'); }}
    apply();
  }});
  document.getElementById('qSearch').addEventListener('input', function () {{ q = norm(this.value); limit = PAGE; apply(); }});
  more.addEventListener('click', function () {{ limit += PAGE; apply(); }});
  if (location.hash) {{
    var target = document.getElementById(location.hash.slice(1));
    if (target) {{ var ti = rows.indexOf(target); if (ti >= limit) limit = ti + 1; }}
  }}
  apply();
}})();
</script>"""
    return page(f"퀘스트 도감 {label} — 알팡지지", f"알팡서버를 기다리며 정리한 퀘스트 도감. {label} 구간 퀘스트의 시작·완료 NPC, 조건, 보상을 본진 GMS 95 기준으로 모았습니다.", f"https://alpang.gg/quests/{slug}.html", "/npcs/", body)

def build_quests():
    """구간 분할 빌드. (인덱스 HTML, {파일명: HTML}) 반환."""
    grouped = {b[0]: [] for b in BANDS}
    for q in quests_raw:
        grouped[quest_band(q)[0]].append(q)
    counts = [len(grouped[b[0]]) for b in BANDS]
    index = build_quests_index(counts)
    pages = {}
    for band in BANDS:
        pages[band[0] + ".html"] = build_quests_band(band, grouped[band[0]])
    return index, pages, counts

if __name__ == "__main__":
    os.makedirs(os.path.join(SITE, "npcs"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "quests"), exist_ok=True)
    html_npcs = build_npcs()
    open(os.path.join(SITE, "npcs/index.html"), "w", encoding="utf-8").write(html_npcs)
    print("npcs built | bytes:", len(html_npcs.encode("utf-8")), "| confirmed:", len(CONFIRMED), "| unconfirmed:", len(UNCONFIRMED),
          "| 관련퀘스트 NPC:", sum(1 for n in CONFIRMED if RELATED.get(n)), "| 출현맵 NPC:", sum(1 for n in CONFIRMED if NPC[n].get("map_locations")))
    q_index, q_pages, q_counts = build_quests()
    open(os.path.join(SITE, "quests/index.html"), "w", encoding="utf-8").write(q_index)
    print("quests index | bytes:", len(q_index.encode("utf-8")))
    for fname, content in q_pages.items():
        open(os.path.join(SITE, "quests", fname), "w", encoding="utf-8").write(content)
        print(f"quests {fname} | bytes:", len(content.encode("utf-8")))
    print("quest band counts:", q_counts, "| total:", sum(q_counts))
    # ③ 클렌징 집계 — 규칙 대상은 NPC 대사 전 문장 (게이트 A 대조: 토큰 82 · 성공 76 · [이름 미확인] 6 · 불완전 1)
    from collections import Counter
    stats = {"total": 0, "ok": 0, "fail": [], "incomplete": [], "unknown": []}
    leftover = 0
    for n in npcs_raw:
        dd = n.get("dialogue") or {}
        if isinstance(dd, dict):
            for k, v in dd.items():
                if v:
                    out = clean_dialogue(v, n["id"], k, stats)
                    if re.search(r"#[bkrgenc]", out):
                        leftover += 1
    print("cleanse | 참조 토큰:", stats["total"], "| 치환 성공:", stats["ok"],
          "| [이름 미확인]:", len(stats["fail"]), dict(Counter(stats["fail"])),
          "| 불완전 토큰:", stats["incomplete"], "| 미지 코드:", sorted(set(stats["unknown"])),
          "| 제어 코드 잔류 문장:", leftover)
