import json, os, re
from html import escape
from collections import OrderedDict

BASE = os.path.expanduser("~/workspace/alpang")
SRC = f"{BASE}/data/db/items.json"  # 최종 채택 정본 (2026-10-27)
EQUIP_SRC = f"{BASE}/data/db/equipment.json"
OUT = f"{BASE}/out-items-final-adopted-20261027"
os.makedirs(OUT, exist_ok=True)

NOTICE = "본진 빅뱅 직후(GMS 95) 기준 데이터이며 알팡서버 실서버와 다를 수 있습니다. 한글 이름은 표시명 후보입니다. 알팡서버 공식 오픈 시 해당 버전에 맞춰 상세 정보를 업데이트할 예정입니다.<br>아이콘·이미지: maplestory.io"
SORT_UI = """  <div class="sortbar"><label class="flb" for="itemSort">정렬</label><select id="itemSort" class="fsort"><option value="base">기본 정렬</option><option value="lvAsc">요구 레벨 낮은 순</option><option value="lvDesc">요구 레벨 높은 순</option><option value="name">이름순</option></select></div>
"""
SORT_SCRIPT = """<script>
(function(){
var sel=document.getElementById('itemSort');if(!sel)return;
var grids=[].slice.call(document.querySelectorAll('.igrid'));
var base=grids.map(function(g){return [].slice.call(g.querySelectorAll('.icard'));});
function lv(c){var v=c.getAttribute('data-lv');return v===''||v===null?null:parseInt(v,10);}
function tail(c){return lv(c)===null||c.getAttribute('data-unv')==='1';}
function nm(c){return c.getAttribute('data-name')||'';}
sel.addEventListener('change',function(){
  var mode=sel.value;
  grids.forEach(function(g,gi){
    var cards;
    if(mode==='base'){cards=base[gi].slice();}
    else{cards=[].slice.call(g.querySelectorAll('.icard')).sort(function(a,b){
      var la=lv(a),lb=lv(b);
      var ta=tail(a),tb=tail(b);
      if(mode==='name'){if(ta&&!tb)return 1;if(!ta&&tb)return -1;return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);}
      if(ta&&tb)return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);
      if(ta)return 1;if(tb)return -1;
      var d=mode==='lvDesc'?(lb-la):(la-lb);if(d)return d;
      return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);});}
    cards.forEach(function(c){g.appendChild(c);});
  });
});
})();
</script>"""
STAT_NOTICE = "<b>본진 GMS 95 기준 기본 능력치</b> — 장비 행에 표시되는 능력치는 강화 전 원본 수치이며, 개별 아이템의 랜덤 옵션·강화 결과·알팡 적용 여부는 확인되지 않았습니다."
CAT_KO = {"Equip": "장비", "Use": "소비", "Etc": "기타", "Cash": "캐시", "Setup": "설치"}
# 세부 분류 영문 원본명 → 한글 표시명 (파일명·URL·slug는 원본 유지, 화면 표시만 교체)
SUB_KO = {
    # Equip
    "Belt": "벨트", "Bottom": "하의", "Bow": "활", "Cape": "망토", "Cash": "캐시 장비",
    "Claw": "아대", "Crossbow": "석궁", "Dagger": "단검", "Dragon Equipment": "드래곤 장비",
    "Earrings": "귀고리", "Eye Decoration": "눈장식", "Face": "얼굴", "Face Accessory": "얼굴장식",
    "Glove": "장갑", "Gun": "총", "Hair": "헤어", "Hat": "모자", "Katara": "카타라",
    "Knuckle": "너클", "Mechanic Equipment": "메카닉 장비", "Medal": "훈장", "Mount": "라이딩",
    "One-Handed Axe": "한손도끼", "One-Handed Blunt Weapon": "한손둔기", "One-Handed Sword": "한손검",
    "Overall": "한벌옷", "Pendant": "펜던트", "Pet Equipment": "펫 장비", "Pet Use": "펫 아이템",
    "Pole Arm": "폴암", "Ring": "반지", "Shield": "방패", "Shoes": "신발",
    "Shoulder Accessory": "어깨장식", "Skill Effect": "스킬 이펙트", "Spear": "창",
    "Staff": "스태프", "Top": "상의", "Two-Handed Axe": "두손도끼", "Two-Handed Blunt": "두손둔기",
    "Two-Handed Sword": "두손검", "Wand": "완드",
    # Use
    "AP/SP Reset": "AP/SP 초기화", "Accessory": "장신구", "Armor": "방어구", "Arrow": "화살",
    "Belts": "벨트", "Bottomwear": "하의", "Bullet": "총알", "Capsule": "캡슐",
    "Chaos Scroll": "혼돈의 주문서", "Clean Slate Scroll": "순백의 주문서", "Consumable": "소비",
    "Crossbow Bolt": "볼트", "Equip Enhancement": "장비 강화", "Equipment Box": "장비 상자",
    "EXP Buff": "경험치 버프", "EXP Potion": "경험치 물약", "Eye": "눈",
    "Food and Drink": "음식과 음료", "Gloves": "장갑", "Hammer": "망치", "Helmet": "헬멧",
    "Item Pot": "아이템 팟", "Lie Detector": "거짓말 탐지기", "Magnifying Glass": "돋보기",
    "Mastery Book": "마스터리북", "Message": "메시지", "Monster Card": "몬스터 카드",
    "Monster Taming": "몬스터 테이밍", "One-Handed BW": "한손둔기", "One-Handed Weapon": "한손무기",
    "Other": "기타", "Owl": "부엉이", "Pet": "펫", "Pet Food": "펫 먹이", "Polearm": "폴암",
    "Potential Scroll": "잠재능력 주문서", "Potion": "물약", "Status Cure": "상태 회복",
    "Summoning Sack": "소환 주머니", "Teleport Item": "텔레포트 아이템", "Thrown": "표창",
    "Time Extension": "시간 연장", "Topwear": "상의", "Transformation": "변신",
    "Two-Handed BW": "두손둔기", "Two-Handed Weapon": "두손무기", "White Scroll": "백의 주문서",
    # Etc
    "Book": "책", "Coin": "코인", "Cosmetic": "뷰티", "Effect": "이펙트", "Maker": "제작",
    "Mineral Ore": "광석", "Mineral Processed": "가공 광석", "Minigame": "미니게임",
    "Monster Drop": "몬스터 드롭", "Pet Command": "펫 명령어", "Quest Item": "퀘스트 아이템",
    "Rare Ore": "희귀 광석", "Rare Processed  Ore": "가공 희귀 광석", "Reward Item": "보상 아이템",
    "Wedding": "웨딩",
    # Cash
    "Character Effect": "캐릭터 이펙트", "Cosmetic Lens": "미용 렌즈", "Drop Coupon": "드롭률 쿠폰",
    "Entry Pass": "입장권", "Exchange Coupon": "교환 쿠폰", "EXP Coupon": "경험치 쿠폰",
    "Face Coupon": "성형 쿠폰", "Facial Expression": "표정", "Gachapon": "가챠폰",
    "Guild Forum Emoticon": "길드 이모티콘", "Hair Color Coupon": "염색 쿠폰", "Hair Coupon": "헤어 쿠폰",
    "Hired Merchant": "고용 상인", "Inventory Slot": "인벤토리 확장", "Item Store": "아이템 보관",
    "Kite": "연", "Messageboard": "게시판", "Messenger": "메신저", "Miracle Cube": "미라클 큐브",
    "Note": "노트", "Package": "패키지", "Protection": "보호", "Quest Helper": "퀘스트 도우미",
    "Scroll": "주문서", "Skin Coupon": "피부 쿠폰", "Song": "노래", "SP/AP Modification": "AP/SP 변경",
    "Special Item": "스페셜 아이템", "Store Permit": "상점 이용권", "Surprise Box": "서프라이즈 박스",
    "Teleport Rock": "텔레포트 락", "Trade": "거래", "Upgrade Slot": "업그레이드 슬롯",
    "Weather Effect": "날씨 효과",
    # Setup
    "Chair": "의자", "Decoration": "장식", "Event Item": "이벤트 아이템", "Key": "열쇠",
}

def sub_ko(s):
    return SUB_KO.get(s, s)
CAT_ORDER = ["Equip", "Use", "Etc", "Cash", "Setup"]
# 대분류 탭 표시 순서 (대표 확정: 장비 / 소비 / 설치 / 기타 / 캐시)
TAB_ORDER = ["Equip", "Use", "Setup", "Etc", "Cash"]
# 장비 세부 분류 42종 → 구분 그룹 (무기/방어구/장신구/기타)
# 근거: items.json의 category 필드 합계와 정확히 일치하는 매핑
#   무기 = One-Handed Weapon + Two-Handed Weapon (1,491개), 방어구 = Armor (3,450개),
#   장신구 = Accessory (757개, 훈장 포함), 기타 = Character + Other + Mount (2,729개)
# Cash(캐시 장비)는 세부 분류명과 달리 전 항목이 category=One-Handed Weapon(캐시 무기)이라 무기로 분류.
SUB_GROUP = {
    # 무기 (18)
    "Bow": "무기", "Claw": "무기", "Crossbow": "무기", "Dagger": "무기", "Gun": "무기",
    "Katara": "무기", "Knuckle": "무기", "One-Handed Axe": "무기", "One-Handed Blunt Weapon": "무기",
    "One-Handed Sword": "무기", "Pole Arm": "무기", "Spear": "무기", "Staff": "무기",
    "Two-Handed Axe": "무기", "Two-Handed Blunt": "무기", "Two-Handed Sword": "무기", "Wand": "무기",
    "Cash": "무기",
    # 방어구 (8)
    "Hat": "방어구", "Overall": "방어구", "Top": "방어구", "Bottom": "방어구",
    "Shoes": "방어구", "Glove": "방어구", "Cape": "방어구", "Shield": "방어구",
    # 장신구 (8)
    "Face Accessory": "장신구", "Ring": "장신구", "Earrings": "장신구", "Eye Decoration": "장신구",
    "Pendant": "장신구", "Belt": "장신구", "Shoulder Accessory": "장신구", "Medal": "장신구",
    # 기타 (8)
    "Hair": "기타", "Face": "기타", "Pet Equipment": "기타", "Pet Use": "기타",
    "Mount": "기타", "Mechanic Equipment": "기타", "Dragon Equipment": "기타", "Skill Effect": "기타",
}
GROUP_ORDER = ["무기", "방어구", "장신구", "기타"]
# 직업 필터 (reqJob 비트: 전사 1 / 마법사 2 / 궁수 4 / 도적 8 / 해적 16, 0 = 공용)
JOB_FILTERS = [("common", "공용"), ("1", "전사"), ("2", "마법사"), ("4", "궁수"), ("8", "도적"), ("16", "해적")]
SIZE_LIMIT = 2_000_000

THEME_INIT = "<script>(function(){var t=null;try{t=localStorage.getItem('alpang-theme');}catch(e){}if(t!=='dark'&&t!=='light'){t='dark';}document.documentElement.setAttribute('data-theme',t);})();</script>"
THEME_BTN = '<button type="button" class="theme-toggle" id="themeToggle" aria-label="다크모드 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg></button>'
THEME_SCRIPT = "<script>(function(){var b=document.getElementById('themeToggle');if(!b){return;}b.addEventListener('click',function(){var n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',n);try{localStorage.setItem('alpang-theme',n);}catch(e){}});})();</script>"

LIVE_BADGE = ''  # 배지 끈 조건 (사업실장 승인 2026-10-23 — 라이브 기준 산출과 표시 동일)

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
  .notice{background:var(--accent-soft);border:1px solid var(--line);border-radius:10px;padding:12px 16px;font-size:14px;color:var(--text);margin-top:16px;text-align:left}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-top:18px}
  .kpi{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 14px;box-shadow:0 1px 3px rgba(30,25,15,.05);text-decoration:none;color:var(--text)}
  .kpi .lb{font-size:13px;color:var(--sub);font-weight:700}
  .kpi .vl{font-size:26px;font-weight:800;margin-top:2px} .kpi .vl small{font-size:13px;color:var(--sub);font-weight:600}
  section.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 3px rgba(30,25,15,.05);padding:20px 22px;margin-top:14px}
  h2{font-size:18px;font-weight:700;margin-bottom:10px;scroll-margin-top:76px}
  h2 .cnt{color:var(--accent-dark);font-size:13.5px;font-weight:700;margin-left:6px}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 4px}
  .chip{font-size:13.5px;font-weight:600;padding:4px 11px;border-radius:999px;background:#f4f1ea;color:var(--text);text-decoration:none}
  .chip b{color:var(--accent-dark);font-weight:800}
  table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
  th{font-size:12.5px;color:var(--sub);text-align:left;padding:8px 10px;border-bottom:2px solid var(--line)}
  td{padding:8px 10px;border-bottom:1px solid #f0ece3;vertical-align:top}
  td.lv,td.cs,th.lv,th.cs{text-align:center;width:76px;white-space:nowrap}
    .nwrap{display:flex;align-items:center;gap:8px}
  .islot{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:#F3F4F6;border-radius:6px;flex:none}
  .iic{width:32px;height:32px;object-fit:contain;flex:none}
  .ntxt{display:block;min-width:0}
  .en{display:block;font-size:12.5px;color:var(--sub);font-weight:400}
  .stats{display:block;font-size:13.5px;color:var(--sub);font-weight:400;line-height:1.55}
  .st-hl{color:#E8930C;font-weight:700}.st-base{color:var(--sub)}.st-up{background:#DCEEFF;color:#1668B4;border-radius:4px;padding:0 5px;font-weight:700}
  .cash{display:inline-block;font-size:11px;font-weight:800;padding:2px 6px;border-radius:4px;background:var(--accent-soft);color:var(--accent-dark)}
  .back{font-size:14px;margin-top:14px}
  a{color:var(--accent-dark)}
  footer{text-align:center;color:var(--unknown);font-size:12.5px;margin-top:28px;line-height:1.8}
  @media (max-width:560px){ section.card{padding:16px} td.lv,td.cs,th.lv,th.cs{width:58px} table{font-size:14px} }
  .tabs{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
  .tabs a{font-size:14.5px;font-weight:700;padding:7px 16px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--text);text-decoration:none}
  .tabs a .n{color:var(--accent-dark);font-weight:800;margin-left:5px;font-size:13px}
  .jobfilter{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:2px 0 12px}
  .jobfilter .fl{font-size:13.5px;font-weight:700;color:var(--sub);margin-right:2px}
  .jfbtn{font-size:13.5px;font-weight:600;padding:5px 12px;border-radius:999px;background:#f4f1ea;border:1px solid transparent;color:var(--text);cursor:pointer}
  .jfbtn.on{background:var(--accent);color:#fff;font-weight:800}
  .jfcount{font-size:13px;color:var(--sub);margin-left:4px}
  .gentoggle{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:600;margin-left:14px;cursor:pointer}
  .gentoggle input{width:16px;height:16px;accent-color:#FF6B00}
  .emptyf{font-size:14px;color:var(--sub);padding:10px 2px 4px}
  .gnav .grow{display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px;padding:5px 0}
  .gnav .glb{flex:none;width:46px;font-size:13.5px;font-weight:800;color:var(--accent-dark);padding-top:5px}
  .igrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
  .imore{display:block;margin:12px auto 4px;font:inherit;font-size:14.5px;font-weight:700;padding:10px 26px;border-radius:999px;background:var(--card);border:1px solid var(--line);color:var(--accent-dark);cursor:pointer}
  .icard{border:1px solid var(--line);border-radius:12px;padding:12px 10px;background:var(--bg);display:flex;flex-direction:column;scroll-margin-top:90px}
  .icard:target{outline:2px solid var(--accent);outline-offset:2px}
  .icard .islot{width:48px;height:48px;margin:2px auto 0;border-radius:8px}
  .icard .iic{width:40px;height:40px}
  .icard .nm{display:block;text-align:center;margin-top:8px;font-size:15px;line-height:1.45;font-weight:800;word-break:keep-all}
  .icard .en{text-align:center;font-size:12px;color:var(--sub)}
  .icard .stats{margin-top:6px;font-size:12.5px;line-height:1.5}
  .icard .meta{display:flex;justify-content:space-between;align-items:center;gap:6px;border-top:1px solid var(--line);margin-top:9px;padding-top:7px;font-size:12px;color:var(--sub)}
  @media (min-width:640px){ .igrid{grid-template-columns:repeat(3,1fr)} }
  @media (min-width:900px){ .igrid{grid-template-columns:repeat(4,1fr)} }
  @media (min-width:1120px){ .igrid{grid-template-columns:repeat(5,1fr)} }
  @media (min-width:1320px){ .igrid{grid-template-columns:repeat(6,1fr)} }
  .cgwrap h3{font-size:15px;font-weight:800;color:var(--accent-dark);margin:16px 0 8px}
  .cgwrap h3:first-child{margin-top:2px}
  .cgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
  .icat{display:flex;flex-direction:column;align-items:center;border:1px solid var(--line);border-radius:12px;padding:14px 10px;background:var(--bg);text-decoration:none;color:var(--text)}
  .icat .islot{width:48px;height:48px;border-radius:8px}
  .icat .iic{width:40px;height:40px}
  .icat   .icat .cc{font-size:12.5px;color:var(--sub);margin-top:2px}
  @media (min-width:700px){ .cgrid{grid-template-columns:repeat(3,1fr)} }
  @media (min-width:1000px){ .cgrid{grid-template-columns:repeat(4,1fr)} }
  @media (min-width:1240px){ .cgrid{grid-template-columns:repeat(5,1fr)} }
  .chip.on{background:var(--accent);color:#fff}
  .chip.on b{color:#fff}
  [data-theme="dark"] .jfbtn{background:#22252B}
  [data-theme="dark"] .jfbtn.on{background:var(--accent);color:#fff}
  .theme-toggle{flex:none;width:34px;height:34px;margin-left:12px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:999px;color:var(--sub);cursor:pointer;padding:0}
  .theme-toggle svg{width:18px;height:18px;display:block}
  .theme-toggle .ic-sun{display:none}
  [data-theme="dark"]{--bg:#121417;--card:#1E2229;--line:#2E3238;--text:#ECE9E2;--sub:#AEA392;--accent-dark:#FF9E57;--accent-soft:#2A1C0F;--unknown:#A79E8B;color-scheme:dark}
  [data-theme="dark"] body{letter-spacing:-0.01em}
  [data-theme="dark"] .theme-toggle .ic-sun{display:block}
  [data-theme="dark"] .theme-toggle .ic-moon{display:none}
  [data-theme="dark"] .gnb{background:rgba(18,20,23,.92)}
  [data-theme="dark"] section.card{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .kpi{box-shadow:0 1px 3px rgba(0,0,0,.35)}
  [data-theme="dark"] .chip{background:#22252B}
  [data-theme="dark"] .islot{background:#26292F}
  [data-theme="dark"] td{border-bottom-color:var(--line)}

/* 디렉터 4번 — GNB · 필터 탭 인게임 버튼 느낌 (입체감만, 색상 체계 유지) */
header nav a, .chips .chip, .tabs .tab, .fchip{transition:transform .12s ease, box-shadow .12s ease}
header nav a:hover, .chips .chip:hover, .tabs .tab:hover, .fchip:hover{transform:translateY(-2px)}
header nav a.on, .chips .chip.on, .tabs .tab.on, .fchip.on{background:linear-gradient(180deg, color-mix(in srgb, var(--accent) 72%, #fff) 0%, var(--accent) 55%, var(--accent-dark) 100%);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.55), inset 0 1px 0 rgba(255,255,255,.65), 0 1px 2px rgba(0,0,0,.18)}

  .tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}
  .tscroll-hint{display:block;text-align:right;font-size:11px;color:var(--sub);margin-bottom:4px}

  .topbtn{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--accent);color:#fff;border:none;border-radius:999px;padding:10px 14px;font-size:13px;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.25);cursor:pointer;opacity:0;pointer-events:none;transition:opacity .18s}
  .topbtn.on{opacity:1;pointer-events:auto}
"""

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-") or "etc"

TL_DOT = '<span class="new-dot" id="tlNewDot" aria-label="새 글 있음"></span>'

def gnb(active):
    links = [("/", "홈"), ("/timeline/", "타임라인"), ("/faq/", "FAQ"), ("/mobs/", "몬스터 도감"), ("/maps/", "맵 탐색"), ("/items/", "아이템"), ("/npcs/", "NPC·퀘스트"), ("/jobs/", "직업·스킬"), ("/calculator/cube/", "큐브값 계산기")]
    nav = "".join(f'<a href="{h}"{" class=\"on\"" if h == active else ""}>{t}{TL_DOT if h == "/timeline/" else ""}</a>' for h, t in links)
    return f'<div class="gnb"><a href="/" class="logo" aria-label="알팡지지 홈"><img src="/assets/logo.png" alt="알팡지지" style="height:30px;width:auto;display:block"></a><nav>{nav}</nav>{THEME_BTN}</div>'

def page(title, desc, canonical, active, body):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7564661082214740" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 알팡지지</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="알팡지지">
<meta property="og:title" content="{title} — 알팡지지">
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
<style>{CSS}
  .new-dot{{display:none;width:7px;height:7px;border-radius:50%;background:#E5484D;margin-left:5px;vertical-align:super}}
  .new-dot.on{{display:inline-block}}

  .twrap{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
  .twrap>table{{margin:0}}
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
    데이터 기준: 본진 메이플스토리 빅뱅 직후 구간(GMS 95) · 페이지 갱신일: 2026-10-14
  <br>
    <span style="font-size:12px;color:var(--sub)">본 사이트의 게임 데이터는 본진 GMS 95 기준으로 maplestory.io를 참조해 정리했습니다.<br>
    메이플스토리 및 관련 이미지·자료의 권리는 넥슨에 있으며, 알팡지지는 넥슨과 관계없는 비공식 팬 사이트입니다.</span>
    <div class="lang-switch" style="margin-top:8px;font-size:13px"><strong aria-current="true">한국어</strong> · <a href="/taiwan/" style="color:var(--sub)">繁體中文</a> · <a href="/vietnam/" style="color:var(--sub)">Tiếng Việt</a></div>
  </footer>
</div>
{THEME_SCRIPT}
<script src="/assets/hit.js?v=2" defer></script>
<script src="/assets/timeline-latest.js"></script><script src="/assets/timeline-signal.js"></script>
<button type="button" class="topbtn" id="topBtn" aria-label="맨 위로 이동">↑ Top</button><script>(function(){{var b=document.getElementById('topBtn');if(!b)return;addEventListener('scroll',function(){{b.classList.toggle('on',scrollY>600)}},{{passive:true}});b.addEventListener('click',function(){{scrollTo({{top:0,behavior:'smooth'}})}});}})();</script>
{PAGING_SCRIPT}
</body>
</html>"""

# 장비 기본 능력치 (build 0500 equipment.json) — 값은 원본 그대로만 표시한다.
# null(미확인)인 스탯 값은 표시하지 않고, 실제 0인 스탯도 요약에서는 제외한다.
# 단 요구 레벨은 null만 미확인으로 처리하고 실제 0은 "요구Lv 0"으로 표시한다 (기술이사 검수 지시 2026-10-14).
# detail_status가 unverified_null인 행은 능력치 대신 '상세 미확인 · 목록 정보만 표시' 안내를 붙인다.
try:
    _eq_doc = json.load(open(EQUIP_SRC))
    EQUIP_STATS = {str(x["id"]): x for x in _eq_doc.get("equipment", [])}
except (OSError, ValueError):
    EQUIP_STATS = {}

def job_attr(it):
    """행의 data-job 값. 원본 job_code_raw를 그대로 쓰되, 원본에 값이 없으면 'all'(직업 제한 미기록).
    판정 규칙(JS와 동일): 'all'·0·-1은 전 직업 표시, 양수는 비트 합 — 해당 비트 직업들에 모두 걸린다."""
    rec = EQUIP_STATS.get(str(it["id"]))
    if not rec:
        return "all"
    jc = (rec.get("requirements") or {}).get("job_code_raw")
    return "all" if jc is None else str(jc)

JOB_FILTER_HTML = ('<div class="jobfilter" role="group" aria-label="직업 필터"><span class="fl">직업</span>'
                   '<button type="button" class="jfbtn on" data-jf="all">전체</button>'
                   + "".join(f'<button type="button" class="jfbtn" data-jf="{q}">{label}</button>' for q, label in JOB_FILTERS)
                   + '<span class="jfcount"></span></div>')
JOB_EMPTY_HTML = '<p class="emptyf" hidden>선택한 직업으로 볼 수 있는 아이템이 이 분류에는 없습니다.</p>'
JOB_FILTER_SCRIPT = """<script>(function(){
var btns=document.querySelectorAll('.jfbtn');if(!btns.length)return;
var rows=document.querySelectorAll('[data-job]');
var empty=document.querySelector('.emptyf');var cnt=document.querySelector('.jfcount');
function apply(f){
  var shown=0;
  rows.forEach(function(r){
    var raw=r.getAttribute('data-job');var ok;
    if(f==='all'||raw==='all'){ok=true;}
    else{var j=parseInt(raw,10);
      if(j===0||j===-1){ok=true;}
      else if(f==='common'){ok=false;}
      else{ok=(j&parseInt(f,10))!==0;}}
    r.style.display=ok?'':'none';if(ok){shown++;}
  });
  if(empty){empty.hidden=shown>0;}
  if(cnt){cnt.textContent=shown.toLocaleString()+'개 표시';}
  btns.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-jf')===f);});
}
btns.forEach(function(b){b.addEventListener('click',function(){apply(b.getAttribute('data-jf'));});});
var q=new URLSearchParams(location.search).get('job');
if(q&&document.querySelector('.jfbtn[data-jf="'+q+'"]')){apply(q);}else{apply('all');}
})();</script>"""

PAGING_SCRIPT = """<script>
(function(){
  var PAGE = 50;
  var grids = [].slice.call(document.querySelectorAll('.igrid'));
  if (!grids.length) return;
  var states = grids.map(function (g) {
    return { g: g, limit: PAGE, btn: (function () { var n = g.nextElementSibling; return (n && n.classList.contains('imore')) ? n : null; })() };
  });
  function applyGrid(st) {
    var cards = [].slice.call(st.g.querySelectorAll('.icard'));
    cards.forEach(function (c) { if (c.getAttribute('data-pg') === '1') { c.style.display = ''; c.removeAttribute('data-pg'); } });
    var passed = cards.filter(function (c) { return c.style.display !== 'none'; });
    var visible = 0;
    passed.forEach(function (c, i) {
      if (i >= st.limit) { c.style.display = 'none'; c.setAttribute('data-pg', '1'); }
      else visible++;
    });
    if (!st.btn) return;
    if (passed.length <= visible) { st.btn.hidden = true; }
    else { st.btn.hidden = false; st.btn.textContent = '더 보기 (남은 ' + (passed.length - visible).toLocaleString('ko-KR') + '건)'; }
  }
  function applyAll() { states.forEach(applyGrid); }
  states.forEach(function (st) {
    if (st.btn) st.btn.addEventListener('click', function () { st.limit += PAGE; applyGrid(st); });
  });
  document.addEventListener('click', function () { setTimeout(applyAll, 0); });
  document.addEventListener('change', function () { setTimeout(applyAll, 0); });
  if (location.hash) {
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('icard')) {
      states.forEach(function (st) {
        var cards = [].slice.call(st.g.querySelectorAll('.icard'));
        var ti = cards.indexOf(target);
        if (ti >= st.limit) st.limit = ti + 1;
      });
    }
  }
  applyAll();
})();
</script>"""

EQUIP_SCRIPT = """<script>(function(){
var sel=document.getElementById('itemSort');
var genBox=document.getElementById('genOnly');
var btns=document.querySelectorAll('.jfbtn');
var rows=[].slice.call(document.querySelectorAll('.icard'));
var empty=document.querySelector('.emptyf');var cnt=document.querySelector('.jfcount');
var jobF='all';
var grids=[].slice.call(document.querySelectorAll('.igrid'));
var base=grids.map(function(g){return [].slice.call(g.querySelectorAll('.icard'));});
function lv(c){var v=c.getAttribute('data-lv');return v===''||v===null?null:parseInt(v,10);}
function nm(c){return c.getAttribute('data-name')||'';}
function tail(c){return lv(c)===null||c.getAttribute('data-unv')==='1';}
function jobOk(r){
  var raw=r.getAttribute('data-job');
  if(jobF==='all'||raw==='all'||raw===null){return true;}
  var j=parseInt(raw,10);
  if(j===0||j===-1){return true;}
  if(jobF==='common'){return false;}
  return (j&parseInt(jobF,10))!==0;
}
function applyDisplay(){
  var shown=0;
  rows.forEach(function(r){
    var ok=jobOk(r)&&(!genBox||!genBox.checked||r.getAttribute('data-gen')==='1');
    r.style.display=ok?'':'none';if(ok){shown++;}
  });
  if(empty){empty.hidden=shown>0;}
  if(cnt){cnt.textContent=shown.toLocaleString()+'개 표시';}
  btns.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-jf')===jobF);});
}
function applySort(){
  if(!sel)return;
  var mode=sel.value;
  grids.forEach(function(g,gi){
    var cards;
    if(mode==='base'){cards=base[gi].slice();}
    else{cards=[].slice.call(g.querySelectorAll('.icard')).sort(function(a,b){
      var la=lv(a),lb=lv(b);
      var ta=tail(a),tb=tail(b);
      if(mode==='name'){if(ta&&!tb)return 1;if(!ta&&tb)return -1;return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);}
      if(ta&&tb)return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);
      if(ta)return 1;if(tb)return -1;
      var d=mode==='lvDesc'?(lb-la):(la-lb);if(d)return d;
      return nm(a)<nm(b)?-1:(nm(a)>nm(b)?1:0);});}
    cards.forEach(function(c){g.appendChild(c);});
  });
}
if(sel){sel.addEventListener('change',function(){applySort();applyDisplay();});}
if(genBox){genBox.addEventListener('change',applyDisplay);}
btns.forEach(function(b){b.addEventListener('click',function(){jobF=b.getAttribute('data-jf');applyDisplay();});});
var q=new URLSearchParams(location.search).get('job');
if(q&&document.querySelector('.jfbtn[data-jf="'+q+'"]')){jobF=q;}
applyDisplay();
})();</script>"""
GEN_TOGGLE = '  <label class="gentoggle"><input type="checkbox" id="genOnly" checked> 일반 장비만 보기</label>\n'
JOB_NAV_CARD = ('  <section class="card"><h2>직업별로 보기</h2><div class="chips jnav">'
                + "".join(f'<a class="chip" data-j="{q}" href="?job={q}">{label}</a>' for q, label in JOB_FILTERS)
                + '</div><p class="emptyf" id="jobnote" hidden></p></section>\n')
JOB_NAV_SCRIPT = """<script>(function(){
var q=new URLSearchParams(location.search).get('job');
var names={'common':'공용','1':'전사','2':'마법사','4':'궁수','8':'도적','16':'해적'};
if(!q||!names[q]){return;}
document.querySelectorAll('a[href^="/items/equip-"]').forEach(function(a){a.setAttribute('href',a.getAttribute('href')+'?job='+q);});
var el=document.getElementById('jobnote');
if(el){el.hidden=false;el.textContent='직업 필터: '+names[q]+' — 아래 분류를 열면 선택한 직업으로 걸러서 보여줍니다.';}
document.querySelectorAll('.jnav a').forEach(function(a){if(a.getAttribute('data-j')===q){a.classList.add('on');}});
})();</script>"""

def stat_line(it):
    """장비 행의 능력치 한 줄 요약. 표시할 값이 없으면 빈 문자열."""
    if it.get("overall_category") != "Equip":
        return ""
    rec = EQUIP_STATS.get(str(it["id"]))
    if not rec:
        return ""
    # 상세 미확인 안내는 외형(얼굴·헤어 등 Character 분류)에도 동일하게 표시한다 (기술이사 검수 지시 2026-10-14).
    # 단 외형 항목에는 능력치 요약을 붙이지 않는다.
    if rec.get("detail_status") == "unverified_null":
        return "상세 미확인 · 목록 정보만 표시"
    if it.get("category") == "Character":
        return ""
    if rec.get("detail_status") != "confirmed":
        return ""
    rq = rec.get("requirements") or {}
    bs = rec.get("base_stats") or {}
    up = (rec.get("upgrade") or {}).get("base_slots")
    parts = []
    lv = rq.get("level")
    if lv is not None:
        parts.append(f"요구Lv {lv}")
    for key, label in (("str", "STR"), ("dex", "DEX"), ("int", "INT"), ("luk", "LUK"), ("hp", "HP"), ("mp", "MP")):
        v = bs.get(key)
        if v:
            _cls = ' class="st-base"' if key in ("str", "dex", "int", "luk") else ""
            parts.append(f"<span{_cls}>{label} {v:+d}</span>")
    for key, label in (("physical_attack", "공격력"), ("magic_attack", "마력"),
                       ("physical_defense", "물방"), ("magic_defense", "마방"),
                       ("accuracy", "명중"), ("avoidability", "회피"),
                       ("speed", "이동속도"), ("jump", "점프력")):
        v = bs.get(key)
        if v:
            _cls = ' class="st-hl"' if key in ("physical_attack", "magic_attack", "speed", "jump") else ""
            parts.append(f"<span{_cls}>{label} {v}</span>")
    if up is not None:
        parts.append(f'<span class="st-up">업글 {up}회</span>')
    return " · ".join(parts)

def name_cell(it, stats=""):
    ko = (it.get("name_ko") or it.get("name_ko_candidate") or "").strip()
    en = escape(it.get("name_en") or "")
    if ko:
        txt = f'<span class="nm t-ko">{escape(ko)}</span><span class="en">{en}</span>'
    else:
        txt = f'<span class="nm t-en">{en}</span>'
    if stats:
        txt += f'<span class="stats">{stats}</span>'  # stats는 stat_line이 수치로 조립한 강조 span — 이스케이프 시 태그 날것 노출 (2026-11-10 핫픽스)
    icon = f'<img class="iic" src="https://maplestory.io/api/GMS/95/item/{it["id"]}/icon" alt="" loading="lazy" onerror="this.style.display=\'none\'">'
    return f'<span class="nwrap"><span class="islot">{icon}</span><span class="ntxt">{txt}</span></span>'

def rows_html(items, with_stats=False, with_jobs=False):
    rows = []
    for it in items:
        lv = it.get("required_level")
        # 필요 레벨 셀: null만 '-' (미확인), 실제 0은 '0'으로 표시 (기술이사 검수 지시 2026-10-14 — truthy 검사로 0을 누락시키지 말 것)
        lv = str(lv) if lv is not None else "-"
        cs = '<span class="cash">캐시</span>' if it.get("is_cash") else "-"
        attr = f' data-job="{job_attr(it)}"' if with_jobs else ""
        rows.append(f'<tr{attr}><td>{name_cell(it, stat_line(it) if with_stats else "")}</td><td class="lv">{lv}</td><td class="cs">{cs}</td></tr>')
    return "\n".join(rows)

def table_html(items, with_stats=False, with_jobs=False):
    return ('<div class="tscroll"><span class="tscroll-hint" aria-hidden="true">좌우로 밀어 표 전체를 볼 수 있어요</span><table><thead><tr><th>이름</th><th class="lv">필요 레벨</th><th class="cs">캐시</th></tr></thead><tbody>'
            + rows_html(items, with_stats, with_jobs) + "</tbody></table></div>")

def icon_img(it, cls="iic"):
    return (f'<img class="{cls}" src="https://maplestory.io/api/GMS/95/item/{it["id"]}/icon" alt="" loading="lazy" '
            f'onerror="this.style.display=\'none\'">')

def card_html(it, with_stats=False, with_jobs=False):
    """아이템 카드 1개. 기존 표의 핵심 열(필요 레벨·캐시)을 카드 하단 메타 줄로 보존한다."""
    ko = (it.get("name_ko") or it.get("name_ko_candidate") or "").strip()
    en = escape(it.get("name_en") or "")
    if ko:
        txt = f'<span class="nm t-ko">{escape(ko)}</span><span class="en">{en}</span>'
    else:
        txt = f'<span class="nm t-en">{en}</span>'
    stats = stat_line(it) if with_stats else ""
    if stats:
        txt += f'<span class="stats">{stats}</span>'  # stats는 stat_line이 수치로 조립한 강조 span — 이스케이프 시 태그 날것 노출 (2026-11-10 핫픽스)
    lv = it.get("required_level")
    lv = str(lv) if lv is not None else "-"
    cs = '<span class="cash">캐시</span>' if it.get("is_cash") else "<span>캐시 아님</span>"
    attr = f' data-job="{job_attr(it)}"' if with_jobs else ""
    disp = (it.get("name_ko") or it.get("name_ko_candidate") or it.get("name_en") or "")
    disp = disp.strip()
    attr += f' data-lv="{lv if lv != "-" else ""}" data-name="{escape(disp)}"'
    if _item_unv(it):
        attr += ' data-unv="1"'
    if _item_gen(it):
        attr += ' data-gen="1"'
    return (f'<div class="icard" id="it{it["id"]}"{attr}><span class="islot">{icon_img(it)}</span>{txt}'
            f'<div class="meta"><span>필요 레벨 {lv}</span>{cs}</div></div>')

def grid_html(items, with_stats=False, with_jobs=False):
    html = '<div class="igrid">' + "".join(card_html(it, with_stats, with_jobs) for it in items) + "</div>"
    if len(items) > 50:
        html += '<button type="button" class="imore" hidden>더 보기</button>'
    return html

STAT_KEYS = ("str", "dex", "int", "luk", "hp", "mp", "physical_attack", "magic_attack", "physical_defense", "magic_defense", "accuracy", "avoidability", "speed", "jump")

def _item_gen(it):
    """일반 장비 판정 (2026-10-29 기준② 확정): 캐시 아님 + 요구 레벨 1 이상.
    요구 레벨은 equipment.json 요구 레벨 기준, 레코드가 없으면 items.json의 required_level로 본다."""
    if it.get("overall_category") != "Equip" or it.get("is_cash"):
        return False
    rec = EQUIP_STATS.get(str(it["id"]))
    lv = (rec.get("requirements") or {}).get("level") if rec else it.get("required_level")
    return lv is not None and lv >= 1


def _item_unv(i):
    # 후순위 통일 기준 (2026-10-29): 레벨 미확인(None)이거나 상세 미확인(detail_status unverified_null) — 화면 표기 기준과 동일
    return i.get("required_level") is None or i.get("detail_status") == "unverified_null"

def sort_items(items):
    # 미확인(레벨 없음 · 상세 미확인)은 0으로 취급하지 않고 어느 정렬에서도 맨 뒤 (사업실장 확정 2026-10-29)
    return sorted(items, key=lambda i: (_item_unv(i), i.get("required_level") or 0, (i.get("name_ko") or i.get("name_ko_candidate") or i.get("name_en") or "")))

data = json.load(open(SRC))
items = data["items"]
build_id = data.get("build_id", "")

by_cat = OrderedDict()
for cat in CAT_ORDER:
    subs = OrderedDict()
    for it in items:
        if it.get("overall_category") == cat:
            subs.setdefault(it.get("sub_category") or "Other", []).append(it)
    by_cat[cat] = OrderedDict(sorted(subs.items(), key=lambda kv: -len(kv[1])))

results = {}
split_map = {}  # cat -> {sub: filename} when split

for cat, subs in by_cat.items():
    total = sum(len(v) for v in subs.values())
    fn = f"{cat.lower()}.html"
    chips = "".join(f'<a class="chip" href="#{slug(s)}">{escape(sub_ko(s))} <b>{len(v):,}</b></a>' for s, v in subs.items())
    is_equip = cat == "Equip"
    sections = ""
    for s, v in subs.items():
        sections += (f'<section class="card"><h2 id="{slug(s)}">{escape(sub_ko(s))}<span class="cnt">{len(v):,}개</span></h2>'
                     + grid_html(sort_items(v), with_stats=is_equip) + "</section>\n")
    stat_notice = f'\n  <div class="notice">{STAT_NOTICE}</div>' if is_equip else ""
    body = f"""  <div class="intro">
    <h1>아이템 · <span>{CAT_KO[cat]}</span></h1>
    <div class="tag">{cat} 카테고리 {total:,}개 · 세부 분류 {len(subs)}종</div>
  </div>
  <div class="notice">{NOTICE}</div>{stat_notice}
  <section class="card"><h2>세부 분류 바로가기</h2><div class="chips">{chips}</div></section>
{SORT_UI}{sections}  <p class="back"><a href="/items/">← 아이템 전체 목차로</a></p>""" + "\n" + SORT_SCRIPT
    html = page(f"아이템 목록 · {CAT_KO[cat]}({cat})", f"알팡지지 아이템 목록 후보 — {CAT_KO[cat]} 카테고리 {total:,}개. 본진 빅뱅 직후(GMS 95) 기준, 한글 이름은 표시명 후보입니다.",
                f"https://alpang.gg/items/{fn}", "/items/", body)
    if len(html.encode("utf-8")) > SIZE_LIMIT:
        # split by sub_category
        split_map[cat] = {}
        idx_sections = ""
        idx_cards = {}
        for s, v in subs.items():
            sfn = f"{cat.lower()}-{slug(s)}.html"
            split_map[cat][s] = sfn
            filt = JOB_FILTER_HTML if is_equip else ""
            empty = JOB_EMPTY_HTML if is_equip else ""
            fscript = ("\n" + EQUIP_SCRIPT) if is_equip else ""
            sbody = f"""  <div class="intro">
    <h1>아이템 · <span>{CAT_KO[cat]}</span></h1>
    <div class="tag">{cat} · {escape(sub_ko(s))} {len(v):,}개</div>
  </div>
  <div class="notice">{NOTICE}</div>{stat_notice}
{SORT_UI}{GEN_TOGGLE if is_equip else ""}  <section class="card"><h2>{escape(sub_ko(s))}<span class="cnt">{len(v):,}개</span></h2>{filt}{grid_html(sort_items(v), with_stats=is_equip, with_jobs=is_equip)}{empty}</section>{fscript}
  <p class="back"><a href="/items/{fn}">← {CAT_KO[cat]} 분류 목차로</a> · <a href="/items/">아이템 전체 목차로</a></p>"""
            shtml = page(f"아이템 목록 · {CAT_KO[cat]} {escape(sub_ko(s))}", f"알팡지지 아이템 목록 후보 — {CAT_KO[cat]} · {escape(sub_ko(s))} {len(v):,}개. 본진 빅뱅 직후(GMS 95) 기준.",
                         f"https://alpang.gg/items/{sfn}", "/items/", sbody)
            open(f"{OUT}/{sfn}", "w").write(shtml)
            if is_equip:
                first = sort_items(v)[0]
                idx_cards[s] = (f'<a class="icat" href="/items/{sfn}"><span class="islot">{icon_img(first)}</span>'
                                f'<span class="nm">{escape(sub_ko(s))}</span><span class="cc">{len(v):,}개</span></a>')
            else:
                idx_sections += f'<div class="row" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f0ece3;font-size:15px;line-height:1.55"><a href="/items/{sfn}">{escape(sub_ko(s))}</a><span style="color:var(--sub)">{len(v):,}개</span></div>\n'
        jobcard = JOB_NAV_CARD if is_equip else ""
        jobscript = ("\n" + JOB_NAV_SCRIPT) if is_equip else ""
        if is_equip:
            groups_html = ""
            for g in GROUP_ORDER:
                cards = "".join(idx_cards[s] for s in subs if s in idx_cards and SUB_GROUP.get(s, "기타") == g)
                groups_html += f'<h3>{g}</h3><div class="cgrid">{cards}</div>\n'
            idx_block = f'  <section class="card"><h2>세부 분류</h2><div class="cgwrap">\n{groups_html}  </div></section>'
        else:
            idx_block = f'  <section class="card"><h2>세부 분류</h2>\n{idx_sections}  </section>'
        body2 = f"""  <div class="intro">
    <h1>아이템 · <span>{CAT_KO[cat]}</span></h1>
    <div class="tag">{cat} 카테고리 {total:,}개 · 세부 분류 {len(subs)}종 (항목이 많아 세부 분류별 페이지로 나뉘어 있습니다)</div>
  </div>
  <div class="notice">{NOTICE}</div>{stat_notice}
{jobcard}{idx_block}{jobscript}
  <p class="back"><a href="/items/">← 아이템 전체 목차로</a></p>"""
        html = page(f"아이템 목록 · {CAT_KO[cat]}({cat})", f"알팡지지 아이템 목록 후보 — {CAT_KO[cat]} 카테고리 {total:,}개. 본진 빅뱅 직후(GMS 95) 기준, 한글 이름은 표시명 후보입니다.",
                    f"https://alpang.gg/items/{fn}", "/items/", body2)
    open(f"{OUT}/{fn}", "w").write(html)
    results[cat] = total

# index page
total_all = sum(results.values())
cards = "".join(
    f'<a class="kpi" href="/items/{cat.lower()}.html"><div class="lb">{CAT_KO[cat]} · {cat}</div><div class="vl">{results[cat]:,}<small> 개</small></div></a>'
    for cat in CAT_ORDER)
tabs = "".join(
    f'<a href="/items/{c.lower()}.html">{CAT_KO[c]}<span class="n">{results[c]:,}</span></a>'
    for c in TAB_ORDER)

def sub_href(cat, s):
    if cat in split_map:
        return f"/items/{split_map[cat][s]}"
    return f"/items/{cat.lower()}.html#{slug(s)}"

def equip_group_nav(subs):
    """인덱스 장비 섹션: 구분 그룹(무기/방어구/장신구/기타) + 직업 그룹 내비."""
    rows = ""
    for g in GROUP_ORDER:
        chips = "".join(
            f'<a class="chip" href="{sub_href("Equip", s)}">{escape(sub_ko(s))} <b>{len(v):,}</b></a>'
            for s, v in subs.items() if SUB_GROUP.get(s, "기타") == g)
        rows += f'<div class="grow"><span class="glb">{g}</span><div class="chips">{chips}</div></div>\n'
    jobchips = '<a class="chip" href="/items/equip.html">전체</a>' + "".join(
        f'<a class="chip" href="/items/equip.html?job={q}">{label}</a>' for q, label in JOB_FILTERS)
    rows += f'<div class="grow"><span class="glb">직업</span><div class="chips">{jobchips}</div></div>\n'
    return f'<div class="gnav">\n{rows}</div>'

sub_lists = ""
for cat, subs in by_cat.items():
    if cat == "Equip":
        sub_lists += f'<section class="card"><h2>{CAT_KO[cat]} ({cat}) · {results[cat]:,}개</h2>{equip_group_nav(subs)}</section>\n'
        continue
    chips = ""
    for s, v in subs.items():
        chips += f'<a class="chip" href="{sub_href(cat, s)}">{escape(sub_ko(s))} <b>{len(v):,}</b></a>'
    sub_lists += f'<section class="card"><h2>{CAT_KO[cat]} ({cat}) · {results[cat]:,}개</h2><div class="chips">{chips}</div></section>\n'

# --- 아이템 허브 개선 역이식 (2026-11-13 동결 staging-items-hub-20261113와 정합) ---
HUB_SEARCH = '<div class="searchbar">\n    <div class="sb-in">\n      <span class="sb-ic"><img class="dic" src="/assets/icons/icon-search.png" alt=""></span>\n      <div class="sb-wrap">\n        <input type="text" id="alpangSearch" placeholder="몬스터·맵·아이템·NPC·퀘스트 통합 검색" aria-label="통합 검색" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="sbResults">\n        <div class="sb-results" id="sbResults" role="listbox"></div>\n      </div>\n      <button type="button" class="sb-btn" id="sbGo">검색</button>\n    </div>\n    <p class="sb-note">한글·영문 이름으로 몬스터 175종, 맵 419곳, 아이템 14,577개를 한 번에 검색할 수 있어요. 한글 이름은 표시명 후보입니다.</p>\n<style>\n/* 통합 검색 안내 바 (검색 기능은 준비 중 — 도감·목록으로 안내) */\n  .searchbar{margin-top:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 1px 3px rgba(30,25,15,.05)}\n.sb-in{display:flex;align-items:center;gap:10px;flex-wrap:wrap}\n.sb-ic{font-size:19px}\n.sb-in input{flex:1;min-width:180px;font-size:16px;padding:11px 14px;border:1px solid var(--line);border-radius:10px;background:#f7f4ee;color:var(--text);font-family:inherit}\n.sb-btn{display:inline-block;background:var(--accent);color:#fff;font-weight:700;font-size:15px;padding:11px 20px;border-radius:10px;text-decoration:none;white-space:nowrap;border:none;cursor:pointer;font-family:inherit;min-height:44px}\n.sb-note{font-size:13.5px;color:var(--sub);margin-top:9px}\n.sb-wrap{position:relative;flex:1;min-width:180px;display:flex}\n.sb-wrap input{flex:1;min-width:0}\n.sb-results{position:absolute;top:calc(100% + 6px);left:0;right:0;z-index:60;background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 24px rgba(30,25,15,.14);max-height:420px;overflow-y:auto;display:none;text-align:left}\n.sb-results.open{display:block}\n.sb-item{display:flex;align-items:center;gap:9px;padding:10px 14px;min-height:44px;text-decoration:none;color:var(--text);border-bottom:1px solid var(--line)}\n.sb-item:last-child{border-bottom:none}\n.sb-item.sel,.sb-item:hover{background:var(--accent-soft)}\n.sb-badge{flex:none;font-size:11px;font-weight:800;padding:2px 7px;border-radius:4px;color:#fff;background:var(--accent)}\n.sb-badge.map{background:#7A6A53}\n.sb-badge.item{background:#4A6FA5}\n.sb-badge.npc{background:#8A5AA5}\n.sb-badge.quest{background:#B7791F}\n.sb-icon{flex:none;width:32px;height:32px;object-fit:contain;image-rendering:pixelated}\n.sb-nm{font-weight:700;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.sb-en{font-size:12.5px;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.sb-unv{flex:none;font-size:11px;font-weight:700;color:var(--unknown);background:#f4f1ea;border-radius:4px;padding:2px 6px}\n.sb-none{padding:14px;font-size:14px;color:var(--sub)}\n.sb-more{display:block;width:100%;padding:11px;font-size:14px;font-weight:700;color:var(--accent-dark);background:transparent;border:none;border-top:1px solid var(--line);cursor:pointer;font-family:inherit;min-height:44px}\n[data-theme="dark"] .searchbar{box-shadow:0 1px 3px rgba(0,0,0,.35)}\n[data-theme="dark"] .sb-in input{background:#22252B}\n#notice-item-category-level summary{cursor:pointer;list-style:none}\n#notice-item-category-level summary::-webkit-details-marker{display:none}\n#notice-item-category-level summary h2{display:inline}\n</style>'
HUB_STAT_ACCORDION = '<details class="card" id="notice-item-category-level">\n    <summary><h2>장비 종류별로 요구 레벨이 다릅니다</h2></summary>\n    <p>장비 5,770개(착용 레벨이 기록된 장비 기준)를 종류별로 나누어, 요구 레벨 100을 넘는 장비의 비중을 비교하면 종류마다 차이가 큽니다. 탈것(Mount)은 21개 중 28.6%가 100을 넘고, 양손 무기(Two-Handed Weapon)는 686개 중 9.8%, 한손 무기(One-Handed Weapon)는 792개 중 7.7%입니다. 반면 방어구(Armor)는 3,434개 중 2.3%로 낮은 편이고, 장신구(Accessory)는 718개 중 3.8%입니다. 전체 장비의 레벨 분포가 아니라 종류 사이의 차이를 비교한 수치입니다.</p>\n    <div class="twrap"><table><thead><tr><th>종류</th><th>장비 수</th><th>요구 레벨 100 초과</th><th>비중</th></tr></thead><tbody><tr><td>탈것 (Mount)</td><td>21개</td><td>6개</td><td>28.6%</td></tr><tr><td>양손 무기 (Two-Handed Weapon)</td><td>686개</td><td>67개</td><td>9.8%</td></tr><tr><td>한손 무기 (One-Handed Weapon)</td><td>792개</td><td>61개</td><td>7.7%</td></tr><tr><td>기타 (Other)</td><td>119개</td><td>9개</td><td>7.6%</td></tr><tr><td>장신구 (Accessory)</td><td>718개</td><td>27개</td><td>3.8%</td></tr><tr><td>방어구 (Armor)</td><td>3,434개</td><td>80개</td><td>2.3%</td></tr></tbody></table></div>\n  </details>'
HUB_SEARCH_SCRIPT = '<script src="/assets/search.js?v=4" data-index="/assets/alpang-search-20261028-11.json" defer></script>'

body = f"""  <div class="intro">
    <h1>아이템 <span>목록</span></h1>
    <div class="tag">본진 빅뱅 직후 기준 아이템 목록 후보 {total_all:,}개</div>
  </div>
{HUB_SEARCH}
  <div class="notice">{NOTICE}</div>
{HUB_STAT_ACCORDION}
  <div class="tabs">
{tabs}  </div>
  <div class="cards">
{cards}  </div>
{sub_lists}{HUB_SEARCH_SCRIPT}"""
html = page("아이템 목록", f"알팡지지 아이템 목록 후보 {total_all:,}개 — 카테고리별 안내. 본진 빅뱅 직후(GMS 95) 기준, 한글 이름은 표시명 후보입니다.",
            "https://alpang.gg/items/", "/items/", body)
open(f"{OUT}/index.html", "w").write(html)

print("items pages built | build:", build_id, "| total:", total_all)
for cat in CAT_ORDER:
    print(f"  {cat}: {results[cat]}" + (" (SPLIT)" if cat in split_map else ""))
for f in sorted(os.listdir(OUT)):
    print(f"  file: {f} {os.path.getsize(f'{OUT}/{f}'):,}B")
