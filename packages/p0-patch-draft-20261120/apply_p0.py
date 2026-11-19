#!/usr/bin/env python3
"""알팡지지 P0 패치 초안 적용기 (2026-11-20, 기술이사).

사용: py -3.11 -I -X utf8 apply_p0.py <main 체크아웃 경로> [개정일 YYYY-MM-DD]
- 바이트 단위(newline='')로 읽고 써서 CRLF/LF를 보존한다.
- 모든 치환은 '정확히 기대한 횟수'만 일어나야 하고, 아니면 즉시 중단한다.
- 사이트 소스 위생 게이트(cdn-cgi 0 · Analytics 0 · beacon 0)를 건드리지 않는다.
"""
import os, re, sys

root = sys.argv[1].rstrip('/\\')
DATE = sys.argv[2] if len(sys.argv) > 2 else '2026-11-20'
DATE_KO = '%d년 %d월 %d일' % tuple(int(x) for x in DATE.split('-'))
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
        sys.exit('중단: %s — 기대 %d회, 실제 %d회: %r' % (path, count, n, old[:60]))
    wr(path, s.replace(old, new))


# ① market noindex 복원 (3dab7be가 지운 줄을 같은 자리에 되돌린다)
s = rd('market/index.html')
assert 'noindex' not in s.lower(), 'market에 이미 noindex가 있음'
nl = '\r\n' if '\r\n' in s else '\n'
anchor = '<meta charset="utf-8">' + nl
assert s.count(anchor) == 1
wr('market/index.html', s.replace(anchor, anchor + '<meta name="robots" content="noindex">' + nl))
report.append('① market/index.html: noindex 1줄 복원 (+39B)')

# ② 중복 5쌍 정리: 구 세대 디렉터리 페이지 삭제 + 301
cats = ['cash', 'equip', 'etc', 'setup', 'use']
for c in cats:
    p = os.path.join(root, 'items', c, 'index.html')
    assert os.path.isfile(p), p
    os.remove(p)
    d = os.path.join(root, 'items', c)
    if not os.listdir(d):
        os.rmdir(d)
redir = ''.join('/items/%s/ /items/%s 301\n' % (c, c) for c in cats)
assert not os.path.exists(os.path.join(root, '_redirects')), '_redirects가 이미 있음 — 병합 필요'
wr('_redirects', redir)
report.append('② items/{cash,equip,etc,setup,use}/index.html 5개 삭제 + _redirects 5행(301)')

# ④ items 설명의 "목록 후보" 삭제 (description · og:description)
n_files = 0
for fn in sorted(os.listdir(os.path.join(root, 'items'))):
    if not fn.endswith('.html'):
        continue
    p = 'items/' + fn
    s = rd(p)
    old = '알팡지지 아이템 목록 후보 — '
    n = s.count(old)
    if n == 0:
        continue
    assert n == 2, (p, n)  # description + og:description
    wr(p, s.replace(old, '알팡지지 아이템 목록 — '))
    n_files += 1
report.append('④ items/*.html %d개: "아이템 목록 후보 —" → "아이템 목록 —" (각 2곳)' % n_files)

# ④-b 허브 설명의 "표시명 후보" 문구 · 아이템 허브의 "목록 후보" 삭제 (메타 한정, 본문 고지는 그대로)
for p in ['items/%s.html' % c for c in cats]:
    sub_exact(p, ', 한글 이름은 표시명 후보입니다.">', '.">', 2)
sub_exact('items/index.html', '알팡지지 아이템 목록 후보 14,577개', '알팡지지 아이템 목록 14,577개', 2)
sub_exact('items/index.html', ', 한글 이름은 표시명 후보입니다.">', '.">', 2)
report.append('④-b items 허브 5쪽 + items/index.html 메타: "표시명 후보" 고지 삭제, "목록 후보" 삭제 (본문 고지는 유지)')

# ③ 개인정보처리방침 보강
P = 'privacy/index.html'
sub_exact(P, '<div class="tag">시행일: 2026년 10월 14일</div>',
          '<div class="tag">시행일: 2026년 10월 14일 · 개정일: %s</div>' % DATE_KO)
sub_exact(P, '이용자의 개인정보를 직접 수집하지 않습니다. 다만 이용자가 문의 이메일',
          '이용자의 개인정보를 직접 수집하지 않습니다. 사이트 이용 통계는 아래 3항과 같이 개인을 식별할 수 없는 형태로만 기록합니다. 다만 이용자가 문의 이메일')

old_s3 = ('<section class="card"><h2>3. 쿠키와 광고</h2><p>사이트는 구글 애드센스 등 제3자 광고 서비스를 사용할 수 있습니다. '
          '이 경우 광고 제공자가 쿠키를 이용해 이용자의 방문 기록에 기반한 맞춤 광고를 표시할 수 있습니다. '
          '이용자는 브라우저 설정에서 쿠키를 거부하거나, 구글 광고 설정 페이지에서 맞춤 광고를 끌 수 있습니다.</p></section>')
new_s3 = (
    '<section class="card"><h2>3. 익명 방문 통계</h2>'
    '<p>사이트는 서비스 개선을 위해 방문 통계를 수집합니다. 페이지를 열 때 접속한 <b>페이지 경로</b>, '
    '<b>이전 사이트의 도메인 이름</b>(주소 전체가 아니라 도메인 이름만), <b>기기 종류</b>(PC·모바일·태블릿), '
    '<b>브라우저 종류</b>, <b>접속 시각</b>만 기록합니다.</p>'
    '<p>IP 주소, 쿠키, 브라우저 식별 문자열 원문, 로그인 정보는 저장하지 않으며, 이 기록만으로 이용자 개인을 알아볼 수 없습니다. '
    '자동화 프로그램(봇)의 접속은 기록하지 않습니다. 방문 기록은 90일 보관을 원칙으로 하며, 그 이후에는 개인과 무관한 월별 집계 수치만 남깁니다.</p>'
    '<p>사이트는 보안과 속도를 위해 Cloudflare의 서비스를 이용하며, 이 과정에서 접속 정보(IP 주소 등)가 Cloudflare의 서버에서 처리될 수 있습니다.</p></section>\n'
    '<section class="card"><h2>4. 쿠키와 광고</h2>'
    '<p>사이트는 구글 애드센스 등 제3자 광고 서비스를 사용할 수 있습니다. Google을 포함한 제3자 공급업체는 쿠키를 사용하여 '
    '이용자가 이 사이트나 다른 사이트를 방문한 기록을 바탕으로 광고를 게재할 수 있습니다.</p>'
    '<p>이용자는 <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer">Google 광고 설정</a>에서 맞춤 광고를 해제할 수 있고, '
    '<a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener noreferrer">Google이 광고 기술에서 데이터를 사용하는 방식</a>을 확인할 수 있습니다. '
    '또는 <a href="https://www.aboutads.info" target="_blank" rel="noopener noreferrer">www.aboutads.info</a>에서 제3자 공급업체의 맞춤 광고용 쿠키 사용을 해제할 수 있으며, '
    '브라우저 설정에서 쿠키를 거부할 수도 있습니다.</p></section>')
sub_exact(P, old_s3, new_s3)
sub_exact(P, '<h2>4. 개인정보의 제3자 제공</h2>', '<h2>5. 개인정보의 제3자 제공</h2>')
sub_exact(P, '<h2>5. 개인정보 보호책임자 및 문의</h2>', '<h2>6. 개인정보 보호책임자 및 문의</h2>')
sub_exact(P, '<h2>6. 방침의 변경</h2>', '<h2>7. 방침의 변경</h2>')
dup = ('<a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · '
       '<a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · '
       '<a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a>')
fix = ('<a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · '
       '<a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a>')
sub_exact(P, dup, fix)
sub_exact(P, '페이지 갱신일: 2026-10-14', '페이지 갱신일: ' + DATE)
report.append('③ privacy/index.html: 3항 익명 방문 통계 신설, 4항 광고 쿠키 고지 + 링크 3개, 번호 재정렬, 푸터 중복 링크 정리, 개정일 %s' % DATE)

# ⑤ sitemap.xml 고아 태그 제거 (</url> 바깥 <changefreq>·<priority> 2줄 — 477~478행)
S = rd('sitemap.xml')
nl = '\r\n' if '\r\n' in S else '\n'
orphan = ('  </url>' + nl + '    <changefreq>monthly</changefreq>' + nl + '    <priority>0.6</priority>' + nl + '  <url>' + nl)
assert S.count(orphan) == 1, '고아 태그 패턴이 정확히 1곳이어야 함'
S = S.replace(orphan, '  </url>' + nl + '  <url>' + nl)
wr('sitemap.xml', S)
# 구문 검증: urlset 직속 자식은 url뿐, url 자식은 loc/lastmod/changefreq/priority뿐
import xml.etree.ElementTree as ET
tree = ET.parse(os.path.join(root, 'sitemap.xml'))
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
kids = list(tree.getroot())
assert all(k.tag == ns + 'url' for k in kids), 'urlset 직속에 url 아닌 태그가 남음'
for k in kids:
    tags = [c.tag.replace(ns, '') for c in k]
    assert tags.count('loc') == 1 and set(tags) <= {'loc', 'lastmod', 'changefreq', 'priority'}, tags
locs = [k.find(ns + 'loc').text for k in kids]
assert len(locs) == len(set(locs)) and not any(l.endswith('.html') for l in locs)
report.append('⑤ sitemap.xml: 고아 <changefreq>·<priority> 2줄 제거 → url %d개, 직속 자식 전부 <url>, loc 중복 0, .html loc 0' % len(locs))

# ⑥ 내부 링크의 .html 확장자 제거 (href="/…/x.html[#…]" → href="/…/x[#…]")
href_re = re.compile(r'href="(/[^"#?]*?)\.html([#?][^"]*)?"')
n_links = n_pages = 0
for dp, dn, fns in os.walk(root):
    for fn in fns:
        if not fn.endswith('.html'):
            continue
        full = os.path.join(dp, fn)
        with open(full, encoding='utf-8', newline='') as f:
            t = f.read()

        def fix(m):
            global n_links
            target = os.path.join(root, m.group(1).lstrip('/') + '.html')
            assert os.path.isfile(target), '링크 대상 없음: ' + m.group(1)
            assert not m.group(1).endswith('/index'), 'index.html 링크는 별도 처리 필요: ' + m.group(1)
            n_links += 1
            return 'href="%s%s"' % (m.group(1), m.group(2) or '')

        t2 = href_re.sub(fix, t)
        if t2 != t:
            n_pages += 1
            with open(full, 'w', encoding='utf-8', newline='') as f:
                f.write(t2)
report.append('⑥ 내부 링크 .html 제거: %d건 / %d개 페이지 (대상 전부 실재 확인, index.html 형태 0)' % (n_links, n_pages))

# ⑦ 404 정리 리다이렉트 (_redirects에 추가)
extra = (
    '/quests/lv-11-30 /quests/ 301\n'
    '/quests/lv-11-30.html /quests/ 301\n'
    '/taiwan/guide/ludibrium/ /taiwan/ 301\n'
    '/vietnam/guide/ludibrium/ /vietnam/ 301\n'
    '/assets/cube-data/ /calculator/cube/ 301\n'
)
wr('_redirects', rd('_redirects') + extra)
report.append('⑦ _redirects +5행: lv-11-30(.html 포함) → /quests/, 대만·베트남 ludibrium → 각 홈, /assets/cube-data/ → 큐브 계산기. /status/는 참조 0이라 404 유지')

print('\n'.join(report))
