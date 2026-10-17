/* 알팡지지 비공개 방문 통계 수집 (페이지뷰 1건 전송, IP 미수집·쿠키 미사용) */
(function () {
  try {
    var ua = navigator.userAgent || '';
    // 1차 봇 필터: 자동화·헤드리스·명백한 봇 UA는 전송하지 않음
    if (navigator.webdriver) return;
    if (/bot|spider|crawler|headless|phantom|slurp|bingpreview|facebookexternalhit|embedly|quora link preview/i.test(ua)) return;
    if (/HeadlessChrome|Lighthouse|PageSpeed/i.test(ua)) return;
    var path = location.pathname || '/';
    if (path.indexOf('/api/') === 0) return;
    if (/^\/manage-/.test(path)) return; // 관리자 경로는 수집 제외 (서버에서도 이중 차단)
    var payload = JSON.stringify({ p: path, r: document.referrer || '' });
    var url = '/api/hit';
    if (navigator.sendBeacon) {
      navigator.sendBeacon(url, new Blob([payload], { type: 'application/json' }));
    } else {
      fetch(url, { method: 'POST', body: payload, headers: { 'Content-Type': 'application/json' }, keepalive: true }).catch(function () {});
    }
  } catch (e) { /* 통계 실패가 페이지 동작에 영향을 주지 않음 */ }
})();
