'use strict';
/* 안전 평가기 — 스킬 수치 조회 전용 (기술이사 구현 계약)
   허용 문법: 숫자 · x · 괄호 · 사칙연산(+ - * /)만. 그 외 토큰은 거부한다.
   임의 코드 실행 없음 (eval/Function 미사용, 재귀 하강 파서).
   자원 한도: 식 길이 200자 · 토큰 100개 · 괄호 깊이 10 · 연산 200회.
   0 나눗셈·평가 실패는 throw 하지 않고 { ok:false, reason } 으로 돌려준다. */
const LIMITS = { maxLen: 200, maxTokens: 100, maxDepth: 10, maxOps: 200, maxUnary: 10, maxLiteral: 1e12, maxValue: 1e15 };

function tokenize(expr) {
  if (typeof expr !== 'string' || expr.length === 0) return { ok: false, reason: 'empty' };
  if (expr.length > LIMITS.maxLen) return { ok: false, reason: 'too_long' };
  const tokens = [];
  let i = 0;
  while (i < expr.length) {
    const ch = expr[i];
    if (ch === ' ' || ch === '\t') { i++; continue; }
    if (ch >= '0' && ch <= '9' || ch === '.') {
      let j = i, dot = false;
      while (j < expr.length && ((expr[j] >= '0' && expr[j] <= '9') || expr[j] === '.')) {
        if (expr[j] === '.') { if (dot) return { ok: false, reason: 'bad_number' }; dot = true; }
        j++;
      }
      const num = Number(expr.slice(i, j));
      if (!Number.isFinite(num)) return { ok: false, reason: 'bad_number' };
      if (Math.abs(num) > LIMITS.maxLiteral) return { ok: false, reason: 'literal_too_large' };
      tokens.push({ t: 'num', v: num });
      i = j; continue;
    }
    if (ch === 'x') { tokens.push({ t: 'x' }); i++; continue; }
    if ('+-*/()'.includes(ch)) { tokens.push({ t: ch }); i++; continue; }
    return { ok: false, reason: 'forbidden_token:' + ch };
  }
  if (tokens.length > LIMITS.maxTokens) return { ok: false, reason: 'too_many_tokens' };
  return { ok: true, tokens };
}

function evaluate(expr, level, levelRange) {
  if (typeof level !== 'number' || !Number.isInteger(level)) {
    return { ok: false, reason: 'level_not_integer' };
  }
  if (level <= 0) return { ok: false, reason: 'level_not_positive' };
  if (!Array.isArray(levelRange) || levelRange.length !== 2) {
    return { ok: false, reason: 'level_range_missing' };
  }
  for (const b of levelRange) {
    if (typeof b !== 'number' || !Number.isFinite(b) || !Number.isInteger(b)) {
      return { ok: false, reason: 'level_range_invalid' };
    }
  }
  if (level < levelRange[0] || level > levelRange[1]) {
    return { ok: false, reason: 'level_out_of_range' };
  }
  const tk = tokenize(expr);
  if (!tk.ok) return tk;
  const tokens = tk.tokens;
  let pos = 0, ops = 0;
  function peek() { return tokens[pos]; }
  function checkMid(v) {
    if (!Number.isFinite(v)) throw { reason: 'non_finite' };
    if (Math.abs(v) > LIMITS.maxValue) throw { reason: 'value_too_large' };
    return v;
  }
  function parseExpr(depth) {
    if (depth > LIMITS.maxDepth) throw { reason: 'too_deep' };
    let v = parseTerm(depth);
    while (peek() && (peek().t === '+' || peek().t === '-')) {
      const op = tokens[pos++].t;
      if (++ops > LIMITS.maxOps) throw { reason: 'too_many_ops' };
      const r = parseTerm(depth);
      v = checkMid(op === '+' ? v + r : v - r);
    }
    return v;
  }
  function parseTerm(depth) {
    let v = parseFactor(depth);
    while (peek() && (peek().t === '*' || peek().t === '/')) {
      const op = tokens[pos++].t;
      if (++ops > LIMITS.maxOps) throw { reason: 'too_many_ops' };
      const r = parseFactor(depth);
      if (op === '/') {
        if (r === 0) throw { reason: 'div_by_zero' };
        v = checkMid(v / r);
      } else v = checkMid(v * r);
    }
    return v;
  }
  function parseFactor(depth, unary) {
    const tok = tokens[pos];
    if (!tok) throw { reason: 'unexpected_end' };
    if (tok.t === '-' || tok.t === '+') {
      if ((unary || 0) + 1 > LIMITS.maxUnary) throw { reason: 'unary_too_deep' };
      pos++;
      const v = parseFactor(depth, (unary || 0) + 1);
      return tok.t === '-' ? -v : v;
    }
    if (tok.t === 'num') { pos++; return tok.v; }
    if (tok.t === 'x') { pos++; return level; }
    if (tok.t === '(') {
      pos++;
      const v = parseExpr(depth + 1);
      if (!peek() || peek().t !== ')') throw { reason: 'unbalanced_paren' };
      pos++;
      return v;
    }
    throw { reason: 'unexpected_token' };
  }
  try {
    const raw = parseExpr(0);
    if (pos !== tokens.length) return { ok: false, reason: 'trailing_tokens' };
    // 원값(rawValue)과 표시용 값(value)을 분리한다. value의 반올림은 표시용 정리이며
    // 게임의 반올림 규칙을 구현한 것이 아니다.
    const v = Math.round(raw * 1e6) / 1e6;
    return { ok: true, value: v, rawValue: raw };
  } catch (e) {
    return { ok: false, reason: (e && e.reason) || 'eval_failed' };
  }
}

if (typeof module !== 'undefined') module.exports = { evaluate, tokenize, LIMITS };
