/* 모션 공통 모듈 (2026-11-13, 디렉터 확정 3모듈 중 2·3의 동작)
   모듈 2: [data-stagger] 요소를 단어 단위로 쪼개 스태거 인덱스를 부여한다.
           요소를 찾지 못하거나 JS가 꺼져 있으면 원문이 그대로 남는다.
   모듈 3: [data-tilt] 카드에 포인터 기반 3D 틸트 (최대 6도).
           포인터 정밀 기기 + reduced-motion 아님일 때만 동작한다. */
(function () {
  document.querySelectorAll('[data-stagger]').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w, i) { return '<span style="--i:' + i + '">' + w + '</span>'; }).join(' ');
    el.classList.add('stag');
  });
  var fine = window.matchMedia('(pointer:fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!fine) return;
  document.querySelectorAll('[data-tilt]').forEach(function (card) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      card.style.transform = 'perspective(700px) rotateX(' + (-y * 6).toFixed(2) + 'deg) rotateY(' + (x * 6).toFixed(2) + 'deg)';
    });
    card.addEventListener('pointerleave', function () { card.style.transform = ''; });
  });
})();
