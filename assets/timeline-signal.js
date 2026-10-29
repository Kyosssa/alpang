// 타임라인 새 글 신호 — 판정은 저장된 마지막 확인 시점과 최신 등록 시각의 비교만으로 가볍게 유지한다
(function () {
  var SEEN_KEY = 'alpang-tl-seen-at';
  var latest = window.ALPANG_TL_LATEST || null;
  if (!latest) return;
  var seen = null;
  try { seen = localStorage.getItem(SEEN_KEY); } catch (e) {}
  var items = document.querySelectorAll('.tl-item[data-registered-at]');
  if (items.length) {
    // 첫 방문(확인 기록 없음)이면 최신 항목만 NEW가 되도록 기준점을 최신 직전 등록 시각으로 둔다
    var baseline = seen;
    if (!baseline) {
      baseline = '';
      items.forEach(function (it) {
        var v = it.getAttribute('data-registered-at');
        if (v < latest && v > baseline) baseline = v;
      });
      if (!baseline) baseline = latest;
    }
    // 타임라인 페이지: 기준점보다 뒤에 등록된 항목에 NEW를 붙인 뒤, 확인 시점을 최신으로 갱신한다 (신호 소멸)
    items.forEach(function (it) {
      if (it.getAttribute('data-registered-at') > baseline) {
        var d = it.querySelector('.tl-date .d');
        if (d && !it.querySelector('.tl-new')) {
          var b = document.createElement('span');
          b.className = 'tl-new'; b.textContent = 'NEW';
          d.appendChild(b);
        }
      }
    });
    try { localStorage.setItem(SEEN_KEY, latest); } catch (e) {}
    return;
  }
  // 그 밖의 페이지: 최신 등록이 마지막 확인보다 뒤면 GNB 타임라인 탭에 점을 켠다
  var dot = document.getElementById('tlNewDot');
  if (dot && (!seen || seen < latest)) dot.classList.add('on');
})();
