#!/usr/bin/env python3
"""모바일 실기기 QA(피클 REPORT.md) P0 핫픽스 적용기 (2026-11-20, 기술이사).

사용: py -3.11 -I -X utf8 apply_hotfix.py <main 체크아웃 경로>
- 바이트 단위(newline='')로 읽고 써서 줄바꿈(CRLF/LF)을 보존한다.
- 모든 치환은 기대 횟수와 정확히 같을 때만 일어나고 아니면 즉시 중단한다.
- 정적 HTML 수정과 같은 변경을 빌더 소스에도 역이식한다(재생성 때 되돌아가지 않게).
"""
import os, re, sys, glob, json

root = sys.argv[1].rstrip('/\\')
report = []


def rd(p):
    with open(os.path.join(root, p), encoding='utf-8', newline='') as f:
        return f.read()


def wr(p, s):
    with open(os.path.join(root, p), 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def sub_exact(path, old, new, count=1):
    s = rd(path)
    n = s.count(old)
    if n != count:
        sys.exit('중단: %s — 기대 %d회, 실제 %d회: %r' % (path, count, n, old[:70]))
    wr(path, s.replace(old, new))


def nl_of(s):
    return '\r\n' if '\r\n' in s else '\n'


def fb(s):
    """f-string 빌더 템플릿용: 중괄호 이중화"""
    return s.replace('{', '{{').replace('}', '}}')


# ───────────── 1. /npcs/ 해시 확장 무한 루프 가드 ─────────────
OLD_GOHASH = (
    "  function goHash() {\n"
    "    if (!location.hash) return;\n"
    "    var t = document.querySelector(location.hash);\n"
    "    if (!t) { loadRest().then(function () { goHash(); }); return; }\n")
NEW_GOHASH = (
    "  var hashTried = {};\n"
    "  function goHash() {\n"
    "    if (!location.hash) return;\n"
    "    var t = null;\n"
    "    try { t = document.querySelector(location.hash); } catch (e) { return; }\n"
    "    if (!t) {\n"
    "      // 대상 앵커가 없으면 나머지 NPC를 한 번만 불러 재시도하고, 그래도 없으면 즉시 중단 (무한 재귀 방지)\n"
    "      if (restLoaded || hashTried[location.hash]) return;\n"
    "      hashTried[location.hash] = 1;\n"
    "      loadRest().then(function () { goHash(); });\n"
    "      return;\n"
    "    }\n")
OLD_LOAD_DECL = "      restLoaded = false, restLoading = null,"
NEW_LOAD_DECL = "      restLoaded = false, restLoading = null, restFailed = false,"
OLD_CATCH = "}).catch(function () { restLoading = null; });"
NEW_CATCH = "}).catch(function () { restLoading = null; restFailed = true; });"
OLD_APPLY = "if (!restLoaded && (q || main !== 'all' || nameF !== 'all' || rfActive())) { loadRest().then(function () { apply(); }); }"
NEW_APPLY = "if (!restLoaded && !restFailed && (q || main !== 'all' || nameF !== 'all' || rfActive())) { loadRest().then(function () { apply(); }); }"

for path, conv in (('npcs/index.html', lambda x: x), ('builders/npc_quest_build_unified.py', fb)):
    sub_exact(path, conv(OLD_GOHASH), conv(NEW_GOHASH))
    sub_exact(path, OLD_LOAD_DECL, NEW_LOAD_DECL)
    sub_exact(path, conv(OLD_CATCH), conv(NEW_CATCH))
    sub_exact(path, conv(OLD_APPLY), conv(NEW_APPLY))
report.append('1-①  npcs/index.html + 빌더(npc_quest_build_unified): goHash 재귀 가드(대상 없음 → 1회 로드 후 중단, 잘못된 셀렉터는 무시), 로드 실패 시 재시도 루프 차단')

# early-quests 139개 링크: /npcs/#quest-N → 실제 앵커가 있는 /quests/lv-*#quest-N
where = {}
for p in sorted(glob.glob(os.path.join(root, 'quests', 'lv-*.html'))):
    t = open(p, encoding='utf-8', newline='').read()
    base = os.path.basename(p)[:-5]
    for qid in re.findall(r'id="quest-(\d+)"', t):
        where.setdefault(qid, []).append(base)
EQ = 'guide/early-quests/index.html'
s = rd(EQ)
links = re.findall(r'href="/npcs/#quest-(\d+)"', s)
assert len(links) == 139, len(links)
for qid in set(links):
    assert len(where.get(qid, [])) == 1, ('앵커 위치가 정확히 1곳이어야 함', qid, where.get(qid))
s2 = re.sub(r'href="/npcs/#quest-(\d+)"', lambda m: 'href="/quests/%s#quest-%s"' % (where[m.group(1)][0], m.group(1)), s)
wr(EQ, s2)
report.append('1-②  guide/early-quests: /npcs/#quest-N 139건(고유 %d) → /quests/lv-*#quest-N (앵커 존재 전건 확인, 중복 위치 0). 이 페이지는 저장소 빌더가 생성하지 않아 정적 수정만' % len(set(links)))

# ───────────── 2. /calculator/onehit/ select 스타일 ─────────────
OLD_LK = "  .lk-form{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}"
NEW_SELECT = ("  .lk-form select{width:100%;min-width:0;height:43px;padding:0 12px;border:1px solid var(--line);border-radius:10px;"
              "background:var(--card);color:var(--text);font-size:15.5px;outline:none;text-overflow:ellipsis}\n"
              "  .lk-form select:focus{border-color:var(--accent)}")
for path in ('calculator/onehit/index.html', 'builders/onehit_build_skilllookup.py'):
    s = rd(path)
    nl = nl_of(s)
    assert s.count(OLD_LK) == 1, path
    wr(path, s.replace(OLD_LK, OLD_LK + nl + NEW_SELECT.replace('\n', nl)))
report.append('2    calculator/onehit + 빌더(onehit_build_skilllookup): `.lk-form select` 높이 43px·폰트 15.5px·입력칸과 같은 테두리·모서리')

# ───────────── 3. .qmore 더 보기 버튼 hidden 무시 ─────────────
QRULE = re.compile(r'(  \.qmore\{display:block;[^}\n]*\})')
n_pages = 0
for p in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
    rel = os.path.relpath(p, root).replace(os.sep, '/')
    s = open(p, encoding='utf-8', newline='').read()
    if '.qmore{display:block' not in s:
        continue
    assert '.qmore[hidden]' not in s, rel
    nl = nl_of(s)
    s2, n = QRULE.subn(lambda m: m.group(1) + nl + '  .qmore[hidden]{display:none}', s)
    assert n == 1, (rel, n)
    wr(rel, s2)
    n_pages += 1
assert n_pages == 14, n_pages
for path in ('builders/jobs_skills_build_lineage_rev6.py', 'builders/npc_quest_build_unified.py'):
    s = rd(path)
    nl = nl_of(s)
    s2, n = QRULE.subn(lambda m: m.group(1) + nl + '  .qmore[hidden]{display:none}', s)
    assert n == 1, (path, n)
    wr(path, s2)
# 도감 빌더(저스티스)는 파이썬 문자열 안에서 주입하는 형태
sub_exact('data_pages_build_caption_justice.py',
          'color:var(--accent-dark);cursor:pointer}", 1)  # 더보기 버튼 규칙',
          'color:var(--accent-dark);cursor:pointer}\\n  .qmore[hidden]{display:none}", 1)  # 더보기 버튼 규칙')
report.append('3    `.qmore[hidden]{display:none}` 추가: 14개 페이지(mobs·jobs·npcs·quests 11) + 빌더 3종. 원인: `.qmore{display:block}`이 `hidden` 속성을 덮어써 0건에서도 버튼과 이전 문구가 남음')

# ───────────── 4. sitemap: /guide/mushroom-shrine/ ─────────────
S = rd('sitemap.xml')
nl = nl_of(S)
anchor = '  <url><loc>https://alpang.gg/guide/town-npcs/</loc></url>' + nl
assert S.count(anchor) == 1 and 'guide/mushroom-shrine' not in S
S = S.replace(anchor, anchor + '  <url><loc>https://alpang.gg/guide/mushroom-shrine/</loc></url>' + nl)
wr('sitemap.xml', S)
import xml.etree.ElementTree as ET
r = ET.parse(os.path.join(root, 'sitemap.xml')).getroot()
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
assert all(k.tag == ns + 'url' for k in r)
locs = [k.find(ns + 'loc').text for k in r]
assert len(locs) == 99 and len(set(locs)) == 99
report.append('4    sitemap.xml: /guide/mushroom-shrine/ 추가 → url 99개, 직속 자식 전부 url, loc 중복 0')

# ───────────── 5. /items/ 첫 화면 종수 (가이드는 제외 — 보고서 참조) ─────────────
sub_exact('items/index.html', '몬스터 175종, 맵 419곳', '몬스터 188종, 맵 419곳')
sub_exact('builders/items_build_final_adopted.py', '몬스터 175종, 맵 419곳', '몬스터 188종, 맵 419곳')
report.append('5    items/index.html + 빌더: "몬스터 175종" → "188종" 1곳. 가이드 7편은 175종 기준 계산 통계라 치환하지 않음')

print('\n'.join(report))
