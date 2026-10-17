// 알팡지지 비공개 관리자 통계 — 조회 화면 (설계 006 개정 4 기준)
// 인증: Cloudflare Access + Function에서 JWT 서버 검증 (../_lib/access.js). 자체 비밀번호·세션 없음.
// 경로 slug(9n8xu3nqy4bjars4)는 2026-10-17 사업실장 확정값이다.
// 보호: 이 경로 하위 전체(HTML·향후 JSON·CSV 포함)가 동일 검증을 거친다. 공개 예외는 /api/hit POST뿐.
import { verifyAccessRequest } from '../_lib/access.js';
import { getSearchSectionData } from '../_lib/gsc.js';

const SITE_HOST = 'alpang.gg';
const SEC_HEADERS = {
  'Cache-Control': 'private, no-store',
  'Referrer-Policy': 'no-referrer',
  'X-Robots-Tag': 'noindex, nofollow',
};
const HTML_HEADERS = { 'Content-Type': 'text/html; charset=utf-8', ...SEC_HEADERS };

function forbidden() {
  // 검증 실패 시 어떤 정보도 담지 않은 403
  return new Response('Forbidden', { status: 403, headers: { 'Content-Type': 'text/plain; charset=utf-8', ...SEC_HEADERS } });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function kstMidnightUnix(offsetDays) {
  const nowKst = new Date(Date.now() + 9 * 3600 * 1000);
  nowKst.setUTCHours(0, 0, 0, 0);
  return Math.floor((nowKst.getTime() - 9 * 3600 * 1000) / 1000) + offsetDays * 86400;
}
function kstText(unix) {
  if (!unix) return '-';
  return new Date(unix * 1000 + 9 * 3600 * 1000).toISOString().replace('T', ' ').slice(0, 16);
}

function table(title, rows, colA, colB) {
  const trs = rows.map(r => `<tr><td>${esc(r.k)}</td><td class="n">${Number(r.v).toLocaleString('ko-KR')}</td></tr>`).join('');
  return `<section><h2>${esc(title)}</h2><table><thead><tr><th>${esc(colA)}</th><th class="n">${esc(colB)}</th></tr></thead><tbody>${trs || '<tr><td colspan="2" class="empty">기록 없음</td></tr>'}</tbody></table></section>`;
}

// ---- 구글 검색 (서치콘솔) 섹션 — 2차 확장. 실패해도 자체 통계는 그대로 뜬다 (섹션 단위 격리) ----
function gscTable(title, rows) {
  const trs = rows.map(r => `<tr><td>${esc(r.key)}</td><td class="n">${Number(r.clicks).toLocaleString('ko-KR')}</td><td class="n">${Number(r.impressions).toLocaleString('ko-KR')}</td><td class="n">${Number(r.ctrPct).toFixed(1)}%</td><td class="n">${Number(r.position).toFixed(1)}</td></tr>`).join('');
  return `<section><h2>${esc(title)}</h2><table><thead><tr><th>항목</th><th class="n">클릭</th><th class="n">노출</th><th class="n">CTR</th><th class="n">평균 순위</th></tr></thead><tbody>${trs || '<tr><td colspan="5" class="empty">기록 없음</td></tr>'}</tbody></table></section>`;
}
function gscSection(data, period) {
  if (!data || !data.ok) {
    let msg = '서치콘솔 데이터를 일시적으로 불러올 수 없습니다.';
    if (data && data.error === 'not_configured') msg = '서치콘솔 미연동 — 서비스 계정 연결 후 표시됩니다. (실값 필요: GSC_SA_EMAIL · GSC_SA_PRIVATE_KEY · GSC_SITE_URL)';
    else if (data && data.error === 'forbidden') msg = '서치콘솔 권한 오류 — 서비스 계정이 속성에 추가됐는지, 권한(Restricted 이상)인지 확인이 필요합니다.';
    return `<section><h2>구글 검색 (서치콘솔)</h2><p class="sub">${esc(msg)}</p></section>`;
  }
  const t = data.totals;
  const toggle = period === 28
    ? `<a href="?g=7">최근 7일</a> · <b>최근 28일</b>`
    : `<b>최근 7일</b> · <a href="?g=28">최근 28일</a>`;
  return `<section><h2>구글 검색 (서치콘솔)</h2>
<p class="sub">서치콘솔 확정 데이터 기준: ${esc(data.endDate)}까지 (구글 데이터는 2~3일 늦게 확정됩니다 · 조회 기간 ${esc(data.startDate)} ~ ${esc(data.endDate)}) · 기간: ${toggle}</p>
<p class="sub">합계 — 클릭 ${Number(t.clicks).toLocaleString('ko-KR')} · 노출 ${Number(t.impressions).toLocaleString('ko-KR')} · 평균 CTR ${Number(t.ctrPct).toFixed(1)}% · 평균 순위 ${Number(t.position).toFixed(1)}</p>
</section>
${gscTable('검색어별 — 클릭순', data.queries)}
${gscTable('페이지별 (구글 검색)', data.pages)}
<p class="sub">일부 검색어는 구글 정책상 표시되지 않습니다.</p>`;
}

async function reportPage(db, env, period) {
  const t0 = kstMidnightUnix(0), t1 = t0 + 86400, y0 = t0 - 86400, w0 = t0 - 6 * 86400;
  const q = (sql, ...binds) => db.prepare(sql).bind(...binds);
  const [today, yday, week, pagesToday, pagesWeek, refs, hours, devices, lastHit] = await db.batch([
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?', t0, t1),
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?', y0, t0),
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ?', w0),
    q('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY path ORDER BY v DESC LIMIT 20', t0, t1),
    q('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY path ORDER BY v DESC LIMIT 20', w0),
    q('SELECT ref_domain k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY ref_domain ORDER BY v DESC LIMIT 15', w0),
    q("SELECT strftime('%H', ts + 32400, 'unixepoch') k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY k ORDER BY k", t0, t1),
    q('SELECT device || \' · \' || browser k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY k ORDER BY v DESC LIMIT 10', w0),
    q('SELECT MAX(ts) mx FROM hits'),
  ]);
  const pv = r => Number((r.results && r.results[0] && r.results[0].pv) || 0);
  const list = r => (r.results || []).map(x => ({ k: x.k, v: x.v }));
  const T = pv(today), Y = pv(yday), W = pv(week);
  const lastTs = (lastHit.results && lastHit.results[0] && lastHit.results[0].mx) || null;
  // 수집 공백 경고: 오늘 기록이 없는데 마지막 수집이 오늘 시작보다 이전이면 숨기지 않고 표시
  const gapWarn = T === 0 && (!lastTs || lastTs < t0)
    ? '<p class="warn">오늘 수집된 기록이 없습니다 — 수집 중단 또는 공백 가능 (마지막 정상 수집 시각을 확인하세요)</p>' : '';
  // 서치콘솔 섹션 데이터 — 실패는 섹션 안에서만 격리하고 자체 통계 렌더를 막지 않는다
  let gsc = null;
  try { gsc = await getSearchSectionData(env, { period }); } catch { gsc = { ok: false, error: 'api_error' }; }
  const hourRows = list(hours);
  const maxH = Math.max(1, ...hourRows.map(r => r.v));
  const hourBars = Array.from({ length: 24 }, (_, h) => {
    const row = hourRows.find(r => Number(r.k) === h);
    const v = row ? row.v : 0;
    return `<div class="hb"><span class="hv" title="${h}시 ${v}건" style="height:${Math.round(v / maxH * 100)}%"></span><span class="hl">${h}</span></div>`;
  }).join('');
  return `<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>관리자 통계 — 알팡지지</title>
<style>body{font-family:-apple-system,'Malgun Gothic',sans-serif;background:#121317;color:#ECEFF3;margin:0;padding:20px 16px 40px}a{color:#FFB37E}.wrap{max-width:860px;margin:0 auto}h1{font-size:20px}.sub{color:#A7ADB8;font-size:13px}.warn{color:#FFC46B;font-size:13px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}.card{background:#1B1E24;border-radius:12px;padding:14px}.card b{font-size:22px;display:block}.card span{color:#A7ADB8;font-size:12.5px}section{background:#1B1E24;border-radius:12px;padding:16px;margin-bottom:12px}h2{font-size:15px;margin:0 0 10px}table{width:100%;border-collapse:collapse;font-size:13.5px}td,th{padding:6px 4px;border-bottom:1px solid #2A2D33;text-align:left;word-break:break-all}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}.empty{color:#A7ADB8}.hchart{display:flex;align-items:flex-end;gap:2px;height:110px;margin-top:6px}.hb{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}.hv{display:block;width:100%;background:#FF7A1A;border-radius:2px 2px 0 0;min-height:1px}.hl{font-size:9.5px;color:#A7ADB8;margin-top:3px}@media(max-width:560px){.cards{grid-template-columns:1fr}}</style></head>
<body><div class="wrap"><h1>📊 알팡지지 방문 통계</h1>
<p class="sub">기준 시각 ${esc(kstText(Math.floor(Date.now() / 1000)))} (KST) · 마지막 정상 수집 ${esc(kstText(lastTs))} (KST) · 지표는 '수집된 페이지 조회' 기준이며 봇 필터를 거친 값이라 실제 방문과 차이가 있을 수 있습니다 · 일일 수집 상한의 카운터 기준은 UTC 날짜로, 화면의 '오늘'(KST)과 다릅니다 · 구글 검색 수치는 아래 서치콘솔 섹션 (확정일 기준)을 보세요</p>
${gapWarn}
<div class="cards">
<div class="card"><span>오늘 수집된 페이지 조회</span><b>${T.toLocaleString('ko-KR')}</b></div>
<div class="card"><span>어제 수집된 페이지 조회</span><b>${Y.toLocaleString('ko-KR')}</b></div>
<div class="card"><span>최근 7일 합계 · 일평균</span><b>${W.toLocaleString('ko-KR')}</b><span>일평균 ${(W / 7).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}</span></div>
</div>
<section><h2>오늘 시간대별 (KST)</h2><div class="hchart">${hourBars}</div></section>
${table('페이지별 순위 — 오늘', list(pagesToday), '페이지', '조회')}
${table('페이지별 순위 — 최근 7일', list(pagesWeek), '페이지', '조회')}
${table('유입 도메인 — 최근 7일', list(refs), '도메인', '건수')}
${table('기기 · 브라우저 — 최근 7일', list(devices), '구분', '건수')}
${gscSection(gsc, period)}
</div></body></html>`;
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  if (url.hostname !== SITE_HOST) return forbidden();
  if (!env.STATS_DB || !env.ACCESS_AUD || !env.ACCESS_TEAM_DOMAIN) return forbidden(); // 설정 없으면 차단 (안내 화면 없음)
  const auth = await verifyAccessRequest(request, env);
  if (!auth.ok) return forbidden();
  if (request.method !== 'GET') {
    return new Response(null, { status: 405, headers: SEC_HEADERS });
  }
  const period = url.searchParams.get('g') === '28' ? 28 : 7;
  try {
    return new Response(await reportPage(env.STATS_DB, env, period), { headers: HTML_HEADERS });
  } catch {
    return new Response('<!DOCTYPE html><html lang="ko"><body style="font-family:sans-serif;background:#121317;color:#ECEFF3;padding:40px">아직 수집된 기록이 없습니다.</body></html>', { headers: HTML_HEADERS });
  }
}
