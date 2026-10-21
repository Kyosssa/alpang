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

// 이식 1단계 골격: 게이지 바 + 비중 행 (분모는 호출자가 넘긴 합계)
function gaugeRows(rows, total) {
  const max = Math.max(1, ...rows.map(r => r.v));
  return rows.map(r => `<tr><td class="bar-cell"><div class="bar-bg" style="width:${Math.round(r.v / max * 100)}%"></div><div class="bar-content">${esc(r.k)}</div></td><td class="n">${Number(r.v).toLocaleString('ko-KR')}</td><td class="n">${total > 0 ? (r.v / total * 100).toFixed(1) + '%' : '-'}</td></tr>`).join('');
}

// ---- 구글 검색 (서치콘솔) 섹션 — 2차 확장. 실패해도 자체 통계는 그대로 뜬다 (섹션 단위 격리) ----
function gscTable(title, rows) {
  const trs = rows.map(r => `<tr><td>${esc(r.key)}</td><td class="n">${Number(r.clicks).toLocaleString('ko-KR')}</td><td class="n">${Number(r.impressions).toLocaleString('ko-KR')}</td><td class="n">${Number(r.ctrPct).toFixed(1)}%</td><td class="n">${Number(r.position).toFixed(1)}</td></tr>`).join('');
  return `<table><thead><tr><th>항목</th><th class="n">클릭</th><th class="n">노출</th><th class="n">CTR</th><th class="n">평균 순위</th></tr></thead><tbody>${trs || '<tr><td colspan="5" class="empty">기록 없음</td></tr>'}</tbody></table>`;
}
// 이식 1단계 골격: 검색어 표 — CTR 미니 바 바인딩, 순위 배지는 자리만 (구간 경계 미확정이라 색 구간 미적용)
// [연결 완료 P2 · 2026-10-18 확정] 순위 배지 구간 — 상위 3위 이하 · 중위 10위 이하, 둘 다 '이하(포함)'이라 비교는 <= 유지.
const RANK_TOP_MAX = 3;
const RANK_MID_MAX = 10;
function rankClass(pos) {
  if (RANK_TOP_MAX === null || RANK_MID_MAX === null) return '';
  if (pos <= RANK_TOP_MAX) return 'rank-top';
  if (pos <= RANK_MID_MAX) return 'rank-mid';
  return 'rank-low';
}
function gscQueryTable(rows, prevRows) {
  const prevMap = new Map((prevRows || []).map(r => [r.key, r.clicks]));
  const trs = rows.map(r => {
    const prev = prevRows ? prevMap.get(r.key) : undefined;
    const prevCell = prev === undefined ? '—' : Number(prev).toLocaleString('ko-KR');
    const diffCell = prev === undefined ? '—' : (Number(r.clicks) - Number(prev) > 0 ? '+' : '') + (Number(r.clicks) - Number(prev)).toLocaleString('ko-KR');
    return `<tr><td>${esc(r.key)}</td><td class="n">${Number(r.clicks).toLocaleString('ko-KR')}</td><td class="n">${prevCell}</td><td class="n">${diffCell}</td><td class="n">${Number(r.impressions).toLocaleString('ko-KR')}</td><td class="n"><span class="ctr-wrap"><span class="ctr-track"><span class="ctr-fill" style="width:${Math.min(100, Number(r.ctrPct))}%"></span></span>${Number(r.ctrPct).toFixed(1)}%</span></td><td class="n"><span class="rank-pill ${rankClass(r.position)}">${Number(r.position).toFixed(1)}위</span></td></tr>`;
  }).join('');
  return `<table><thead><tr><th>검색어</th><th class="n">클릭</th><th class="n">전 기간 클릭</th><th class="n">증감</th><th class="n">노출</th><th class="n">CTR</th><th class="n">평균 순위</th></tr></thead><tbody>${trs || '<tr><td colspan="7" class="empty">기록 없음</td></tr>'}</tbody></table>`;
}
function gscSection(data, period, days) {
  if (!data || !data.ok) {
    let msg = '서치콘솔 데이터를 일시적으로 불러올 수 없습니다.';
    if (data && data.error === 'not_configured') msg = '서치콘솔 미연동 — 서비스 계정 연결 후 표시됩니다. (실값 필요: GSC_SA_EMAIL · GSC_SA_PRIVATE_KEY · GSC_SITE_URL)';
    else if (data && data.error === 'forbidden') msg = '서치콘솔 권한 오류 — 서비스 계정이 속성에 추가됐는지, 권한(Restricted 이상)인지 확인이 필요합니다.';
    return `<section><h2>구글 검색 (서치콘솔) <span class="badge-gsc">확정 데이터</span></h2><p class="sub">${esc(msg)}</p></section>`;
  }
  const t = data.totals;
  const toggle = period === 28
    ? `<a href="?g=7&d=${days}">최근 7일</a> · <b>최근 28일</b>`
    : `<b>최근 7일</b> · <a href="?g=28&d=${days}">최근 28일</a>`;
  return `<section><div class="panel-head"><h2>구글 서치콘솔 (GSC) 검색 성과 <span class="badge-gsc">확정 데이터</span></h2><div class="sub-tabs"><button class="sub-tab active" onclick="swTab(this,'gscQ')">검색어별</button><button class="sub-tab" onclick="swTab(this,'gscP')">페이지별</button></div></div>
<p class="sub">서치콘솔 확정 데이터 기준: ${esc(data.endDate)}까지 (구글 데이터는 2~3일 늦게 확정됩니다 · 조회 기간 ${esc(data.startDate)} ~ ${esc(data.endDate)}) · 기간: ${toggle}</p>
<div class="gsc-bar"><span>총 클릭 <b>${Number(t.clicks).toLocaleString('ko-KR')}</b></span><span>총 노출 <b>${Number(t.impressions).toLocaleString('ko-KR')}</b></span><span>평균 CTR <b>${Number(t.ctrPct).toFixed(1)}%</b></span><span>평균 순위 <b>${Number(t.position).toFixed(1)}위</b></span></div>
<div class="tabpane" id="gscQ">${gscQueryTable(data.queries, data.prevQueries)}</div>
<div class="tabpane" id="gscP" style="display:none">${gscTable('페이지별', data.pages)}</div>
<p class="sub">일부 검색어는 구글 정책상 표시되지 않습니다.</p></section>`;
}


// [월별 적재 확장 · 2026-10-22 대표 결정] 보관 90일 · 스냅샷 신설 · 삭제 수동.
// 월 경계는 KST. counters(UTC)는 월별 계산에 쓰지 않는다 (일일 상한 전용 유지).
const MONTH_RE = /^\d{4}-(0[1-9]|1[0-2])$/;
const RETENTION_DAYS = 90;
function monthRangeUnix(m) {
  const y = Number(m.slice(0, 4)), mo = Number(m.slice(5, 7));
  const start = Date.UTC(y, mo - 1, 1) / 1000 - 32400;
  const end = Date.UTC(y, mo, 1) / 1000 - 32400;
  return [start, end];
}
function currentMonthKst() {
  return new Date(Date.now() + 32400 * 1000).toISOString().slice(0, 7);
}
function recentMonths(n) {
  const out = [];
  let [y, mo] = currentMonthKst().split('-').map(Number);
  for (let i = 0; i < n; i++) {
    out.push(String(y).padStart(4, '0') + '-' + String(mo).padStart(2, '0'));
    mo -= 1; if (mo === 0) { mo = 12; y -= 1; }
  }
  return out;
}
async function readMonth(db, m) {
  const [a, b] = monthRangeUnix(m);
  const snapMeta = await db.prepare('SELECT MAX(loaded_at) mx FROM monthly_snapshots WHERE month = ?').bind(m).first();
  if (snapMeta && snapMeta.mx) {
    const rows = await db.prepare('SELECT path, views FROM monthly_snapshots WHERE month = ? AND loaded_at = ? ORDER BY (path IS NULL) DESC, views DESC').bind(m, snapMeta.mx).all();
    const list = (rows.results || []);
    const totalRow = list.find(r => r.path === null);
    const pages = list.filter(r => r.path !== null).map(r => ({ k: r.path, v: r.views }));
    return { source: 'snapshot', loadedAt: snapMeta.mx, total: totalRow ? totalRow.views : 0, pages };
  }
  const tot = await db.prepare('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?').bind(a, b).first();
  const pg = await db.prepare('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY path ORDER BY v DESC').bind(a, b).all();
  return { source: 'live', loadedAt: null, total: Number((tot && tot.pv) || 0), pages: (pg.results || []).map(r => ({ k: r.k, v: r.v })) };
}
async function loadSnapshot(db, m) {
  if (!MONTH_RE.test(m)) return { ok: false, error: 'bad_month' };
  if (m >= currentMonthKst()) return { ok: false, error: 'month_not_closed' };
  const [a, b] = monthRangeUnix(m);
  const tot = await db.prepare('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?').bind(a, b).first();
  const pg = await db.prepare('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY path ORDER BY v DESC').bind(a, b).all();
  const total = Number((tot && tot.pv) || 0);
  const pages = (pg.results || []).map(r => ({ k: r.k, v: r.v }));
  const sum = pages.reduce((x, r) => x + r.v, 0);
  if (sum !== total) return { ok: false, error: 'sum_mismatch', total, sum };
  const now = Date.now(); // loaded_at은 밀리초 — 같은 초 재적재도 이력 묶음이 갈리게
  const stmts = [db.prepare('INSERT INTO monthly_snapshots (month, path, views, loaded_at) VALUES (?, NULL, ?, ?)').bind(m, total, now)];
  for (const r of pages) stmts.push(db.prepare('INSERT INTO monthly_snapshots (month, path, views, loaded_at) VALUES (?, ?, ?, ?)').bind(m, r.k, r.v, now));
  await db.batch(stmts);
  return { ok: true, month: m, total, pageCount: pages.length, loadedAt: now };
}
async function pruneOld(db) {
  const cutoff = kstMidnightUnix(0) - RETENTION_DAYS * 86400;
  const months = await db.prepare("SELECT DISTINCT strftime('%Y-%m', ts + 32400, 'unixepoch') m FROM hits WHERE ts < ?").bind(cutoff).all();
  const deleted = [], skipped = [];
  for (const row of (months.results || [])) {
    const m = row.m;
    const snap = await db.prepare('SELECT COUNT(*) c FROM monthly_snapshots WHERE month = ?').bind(m).first();
    if (snap && snap.c > 0) {
      const [a, b] = monthRangeUnix(m);
      const res = await db.prepare('DELETE FROM hits WHERE ts >= ? AND ts < ? AND ts < ?').bind(a, b, cutoff).run();
      deleted.push({ month: m, rows: (res.meta && res.meta.changes) || 0 });
    } else {
      skipped.push(m);
    }
  }
  return { ok: true, cutoff, deleted, skippedNoSnapshot: skipped };
}
function monthSection(monthData, selected) {
  if (!monthData) return '';
  const { source, total, pages, loadedAt } = monthData;
  const badge = source === 'snapshot'
    ? '<span class="badge badge-gsc">스냅샷 확정</span>'
    : '<span class="badge badge-live">실시간 집계</span>';
  const top = pages.slice(0, 20);
  const rest = pages.slice(20).reduce((a, r) => a + r.v, 0);
  const rows = top.map(r => `<tr><td>${esc(r.k)}</td><td class="n">${Number(r.v).toLocaleString('ko-KR')}</td><td class="n">${total > 0 ? (r.v / total * 100).toFixed(1) + '%' : '-'}</td></tr>`).join('')
    + (rest > 0 ? `<tr><td>상위 20위 밖 합계</td><td class="n">${rest.toLocaleString('ko-KR')}</td><td class="n">${(rest / total * 100).toFixed(1)}%</td></tr>` : '');
  const note = source === 'snapshot' ? `적재 시각 ${esc(kstText(Math.floor(loadedAt / 1000)))} (KST) · 원시 행이 삭제돼도 이 스냅샷으로 표시가 유지됩니다` : '스냅샷이 없는 달이라 원시 기록 범위 조회로 표시 중입니다';
  return `<section><div class="panel-head"><h2>월별 조회 — ${esc(selected)}</h2>${badge}</div><p class="sub">월 합계 ${Number(total).toLocaleString('ko-KR')}건 · ${note}</p><table><thead><tr><th>페이지</th><th class="n">조회</th><th class="n">점유율</th></tr></thead><tbody>${rows || '<tr><td colspan="3" class="empty">기록 없음</td></tr>'}</tbody></table></section>`;
}

async function reportPage(db, env, period, days = 7, month = null) {
  const t0 = kstMidnightUnix(0), t1 = t0 + 86400, y0 = t0 - 86400, w0 = t0 - (days - 1) * 86400;
  const q = (sql, ...binds) => db.prepare(sql).bind(...binds);
  const [today, yday, week, pagesToday, pagesWeek, refs, hours, devices, extHit, lastHit] = await db.batch([
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?', t0, t1),
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ts < ?', y0, t0),
    q('SELECT COUNT(*) pv FROM hits WHERE ts >= ?', w0),
    q('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY path ORDER BY v DESC LIMIT 20', t0, t1),
    q('SELECT path k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY path ORDER BY v DESC LIMIT 20', w0),
    q('SELECT ref_domain k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY ref_domain ORDER BY v DESC LIMIT 15', w0),
    q("SELECT strftime('%H', ts + 32400, 'unixepoch') k, COUNT(*) v FROM hits WHERE ts >= ? AND ts < ? GROUP BY k ORDER BY k", t0, t1),
    q('SELECT device || \' · \' || browser k, COUNT(*) v FROM hits WHERE ts >= ? GROUP BY k ORDER BY v DESC LIMIT 10', w0),
    q("SELECT COUNT(*) pv FROM hits WHERE ts >= ? AND ref_domain IS NOT NULL AND ref_domain <> '' AND ref_domain <> '(direct)'", w0),
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
  let monthData = null;
  if (month) { try { monthData = await readMonth(db, month); } catch { monthData = null; } }
  const monthLinks = recentMonths(4).map(m => m === month ? '<b>' + m + '</b>' : '<a href="?m=' + m + '&d=' + days + '&g=' + period + '">' + m + '</a>').join(' · ');
  let gsc = null;
  try { gsc = await getSearchSectionData(env, { period }); } catch { gsc = { ok: false, error: 'api_error' }; }
  const hourRows = list(hours);
  const maxH = Math.max(1, ...hourRows.map(r => r.v));
  const hourBars = Array.from({ length: 24 }, (_, h) => {
    const row = hourRows.find(r => Number(r.k) === h);
    const v = row ? row.v : 0;
    return `<div class="hb"><span class="hv" title="${h}시 ${v}건" style="height:${Math.round(v / maxH * 100)}%"></span><span class="hl">${h}</span></div>`;
  }).join('');
  // [연결 완료 P3 · 2026-10-18 확정] 외부 = 직접 접속('(direct)')과 빈 유입 경로를 뺀 나머지. 분모는 선택 기간 전체 방문 수(W).
  // 빈 referrer는 수집 단계(hit.js)에서 '(direct)'로 저장되므로 판정은 저장값 기준이다.
  const devRows = list(devices), refRows = list(refs);
  const extShare = W > 0 ? (pv(extHit) / W * 100).toFixed(1) : null;
  const devTotal = devRows.reduce((a, r) => a + r.v, 0);
  const refTotal = refRows.reduce((a, r) => a + r.v, 0);
  const weekRows = list(pagesWeek);
  const topPathPct = weekRows.length && W > 0 ? ' · 1위 ' + weekRows[0].k + ' ' + (weekRows[0].v / W * 100).toFixed(1) + '%' : '';
  // [후단 연결 지점 P4] 카테고리 라벨 매핑 — 큐브 두 경로는 2026-10-22 대표 확정 A안으로 '큐브값 계산기' 정식 채택.
  const PATH_LABELS = { '/': '홈 메인', '/timeline/': '타임라인', '/guide/hunting/': '초반 사냥터 후보', '/faq/': '확인된 발언 FAQ', '/npcs/': 'NPC 도감', '/mobs/': '몬스터 도감', '/maps/': '맵 탐색', '/quests/': '퀘스트 도감', '/guide/orbis-leafre/': '오르비스·리프레', '/guide/edelstein/': '에델슈타인', '/calculator/cube/': '큐브값 계산기', '/calculator/cube': '큐브값 계산기' };
  function pageRows(rows, total) {
    const max = Math.max(1, ...rows.map(r => r.v));
    return rows.map(r => `<tr><td class="bar-cell"><div class="bar-bg" style="width:${Math.round(r.v / max * 100)}%"></div><div class="bar-content">${esc(r.k)}</div></td><td><span class="page-label">${esc(PATH_LABELS[r.k] || '—')}</span></td><td class="n">${Number(r.v).toLocaleString('ko-KR')}</td><td class="n">${total > 0 ? (r.v / total * 100).toFixed(1) + '%' : '-'}</td></tr>`).join('');
  }
  return `<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>관리자 통계 — 알팡지지</title>
<style>body{font-family:-apple-system,'Malgun Gothic',sans-serif;background:#0D1014;color:#ECEFF3;margin:0;padding:20px 16px 40px}a{color:#FFB37E}.wrap{max-width:1240px;margin:0 auto}h1{font-size:20px}.sub{color:#A7ADB8;font-size:13px}.warn{color:#FFC46B;font-size:13px}.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:16px 0}.kpi-card{background:#161B24;border:1px solid #262F3F;border-radius:12px;padding:14px}.kpi-card .lbl{color:#A7ADB8;font-size:12.5px;display:block}.kpi-card b{font-size:26px;display:block;margin:6px 0 4px}.kpi-card .sub2{color:#64748B;font-size:12px}section,.panel{background:#161B24;border:1px solid #262F3F;border-radius:12px;padding:16px;margin-bottom:12px}h2{font-size:15px;margin:0 0 10px}.panel-head{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}.chart-grid{display:grid;grid-template-columns:1.55fr 1fr;gap:12px}.two-col{display:grid;grid-template-columns:1.25fr 1fr;gap:12px}.chart-grid section,.two-col section{margin-bottom:12px}table{width:100%;border-collapse:collapse;font-size:13.5px}td,th{padding:6px 4px;border-bottom:1px solid #2A2D33;text-align:left;word-break:break-all}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}.empty{color:#A7ADB8}.hchart{display:flex;align-items:flex-end;gap:2px;height:110px;margin-top:6px}.hb{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}.hv{display:block;width:100%;background:#FF7A1A;border-radius:2px 2px 0 0;min-height:1px}.hl{font-size:9.5px;color:#A7ADB8;margin-top:3px}.bar-cell{position:relative}.bar-bg{position:absolute;left:0;top:4px;bottom:4px;background:rgba(255,122,26,.16);border-radius:4px}.bar-content{position:relative}.sub-tabs{display:flex;gap:4px}.sub-tab{background:transparent;border:1px solid #262F3F;color:#A7ADB8;font-size:12px;font-weight:600;padding:4px 10px;border-radius:6px;cursor:pointer}.sub-tab.active{background:#1E2532;color:#ECEFF3}.sub-tab.disabled{opacity:.45;cursor:default}.gsc-bar{display:flex;flex-wrap:wrap;gap:16px;background:#0D1014;border:1px solid #262F3F;border-radius:8px;padding:10px 14px;margin-bottom:12px;font-size:12.5px;color:#A7ADB8}.gsc-bar b{color:#ECEFF3;font-size:14px}.ctr-wrap{display:inline-flex;align-items:center;gap:6px;justify-content:flex-end}.ctr-track{width:48px;height:6px;background:#0D1014;border-radius:99px;overflow:hidden;display:inline-block}.ctr-fill{height:100%;background:#FF7A1A;display:block}.rank-pill{display:inline-block;padding:2px 7px;border-radius:5px;font-size:12px;font-weight:700;background:rgba(148,163,184,.12);color:#A7ADB8}.rank-pill.rank-top{background:rgba(255,122,26,.18);color:#FF8533}.rank-pill.rank-mid{background:rgba(16,185,129,.15);color:#34D399}.rank-pill.rank-low{background:rgba(148,163,184,.12);color:#A7ADB8}.page-label{font-size:11.5px;color:#64748B}.badge-own{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600;color:#FFB37E;background:#3A2A1A;border:1px solid #8A5A2A;vertical-align:middle;margin-left:8px}.badge-gsc{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600;color:#9CC7FF;background:#1E2A38;border:1px solid #33549E;vertical-align:middle;margin-left:8px}@media(max-width:1024px){.kpi-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:960px){.chart-grid,.two-col{grid-template-columns:1fr}}@media(max-width:560px){.kpi-grid{grid-template-columns:1fr}}</style></head>
<body><div class="wrap"><h1>📊 알팡지지 방문 통계 <span class="badge-own">실시간 집계</span></h1>
<p class="sub">기준 시각 ${esc(kstText(Math.floor(Date.now() / 1000)))} (KST) · 마지막 정상 수집 ${esc(kstText(lastTs))} (KST) · 지표는 '수집된 페이지 조회' 기준이며 봇 필터를 거친 값이라 실제 방문과 차이가 있을 수 있습니다 · 일일 수집 상한의 카운터 기준은 UTC 날짜로, 화면의 '오늘'(KST)과 다릅니다 · 구글 검색 수치는 아래 서치콘솔 섹션 (확정일 기준)을 보세요</p>
${gapWarn}
<div class="kpi-grid">
<div class="kpi-card"><span class="lbl">오늘 수집된 페이지 조회 (KST)</span><b>${T.toLocaleString('ko-KR')}</b><span class="sub2"></span></div>
<div class="kpi-card"><span class="lbl">어제 수집된 페이지 조회</span><b>${Y.toLocaleString('ko-KR')}</b><span class="sub2">${W > 0 && Y > 0 ? '최근 ' + days + '일 일평균 대비 ' + (Y / (W / days)).toFixed(1) + '배' : ''}</span></div>
<div class="kpi-card"><span class="lbl">최근 ${days}일 합계</span><b>${W.toLocaleString('ko-KR')}</b><span class="sub2">일평균 ${(W / days).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}${topPathPct}${extShare === null ? '' : ' · 외부 유입 비중 ' + extShare + '%'}</span></div>
<div class="kpi-card"><span class="lbl">집계 기간 선택</span><b style="font-size:19px">${[1, 7, 30].map(n => n === days ? '<b>' + n + '일</b>' : '<a href="?d=' + n + '&g=' + period + '">' + n + '일</a>').join(' · ')}</b><span class="sub2">월별 조회: ${monthLinks}</span></div>
<div class="kpi-card"><span class="lbl">구글 검색 클릭 (GSC)</span><b>${gsc && gsc.ok ? Number(gsc.totals.clicks).toLocaleString('ko-KR') : '—'}</b><span class="sub2">${gsc && gsc.ok ? '노출 ' + Number(gsc.totals.impressions).toLocaleString('ko-KR') + ' · 평균 CTR ' + Number(gsc.totals.ctrPct).toFixed(1) + '% · 평균 순위 ' + Number(gsc.totals.position).toFixed(1) + '위' : '서치콘솔 아래 섹션 참조'}</span></div>
</div>
<div class="chart-grid">
<section><div class="panel-head"><h2>시간대별 추이 (KST)</h2><div class="sub-tabs"><span class="sub-tab active">시간대별 (오늘)</span><span class="sub-tab disabled">일별 추이 (후단)</span></div></div><div class="hchart">${hourBars}</div></section>
<section><div class="panel-head"><h2>분포 — 최근 ${days}일</h2><div class="sub-tabs"><button class="sub-tab active" onclick="swTab(this,'paneDev')">기기 · 브라우저</button><button class="sub-tab" onclick="swTab(this,'paneRef')">유입 도메인</button></div></div>
<div class="tabpane" id="paneDev"><table><thead><tr><th>구분</th><th class="n">건수</th><th class="n">비중</th></tr></thead><tbody>${gaugeRows(devRows, devTotal) || '<tr><td colspan="3" class="empty">기록 없음</td></tr>'}</tbody></table></div>
<div class="tabpane" id="paneRef" style="display:none"><table><thead><tr><th>도메인</th><th class="n">건수</th><th class="n">비중</th></tr></thead><tbody>${gaugeRows(refRows, refTotal) || '<tr><td colspan="3" class="empty">기록 없음</td></tr>'}</tbody></table></div>
</section>
</div>
<div class="two-col">
<section><div class="panel-head"><h2>페이지별 조회 순위</h2><div class="sub-tabs"><button class="sub-tab" onclick="swTab(this,'panePageT')">오늘</button><button class="sub-tab active" onclick="swTab(this,'panePageW')">최근 ${days}일</button></div></div>
<div class="tabpane" id="panePageT" style="display:none"><table><thead><tr><th>페이지</th><th>카테고리</th><th class="n">조회</th><th class="n">점유율</th></tr></thead><tbody>${pageRows(list(pagesToday), T) || '<tr><td colspan="4" class="empty">기록 없음</td></tr>'}</tbody></table></div>
<div class="tabpane" id="panePageW"><table><thead><tr><th>페이지</th><th>카테고리</th><th class="n">조회</th><th class="n">점유율</th></tr></thead><tbody>${pageRows(list(pagesWeek), W) || '<tr><td colspan="4" class="empty">기록 없음</td></tr>'}</tbody></table></div>
</section>
${gscSection(gsc, period, days)}
</div>
${monthSection(monthData, month)}
<script>function swTab(btn,id){var p=btn.closest('section');p.querySelectorAll('.tabpane').forEach(function(x){x.style.display='none'});document.getElementById(id).style.display='block';btn.parentElement.querySelectorAll('.sub-tab').forEach(function(b){b.classList.remove('active')});btn.classList.add('active')}</script>
</div></body></html>`;
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  if (url.hostname !== SITE_HOST) return forbidden();
  if (!env.STATS_DB || !env.ACCESS_AUD || !env.ACCESS_TEAM_DOMAIN) return forbidden(); // 설정 없으면 차단 (안내 화면 없음)
  const auth = await verifyAccessRequest(request, env);
  if (!auth.ok) return forbidden();
  if (request.method === 'POST') {
    const action = url.searchParams.get('action');
    try {
      if (action === 'snapshot') {
        const r = await loadSnapshot(env.STATS_DB, url.searchParams.get('m') || '');
        return new Response(JSON.stringify(r), { status: r.ok ? 200 : 400, headers: { ...SEC_HEADERS, 'Content-Type': 'application/json; charset=utf-8' } });
      }
      if (action === 'prune') {
        const r = await pruneOld(env.STATS_DB);
        return new Response(JSON.stringify(r), { status: 200, headers: { ...SEC_HEADERS, 'Content-Type': 'application/json; charset=utf-8' } });
      }
    } catch {
      return new Response(JSON.stringify({ ok: false, error: 'internal' }), { status: 500, headers: { ...SEC_HEADERS, 'Content-Type': 'application/json; charset=utf-8' } });
    }
    return new Response(null, { status: 405, headers: SEC_HEADERS });
  }
  if (request.method !== 'GET') {
    return new Response(null, { status: 405, headers: SEC_HEADERS });
  }
  const period = url.searchParams.get('g') === '28' ? 28 : 7;
  const days = [1, 7, 30].includes(Number(url.searchParams.get('d'))) ? Number(url.searchParams.get('d')) : 7;
  try {
    const mParam = url.searchParams.get('m');
    const month = mParam && MONTH_RE.test(mParam) ? mParam : null;
    return new Response(await reportPage(env.STATS_DB, env, period, days, month), { headers: HTML_HEADERS });
  } catch {
    return new Response('<!DOCTYPE html><html lang="ko"><body style="font-family:sans-serif;background:#121317;color:#ECEFF3;padding:40px">아직 수집된 기록이 없습니다.</body></html>', { headers: HTML_HEADERS });
  }
}
