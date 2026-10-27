// 알팡지지 관리자 통계 2차 확장 — 구글 서치콘솔 연동 모듈 (설계: stats/개발담당2-설계-서치콘솔연동-2차확장-20261017.md)
// 상태: 골격 + 로컬 mock 검증 완료. 화면 렌더 연결은 구현 지시 후 manage Function에서 이 모듈을 호출해 붙인다.
// 실값 필요 지점 (이 파일에 값을 넣지 않는다 — 전부 Pages 환경변수/Secret):
//   - GSC_SA_EMAIL: 서비스 계정 이메일 (대표가 Secret으로 입력)
//   - GSC_SA_PRIVATE_KEY: 서비스 계정 개인키 PEM (대표가 Secret으로 입력)
//   - GSC_SITE_URL: 속성 표기 (도메인 속성 'sc-domain:alpang.gg' 또는 URL 접두사 'https://alpang.gg/') — 속성 유형 확정 후 설정
// 키·토큰은 로그와 에러 응답에 남기지 않는다. 오류는 상태 구분 문자열만 돌려준다.
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const API_BASE = 'https://www.googleapis.com/webmasters/v3';
const READONLY_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly';
const GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:jwt-bearer';
const RESULT_CACHE_TTL_MS = 6 * 3600 * 1000;

let tokenCache = { token: null, exp: 0 };
const resultCache = new Map(); // key -> { at, data }
export function _resetGscCaches() { tokenCache = { token: null, exp: 0 }; resultCache.clear(); }

// 구글 응답이 늦게 매달리면 통계 화면 전체가 늦어지므로 호출마다 8초 상한을 건다.
function withTimeout(init = {}) {
  try {
    if (typeof AbortSignal !== 'undefined' && AbortSignal.timeout) return { ...init, signal: AbortSignal.timeout(8000) };
  } catch { /* 타임아웃을 못 걸면 그냥 호출 */ }
  return init;
}

function b64urlEncode(data) {
  const bytes = typeof data === 'string' ? new TextEncoder().encode(data) : data;
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// 속성 입력값을 API siteUrl 표기로 정규화한다. 두 유형 모두 대응:
//   'alpang.gg' / 'sc-domain:alpang.gg' → 'sc-domain:alpang.gg' (도메인 속성)
//   'https://alpang.gg' / 'https://alpang.gg/' → 'https://alpang.gg/' (URL 접두사 속성)
export function toSiteUrl(input) {
  const s = String(input || '').trim();
  if (!s) return '';
  if (s.startsWith('sc-domain:')) return s;
  if (/^https?:\/\//.test(s)) {
    try {
      const u = new URL(s);
      if (u.pathname === '' || u.pathname === '/') return `${u.origin}/`;
      return s;
    } catch { return s; }
  }
  return 'sc-domain:' + s.replace(/\/+$/, '');
}
export function buildQueryUrl(siteUrl) {
  return `${API_BASE}/sites/${encodeURIComponent(toSiteUrl(siteUrl))}/searchAnalytics/query`;
}

// Secret에 들어간 PEM을 정규화해 DER로 바꾼다. 실무에서 흔한 변형을 모두 흡수:
//   줄바꿈이 \\n 이스케이프 문자열로 들어간 경우, CRLF, 앞뒤 따옴표·공백.
function pemToDer(pem) {
  let t = String(pem || '').trim();
  if (t.length >= 2 && ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith("'") && t.endsWith("'")))) t = t.slice(1, -1);
  t = t.replace(/\\r/g, '').replace(/\\n/g, '\n');
  const body = t.replace(/-----BEGIN [^-]+-----/, '').replace(/-----END [^-]+-----/, '').replace(/\s+/g, '');
  const bin = atob(body);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
export async function importServiceAccountKey(pem) {
  return crypto.subtle.importKey('pkcs8', pemToDer(pem), { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']);
}

export async function createAssertionJwt({ email, key, nowSec }) {
  const header = { alg: 'RS256', typ: 'JWT' };
  const payload = { iss: email, scope: READONLY_SCOPE, aud: TOKEN_URL, iat: nowSec, exp: nowSec + 3600 };
  const unsigned = b64urlEncode(JSON.stringify(header)) + '.' + b64urlEncode(JSON.stringify(payload));
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(unsigned));
  return unsigned + '.' + b64urlEncode(new Uint8Array(sig));
}

// 액세스 토큰 교환 (메모리 캐시: 만료 60초 전까지 재사용)
export async function getAccessToken(env, { fetchImpl, nowSec } = {}) {
  if (!env || !env.GSC_SA_EMAIL || !env.GSC_SA_PRIVATE_KEY) return { ok: false, error: 'not_configured' };
  const now = typeof nowSec === 'number' ? nowSec : Math.floor(Date.now() / 1000);
  if (tokenCache.token && tokenCache.exp - now > 60) return { ok: true, token: tokenCache.token };
  const doFetch = fetchImpl || ((...a) => globalThis.fetch(...a));
  try {
    const key = await importServiceAccountKey(env.GSC_SA_PRIVATE_KEY);
    const assertion = await createAssertionJwt({ email: env.GSC_SA_EMAIL, key, nowSec: now });
    const res = await doFetch(TOKEN_URL, withTimeout({
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ grant_type: GRANT_TYPE, assertion }).toString(),
    }));
    if (!res || !res.ok) return { ok: false, error: 'token_exchange_failed' };
    const data = await res.json();
    if (!data || !data.access_token) return { ok: false, error: 'token_exchange_failed' };
    tokenCache = { token: data.access_token, exp: now + (Number(data.expires_in) || 3600) };
    return { ok: true, token: tokenCache.token };
  } catch {
    return { ok: false, error: 'token_exchange_failed' };
  }
}

function mapRow(r) {
  return {
    key: (r.keys && r.keys[0]) || '',
    clicks: Number(r.clicks) || 0,
    impressions: Number(r.impressions) || 0,
    ctrPct: Math.round((Number(r.ctr) || 0) * 1000) / 10,
    position: Math.round((Number(r.position) || 0) * 10) / 10,
  };
}

export async function querySearchAnalytics({ accessToken, siteUrl, startDate, endDate, dimensions = [], rowLimit = 25, fetchImpl }) {
  const doFetch = fetchImpl || ((...a) => globalThis.fetch(...a));
  try {
    const res = await doFetch(buildQueryUrl(siteUrl), withTimeout({
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ startDate, endDate, dimensions, rowLimit }),
    }));
    if (!res || !res.ok) {
      return { ok: false, error: res && res.status === 403 ? 'forbidden' : 'api_error', status: res ? res.status : 0 };
    }
    const data = await res.json();
    return { ok: true, rows: ((data && data.rows) || []).map(mapRow) };
  } catch {
    return { ok: false, error: 'api_error', status: 0 };
  }
}

// 연동 검증용: 서비스 계정이 볼 수 있는 속성 목록 (착수 직후 권한 대조에만 사용)
export async function listSites(env, { fetchImpl } = {}) {
  const tok = await getAccessToken(env, { fetchImpl });
  if (!tok.ok) return tok;
  const doFetch = fetchImpl || ((...a) => globalThis.fetch(...a));
  try {
    const res = await doFetch(`${API_BASE}/sites`, withTimeout({ headers: { Authorization: `Bearer ${tok.token}` } }));
    if (!res || !res.ok) return { ok: false, error: res && res.status === 403 ? 'forbidden' : 'api_error' };
    const data = await res.json();
    return { ok: true, entries: ((data && data.siteEntry) || []).map(e => ({ siteUrl: e.siteUrl, permissionLevel: e.permissionLevel })) };
  } catch {
    return { ok: false, error: 'api_error' };
  }
}

function kstDateStr(nowMs) {
  return new Date(nowMs + 9 * 3600 * 1000).toISOString().slice(0, 10);
}
function shiftDateStr(dateStr, deltaDays) {
  const ms = Date.parse(dateStr + 'T00:00:00Z') + deltaDays * 86400 * 1000;
  return new Date(ms).toISOString().slice(0, 10);
}
function pagePath(url) {
  try { return new URL(url).pathname; } catch { return url; }
}

// 화면 섹션용 데이터 한 번에 조회: 합계 + 검색어 25 + 페이지 20. 결과는 6시간 캐시.
export async function getSearchSectionData(env, { period = 7, fetchImpl, nowMs } = {}) {
  if (!env || !env.GSC_SA_EMAIL || !env.GSC_SA_PRIVATE_KEY || !env.GSC_SITE_URL) {
    return { ok: false, error: 'not_configured' };
  }
  const days = period === 28 ? 28 : 7;
  const now = typeof nowMs === 'number' ? nowMs : Date.now();
  const endDate = shiftDateStr(kstDateStr(now), -2); // 확정 데이터 기준: 오늘(KST) - 2일
  const startDate = shiftDateStr(endDate, -(days - 1));
  const cacheKey = `gsc:${days}:${endDate}`;
  const hit = resultCache.get(cacheKey);
  if (hit && now - hit.at < RESULT_CACHE_TTL_MS) return hit.data;

  const tok = await getAccessToken(env, { fetchImpl, nowSec: Math.floor(now / 1000) });
  if (!tok.ok) return tok;
  const common = { accessToken: tok.token, siteUrl: env.GSC_SITE_URL, startDate, endDate, fetchImpl };
  const [totals, queries, pages] = await Promise.all([
    querySearchAnalytics({ ...common, dimensions: [], rowLimit: 1 }),
    querySearchAnalytics({ ...common, dimensions: ['query'], rowLimit: 25 }),
    querySearchAnalytics({ ...common, dimensions: ['page'], rowLimit: 20 }),
  ]);
  const firstFail = [totals, queries, pages].find(r => !r.ok);
  if (firstFail) return firstFail;
  // [자리 2 · 기간 비교] 전 기간 검색어 — 실패해도 본 기간을 막지 않고 자리만 비운다 (prevQueries = null → 렌더에서 '—')
  const prevEnd = shiftDateStr(startDate, -1);
  const prevStart = shiftDateStr(prevEnd, -(days - 1));
  let prevQueries = null;
  try {
    const prev = await querySearchAnalytics({ ...common, startDate: prevStart, endDate: prevEnd, dimensions: ['query'], rowLimit: 25 });
    if (prev.ok) prevQueries = prev.rows;
  } catch { prevQueries = null; }
  // [표시 확장 준비본 · 2026-10-26] 전 기간 페이지 — 페이지별 표의 증감 자리용. 격리 규칙은 prevQueries와 동일.
  let prevPages = null;
  try {
    const prevP = await querySearchAnalytics({ ...common, startDate: prevStart, endDate: prevEnd, dimensions: ['page'], rowLimit: 20 });
    if (prevP.ok) prevPages = prevP.rows.map(r => ({ ...r, key: pagePath(r.key) }));
  } catch { prevPages = null; }
  const t = totals.rows[0] || { clicks: 0, impressions: 0, ctrPct: 0, position: 0 };
  const data = {
    ok: true, startDate, endDate,
    totals: { clicks: t.clicks, impressions: t.impressions, ctrPct: t.ctrPct, position: t.position },
    queries: queries.rows,
    prevQueries,
    prevStart, prevEnd,
    pages: pages.rows.map(r => ({ ...r, key: pagePath(r.key) })),
    prevPages,
  };
  resultCache.set(cacheKey, { at: now, data });
  return data;
}
