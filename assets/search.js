/* 알팡지지 통합 검색 (클라이언트 전용)
   - 인덱스는 검색창 첫 사용 시 1회 로드 후 메모리 캐시
   - 정규화: NFKC + 소문자 + 공백·기호 제거 (검색 전용, 표시 문자열은 원본 보존)
   - 정렬: ID 정확 일치(숫자 질의) 최우선, 이름 정확 -> 접두 -> 부분 일치
*/
(function () {
  var input = document.getElementById('alpangSearch');
  var box = document.getElementById('sbResults');
  if (!input || !box) return;
  var script = document.querySelector('script[data-index]');
  var INDEX_URL = script ? script.getAttribute('data-index') : '/assets/alpang-search.json';
  var TYPE_KO = { mob: '몬스터', map: '맵', item: '아이템', npc: 'NPC', quest: '퀘스트' };
  var TYPE_W = { mob: 0, map: 1, item: 2, npc: 3, quest: 4 };
  var PAGE = 10;
  var records = null, loading = false, shown = [], limit = PAGE, sel = -1;

  function norm(s) {
    if (!s) return '';
    return s.normalize('NFKC').toLowerCase().replace(/[\s\-_·.,'"!?()\[\]]/g, '');
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function load() {
    if (records || loading) return;
    loading = true;
    fetch(INDEX_URL)
      .then(function (r) { if (!r.ok) throw new Error('index'); return r.json(); })
      .then(function (data) {
        records = data.records.map(function (r) {
          r._nko = norm(r.name_ko_candidate);
          r._nen = norm(r.name_original);
          return r;
        });
        loading = false;
        run();
      })
      .catch(function () { loading = false; });
  }
  function score(r, q, qNum) {
    if (qNum !== null && r.id === qNum) return 0;              // ID 정확 일치
    var ko = r._nko, en = r._nen;
    if (ko === q || en === q) return 1;                        // 이름 정확
    if (ko.indexOf(q) === 0 || en.indexOf(q) === 0) return 2;  // 접두
    if (ko.indexOf(q) >= 0 || en.indexOf(q) >= 0) return 3;    // 부분
    return -1;
  }
  function run() {
    var q = norm(input.value);
    sel = -1;
    if (!q || !records) { close(); return; }
    var qNum = /^\d+$/.test(input.value.trim()) ? parseInt(input.value.trim(), 10) : null;
    var hits = [];
    for (var i = 0; i < records.length; i++) {
      var s = score(records[i], q, qNum);
      if (s >= 0) hits.push([s, records[i]]);
    }
    function tw(t) { return (t in TYPE_W) ? TYPE_W[t] : 9; }
    hits.sort(function (a, b) {
      if (a[0] !== b[0]) return a[0] - b[0];
      var d = tw(a[1].type) - tw(b[1].type);
      if (d) return d;
      var an = a[1].name_ko_candidate || a[1].name_original || '';
      var bn = b[1].name_ko_candidate || b[1].name_original || '';
      if (an.length !== bn.length) return an.length - bn.length;
      return an < bn ? -1 : an > bn ? 1 : 0;
    });
    shown = hits.map(function (h) { return h[1]; });
    render();
  }
  function render() {
    if (!shown.length) {
      box.innerHTML = '<div class="sb-none">검색 결과가 없어요. 몬스터 도감과 아이템 목록에서 찾아보실 수 있어요.</div>';
      open();
      return;
    }
    var html = '';
    var n = Math.min(limit, shown.length);
    for (var i = 0; i < n; i++) {
      var r = shown[i];
      var main = r.name_ko_candidate || r.name_original || ('#' + r.id);
      var sub = r.name_ko_candidate ? (r.name_original || '') : '';
      html += '<a class="sb-item' + (i === sel ? ' sel' : '') + '" role="option" data-i="' + i + '" href="' + esc(r.href) + '">' +
        '<span class="sb-badge ' + r.type + '">' + (TYPE_KO[r.type] || r.type) + '</span>' +
        '<span class="sb-nm">' + esc(main) + '</span>' +
        (sub ? '<span class="sb-en">' + esc(sub) + '</span>' : '') +
        (r.detail_status && r.detail_status !== 'confirmed' ? '<span class="sb-unv">미확인</span>' : '') +
        '</a>';
    }
    if (shown.length > limit) {
      html += '<button type="button" class="sb-more" id="sbMore">결과 더 보기 (' + shown.length + '건 중 ' + n + '건 표시)</button>';
    }
    box.innerHTML = html;
    var more = document.getElementById('sbMore');
    if (more) more.addEventListener('click', function () { limit += PAGE; render(); });
    open();
  }
  function open() { box.classList.add('open'); input.setAttribute('aria-expanded', 'true'); }
  function close() { box.classList.remove('open'); input.setAttribute('aria-expanded', 'false'); }
  input.addEventListener('focus', load);
  input.addEventListener('input', function () { limit = PAGE; load(); run(); });
  var goBtn = document.getElementById('sbGo');
  if (goBtn) goBtn.addEventListener('click', function () { input.focus(); limit = PAGE; load(); run(); });
  input.addEventListener('keydown', function (e) {
    var items = box.querySelectorAll('.sb-item');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (!items.length) return;
      sel = e.key === 'ArrowDown' ? Math.min(sel + 1, items.length - 1) : Math.max(sel - 1, 0);
      for (var i = 0; i < items.length; i++) items[i].classList.toggle('sel', i === sel);
      if (items[sel]) items[sel].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter') {
      if (sel >= 0 && items[sel]) { e.preventDefault(); location.href = items[sel].getAttribute('href'); }
    } else if (e.key === 'Escape') {
      close();
    }
  });
  document.addEventListener('click', function (e) {
    if (!box.contains(e.target) && e.target !== input) close();
  });
})();
