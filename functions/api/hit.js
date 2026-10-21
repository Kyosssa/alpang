// 알팡지지 비공개 관리자 통계 — 수집 엔드포인트 (POST /api/hit)
// 설계 006 개정 4 (2026-10-16, 기술이사 최종 통과본) 기준 구현.
// 원칙: 거부되는 요청은 D1에 접근하기 전에 종료한다. 거부·실패는 기록하지 않는다.
// IP 원본 저장 안 함 · 쿠키 없음 · UA 원문 저장 안 함 · referrer는 hostname만 저장.
const CAP = 9000; // 일일 수집 상한 (잠정 — 배포 후 rows_written 실측으로 조정)
const MAX_BODY_BYTES = 512;
const MAX_PATH_LEN = 300;
const SITE_HOST = 'alpang.gg';

const BOT_RE = /bot|spider|crawler|headless|phantom|slurp|lighthouse|pagespeed|facebookexternalhit|embedly|preview/i;

// 허용 경로: 사이트 실제 섹션 접두 + 섹션 루트 자체. 여기에 없으면 무기록 종료.
const ALLOWED_PREFIXES = ['/mobs/', '/maps/', '/items/', '/timeline/', '/faq/', '/guide/', '/npcs/', '/quests/', '/privacy/', '/calculator/'];
const ALLOWED_EXACT = new Set(['/', '/mobs', '/maps', '/items', '/timeline', '/faq', '/guide', '/npcs', '/quests', '/privacy', '/calculator']);

// stats/schema.sql 의 CREATE 문장 본문과 동일본 유지
const SCHEMA = `CREATE TABLE IF NOT EXISTS hits (id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, path TEXT NOT NULL, ref_domain TEXT, device TEXT, browser TEXT);
CREATE INDEX IF NOT EXISTS idx_hits_ts_path ON hits(ts, path);
CREATE TABLE IF NOT EXISTS counters (day TEXT PRIMARY KEY, n INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS monthly_snapshots (id INTEGER PRIMARY KEY AUTOINCREMENT, month TEXT NOT NULL, path TEXT, views INTEGER NOT NULL, loaded_at INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS idx_snap_month ON monthly_snapshots(month, loaded_at);`;

function classifyDevice(ua) {
  if (/iPad|Tablet|PlayBook|Silk/i.test(ua) || (/Android/i.test(ua) && !/Mobile/i.test(ua))) return 'tablet';
  if (/Mobi|Android|iPhone|iPod|BlackBerry|Windows Phone/i.test(ua)) return 'mobile';
  return 'desktop';
}
function classifyBrowser(ua) {
  if (/Edg\//i.test(ua)) return 'Edge';
  if (/OPR\/|Opera/i.test(ua)) return 'Opera';
  if (/Whale\//i.test(ua)) return 'Whale';
  if (/KAKAOTALK/i.test(ua)) return 'KakaoTalk';
  if (/NAVER/i.test(ua)) return 'NaverApp';
  if (/SamsungBrowser\//i.test(ua)) return 'Samsung';
  if (/Chrome\//i.test(ua)) return 'Chrome';
  if (/Firefox\//i.test(ua)) return 'Firefox';
  if (/Safari\//i.test(ua)) return 'Safari';
  return 'Other';
}
function refDomain(referrer, host) {
  if (!referrer) return '(direct)';
  try {
    const u = new URL(referrer);
    if (u.hostname === host) return '(internal)';
    return u.hostname;
  } catch { return '(direct)'; }
}

// path 정제·검증: 통과하면 정제된 pathname, 거부면 null
function sanitizePath(raw) {
  if (typeof raw !== 'string') return null;
  const cut = raw.split(/[?#]/)[0];
  if (!cut.startsWith('/') || cut.length > MAX_PATH_LEN) return null;
  if (cut === '/api' || cut.startsWith('/api/')) return null;
  if (/^\/manage-[^/]+(\/|$)/.test(cut)) return null;
  if (ALLOWED_EXACT.has(cut)) return cut;
  for (const p of ALLOWED_PREFIXES) if (cut.startsWith(p)) return cut;
  return null;
}

function buildBatch(db, row, utcDay) {
  const insertHit = db.prepare(
    'INSERT INTO hits (ts, path, ref_domain, device, browser) SELECT ?, ?, ?, ?, ? ' +
    'WHERE COALESCE((SELECT n FROM counters WHERE day = ?), 0) < ?'
  ).bind(row.ts, row.path, row.ref, row.device, row.browser, utcDay, CAP);
  const bumpCounter = db.prepare(
    'INSERT INTO counters (day, n) VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET n = n + 1 WHERE n < ?'
  ).bind(utcDay, CAP);
  return [insertHit, bumpCounter];
}

async function record(context) {
  const { request, env } = context;
  const done = (status) => new Response(null, { status });

  // --- 게이트: 아래 거부 지점들은 전부 D1 접근 전에 종료 ---
  if (env.STATS_OFF) return done(204); // 수집 중단 스위치: 검증 없이 즉시 종료
  if (!env.STATS_DB) return done(204); // 바인딩 없음(프리뷰 등)에서는 조용히 종료
  const url = new URL(request.url);
  if (url.hostname !== SITE_HOST) return done(204); // 운영 호스트 외 차단
  const ua = request.headers.get('user-agent') || '';
  if (BOT_RE.test(ua)) return done(204); // 서버 봇 필터 (2단 중 2단)
  const ct = request.headers.get('content-type') || '';
  if (!ct.includes('application/json')) return done(204);
  const buf = await request.arrayBuffer();
  if (buf.byteLength > MAX_BODY_BYTES) return done(204); // 실제 수신 바이트 기준 (Content-Length 신뢰 안 함)
  let body;
  try { body = JSON.parse(new TextDecoder().decode(buf)); } catch { return done(204); }
  const path = sanitizePath(body && body.p);
  if (path === null) return done(204);

  const ts = Math.floor(Date.now() / 1000);
  const utcDay = new Date(ts * 1000).toISOString().slice(0, 10); // 카운터 키는 UTC 날짜
  const row = {
    ts, path,
    ref: refDomain(typeof body.r === 'string' ? body.r.slice(0, 500) : '', url.hostname),
    device: classifyDevice(ua),
    browser: classifyBrowser(ua),
  };

  // --- 원자 기록: 조건부 삽입 + 조건부 카운터 증가를 batch로 묶음 ---
  // 두 문장의 changes가 모두 1일 때만 기록된 것. 상한 도달 시 둘 다 0 (한쪽만 적용되는 상태 없음).
  try {
    const results = await env.STATS_DB.batch(buildBatch(env.STATS_DB, row, utcDay));
    return done(204);
  } catch {
    // 스키마 미생성 케이스만: 스키마 실행 후 동일 조건부 batch로 1회만 재시도. 그 외 실패는 조용히 무시.
    try {
      await env.STATS_DB.exec(SCHEMA);
      await env.STATS_DB.batch(buildBatch(env.STATS_DB, row, utcDay));
    } catch { /* 재시도 실패도 무기록 종료 */ }
    return done(204);
  }
}

export async function onRequest(context) {
  if (context.request.method !== 'POST') return new Response(null, { status: 405 });
  try {
    return await record(context);
  } catch {
    return new Response(null, { status: 204 }); // 수집 실패가 페이지 동작에 전파되지 않음
  }
}
