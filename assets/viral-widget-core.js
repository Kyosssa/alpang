// 바이럴 위젯 코어 로직 r4 — 순수 로직 모듈 (브라우저·Node 겸용, 2026-10-22)
// 기준: 이식설계안 / 기술이사 r3 재검수 잔존 3건(예외 경로) 보완.
// - 잠금: runExclusive는 {status:'ok'|'acquire-failed'|'error'}를 돌려준다. 획득 실패(임계영역 미실행)와
//   내부 오류(실행됨)를 구분한다. 획득 실패 시 배지 없이 메모리 플레이로 전환하고 시행을 중복 가산하지 않는다.
// - 실행 중 가드: 같은 도전의 중복 시작을 코어에서 거부한다. 목표 변경·새 도전은 실행 중이면 거부된다.
// - 배지: 결과 반환 시점의 저장·잠금 상태로 다시 평가한다 (도전 도중 강등되면 첫 배지를 남기지 않음).
// 확률값 p는 내부 고정밀 원값을 유지하고, 반올림은 표시 함수에서만 한다.
(function (global) {
  'use strict';

  var HAT_RULE_TEXT = 'STR·DEX·INT·LUK 중 어느 한 스탯이라도, 해당 스탯% 줄 수와 올스탯% 줄 수의 합이 2 이상이면 성공. 대상 스탯을 사전에 고르지 않으며, 서로 다른 단일 스탯끼리는 합산하지 않는다.';
  var HAT_RULE_EXAMPLES = '판정 예시: STR%+DEX%는 실패, STR%+올스탯%는 성공, 올스탯% 두 줄은 성공.';
  var HAT_RULE_NOTE = '어느 스탯이든 성공, 캐릭터 주스탯 사전 지정 없음';

  var TARGETS = [
    { id: 'C1', name: '유니크 무기 공격력/마력% 2줄 이상',
      desc: '미라클 큐브 · 무기 · 120레벨 · 유니크. 공격력% 또는 마력% 줄이 2줄 이상이면 성공 (혼합 허용).',
      p: 0.03219956488479381 },
    { id: 'C2', name: '모자 동일 스탯% 2줄 이상 · 올스탯 포함 (유니크)',
      desc: '미라클 큐브 · 모자 · 120레벨 · 유니크. ' + HAT_RULE_TEXT + ' ' + HAT_RULE_NOTE + '.',
      hatRule: true, p: 0.20864370554158448 },
    { id: 'C3', name: '모자 동일 스탯% 2줄 이상 · 올스탯 포함 (에픽)',
      desc: '미라클 큐브 · 모자 · 120레벨 · 에픽. ' + HAT_RULE_TEXT + ' ' + HAT_RULE_NOTE + '.',
      hatRule: true, p: 0.14053404714844753 },
    { id: 'C4', name: '유니크 무기 공격력/마력% 3줄',
      desc: '미라클 큐브 · 무기 · 120레벨 · 유니크. 공격력% 또는 마력% 줄이 3줄 전부이면 성공 (혼합 허용).',
      p: 0.0012432262291516489 }
  ];

  var AUTO_CAP = 5000;
  var SCHEMA_VER = 1;
  var LOCK_NAME = 'alpang.viral.v1.lock';

  function expected(p) { return 1 / p; }
  function probWithin(p, n) { return 1 - Math.pow(1 - p, n); }
  function quantile(p, q) { return Math.ceil(Math.log(1 - q) / Math.log(1 - p)); }
  function fmtPct(p) { return (p * 100).toFixed(4) + '%'; }
  function fmtExpected(p) { return expected(p).toFixed(1) + '회'; }
  function fmtProb(x) { return '약 ' + (x * 100).toFixed(1) + '%'; }
  function gradeOf(q) {
    if (q <= 0.10) return 'top';
    if (q <= 0.40) return 'high';
    if (q <= 0.75) return 'mid';
    return 'low';
  }
  var GRADE_IMAGES_CANDIDATE = {
    low:  { kind: 'mob',  id: 100100,  url: 'https://maplestory.io/api/GMS/95/mob/100100/icon' },
    mid:  { kind: 'mob',  id: 1210102, url: 'https://maplestory.io/api/GMS/95/mob/1210102/icon' },
    high: { kind: 'item', id: 1002357, url: 'https://maplestory.io/api/GMS/95/item/1002357/icon' },
    top:  { kind: 'item', id: 1003112, url: 'https://maplestory.io/api/GMS/95/item/1003112/icon' }
  };

  function kstDateString(now) {
    var d = now ? new Date(now) : new Date();
    var parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(d);
    var y, m, dd;
    parts.forEach(function (pt) {
      if (pt.type === 'year') y = pt.value;
      if (pt.type === 'month') m = pt.value;
      if (pt.type === 'day') dd = pt.value;
    });
    return y + '-' + m + '-' + dd;
  }

  // ── 공유 잠금 (결과 구분형) ──────────────────────────────────────────────
  // runExclusive(fn) → Promise<{status:'ok', value} | {status:'acquire-failed'} | {status:'error', error}>
  // 획득 실패가 한 번이라도 나면 그 잠금은 failed로 내려간다 (배지 판단에 사용).
  function makeLock(kind, requestFn) {
    var lock = { kind: kind, available: kind !== 'none', failed: false, failReason: null };
    lock.runExclusive = function (fn) {
      if (lock.kind === 'none') return Promise.resolve({ status: 'acquire-failed' });
      return requestFn(fn).then(
        function (value) { return { status: 'ok', value: value }; },
        function (err) {
          // requestFn이 started 여부를 함께 알리면 그 기준으로, 아니면 오류 객체의 표시로 구분한다.
          var started = err && err.__vwStarted === true;
          if (!started) { lock.failed = true; lock.failReason = 'acquire'; return { status: 'acquire-failed' }; }
          return { status: 'error', error: err };
        });
    };
    return lock;
  }
  var processChains = {};
  function createLock(env) {
    var nav = env && env.navigator !== undefined ? env.navigator
      : (typeof navigator !== 'undefined' ? navigator : null);
    var isBrowser = typeof window !== 'undefined';
    if (nav && nav.locks && typeof nav.locks.request === 'function') {
      return makeLock('web-locks', function (fn) {
        var started = false;
        return nav.locks.request(LOCK_NAME, function () {
          started = true;
          return fn();
        }).catch(function (e) {
          if (!started) throw e; // 획득 실패 — 임계영역 미실행
          e.__vwStarted = true; throw e; // 내부 오류 — 임계영역 실행됨
        });
      });
    }
    if (!isBrowser) {
      return makeLock('process', function (fn) {
        var prev = processChains[LOCK_NAME] || Promise.resolve();
        var run = prev.then(function () {
          return Promise.resolve().then(fn).catch(function (e) { e.__vwStarted = true; throw e; });
        });
        processChains[LOCK_NAME] = run.then(function () {}, function () {});
        return run;
      });
    }
    return makeLock('none', null);
  }

  // ── 저장소 (r3와 동일 원칙: 획득 예외 처리·스키마 검증·강등 시 메모리 우선) ──
  var KEY_DAILY = 'alpang.viral.v1.daily';
  var KEY_TOTAL = 'alpang.viral.v1.total';
  var KEY_VER = 'alpang.viral.v1.ver';

  function isSafeCount(x) { return typeof x === 'number' && isFinite(x) && x >= 0 && Math.floor(x) === x && x <= Number.MAX_SAFE_INTEGER; }
  function defaultDaily(dateStr) {
    return { ver: SCHEMA_VER, date: dateStr,
      jobFirst: { used: false, startedAt: null, runId: null, result: null },
      cubeFirst: { used: false, startedAt: null, runId: null, result: null } };
  }
  function defaultTotal() { return { ver: SCHEMA_VER, trials: 0, perMode: { job: 0, cube: 0 }, titles: [] }; }
  function validateDaily(d, todayStr) {
    if (!d || typeof d !== 'object' || d.ver !== SCHEMA_VER || typeof d.date !== 'string') return null;
    var modes = ['jobFirst', 'cubeFirst'];
    for (var i = 0; i < modes.length; i++) {
      var f = d[modes[i]];
      if (!f || typeof f !== 'object' || typeof f.used !== 'boolean') return null;
      if (f.result != null && typeof f.result !== 'object') return null;
    }
    if (d.date !== todayStr) return defaultDaily(todayStr);
    return d;
  }
  function validateTotal(t) {
    if (!t || typeof t !== 'object' || t.ver !== SCHEMA_VER) return null;
    if (!isSafeCount(t.trials)) return null;
    if (!t.perMode || !isSafeCount(t.perMode.job || 0) || !isSafeCount(t.perMode.cube || 0)) return null;
    if (!Array.isArray(t.titles) || !t.titles.every(isSafeCount)) return null;
    return t;
  }
  function acquireBackend(explicit) {
    if (explicit !== undefined) return explicit;
    try { if (typeof localStorage !== 'undefined') return localStorage; } catch (e) {}
    return null;
  }
  function SafeStore(backend) {
    this.backend = null;
    this.mem = {};
    this.persistent = false;
    this.degraded = false;
    this.lastWriteOk = false;
    if (backend) {
      try {
        backend.setItem('__vw_probe__', '1');
        backend.removeItem('__vw_probe__');
        this.backend = backend;
        this.persistent = true;
      } catch (e) { this.persistent = false; }
    }
  }
  SafeStore.prototype.isPersistent = function () { return this.persistent && !this.degraded; };
  SafeStore.prototype._degrade = function () { this.degraded = true; };
  SafeStore.prototype._rawGet = function (key) {
    if (this.isPersistent()) {
      try { var raw = this.backend.getItem(key); if (raw != null) return raw; }
      catch (e) { this._degrade(); }
    }
    return this.mem[key] != null ? JSON.stringify(this.mem[key]) : null;
  };
  SafeStore.prototype.peek = function (key) {
    var raw = this._rawGet(key);
    if (raw == null) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  };
  SafeStore.prototype.get = function (key, todayStr) {
    var raw = this._rawGet(key);
    var val = null;
    if (raw != null) { try { val = JSON.parse(raw); } catch (e) { val = null; } }
    var checked = null;
    if (key === KEY_DAILY) checked = validateDaily(val, todayStr);
    else if (key === KEY_TOTAL) checked = validateTotal(val);
    else checked = val;
    if (checked == null) {
      checked = key === KEY_DAILY ? defaultDaily(todayStr) : key === KEY_TOTAL ? defaultTotal() : null;
      if (checked != null) this.set(key, checked);
    } else if (this.degraded) {
      return this.mem[key] != null ? this.mem[key] : checked;
    } else {
      this.mem[key] = checked;
    }
    return checked;
  };
  SafeStore.prototype.set = function (key, val) {
    this.mem[key] = val;
    this.lastWriteOk = false;
    if (this.persistent && !this.degraded) {
      try { this.backend.setItem(key, JSON.stringify(val)); this.lastWriteOk = true; }
      catch (e) { this._degrade(); this.lastWriteOk = false; }
    } else {
      this.lastWriteOk = true;
    }
    return this.lastWriteOk;
  };

  var TITLES = [
    { at: 1, name: '첫 뽑기의 설렘' }, { at: 10, name: '열 번 찍는 손' },
    { at: 50, name: '뽑기 단골' }, { at: 77, name: '럭키 세븐 입문' },
    { at: 777, name: '세븐 잭팟 꿈나무' }, { at: 1000, name: '천 번의 두근거림' },
    { at: 5000, name: '오천 번의 운 시험' }, { at: 10000, name: '만 번 돌린 손' },
    { at: 30000, name: '전설의 손놀림' }
  ];
  function titleFor(trials) {
    var cur = null, next = null;
    for (var i = 0; i < TITLES.length; i++) {
      if (trials >= TITLES[i].at) cur = TITLES[i];
      else { next = TITLES[i]; break; }
    }
    return { current: cur, next: next, toNext: next ? next.at - trials : 0 };
  }
  function totalsView(t) {
    return { trials: t.trials, title: titleFor(t.trials), unlocked: null };
  }

  // ── 위젯 코어 ────────────────────────────────────────────────────────────
  function WidgetCore(opts) {
    opts = opts || {};
    var backend = acquireBackend(opts.backend);
    this.store = opts.store || new SafeStore(backend);
    this.lock = opts.lock || createLock(opts.env);
    this.rng = opts.rng || Math.random;
    this.now = opts.now || function () { return new Date(); };
    this.idFn = opts.idFn || function () { return 'run-' + Date.now().toString(36) + '-' + Math.floor(Math.random() * 1e9).toString(36); };
    this.target = TARGETS[0];
    this.cubeState = 'idle';
    this.cubeTries = 0;
    this.cubeRun = null;
    this.lastCard = null;
    this._cubeBusy = false;   // 실행 중 가드 (같은 도전 중복 시작 거부)
    this._jobBusy = false;
    this._gen = 0;            // 세대 번호 (목표 변경·새 도전 시 증가 — 늦은 결과 무효화)
    this._mirror = null;      // 메모리 플레이용 누적 미러
    this._daily();
  }
  WidgetCore.prototype.todayStr = function () { return kstDateString(this.now()); };
  WidgetCore.prototype._daily = function () { return this.store.get(KEY_DAILY, this.todayStr()); };
  WidgetCore.prototype._total = function () { return this.store.get(KEY_TOTAL, this.todayStr()); };
  WidgetCore.prototype.storageOk = function () { return this.store.isPersistent(); };
  WidgetCore.prototype.lockOk = function () { return !!this.lock.available && !this.lock.failed; };
  WidgetCore.prototype.badgeOk = function () { return this.storageOk() && this.lockOk(); };
  // 사유 안내용: 왜 배지를 줄 수 없는지
  WidgetCore.prototype.badgeBlockReason = function () {
    if (!this.storageOk()) return 'storage';
    if (!this.lockOk()) return 'lock';
    return null;
  };

  // 잠금 실행 정규화: 결과 객체({status})가 아닌 값을 돌려주는 잠금은 ok로, 거절·동기 예외는 획득 실패로 본다.
  WidgetCore.prototype._lockRun = function (fn) {
    var self = this;
    var p;
    try { p = this.lock.runExclusive(fn); }
    catch (e) { if (this.lock) this.lock.failed = true; return Promise.resolve({ status: 'acquire-failed' }); }
    return Promise.resolve(p).then(function (res) {
      if (res && typeof res === 'object' && typeof res.status === 'string') return res;
      return { status: 'ok', value: res };
    }, function (err) {
      if (err && err.__vwStarted === true) return { status: 'error', error: err }; // 임계영역 실행됨 — 재가산 금지
      if (self.lock) self.lock.failed = true;
      return { status: 'acquire-failed' };
    });
  };
  WidgetCore.prototype._claimFirst = function (mode, runId) {
    var self = this;
    var field = mode === 'job' ? 'jobFirst' : 'cubeFirst';
    return this._lockRun(function () {
      var startDate = self.todayStr();
      var d = self.store.get(KEY_DAILY, startDate);
      if (d[field].used) return false;
      d[field].used = true;
      d[field].startedAt = self.now().toISOString();
      d[field].runId = runId;
      d.date = startDate;
      var ok = self.store.set(KEY_DAILY, d);
      return ok && self.badgeOk();
    }).then(function (res) {
      if (res.status === 'ok') return res.value === true;
      return false; // 획득 실패·내부 오류 모두 배지 없음 (플레이는 계속)
    });
  };
  WidgetCore.prototype._saveFirstResult = function (mode, run, result) {
    if (!run || !run.first) return Promise.resolve(false);
    var self = this;
    var field = mode === 'job' ? 'jobFirst' : 'cubeFirst';
    return this._lockRun(function () {
      var d = self.store.peek(KEY_DAILY);
      if (!d || d.date !== run.startedDate || !d[field] || !d[field].used || d[field].runId !== run.runId) return false;
      d[field].result = result;
      return self.store.set(KEY_DAILY, d);
    }).then(function (res) { return res.status === 'ok' && res.value === true; });
  };
  WidgetCore.prototype.restoreFirst = function (mode, dateStr) {
    if (!this.storageOk()) return null; // 메모리 복원과 영속 복원을 구분 — 영속이 아니면 복원 배지를 만들지 않는다
    var want = dateStr || this.todayStr();
    var d = this.store.peek(KEY_DAILY);
    if (!d || d.date !== want) return null;
    var field = mode === 'job' ? 'jobFirst' : 'cubeFirst';
    if (d[field] && d[field].result) return { date: d.date, runId: d[field].runId, result: d[field].result };
    return null;
  };
  WidgetCore.prototype.isFirstAvailable = function (mode) {
    var d = this._daily();
    var field = mode === 'job' ? 'jobFirst' : 'cubeFirst';
    return !!d && !d[field].used && this.badgeOk();
  };
  WidgetCore.prototype._readTotalsSafe = function () {
    try { var t = this._total(); if (t && isSafeCount(t.trials)) return t; } catch (e) {}
    return null;
  };
  // 누적 증가: 잠금 안에서 직렬화. 획득 실패 시 메모리 미러로만 가산(중복 없음), 내부 오류 시 재가산하지 않는다.
  WidgetCore.prototype._addTrials = function (mode, n) {
    var self = this;
    return this._lockRun(function () {
      var t = self.store.get(KEY_TOTAL, self.todayStr());
      t.trials += n; t.perMode[mode] = (t.perMode[mode] || 0) + n;
      var info = titleFor(t.trials);
      var unlocked = null;
      if (info.current && t.titles.indexOf(info.current.at) === -1) { t.titles.push(info.current.at); unlocked = info.current; }
      self.store.set(KEY_TOTAL, t);
      self._mirror = { trials: t.trials, perMode: { job: t.perMode.job || 0, cube: t.perMode.cube || 0 }, titles: t.titles.slice() };
      return { trials: t.trials, title: info, unlocked: unlocked };
    }).then(function (res) {
      if (res.status === 'ok') return res.value;
      if (res.status === 'error') {
        // 임계영역이 이미 실행됐을 수 있다 — 재가산하지 않고 현재 값을 읽어 보고한다.
        var cur = self._readTotalsSafe() || self._mirror;
        if (cur) return totalsView(cur);
        return { trials: 0, title: titleFor(0), unlocked: null };
      }
      // acquire-failed: 공유 영속 갱신에 의존하지 않는 메모리 플레이
      var m = self._mirror || self._readTotalsSafe() || { trials: 0, perMode: { job: 0, cube: 0 }, titles: [] };
      m = { trials: m.trials, perMode: { job: m.perMode.job || 0, cube: m.perMode.cube || 0 }, titles: (m.titles || []).slice() };
      m.trials += n; m.perMode[mode] += n;
      var info2 = titleFor(m.trials);
      var unlocked2 = null;
      if (info2.current && m.titles.indexOf(info2.current.at) === -1) { m.titles.push(info2.current.at); unlocked2 = info2.current; }
      self._mirror = m;
      return { trials: m.trials, title: info2, unlocked: unlocked2 };
    });
  };

  // ── 직업 뽑기 (실행 중 가드 포함) ───────────────────────────────────────
  WidgetCore.prototype.rollJob = function (jobs) {
    var self = this;
    if (this._jobBusy) return Promise.resolve({ status: 'busy' });
    this._jobBusy = true;
    var runId = this.idFn();
    return this._claimFirst('job', runId).then(function (first) {
      var pick = jobs[Math.floor(self.rng() * jobs.length)];
      return self._addTrials('job', 1).then(function (tr) {
        var date = self.todayStr();
        var card = { kind: 'job', job: pick, isFirst: first, date: date, runId: runId,
          trials: tr.trials, title: tr.title, unlockedTitle: tr.unlocked };
        self.lastCard = card;
        return self._saveFirstResult('job', { runId: runId, startedDate: date, first: first },
          { jobId: pick.id, date: date, trials: tr.trials }).then(function () {
            // 반환 시점의 저장·잠금 상태로 배지를 다시 평가한다 (도전 도중 강등 시 첫 배지 제거)
            card.isFirst = first && self.badgeOk();
            self._jobBusy = false;
            return card;
          });
      });
    }).catch(function (e) {
      self._jobBusy = false;
      throw e;
    });
  };

  // ── 큐브 도전 ───────────────────────────────────────────────────────────
  // 목표 변경·새 도전은 실행 중이면 거부한다 (대기 중 조건 변경으로 늦은 결과가 어긋나는 것을 원천 차단).
  WidgetCore.prototype.setTarget = function (id) {
    if (this._cubeBusy) return null;
    for (var i = 0; i < TARGETS.length; i++) if (TARGETS[i].id === id) this.target = TARGETS[i];
    this._gen++;
    this.cubeState = 'idle'; this.cubeTries = 0; this.cubeRun = null; this.lastCard = null;
    return this.target;
  };
  WidgetCore.prototype.newCubeRun = function () {
    if (this._cubeBusy) return false;
    this._gen++;
    this.cubeState = 'idle'; this.cubeTries = 0; this.cubeRun = null; this.lastCard = null;
    return true;
  };
  WidgetCore.prototype._startCubeRun = function () {
    var self = this;
    var runId = this.idFn();
    return this._claimFirst('cube', runId).then(function (first) {
      self.cubeRun = { runId: runId, startedDate: self.todayStr(), startedAt: self.now().toISOString(), targetId: self.target.id, first: first, gen: self._gen };
      self.cubeState = 'running';
    });
  };
  WidgetCore.prototype.rollCubeOnce = function () {
    var self = this;
    if (this.cubeState === 'success' || this.cubeState === 'failed') {
      return Promise.resolve({ status: 'locked', reason: 'ended' });
    }
    if (this._cubeBusy) return Promise.resolve({ status: 'busy' });
    this._cubeBusy = true;
    var gen = this._gen;
    var startP = this.cubeState === 'idle' ? this._startCubeRun() : Promise.resolve();
    return startP.then(function () {
      self.cubeTries += 1;
      var hit = self.rng() < self.target.p;
      return self._addTrials('cube', 1).then(function () {
        self._cubeBusy = false;
        if (gen !== self._gen) return { status: 'stale' }; // 늦은 결과 무효화 (세대가 바뀐 경우)
        if (hit) return self._succeedCube();
        if (self.cubeTries >= AUTO_CAP) return self._failCube();
        return { status: 'running', tries: self.cubeTries };
      });
    }).catch(function (e) { self._cubeBusy = false; throw e; });
  };
  WidgetCore.prototype.rollCubeAuto = function () {
    var self = this;
    if (this.cubeState === 'success' || this.cubeState === 'failed') {
      return Promise.resolve({ status: 'locked', reason: 'ended' });
    }
    if (this._cubeBusy) return Promise.resolve({ status: 'busy' });
    this._cubeBusy = true;
    var gen = this._gen;
    var startP = this.cubeState === 'idle' ? this._startCubeRun() : Promise.resolve();
    return startP.then(function () {
      var start = self.cubeTries;
      var hit = false;
      while (self.cubeTries < AUTO_CAP) {
        self.cubeTries += 1;
        if (self.rng() < self.target.p) { hit = true; break; }
      }
      return self._addTrials('cube', self.cubeTries - start).then(function () {
        self._cubeBusy = false;
        if (gen !== self._gen) return { status: 'stale' };
        if (hit) return self._succeedCube();
        return self._failCube();
      });
    }).catch(function (e) { self._cubeBusy = false; throw e; });
  };
  WidgetCore.prototype._succeedCube = function () {
    this.cubeState = 'success';
    var p = this.target.p, n = this.cubeTries, run = this.cubeRun;
    var q = probWithin(p, n);
    var totals = this._readTotalsSafe();
    if (this._mirror && (!totals || this._mirror.trials > totals.trials)) totals = this._mirror;
    if (!totals) totals = { trials: n };
    var card = { kind: 'cube', target: this.target, tries: n,
      expected: expected(p), probWithin: q, q90: quantile(p, 0.9),
      grade: gradeOf(q), isFirst: !!(run && run.first),
      date: run ? run.startedDate : this.todayStr(), runId: run ? run.runId : null,
      trials: totals.trials, title: titleFor(totals.trials) };
    this.lastCard = card;
    var self = this;
    return this._saveFirstResult('cube', run, { targetId: this.target.id, tries: n, grade: card.grade, date: card.date, trials: totals.trials })
      .then(function () {
        card.isFirst = !!(run && run.first) && self.badgeOk(); // 반환 시점 재평가
        return { status: 'success', card: card };
      });
  };
  WidgetCore.prototype._failCube = function () {
    this.cubeState = 'failed';
    this.lastCard = null;
    return { status: 'failed', tries: this.cubeTries, cap: AUTO_CAP };
  };
  WidgetCore.prototype.restoreCubeEnded = function (targetId, tries, runId) {
    if (this._cubeBusy) return false;
    this.setTarget(targetId);
    this.cubeTries = tries;
    this.cubeState = 'success';
    this.cubeRun = { runId: runId || null, startedDate: this.todayStr(), targetId: targetId, first: true };
    return true;
  };

  var api = {
    TARGETS: TARGETS, AUTO_CAP: AUTO_CAP, TITLES: TITLES, SCHEMA_VER: SCHEMA_VER, LOCK_NAME: LOCK_NAME,
    HAT_RULE_TEXT: HAT_RULE_TEXT, HAT_RULE_EXAMPLES: HAT_RULE_EXAMPLES, HAT_RULE_NOTE: HAT_RULE_NOTE,
    expected: expected, probWithin: probWithin, quantile: quantile,
    fmtPct: fmtPct, fmtExpected: fmtExpected, fmtProb: fmtProb,
    gradeOf: gradeOf, GRADE_IMAGES_CANDIDATE: GRADE_IMAGES_CANDIDATE,
    kstDateString: kstDateString, SafeStore: SafeStore, titleFor: titleFor,
    createLock: createLock, WidgetCore: WidgetCore,
    KEYS: { daily: KEY_DAILY, total: KEY_TOTAL, ver: KEY_VER },
    defaults: { daily: defaultDaily, total: defaultTotal }
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.ViralCore = api;
})(typeof window !== 'undefined' ? window : globalThis);
