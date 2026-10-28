// 바이럴 위젯 DOM 바인딩 r3 (2026-10-21) — 기술이사 r2 재검수 잔존 3건 반영.
// 추첨은 명시적 버튼 클릭으로만 시작한다. 목표 변경·새 도전·모드 전환 시 이전 결과를 함께 초기화한다.
// 복원: 저장된 첫 결과와 현재 도전을 분리해 들고, 복원 시 모드·목표·횟수·버튼·명함을 일관되게 맞춘다.
(function () {
  'use strict';
  var C = window.ViralCore;
  var core = new C.WidgetCore({});
  var $ = function (id) { return document.getElementById(id); };

  var GRADE_LABEL = { top: '최상 (대박)', high: '상위 (금손)', mid: '중간 (평범)', low: '최하 (눈물)' };
  var GRADE_LINE = {
    top: '이 손, 오늘은 뭔가 있습니다.',
    high: '평균보다 한참 앞질렀습니다. 기분 좋은 손입니다.',
    mid: '딱 평균적인, 정직한 손입니다.',
    low: '이 결과, 혼자 보기 아깝습니다. 같이 울어 줄 사람을 부르세요.'
  };
  var GROUP_LINE = {
    '모험가': '메이플의 시작은 언제나 모험가부터였죠.',
    '영웅': '전설이 다시 깨어나는 순간입니다.',
    '시그너스': '여제의 기사단에 합류했습니다.',
    '레지스탕스': '에델슈타인의 저항군에 합류했습니다.'
  };
  var CUBE_NOTICE = '조건: 미라클 큐브 · 120레벨 고정 · 확률은 공식 공시 기준이며 알팡 서버 적용은 미확인입니다. 실제 게임이 아닌 운 시뮬레이션 결과입니다. 알팡서버 공식 오픈 시 서버 버전에 맞게 확률이 업데이트될 예정입니다.';
  var JOB_NOTICE = 'GMS 95 직업·전직 단계 자료를 기반으로 한 재미 추첨이며, 알팡 서버의 실제 구현 여부는 미확인입니다.';

  // 복원된 첫 결과 카드 (모드별로 분리해 유지 — 현재 도전과 섞지 않는다)
  var restoredCards = { job: null, cube: null };
  var currentMode = 'job';
  var cubeSeq = 0; // 늦은 결과 무효화 토큰 (모드·목표·새 도전 때마다 증가)
  var jobSeq = 0;  // 직업 추첨 늦은 결과 무효화 토큰 (모드 전환 때마다 증가)

  function setStatus(msg) { $('vwStatus').textContent = msg; }

  function refreshStorageNote() {
    var note = $('vwStorageNote');
    if (!note) return;
    if (!core.storageOk()) {
      note.style.display = '';
      note.textContent = '이 브라우저에서는 기록 저장이 안 돼 오늘 첫 결과 표시와 누적 칭호를 붙이지 않습니다. 뽑기 자체는 계속할 수 있습니다.';
    } else if (!core.lockOk()) {
      note.style.display = '';
      note.textContent = '이 브라우저에서는 동시 실행 방지가 지원되지 않아 오늘 첫 결과 표시를 붙이지 않습니다. 뽑기 자체는 계속할 수 있습니다.';
    } else {
      note.style.display = 'none';
    }
  }

  function resetCardUI() {
    hideShareNote();
    $('vwCardKind').textContent = '결과 명함 카드';
    $('vwCardBadge').textContent = '';
    $('vwCardTitle').textContent = '아직 결과가 없습니다. 왼쪽에서 직접 돌려 보세요!';
    $('vwCardSub').textContent = '';
    $('vwGradeText').textContent = '';
    var img = $('vwCardImg');
    img.removeAttribute('src'); img.style.display = 'none';
    ['1', '2', '3', '4'].forEach(function (n) {
      $('vwStat' + n + 'Label').textContent = '';
      $('vwStat' + n + 'Val').textContent = '';
    });
    $('vwShareText').textContent = '';
    $('vwShareRow').style.display = 'none';
    $('vwToast').textContent = '';
    currentShare = null;
  }

  function setCubeButtonsEnded(ended) {
    $('vwCubeOnce').disabled = ended;
    $('vwCubeAuto').disabled = ended;
    $('vwCubeNew').style.display = ended ? '' : 'none';
  }

  function renderJobCard(card) {
    hideShareNote();
    var j = card.job;
    var name = window.finalDisplayName(j);
    $('vwCardKind').textContent = '운명 첫 캐릭 뽑기 결과';
    $('vwCardBadge').textContent = card.isFirst ? '🟠 이 브라우저의 오늘 첫 결과 · ' + card.date : '연습 모드';
    $('vwCardTitle').textContent = '내 운명의 첫 캐릭은 [' + name + '] 입니다!';
    $('vwCardSub').textContent = j.comment || '개성 강한 직업이 당신을 골랐습니다.';
    $('vwGradeText').textContent = '';
    $('vwStat1Label').textContent = '직업 분류';
    $('vwStat1Val').textContent = (j.series || '') + (j.branch ? ' · ' + j.branch : '');
    $('vwStat2Label').textContent = '대표 스킬';
    $('vwStat2Val').textContent = window.finalSkillLine(j) || '';
    var img = $('vwCardImg');
    // 아바타는 직업 아바타만 쓴다 (스킬 아이콘 사용 금지). 없거나 로드 실패하면 공통 단풍잎 로고.
    var DEFAULT_AVATAR = '/assets/logo.png';
    img.onerror = function () { if (img.getAttribute('src') !== DEFAULT_AVATAR) img.src = DEFAULT_AVATAR; };
    img.src = j.avatar || DEFAULT_AVATAR;
    img.alt = name; img.style.display = '';
    $('vwStat3Label').textContent = '누적 시행';
    $('vwStat3Val').textContent = card.trials.toLocaleString() + '회';
    $('vwStat4Label').textContent = '칭호';
    $('vwStat4Val').textContent = card.title && card.title.current ? card.title.current.name : '없음';
    $('vwShareText').textContent = window.shareJobTextV2(card);
    var firstSkill = (j.skills && j.skills.length) ? (j.skills[0].ko || j.skills[0].nameEn) : '';
    currentShare = {
      title: '✨ 내 운명의 첫 캐릭은 ' + name + '!',
      desc: (firstSkill ? '🤖 대표 스킬: ' + firstSkill + ' · ' : '') + '💡 ' + (j.comment || ''),
      imageUrl: j.avatar ? 'https://alpang.gg' + j.avatar : 'https://alpang.gg/assets/og.png',
      detailUrl: 'https://alpang.gg/calculator/cube/',
      buttons: [
        { title: '내 직업 스킬 보기', url: 'https://alpang.gg/jobs/#job-' + j.id },
        { title: '나도 운명 테스트하기', url: 'https://alpang.gg/calculator/cube/' }
      ]
    };
    $('vwShareRow').style.display = '';
  }

  function renderCubeCard(card) {
    hideShareNote();
    var t = card.target;
    $('vwCardKind').textContent = '목표 큐브 운 시뮬레이션 결과';
    $('vwCardBadge').textContent = card.isFirst ? '🟠 이 브라우저의 오늘 첫 결과 · ' + card.date : '연습 모드';
    $('vwCardTitle').textContent = '[' + t.name + '] ' + card.tries.toLocaleString() + '회 만에 성공했습니다!';
    $('vwCardSub').textContent = GRADE_LINE[card.grade];
    var img = $('vwCardImg'); // 등급 이미지는 렌더하지 않는다 (텍스트 등급만)
    img.removeAttribute('src'); img.style.display = 'none';
    $('vwGradeText').textContent = '운 등급 (재미 판정): ' + GRADE_LABEL[card.grade] + (card.title && card.title.current ? ' · 칭호 「' + card.title.current.name + '」' : '');
    $('vwStat1Label').textContent = '나의 도달 횟수';
    $('vwStat1Val').textContent = card.tries.toLocaleString() + '회';
    $('vwStat2Label').textContent = '같은 조건의 이론 기대 횟수';
    $('vwStat2Val').textContent = card.expected.toFixed(1) + '회';
    $('vwStat3Label').textContent = card.tries + '회 이내 성공할 확률';
    $('vwStat3Val').textContent = C.fmtProb(card.probWithin);
    $('vwStat4Label').textContent = '90% 누적 성공 기준 (보장 아님)';
    $('vwStat4Val').textContent = card.q90.toLocaleString() + '회';
    $('vwShareText').textContent = window.shareCubeTextV2({ target: t, tries: card.tries, grade: { label: GRADE_LABEL[card.grade] }, title: card.title && card.title.current });
    currentShare = {
      title: '🎲 ' + t.name + ' ' + card.tries.toLocaleString() + '회 컷!',
      desc: '🏅 획득 칭호: ' + (card.title && card.title.current ? card.title.current.name : 'The First') + ' · 🔥 내 큐브 운빨은 어느 정도일까?',
      imageUrl: window.CUBE_SHARE_IMAGE_URL || 'https://alpang.gg/assets/og.png',
      detailUrl: 'https://alpang.gg/calculator/cube/',
      buttons: [
        { title: '결과 상세보기', url: 'https://alpang.gg/calculator/cube/' },
        { title: '내 큐브 운 시험하기', url: 'https://alpang.gg/calculator/cube/' }
      ]
    };
    $('vwShareRow').style.display = '';
    showSlotsResult(t, true);
  }

  // ── v2 슬롯 박스 연출 (실제 줄 추첨이 아닌 목표 당첨 여부 표시) ──
  function slotEls() { return [$('vwSlot1'), $('vwSlot2'), $('vwSlot3')]; }
  function showSlotsRolling() {
    slotEls().forEach(function (el) { el.className = 'vw-slot rolling'; el.textContent = '···'; });
  }
  function showSlotsResult(target, success) {
    var need = target.slotNeed || 2;
    slotEls().forEach(function (el, i) {
      if (success && i < need) { el.className = 'vw-slot hit'; el.textContent = target.slotLabel || '목표 옵션'; }
      else { el.className = 'vw-slot miss'; el.textContent = '—'; }
    });
  }
  function showSlotsIdle(target) {
    slotEls().forEach(function (el) { el.className = 'vw-slot'; el.textContent = '?'; });
    $('vwSlotNeed').textContent = '목표 ' + (target.slotNeed || 2) + '줄: ' + (target.slotLabel || '');
  }

  // ── v2 공유 본안: 카카오톡 피드 공유 (방안 A). 키·SDK가 없으면 텍스트로 폴백 ──
  var currentShare = null; // {title, desc, imageUrl, detailUrl}
  function kakaoReady() {
    try {
      if (!window.Kakao || !window.KAKAO_JS_KEY) return false;
      if (!window.Kakao.isInitialized()) window.Kakao.init(window.KAKAO_JS_KEY);
      return window.Kakao.isInitialized() && !!window.Kakao.Share;
    } catch (e) { return false; }
  }
  function showShareNote(msg) {
    var n = $('vwShareNote');
    if (!n) return; // 구 HTML과 섞여도 공유 동작이 깨지지 않게 한다
    n.textContent = msg;
    n.hidden = false;
  }
  function hideShareNote() { var n = $('vwShareNote'); if (n) n.hidden = true; }
  function shareKakaoOrFallback() {
    if (!currentShare) { setStatus('먼저 결과를 뽑아 주세요.'); return; }
    if (!kakaoReady()) { // SDK 미지원·차단·키 미도착 시 2줄 텍스트 공유로 폴백 + 눈에 띄는 안내
      copyShareText('✅ 카카오 공유를 쓸 수 없어 텍스트 문구를 복사했습니다.');
      showShareNote('⚠️ 카카오 공유를 열 수 없어서 자랑 문구를 복사해 뒀어요. 카카오톡 대화창에 붙여넣어 공유해 주세요. (광고 차단·네트워크 환경에서는 카카오 창이 열리지 않을 수 있어요)');
      return;
    }
    try {
      window.Kakao.Share.sendDefault({
        objectType: 'feed',
        content: {
          title: currentShare.title,
          description: currentShare.desc,
          imageUrl: currentShare.imageUrl,
          link: { mobileWebUrl: currentShare.detailUrl, webUrl: currentShare.detailUrl }
        },
        buttons: (currentShare.buttons || [
          { title: '자세히 보기', url: currentShare.detailUrl },
          { title: '나도 뽑기', url: 'https://alpang.gg/calculator/cube/' }
        ]).map(function (b) { return { title: b.title, link: { mobileWebUrl: b.url, webUrl: b.url } }; })
      });
      showShareNote('💬 카카오 공유 창을 열었어요. 창이 보이지 않으면 브라우저 팝업 차단을 해제해 주세요.');
    } catch (e) {
      copyShareText('✅ 카카오 공유에 실패해 텍스트 문구를 복사했습니다.');
      showShareNote('⚠️ 카카오 공유 창을 열지 못했어요. 팝업이 차단된 경우 주소창의 팝업 차단 아이콘에서 이 사이트를 허용해 주세요. 대신 자랑 문구를 복사해 뒀으니 붙여넣어 공유할 수 있어요.');
    }
  }

  // ── v2 카드 이미지 클립보드 복사 (미지원 시 텍스트 공유로 폴백) ──
  function copyCardImage() {
    var card = $('vwCard');
    function fallbackText(reason) {
      copyShareText('✅ ' + reason + ' 텍스트 문구를 복사했습니다.');
      showShareNote('⚠️ ' + reason + ' 텍스트 문구를 복사해 뒀어요. 카톡·디코에 붙여넣어 공유해 주세요.');
    }
    if (!window.html2canvas || !navigator.clipboard || typeof ClipboardItem === 'undefined' || !navigator.clipboard.write) {
      fallbackText('이 브라우저는 이미지 복사를 지원하지 않아'); return;
    }
    window.html2canvas(card, { backgroundColor: '#161B24', scale: 2 }).then(function (canvas) {
      canvas.toBlob(function (blob) {
        if (!blob) { fallbackText('이미지 생성에 실패해'); return; }
        var item = {};
        item['image/png'] = blob;
        navigator.clipboard.write([new ClipboardItem(item)]).then(function () {
          $('vwToast').textContent = '✅ 결과 카드 이미지가 복사되었습니다! 카톡·디코에 붙여넣어 자랑하세요.';
          hideShareNote();
        }).catch(function () { fallbackText('이미지 복사가 막혀'); });
      }, 'image/png');
    }).catch(function () { fallbackText('이미지 생성에 실패해'); });
  }

  function copyShareText(doneMsg) {
    var txt = $('vwShareText').textContent;
    var msg = (typeof doneMsg === 'string' && doneMsg) ? doneMsg : '✅ 카톡·디코 자랑 문구가 복사되었습니다!';
    function done() { $('vwToast').textContent = msg; }
    function fallback() {
      var r = document.createRange();
      r.selectNodeContents($('vwShareText'));
      var sel = window.getSelection();
      sel.removeAllRanges(); sel.addRange(r);
      var okCopy = false;
      try { okCopy = document.execCommand && document.execCommand('copy'); } catch (e) { okCopy = false; }
      $('vwToast').textContent = okCopy ? msg
        : '복사가 지원되지 않습니다. 선택된 문구를 길게 눌러 복사해 주세요.';
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, fallback);
    } else fallback();
  }

  // 큐브 모드 진입 시 코어의 현재 상태·횟수에 맞춰 조작 버튼을 동기화한다.
  // 늦은 결과로 코어만 종료된 경우에도 실행은 잠기고 '새 도전' 경로가 사라지지 않는다.
  function syncCubeUI() {
    $('vwCubeCount').textContent = '누적 소모: ' + core.cubeTries.toLocaleString() + '회';
    if (core.cubeState === 'success' || core.cubeState === 'failed') setCubeButtonsEnded(true);
    else setCubeButtonsEnded(false);
  }

  function activateMode(mode) {
    currentMode = mode;
    jobSeq++; // 모드 전환 시 진행 중이던 직업 결과는 늦은 결과로 무효화
    document.querySelectorAll('.vw-tab').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-mode') === mode);
    });
    $('vwJobView').style.display = mode === 'job' ? '' : 'none';
    $('vwCubeView').style.display = mode === 'cube' ? '' : 'none';
    resetCardUI();
    // 복원된 첫 결과가 있는 모드면 그 카드를 다시 보인다 (현재 도전과 분리된 스냅샷)
    if (mode === 'job' && restoredCards.job) renderJobCard(restoredCards.job);
    if (mode === 'cube' && restoredCards.cube) renderCubeCard(restoredCards.cube);
    if (mode === 'cube') syncCubeUI();
  }

  // 복원: 추첨·누적 증가·자격 재소모 없이, 저장된 원결과로 화면과 코어 상태를 일관되게 맞춘다.
  // 두 모드 모두 있으면 큐브 결과를 먼저 보인다 (위젯이 큐브 페이지에 붙는 구성이라 고정).
  function restoreCards() {
    var cc = core.restoreFirst('cube');
    var cj = core.restoreFirst('job');
    if (cj) {
      var job = null;
      window.VIRAL_FINALS.forEach(function (j) { if (j.id === cj.result.jobId) job = j; });
      if (job) restoredCards.job = { kind: 'job', job: job, isFirst: true, date: cj.date, trials: cj.result.trials, title: C.titleFor(cj.result.trials) };
    }
    if (cc) {
      var t = null;
      C.TARGETS.forEach(function (x) { if (x.id === cc.result.targetId) t = x; });
      if (t) {
        restoredCards.cube = { kind: 'cube', target: t, tries: cc.result.tries,
          expected: C.expected(t.p), probWithin: C.probWithin(t.p, cc.result.tries),
          q90: C.quantile(t.p, 0.9), grade: cc.result.grade, isFirst: true,
          date: cc.date, trials: cc.result.trials, title: C.titleFor(cc.result.trials) };
        // 모드·목표·설명·횟수·코어 종료 상태·버튼을 복원 결과에 동기화
        core.restoreCubeEnded(t.id, cc.result.tries, cc.runId);
        $('vwTargetSelect').value = t.id;
        $('vwTargetDesc').textContent = t.desc;
        $('vwCubeCount').textContent = '누적 소모: ' + cc.result.tries.toLocaleString() + '회';
        setCubeButtonsEnded(true);
        activateMode('cube');
        setStatus('오늘 첫 결과가 복원됐습니다. 이어서 하려면 새 도전을 누르세요.');
        return;
      }
    }
    if (restoredCards.job) { activateMode('job'); setStatus('오늘 첫 결과가 복원됐습니다.'); }
  }

  function init() {
    var sel = $('vwTargetSelect');
    C.TARGETS.forEach(function (t) {
      var o = document.createElement('option');
      o.value = t.id; o.textContent = '🎯 ' + t.name + ' (확률 ' + C.fmtPct(t.p) + ' · 이론 기대 ' + C.fmtExpected(t.p) + ')';
      sel.appendChild(o);
    });
    $('vwTargetDesc').textContent = C.TARGETS[0].desc;
    showSlotsIdle(C.TARGETS[0]);
    if ($('vwHatExamples')) $('vwHatExamples').textContent = C.HAT_RULE_EXAMPLES;
    refreshStorageNote();

    document.querySelectorAll('.vw-tab').forEach(function (btn) {
      btn.addEventListener('click', function () {
        cubeSeq++;
        activateMode(btn.getAttribute('data-mode'));
        setStatus('버튼을 눌러야 운명이 움직입니다.');
        refreshStorageNote();
      });
    });

    sel.addEventListener('change', function () {
      var t = core.setTarget(sel.value);
      if (!t) { // 실행 중에는 목표 변경이 거부된다 — 선택값을 현재 목표로 되돌린다
        sel.value = core.target.id;
        setStatus('진행 중인 도전이 있어 목표를 바꿀 수 없습니다. 도전이 끝난 뒤 바꿔 주세요.');
        return;
      }
      cubeSeq++;
      restoredCards.cube = null; // 목표 변경은 복원 스냅샷도 무효화
      showSlotsIdle(t);
      $('vwTargetDesc').textContent = t.desc;
      $('vwCubeCount').textContent = '누적 소모: 0회';
      setCubeButtonsEnded(false);
      resetCardUI();
      setStatus('목표가 바뀌었습니다. 버튼을 눌러 시작하세요.');
    });

    $('vwJobRoll').addEventListener('click', function () {
      restoredCards.job = null;
      $('vwJobRoll').disabled = true;
      var seq = ++jobSeq;
      core.rollJob(window.VIRAL_FINALS).then(function (card) {
        $('vwJobRoll').disabled = false; // 완료 시 실행 중 상태 해제는 항상 한다
        // 다른 모드로 이동한 뒤 돌아온 늦은 결과는 현재 카드·공유를 덮지 않는다
        if (seq !== jobSeq || currentMode !== 'job') { refreshStorageNote(); return; }
        if (!card || card.status === 'busy') { setStatus('이미 뽑기가 진행 중입니다.'); return; }
        renderJobCard(card);
        setStatus(card.unlockedTitle ? '새 칭호가 열렸습니다: ' + card.unlockedTitle.name : '뽑기가 완료됐습니다.');
        refreshStorageNote();
      }).catch(function () {
        $('vwJobRoll').disabled = false; // 오류 시에도 실행 중 상태는 해제한다
        if (seq === jobSeq && currentMode === 'job') setStatus('일시적인 오류로 뽑기가 중단됐습니다. 다시 눌러 주세요.');
        refreshStorageNote();
      });
    });

    function handleCubeResult(r, seq) {
      if (seq !== cubeSeq || currentMode !== 'cube') return; // 늦은 결과는 현재 화면을 덮지 않는다
      $('vwCubeCount').textContent = '누적 소모: ' + core.cubeTries.toLocaleString() + '회';
      if (r.status === 'success') { renderCubeCard(r.card); setCubeButtonsEnded(true); setStatus('목표 달성! 이 도전은 종료 상태로 고정됐습니다. 다시 하려면 새 도전을 누르세요.'); }
      else if (r.status === 'failed') { resetCardUI(); setCubeButtonsEnded(true); setStatus('제한 횟수(' + C.AUTO_CAP.toLocaleString() + '회) 안에 오지 않았습니다. 이 도전은 실패로 종료됐습니다.'); }
      else if (r.status === 'locked') { syncCubeUI(); setStatus('종료된 도전입니다. 새 도전으로 시작하세요.'); }
      else if (r.status === 'busy') { setStatus('이미 진행 중인 도전이 있습니다.'); }
      else if (r.status === 'stale') { setStatus('조건이 바뀌어 이전 도전 결과는 무효화됐습니다.'); }
      else setStatus(core.cubeTries.toLocaleString() + '회째 도전 중입니다.');
      refreshStorageNote();
    }
    function cubeError() {
      // 거절·오류 후에도 조작이 잠기지 않게 버튼 상태를 코어 상태에 맞춰 풀어 준다
      setCubeButtonsEnded(core.cubeState === 'success' || core.cubeState === 'failed');
      setStatus('일시적인 오류로 중단됐습니다. 새 도전으로 다시 시작할 수 있습니다.');
      refreshStorageNote();
    }
    $('vwCubeOnce').addEventListener('click', function () {
      restoredCards.cube = null;
      var seq = cubeSeq;
      showSlotsRolling();
      core.rollCubeOnce().then(function (r) {
        if (seq === cubeSeq && currentMode === 'cube') {
          if (r.status === 'running') showSlotsRolling();
          else if (r.status !== 'success') showSlotsResult(core.target, false);
        }
        handleCubeResult(r, seq);
      }).catch(cubeError);
    });
    $('vwCubeAuto').addEventListener('click', function () {
      restoredCards.cube = null;
      var seq = cubeSeq;
      showSlotsRolling();
      core.rollCubeAuto().then(function (r) {
        if (seq === cubeSeq && currentMode === 'cube' && r.status === 'failed') showSlotsResult(core.target, false);
        handleCubeResult(r, seq);
      }).catch(cubeError);
    });
    $('vwCubeNew').addEventListener('click', function () {
      if (!core.newCubeRun()) { setStatus('진행 중인 도전이 있어 새 도전을 시작할 수 없습니다.'); return; }
      cubeSeq++;
      restoredCards.cube = null;
      showSlotsIdle(core.target);
      $('vwCubeCount').textContent = '누적 소모: 0회';
      setCubeButtonsEnded(false);
      resetCardUI();
      setStatus('새 도전을 시작합니다. 버튼을 눌러 돌리세요.');
      refreshStorageNote();
    });

    $('vwCopyBtn').addEventListener('click', function () { copyShareText(); });
    $('vwImgBtn').addEventListener('click', copyCardImage);
    $('vwKakaoBtn').addEventListener('click', shareKakaoOrFallback);

    window.addEventListener('storage', function (e) {
      if (e.key && e.key.indexOf('alpang.viral.v1.') === 0) setStatus('다른 탭의 기록이 반영됐습니다.');
    });

    resetCardUI();
    restoreCards();
    if (!restoredCards.cube && !restoredCards.job) setStatus('버튼을 눌러야 운명이 움직입니다.');
    refreshStorageNote();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
