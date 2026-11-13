# 가이드 허브 빌더 (2026-11-13, 설계안 안 1 확정)
# /guide/ 허브: 머리말 + 가이드 카드 5장 + 지역 이야기 색인 + data-criteria 연결.
# 카드 갱신일은 각 페이지 푸터의 '페이지 갱신일' 실측값을 읽어 쓴다 (실제 반영일 규칙).
import os, re, json, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("ALPANG_HUB_OUT", os.path.join(ROOT, "staging-guidehub-20261113", "guide"))
REPO_RAW = "https://raw.githubusercontent.com/Kyosssa/alpang/main"

CARDS = [
    ("/guide/hunting/", "초반 사냥터 후보 비교", "빅토리아 아일랜드 초반 사냥터 39곳을 몬스터 · 레벨 · 출현 맵으로 비교하고, 분포 안내와 지역 이야기를 함께 실었습니다.", "빅토리아 아일랜드"),
    ("/guide/orbis-leafre/", "오르비스 & 리프레 몬스터 구경", "오르비스와 리프레 일대의 출현 몬스터와 출현 맵 표, 지역 이야기를 모았습니다.", "오르비스 · 리프레"),
    ("/guide/edelstein/", "에델슈타인 엿보기", "블랙윙의 광산 도시 에델슈타인의 맵과 출현 몬스터를 미리 살펴봅니다.", "에델슈타인"),
    ("/guide/ludibrium/", "루디브리엄 마을 가이드", "장난감 도시 루디브리엄의 맵과 출현 몬스터, 비출현 맵 구성을 정리했습니다.", "루디브리엄"),
    ("/guide/hunting-efficiency/", "사냥터 효율 읽는 법", "경험치와 레벨 범위를 읽는 순서로 내게 맞는 사냥터를 고르는 법을 정리했습니다.", "사냥터 효율"),
    ("/guide/return-routes/", "귀환 연결로 읽는 이동 절약법", "맵 402곳의 귀환 목적지를 역집계해 권역별 보급 거점을 정리했습니다.", "귀환 연결"),
    ("/guide/scroll-reward-quests/", "주문서 주는 퀘스트 총정리", "완료 보상으로 장비 주문서를 주는 퀘스트를 레벨 구간별로 정리했습니다.", "주문서 보상 퀘스트"),
    ("/guide/mushroom-shrine/", "버섯신사 엿보기", "지팡구 지역의 신사 마을 버섯신사의 이야기를 모았습니다.", "버섯신사"),
    ("/guide/early-quests/", "초반 퀘스트 큐레이션", "레벨 구간별로 먼저 볼 퀘스트와 보상 흐름을 골라 정리했습니다.", "초반 구간"),
]

STORIES = [
    ("엘리니아", "/guide/hunting/"), ("커닝시티", "/guide/hunting/"), ("리스항", "/guide/hunting/"),
    ("슬리피우드", "/guide/hunting/"), ("페리온", "/guide/hunting/"), ("엘나스", "/guide/orbis-leafre/"),
    ("노틸러스", "/guide/hunting/"), ("버섯신사", "/guide/mushroom-shrine/"),
    ("무릉", "/guide/orbis-leafre/"), ("백초해안", "/guide/orbis-leafre/"), ("아쿠아리움", "/guide/orbis-leafre/"),
    ("지구방위본부", "/guide/ludibrium/"),
]


def updated_of(url_path, fallback=""):
    """저장소 현행본 푸터에서 페이지 갱신일을 읽는다 (수령 실패 시 fallback)."""
    import urllib.request
    try:
        req = urllib.request.Request(REPO_RAW + url_path + "index.html", headers={"User-Agent": "Mozilla/5.0"})
        t = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        m = re.search(r"페이지 갱신일: ([0-9]{4}-[0-9]{2}-[0-9]{2})", t)
        return m.group(1) if m else fallback
    except Exception:
        return fallback


def build():
    cards = ""
    for url, title, desc, scope in CARDS:
        upd = updated_of(url)
        upd_html = f'<span class="upd">갱신일 {upd}</span>' if upd else ""
        cards += f'''    <a class="gcard" href="{url}">
      <h2>{title}</h2>
      <p>{desc}</p>
      <p class="meta"><span class="scope">{scope}</span>{upd_html}</p>
    </a>
'''
    stories = "\n".join(f'      <li><a href="{u}">{n}</a></li>' for n, u in STORIES)
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>가이드 전체 보기 — 알팡지지</title>
<meta name="description" content="알팡서버를 기다리며 정리한 지역 가이드 모음. 사냥터 · 오르비스 · 리프레 · 에델슈타인 · 루디브리엄 가이드와 초반 퀘스트 큐레이션을 한곳에서 봅니다.">
<link rel="canonical" href="https://alpang.gg/guide/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="가이드 전체 보기 — 알팡지지">
<meta property="og:description" content="지역 가이드와 초반 퀘스트 큐레이션을 한곳에서 봅니다.">
<meta property="og:url" content="https://alpang.gg/guide/">
<meta property="og:image" content="https://alpang.gg/assets/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<style>
:root{{--line:#e3e6ea;--card:#fff;--sub:#6b7280;--accent-dark:#9a4a12}}
body{{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:0;background:#faf9f6;color:#1f2430}}
main{{max-width:860px;margin:0 auto;padding:28px 16px 48px}}
h1{{font-size:24px;margin:0 0 8px}}
.lead{{color:var(--sub);font-size:14.5px;line-height:1.65;margin:0 0 22px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media (max-width:640px){{.grid{{grid-template-columns:1fr}}}}
.gcard{{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;text-decoration:none;color:inherit}}
.gcard h2{{font-size:16.5px;margin:0 0 6px}}
.gcard p{{font-size:13.5px;line-height:1.6;color:var(--sub);margin:0}}
.gcard .meta{{margin-top:10px;font-size:12px}}
.gcard .scope{{font-weight:700;color:var(--accent-dark);margin-right:8px}}
section.idx{{margin-top:30px}}
section.idx h2{{font-size:17px}}
section.idx ul{{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:8px}}
section.idx li a{{display:inline-block;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:6px 12px;font-size:13px;text-decoration:none;color:inherit}}
.foot{{margin-top:34px;font-size:13px;color:var(--sub)}}
.foot a{{color:var(--accent-dark)}}
</style>
</head>
<body>
<main>
  <h1>가이드 전체 보기</h1>
  <p class="lead">알팡서버를 기다리며 지역별로 정리한 가이드 모음입니다. 수록 데이터는 본진 메이플스토리 빅뱅 직후(GMS 95) 기준으로 수집한 자료이며, 알팡서버의 실제 구현과는 달라질 수 있어요.</p>
  <div class="grid">
{cards}  </div>
  <section class="idx">
    <h2>지역 이야기 색인</h2>
    <ul>
{stories}
    </ul>
  </section>
  <p class="foot">수록 데이터의 기준이 궁금하면 <a href="/data-criteria/">데이터 기준 안내</a>를 봐 주세요.</p>
  <footer style="text-align:center;color:var(--sub);font-size:12.5px;margin-top:28px;line-height:1.8">
    알팡지지는 팬이 운영하는 정보 사이트로, 넥슨 및 스트리머 측과 관계가 없습니다.<br>
    <a href="/privacy/" style="color:var(--sub)">개인정보처리방침</a> · <a href="/terms/" style="color:var(--sub)">이용약관</a> · <a href="/about/" style="color:var(--sub)">사이트 소개</a> · <a href="mailto:alpangland@gmail.com" style="color:var(--sub)">문의하기</a><br>
    <span style="font-size:12px">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
  </footer>
</main>
</body>
</html>
"""
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    return html


if __name__ == "__main__":
    h = build()
    print("guide hub built | bytes:", len(h.encode("utf-8")))
