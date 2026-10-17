// 알팡지지 관리자 통계 — Cloudflare Access JWT 서버 검증 (설계 006 개정 2·3)
// Cf-Access-Jwt-Assertion 헤더의 JWT를 팀 도메인 JWKS로 RS256 서명 검증하고 iss·aud·exp를 확인한다.
// 이메일 헤더(Cf-Access-Authenticated-User-Email)만으로 인증 판단하지 않음 — 표시용으로만 가능.
// 검증 실패 사유는 호출자에게 구분해 알리지 않는다 (전부 동일하게 차단).
const JWKS_TTL_MS = 6 * 3600 * 1000; // 메모리 캐시 유지 시간 (수 시간 단위 갱신)

let jwksCache = null; // { keys: Map<kid, jwk>, fetchedAt: number }

export function _resetJwksCache() { jwksCache = null; }

function b64urlToBytes(s) {
  const b64 = s.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(s.length / 4) * 4, '=');
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function b64urlToJson(s) {
  return JSON.parse(new TextDecoder().decode(b64urlToBytes(s)));
}
function teamHost(teamDomain) {
  return String(teamDomain || '').replace(/^https?:\/\//, '').replace(/\/+$/, '');
}

async function fetchJwks(host, fetchImpl) {
  const res = await fetchImpl(`https://${host}/cdn-cgi/access/certs`);
  if (!res || !res.ok) throw new Error('jwks fetch failed');
  const data = await res.json();
  const keys = new Map();
  for (const k of (data && data.keys) || []) if (k && k.kid) keys.set(k.kid, k);
  if (keys.size === 0) throw new Error('jwks empty');
  jwksCache = { keys, fetchedAt: Date.now() };
  return keys;
}

// kid에 맞는 JWK를 돌려준다. 캐시가 신선하고 키가 있으면 캐시 사용,
// 키 교체에 대비해 kid가 없으면 1회 재조회한다. 조회 실패 시 낡은 캐시라도 있으면 그것을 쓰고,
// 캐시 자체가 없으면 null (차단 쪽으로 기움).
async function getKey(kid, host, fetchImpl) {
  const fresh = jwksCache && (Date.now() - jwksCache.fetchedAt < JWKS_TTL_MS);
  if (fresh && jwksCache.keys.has(kid)) return jwksCache.keys.get(kid);
  try {
    const keys = await fetchJwks(host, fetchImpl);
    if (keys.has(kid)) return keys.get(kid);
  } catch { /* 아래 낡은 캐시로 폴백 */ }
  if (jwksCache && jwksCache.keys.has(kid)) return jwksCache.keys.get(kid);
  return null;
}

// 성공하면 { ok: true, email } 실패하면 { ok: false } (사유 비공개)
export async function verifyAccessJwt(token, { teamDomain, aud, fetchImpl, nowSec } = {}) {
  try {
    if (!token || !teamDomain || !aud) return { ok: false };
    const host = teamHost(teamDomain);
    if (!host) return { ok: false };
    const doFetch = fetchImpl || ((...a) => globalThis.fetch(...a));
    const now = typeof nowSec === 'number' ? nowSec : Math.floor(Date.now() / 1000);

    const parts = String(token).split('.');
    if (parts.length !== 3) return { ok: false };
    const header = b64urlToJson(parts[0]);
    if (!header || header.alg !== 'RS256' || !header.kid) return { ok: false };

    const jwk = await getKey(header.kid, host, doFetch);
    if (!jwk) return { ok: false };
    const key = await crypto.subtle.importKey(
      'jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
    const signed = new TextEncoder().encode(parts[0] + '.' + parts[1]);
    const valid = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64urlToBytes(parts[2]), signed);
    if (!valid) return { ok: false };

    const payload = b64urlToJson(parts[1]);
    if (!payload) return { ok: false };
    if (payload.iss !== `https://${host}`) return { ok: false };
    const auds = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
    if (!auds.includes(aud)) return { ok: false };
    if (typeof payload.exp !== 'number' || payload.exp <= now) return { ok: false };
    if (typeof payload.nbf === 'number' && payload.nbf > now + 60) return { ok: false };
    return { ok: true, email: typeof payload.email === 'string' ? payload.email : null };
  } catch {
    return { ok: false };
  }
}

// 요청 단위 편의 함수: env에서 ACCESS_TEAM_DOMAIN·ACCESS_AUD를 읽는다.
export function verifyAccessRequest(request, env, fetchImpl) {
  const token = request.headers.get('cf-access-jwt-assertion');
  if (!token) return Promise.resolve({ ok: false });
  return verifyAccessJwt(token, {
    teamDomain: env && env.ACCESS_TEAM_DOMAIN,
    aud: env && env.ACCESS_AUD,
    fetchImpl,
  });
}
