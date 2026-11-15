(function () {
  // Copy buttons on code blocks
  document.querySelectorAll('.code .copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pres = btn.closest('.code').querySelectorAll('pre'), code = '';
      for (var k = 0; k < pres.length; k++) { if (pres[k].offsetParent !== null) { code = pres[k].innerText; break; } }
      var done = function (ok) {
        btn.textContent = ok ? '복사됨' : '복사 실패';
        btn.dataset.state = ok ? 'done' : '';
        setTimeout(function () { btn.textContent = '복사'; btn.dataset.state = ''; }, 1600);
      };
      try {
        navigator.clipboard.writeText(code).then(function () { done(true); }, function () { done(false); });
      } catch (e) { done(false); }
    });
  });

  // ---- paged site: one part per page, addressed by #part-N (or #sN for a subheading) ----
  var HOME = 'part-0';
  var BASE_TITLE = document.title;
  var sections = Array.prototype.slice.call(document.querySelectorAll('section.part'));
  var byId = {};
  sections.forEach(function (s) { byId[s.id] = s; });
  var owner = {};
  Array.prototype.forEach.call(document.querySelectorAll('.prose h3'), function (h) {
    var s = h.closest('section.part');
    if (s) owner[h.id] = s.id;
  });
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.sidebar .toc a, .sidebar .rail-list a'));
  var lists = Array.prototype.slice.call(document.querySelectorAll('.otp-list'));

  var currentKey = null;

  // Folder-tree menu: parts are folders, concepts are files. Open/closed state is remembered.
  var treeState = { parts: [], groupsClosed: [] };
  try { var ts = JSON.parse(localStorage.getItem('treeState') || 'null'); if (ts && ts.parts) treeState = ts; } catch (e) { /* ignore */ }
  var saveTree = function () { try { localStorage.setItem('treeState', JSON.stringify(treeState)); } catch (e) { /* ignore */ } };
  var groupName = function (g) { var h = g.querySelector('.toc-head span'); return h ? h.textContent : ''; };
  var applyTree = function () {
    document.querySelectorAll('.toc .tree-item.has-sub').forEach(function (li) {
      var on = treeState.parts.indexOf(li.dataset.part) !== -1;
      li.classList.toggle('open', on);
      var b = li.querySelector('.tree-btn'); if (b) b.setAttribute('aria-expanded', String(on));
    });
    document.querySelectorAll('.toc-group').forEach(function (g) {
      var on = treeState.groupsClosed.indexOf(groupName(g)) === -1;
      g.classList.toggle('open', on);
      var h = g.querySelector('.toc-head'); if (h) h.setAttribute('aria-expanded', String(on));
    });
  };
  var openPartInTree = function (id) {
    if (treeState.parts.indexOf(id) === -1) treeState.parts.push(id);
    var li = document.querySelector('.toc .tree-item[data-part="' + id + '"]');
    var g = li && li.closest('.toc-group');
    if (g) { var n = groupName(g), k = treeState.groupsClosed.indexOf(n); if (k !== -1) treeState.groupsClosed.splice(k, 1); }
    saveTree(); applyTree();
  };
  var twUser = function (e) {
    var t = e.target; if (!t.closest) return;
    var inp = t.closest('.twolab .tw-input'); if (!inp) return;
    var f = inp.closest('.twolab'); f._user = true; stop(f);
    if (e.type === 'input') twSet(f, inp.value, 'view', true);
  };
  document.addEventListener('focusin', twUser);
  document.addEventListener('input', twUser);
  document.addEventListener('click', function (e) {
    var tb = e.target.closest && e.target.closest('.tree-btn');
    if (tb && tb.closest('.tree-item')) {
      var id = tb.closest('.tree-item').dataset.part, k = treeState.parts.indexOf(id);
      if (k === -1) treeState.parts.push(id); else treeState.parts.splice(k, 1);
      saveTree(); applyTree(); return;
    }
    var gh = e.target.closest && e.target.closest('.toc-head');
    if (gh) {
      var n = groupName(gh.closest('.toc-group')), k2 = treeState.groupsClosed.indexOf(n);
      if (k2 === -1) treeState.groupsClosed.push(n); else treeState.groupsClosed.splice(k2, 1);
      saveTree(); applyTree();
    }
  });

  var jumpTop = function (y) {
    try { window.scrollTo({ top: y, left: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, y); }
  };

  var activate = function (id, conceptHash) {
    var key = id + '|' + (conceptHash || '');
    if (key === currentKey) return false;
    currentKey = key;
    var sec = byId[id];
    sections.forEach(function (s) { s.classList.toggle('active', s.id === id); });
    sec.classList.toggle('show-concept', !!conceptHash);
    Array.prototype.forEach.call(sec.querySelectorAll('.concept'), function (c) {
      c.classList.toggle('active', !!conceptHash && c.id === 'c-' + conceptHash);
    });
    document.documentElement.classList.toggle('sub-page', id !== HOME);
    openPartInTree(id);
    var target = '#' + (conceptHash || id);
    var curLink = null;
    navLinks.forEach(function (a) {
      var href = a.getAttribute('href');
      var isSub = !!a.closest('.toc-sub');
      var on = isSub ? href === target : href === '#' + id;
      if (on) { a.setAttribute('aria-current', isSub ? 'page' : 'true'); if (a.closest('.sidebar .toc')) curLink = a; }
      else a.removeAttribute('aria-current');
    });
    var keepVisible = function () {
      if (!curLink) return;
      var box = curLink.closest('.side-inner');
      if (!box) return;
      var r = curLink.getBoundingClientRect(), b = box.getBoundingClientRect();
      if (r.top < b.top + 40 || r.bottom > b.bottom - 40) box.scrollTop += r.top - b.top - b.height / 2;
    };
    setTimeout(keepVisible, 280);
    lists.forEach(function (ul) { ul.hidden = ul.dataset.sec !== id; });
    document.querySelectorAll('.otp-list a').forEach(function (a) {
      if (conceptHash && a.getAttribute('href') === '#' + conceptHash) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
    var h2 = sec.querySelector('h2');
    var eb = h2 && h2.querySelector('.eyebrow'), tt = h2 && h2.querySelector('.h2t');
    var label = tt ? (eb ? eb.textContent + ' · ' : '') + tt.textContent.split(' \u2014 ')[0].trim() : '';
    if (conceptHash) {
      var ch = document.getElementById(conceptHash);
      var cn = ch ? (ch.getAttribute('data-plain') || ch.textContent).split(':')[0].trim() : '';
      document.title = cn + ' \u00b7 ' + label + ' \u00b7 ' + BASE_TITLE;
    } else {
      document.title = id === HOME || !label ? BASE_TITLE : label + ' \u00b7 ' + BASE_TITLE;
    }
    if (window.__closeMenu) window.__closeMenu();
    var mc = document.querySelector('.m-cur');
    if (mc) { var tt2 = document.title, sfx = ' \u00b7 ' + BASE_TITLE; mc.textContent = tt2.slice(-sfx.length) === sfx ? tt2.slice(0, -sfx.length) : tt2; }
    return true;
  };

  var route = function () {
    var hash = '';
    try { hash = decodeURIComponent(location.hash.replace(/^#/, '')); } catch (e) { hash = location.hash.replace(/^#/, ''); }
    var secId = HOME, conceptHash = null;
    if (byId[hash]) secId = hash;
    else if (owner[hash]) { secId = owner[hash]; conceptHash = hash; }
    else if (currentKey && hash !== '') {
      var cur = currentKey.split('|');
      secId = cur[0]; conceptHash = cur[1] || null;
    }
    var changed = activate(secId, conceptHash);
    if (changed || hash === 'main') jumpTop(0);
  };

  // In-page links: handle them ourselves so it works inside a sandboxed frame as well
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href === '#') return;
    e.preventDefault();
    try { if (location.hash !== href) location.hash = href; } catch (err) { /* ignore */ }
    route();
  });
  window.addEventListener('hashchange', route);
  applyTree();
  route();

  // Collapsible left menu (folds into a narrow rail)
  (function () {
    var root = document.documentElement;
    var btns = Array.prototype.slice.call(document.querySelectorAll('.side-toggle'));
    function set(collapsed, focusTarget) {
      root.classList.toggle('side-collapsed', collapsed);
      btns.forEach(function (b) { b.setAttribute('aria-expanded', String(b.closest('.rail') ? collapsed : !collapsed)); });
      try { localStorage.setItem('sideCollapsed', collapsed ? '1' : '0'); } catch (e) { /* ignore */ }
      if (focusTarget) focusTarget.focus();
    }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var inRail = !!b.closest('.rail');
        var other = btns.filter(function (x) { return !!x.closest('.rail') !== inRail; })[0];
        set(!inRail, null);
        setTimeout(function () { if (other) other.focus(); }, 300);
      });
    });
  })();

  // Quiz gates: solve the questions one at a time to open the "다음 단계" content
  (function () {
    var KEY = 'unlockedGates';
    function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
    function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* ignore */ } }
    var done = load();
    function idOf(gate) { var s = gate.querySelector('summary'); return s ? s.textContent.replace(/\s+/g, ' ').trim() : ''; }
    function finish(gate, quiz, remember, msg) {
      gate.classList.add('unlocked');
      Array.prototype.forEach.call(quiz.querySelectorAll('.q'), function (q) { q.hidden = true; });
      var d = quiz.querySelector('.quiz-done'); d.hidden = false; d.textContent = msg;
      if (remember) { var id = idOf(gate); if (done.indexOf(id) < 0) { done.push(id); save(done); } }
    }
    Array.prototype.forEach.call(document.querySelectorAll('details.gate, details.practice'), function (gate) {
      var quiz = gate.querySelector('.quiz');
      if (!quiz) return;
      var practice = gate.classList.contains('practice');
      var skip = quiz.querySelector('.gate-skip');
      if (skip) skip.addEventListener('click', function () { finish(gate, quiz, true, '\uc544\ub798 \ub0b4\uc6a9\uc774 \uc5f4\ub838\uc5b4\uc694.'); });
      if (!practice && done.indexOf(idOf(gate)) >= 0) { finish(gate, quiz, false, '이미 푼 문제예요. 내용이 열려 있어요.'); return; }
      Array.prototype.forEach.call(quiz.querySelectorAll('.q'), function (q) {
        var btn = q.querySelector('.quiz-check'), res = q.querySelector('.quiz-result'), hint = q.querySelector('.q-hint');
        var solved = false;
        q.addEventListener('change', function () { q.classList.remove('ok', 'bad'); hint.hidden = true; res.textContent = ''; });
        btn.addEventListener('click', function () {
          if (solved) {
            var next = q.nextElementSibling;
            q.hidden = true;
            if (next && next.classList.contains('q')) { next.hidden = false; try { next.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); } catch (e) { /* ignore */ } }
            return;
          }
          var pick = q.querySelector('input:checked');
          if (!pick) { res.className = 'quiz-result bad'; res.textContent = '답을 골라 주세요.'; return; }
          if (pick.value !== q.dataset.answer) {
            q.classList.remove('ok'); q.classList.add('bad'); hint.hidden = false;
            res.className = 'quiz-result bad'; res.textContent = '아직 아니에요. 안내를 읽고 다시 골라 보세요.';
            return;
          }
          q.classList.remove('bad'); q.classList.add('ok'); hint.hidden = true;
          Array.prototype.forEach.call(q.querySelectorAll('input'), function (i) { i.disabled = true; });
          solved = true;
          if (btn.dataset.last === '1') { finish(gate, quiz, !practice, practice ? '모두 맞혔어요!' : '모두 맞혔어요! 아래 내용이 열렸어요.'); return; }
          res.className = 'quiz-result ok'; res.textContent = '정답이에요!'; btn.textContent = '다음 문제';
        });
      });
    });
  })();
})();


// Mobile: top bar + slide-in contents drawer
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.m-menu'), drawer = document.getElementById('m-drawer');
  var scrim = document.querySelector('.m-scrim'), closeBtn = document.querySelector('.m-close');
  if (!btn || !drawer) return;
  var isOpen = function () { return root.classList.contains('m-open'); };
  var setOpen = function (on) {
    root.classList.toggle('m-open', on);
    document.body.classList.toggle('m-lock', on);
    btn.setAttribute('aria-expanded', String(on));
    drawer.setAttribute('aria-hidden', String(!on));
    if (on) {
      var cur = drawer.querySelector('a[aria-current]');
      if (cur) { try { cur.scrollIntoView({ block: 'center' }); } catch (e) { /* ignore */ } }
      closeBtn.focus({ preventScroll: true });
    } else if (document.activeElement && drawer.contains(document.activeElement)) { btn.focus({ preventScroll: true }); }
  };
  window.__closeMenu = function () { if (isOpen()) setOpen(false); };
  btn.addEventListener('click', function () { setOpen(!isOpen()); });
  closeBtn.addEventListener('click', function () { setOpen(false); });
  scrim.addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && isOpen()) setOpen(false); });
  drawer.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a[href]'); if (a) setOpen(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1023 && isOpen()) setOpen(false); });
})();

/* ---- figures: reveal on scroll, auto-playing demos that stop when the reader interacts ---- */
(function () {
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var q = function (el, sel) { return el.querySelector(sel); };

  // flex lab ------------------------------------------------------------
  var FLEX_STATES = [['HBox', 'Start', 'Stretch'], ['HBox', 'Center', 'Center'], ['HBox', 'End', 'End'],
    ['HBox', 'SpaceBetween', 'Center'], ['HBox', 'SpaceAround', 'Baseline'], ['VBox', 'Start', 'Stretch'],
    ['VBox', 'Center', 'Center'], ['VBox', 'SpaceBetween', 'Start']];
  var pressed = function (lab, k) { return q(lab, '.seg[data-k="' + k + '"] button[aria-pressed="true"]'); };
  var flexApply = function (lab) {
    var d = pressed(lab, 'dir'), j = pressed(lab, 'j'), a = pressed(lab, 'a'), st = q(lab, '.fl-stage');
    var kids = Array.prototype.slice.call(st.children);
    var before = kids.map(function (k) { return k.getBoundingClientRect(); });
    st.style.flexDirection = d.dataset.css; st.style.justifyContent = j.dataset.css; st.style.alignItems = a.dataset.css;
    st.dataset.col = d.dataset.css === 'column' ? '1' : '0';
    q(lab, '.fl-tag').textContent = d.textContent; q(lab, '.fl-j').textContent = j.textContent; q(lab, '.fl-a').textContent = a.textContent;
    if (reduce || !st.animate) return;
    kids.forEach(function (k, n) {
      var r = k.getBoundingClientRect(), dx = before[n].left - r.left, dy = before[n].top - r.top;
      if (dx || dy) k.animate([{ transform: 'translate(' + dx + 'px,' + dy + 'px)' }, { transform: 'none' }], { duration: 380, easing: 'ease' });
    });
  };
  var flexSet = function (lab, vals) {
    ['dir', 'j', 'a'].forEach(function (k, n) {
      Array.prototype.forEach.call(lab.querySelectorAll('.seg[data-k="' + k + '"] button'), function (b) {
        b.setAttribute('aria-pressed', String(b.textContent === vals[n]));
      });
    });
    flexApply(lab);
  };

  // path lab ------------------------------------------------------------
  var pathSelect = function (lab, nb) {
    Array.prototype.forEach.call(lab.querySelectorAll('.is-sel'), function (x) { x.classList.remove('is-sel'); });
    Array.prototype.forEach.call(lab.querySelectorAll('.on-path'), function (x) { x.classList.remove('on-path'); });
    nb.classList.add('is-sel');
    for (var li = nb.closest('li'); li; li = li.parentNode.closest && li.parentNode.closest('li')) li.classList.add('on-path');
    q(lab, '.pl-o-bind').textContent = '{' + nb.dataset.bind + '}';
    q(lab, '.pl-o-js').textContent = nb.dataset.js;
    q(lab, '.pl-o-val').textContent = nb.dataset.val;
  };

  // stepper -------------------------------------------------------------
  var stepShow = function (f) {
    var n = f.dataset.step;
    Array.prototype.forEach.call(f.querySelectorAll('[data-steps]'), function (el) {
      el.classList.toggle('is-on', el.dataset.steps.split(',').indexOf(n) !== -1);
    });
  };

  // two-way binding lab + template copy lab -------------------------------------
  var TW_STATES = [['ABAP', 'view'], ['SAPUI5', 'model']];
  var twSet = function (f, val, from, keepInput) {
    if (!keepInput) q(f, '.tw-input').value = val;
    Array.prototype.forEach.call(f.querySelectorAll('.tw-val, .tw-text'), function (t) { t.textContent = val; });
    f.dataset.from = from;
    f.classList.remove('tw-flash'); void f.offsetWidth; f.classList.add('tw-flash');
  };
  var tlSet = function (f, n) {
    f.dataset.n = String(n);
    Array.prototype.forEach.call(f.querySelectorAll('[data-i]'), function (el) { el.classList.toggle('is-on', parseInt(el.dataset.i, 10) <= n); });
    Array.prototype.forEach.call(f.querySelectorAll('.tl-n'), function (b) { b.textContent = String(n); });
  };

  var FT_STATES = [['all', 'o'], ['CL303', 'o'], ['CL303', 'a'], ['CL303', 'd'], ['all', 'd'], ['CL301', 'a']];
  var ftApply = function (f, fv, sv) {
    f.dataset.f = fv; f.dataset.s = sv;
    Array.prototype.forEach.call(f.querySelectorAll('.seg'), function (sg) {
      var cur = sg.dataset.k === 'f' ? fv : sv;
      Array.prototype.forEach.call(sg.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === cur)); });
    });
    var n = 0;
    Array.prototype.forEach.call(f.querySelectorAll('.ft-row'), function (r) {
      var on = fv === 'all' || r.dataset.c === fv; if (on) n++;
      r.classList.toggle('is-on', on); r.style.order = r.dataset[sv];
    });
    Array.prototype.forEach.call(f.querySelectorAll('.ft-c'), function (c) { c.classList.toggle('is-on', c.dataset.key === 'f:' + fv || c.dataset.key === 's:' + sv); });
    q(f, '.ft-n').textContent = String(n);
  };

  // auto-play lifecycle ---------------------------------------------------
  /* no auto-play: steppers follow the scroll, labs wait for the reader */
  var start = function () {};
  var stop = function (el) { clearTimeout(el._t); clearInterval(el._t); el._t = null; };

  var figs = document.querySelectorAll('svg.diagram-svg.anim');
  Array.prototype.forEach.call(document.querySelectorAll('.stepper'), stepShow);

  /* scroll-driven steppers: the figure sticks to the screen and each stretch of scrolling moves one step */
  var scrubs = [];
  Array.prototype.forEach.call(document.querySelectorAll('.stepper'), function (f) {
    var max = parseInt(f.dataset.max, 10), wrap = document.createElement('div');
    wrap.className = 'st-scrub'; wrap.style.setProperty('--n', String(max + 1));
    f.parentNode.insertBefore(wrap, f); wrap.appendChild(f); f.classList.add('scrub');
    var foot = f.querySelector('.st-foot'), bar = document.createElement('div');
    bar.className = 'st-prog'; bar.innerHTML = '<span></span>';
    if (foot) foot.appendChild(bar);
    f.dataset.step = '0'; stepShow(f);
    scrubs.push({ wrap: wrap, f: f, max: max, bar: bar.firstChild });
  });
  var scrubTick = false;
  var scrubUpdate = function () {
    scrubTick = false;
    var vh = window.innerHeight;
    scrubs.forEach(function (s) {
      if (!s.wrap.offsetParent) return;
      var minTop = window.innerWidth < 1024 ? 64 : 12;
      s.f.style.top = Math.max(minTop, Math.round((vh - s.f.offsetHeight) / 2)) + 'px';
      var r = s.wrap.getBoundingClientRect(), dist = s.wrap.offsetHeight - vh;
      if (dist <= 0) return;
      var p = Math.min(1, Math.max(0, -r.top / dist)), n = Math.min(s.max, Math.floor(p * (s.max + 1)));
      if (String(n) !== s.f.dataset.step) { s.f.dataset.step = String(n); stepShow(s.f); }
      s.bar.style.width = (p * 100).toFixed(1) + '%';
    });
  };
  var scrubReq = function () { if (!scrubTick) { scrubTick = true; requestAnimationFrame(scrubUpdate); } };
  window.addEventListener('scroll', scrubReq, { passive: true });
  window.addEventListener('resize', scrubReq);
  window.addEventListener('hashchange', function () { setTimeout(scrubReq, 0); });
  scrubReq();
  if (reduce || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(figs, function (el) {
      if (el.classList.contains('anim')) el.classList.add('in-view');
      if (el.classList.contains('stepper')) { el.dataset.step = el.dataset.max; stepShow(el); }
    });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target;
        if (el.classList.contains('anim')) { if (en.isIntersecting) el.classList.add('in-view'); return; }
        if (en.isIntersecting) start(el); else stop(el);
      });
    }, { threshold: 0.4 });
    Array.prototype.forEach.call(figs, function (el) { io.observe(el); });
  }

  document.addEventListener('click', function (e) {
    var t = e.target; if (!t.closest) return;
    var rb = t.closest('.stepper .st-run');
    if (rb) { var sf = rb.closest('.stepper'); sf._paused = false; sf.classList.remove('is-paused'); stop(sf); sf.dataset.step = '0'; stepShow(sf); start(sf); return; }
    var pb = t.closest('.stepper .st-pause');
    if (pb) {
      var pf = pb.closest('.stepper');
      if (pf._paused) { pf._paused = false; pf.classList.remove('is-paused'); start(pf); }
      else { pf._paused = true; pf.classList.add('is-paused'); stop(pf); }
      return;
    }
    var sb = t.closest('.flexlab .seg button');
    if (sb) {
      var lab = sb.closest('.flexlab'); lab._user = true; stop(lab);
      Array.prototype.forEach.call(sb.parentNode.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', String(x === sb)); });
      flexApply(lab); return;
    }
    var tb = t.closest('.twolab .tw-set');
    if (tb) { var tf = tb.closest('.twolab'); tf._user = true; stop(tf); twSet(tf, 'ABAP', 'model'); return; }
    var tl = t.closest('.tmpllab .tl-add, .tmpllab .tl-del');
    if (tl) {
      var lf = tl.closest('.tmpllab'); lf._user = true; stop(lf);
      var cur = parseInt(lf.dataset.n, 10), mx = parseInt(lf.dataset.max, 10);
      tlSet(lf, tl.classList.contains('tl-add') ? Math.min(mx, cur + 1) : Math.max(0, cur - 1)); return;
    }
    var fb = t.closest('.filtlab .seg button');
    if (fb) {
      var ff = fb.closest('.filtlab'); ff._user = true; stop(ff);
      var k = fb.parentNode.dataset.k;
      ftApply(ff, k === 'f' ? fb.dataset.v : ff.dataset.f, k === 's' ? fb.dataset.v : ff.dataset.s); return;
    }
    var nb = t.closest('.pathlab .pl-node');
    if (nb) { var pl = nb.closest('.pathlab'); pl._user = true; stop(pl); pathSelect(pl, nb); }
  });
})();


/* ---- "?" tips: hover, focus or tap shows a small popover ---- */
(function () {
  var openTip = null;
  var place = function (t) {
    var body = t.querySelector('.tip-body'); if (!body) return;
    var r = t.getBoundingClientRect(), w = body.offsetWidth, h = body.offsetHeight;
    var left = Math.max(12, Math.min(window.innerWidth - w - 12, r.left + r.width / 2 - w / 2));
    var top = r.top - h - 10; if (top < 60) top = r.bottom + 10;
    body.style.left = left + 'px'; body.style.top = top + 'px';
  };
  var timer = null;
  var show = function (t) { clearTimeout(timer); if (openTip && openTip !== t) openTip.classList.remove('is-open'); t.classList.add('is-open'); openTip = t; place(t); };
  var hide = function () { clearTimeout(timer); if (openTip) { openTip.classList.remove('is-open'); openTip = null; } };
  var hideSoon = function () { clearTimeout(timer); timer = setTimeout(hide, 300); };
  document.addEventListener('mouseover', function (e) { var t = e.target.closest && e.target.closest('.tip'); if (!t) return; if (t.classList.contains('is-open')) clearTimeout(timer); else show(t); });
  document.addEventListener('mouseout', function (e) { var t = e.target.closest && e.target.closest('.tip'); if (t && !(e.relatedTarget && t.contains(e.relatedTarget))) hideSoon(); });
  document.addEventListener('focusin', function (e) { var t = e.target.closest && e.target.closest('.tip'); if (t) show(t); });
  document.addEventListener('focusout', function (e) { var t = e.target.closest && e.target.closest('.tip'); if (t && !(e.relatedTarget && t.contains(e.relatedTarget))) hide(); });
  window.addEventListener('hashchange', hide);
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('.tip');
    if (t) { if (t.classList.contains('is-open') && openTip === t && e.detail > 0 && false) hide(); else show(t); return; }
    hide();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
  window.addEventListener('scroll', hide, { passive: true });
})();


/* ---- ERD lab: place tables, drag them, connect with 1:1 / 1:N / N:M lines ---- */
(function () {
  var NS = 'http://www.w3.org/2000/svg', BW = 130, SLOT = { ZCLASS: 14, ZSTUDENT: 214, ZENROLL: 414, ZSUBJECT: 616 };
  var el = function (name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n); return n;
  };
  var labs = [];
  function fmt(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k] == null ? '' : o[k]; }); }
  function setup(fig) {
    if (fig._erd) return fig._erd;
    var data = JSON.parse(fig.querySelector('.erd-json').textContent);
    var S = { fig: fig, d: data, svg: fig.querySelector('.erd-svg'), msg: fig.querySelector('.erd-msg'), tabs: {}, lines: [], pick: null };
    S.gl = el('g', {}, S.svg); S.gt = el('g', {}, S.svg);
    fig._erd = S; labs.push(S); say(S, data.m.start); return S;
  }
  function say(S, t, bad) { S.msg.textContent = t; S.msg.className = 'erd-msg' + (bad ? ' is-bad' : ''); }
  function height(S, k) { return 32 + S.d.tables[k].f.length * 22 + 6; }
  function addTable(S, k, x, y) {
    if (S.tabs[k]) return;
    var t = S.d.tables[k], h = height(S, k), g = el('g', { 'class': 'erd-t', transform: 'translate(' + x + ',' + y + ')', 'data-t': k }, S.gt);
    el('rect', { width: BW, height: h, rx: 8, 'class': 'erd-box' }, g);
    el('rect', { width: BW, height: 28, rx: 8, 'class': 'erd-head' }, g);
    el('rect', { y: 18, width: BW, height: 10, 'class': 'erd-head' }, g);
    var a = el('text', { x: 10, y: 19, 'class': 'erd-name' }, g); a.textContent = k;
    var b = el('text', { x: BW - 10, y: 19, 'class': 'erd-ko', 'text-anchor': 'end' }, g); b.textContent = t.ko;
    t.f.forEach(function (f, i) {
      var yy = 32 + i * 22;
      if (i) el('line', { x1: 0, x2: BW, y1: yy, y2: yy, 'class': 'erd-sep' }, g);
      var n = el('text', { x: 10, y: yy + 15, 'class': 'erd-field' + (f[1].indexOf('키') === 0 || f[1] === '키·외래키' ? ' is-key' : '') }, g); n.textContent = f[0];
      if (f[1]) { var m = el('text', { x: BW - 10, y: yy + 15, 'class': 'erd-badge', 'text-anchor': 'end' }, g); m.textContent = f[1]; }
    });
    S.tabs[k] = { g: g, x: x, y: y, w: BW, h: h };
    S.fig.querySelector('.erd-add[data-t="' + k + '"]').setAttribute('aria-pressed', 'true');
  }
  function removeTable(S, k) {
    var t = S.tabs[k]; if (!t) return;
    t.g.remove(); delete S.tabs[k];
    S.lines = S.lines.filter(function (l) { return l.a !== k && l.b !== k; });
    if (S.pick === k) S.pick = null;
    S.fig.querySelector('.erd-add[data-t="' + k + '"]').setAttribute('aria-pressed', 'false');
    draw(S); mark(S);
  }
  function mark(S) { for (var k in S.tabs) S.tabs[k].g.classList.toggle('is-pick', S.pick === k); }
  function anchors(A, B) {
    var ac = [A.x + A.w / 2, A.y + A.h / 2], bc = [B.x + B.w / 2, B.y + B.h / 2], dx = bc[0] - ac[0], dy = bc[1] - ac[1];
    if (Math.abs(dx) * 0.55 >= Math.abs(dy) || (A.x + A.w + 8 < B.x) || (B.x + B.w + 8 < A.x)) {
      return dx >= 0 ? [[A.x + A.w, ac[1]], [B.x, bc[1]]] : [[A.x, ac[1]], [B.x + B.w, bc[1]]];
    }
    return dy >= 0 ? [[ac[0], A.y + A.h], [bc[0], B.y]] : [[ac[0], A.y], [bc[0], B.y + B.h]];
  }
  function ends(parent, p, q, kind, cls) {
    var dx = q[0] - p[0], dy = q[1] - p[1], L = Math.sqrt(dx * dx + dy * dy) || 1, ux = dx / L, uy = dy / L, px = -uy, py = ux;
    if (kind === 'N') {
      var c = [p[0] + ux * 16, p[1] + uy * 16];
      [-8, 0, 8].forEach(function (o) { el('line', { x1: c[0], y1: c[1], x2: p[0] + px * o, y2: p[1] + py * o, 'class': cls }, parent); });
    } else {
      var c1 = [p[0] + ux * 12, p[1] + uy * 12];
      el('line', { x1: c1[0] + px * 8, y1: c1[1] + py * 8, x2: c1[0] - px * 8, y2: c1[1] - py * 8, 'class': cls }, parent);
    }
    var t = el('text', { x: p[0] + ux * 26 + px * 13, y: p[1] + uy * 26 + py * 13 + 4, 'class': 'erd-card', 'text-anchor': 'middle' }, parent);
    t.textContent = kind;
  }
  function draw(S) {
    while (S.gl.firstChild) S.gl.removeChild(S.gl.firstChild);
    S.lines.forEach(function (l, i) {
      var A = S.tabs[l.a], B = S.tabs[l.b]; if (!A || !B) return;
      var pr = anchors(A, B), p = pr[0], q = pr[1], cls = 'erd-line' + (l.type === 'NM' ? ' is-nm' : ''), g = el('g', { 'class': 'erd-l' }, S.gl);
      el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], 'class': cls }, g);
      ends(g, p, q, l.type === 'NM' ? 'N' : '1', cls);
      ends(g, q, p, l.type === '11' ? '1' : 'N', cls);
      var h = el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], 'class': 'erd-hit', 'data-i': i }, g);
      var ti = el('title', {}, h); ti.textContent = l.a + ' - ' + l.b;
    });
  }
  function move(S, k, x, y) {
    var t = S.tabs[k]; t.x = Math.max(0, Math.min(760 - t.w, x)); t.y = Math.max(0, Math.min(240 - t.h, y));
    t.g.setAttribute('transform', 'translate(' + t.x + ',' + t.y + ')'); draw(S);
  }
  function same(l, a, b, ty) { return l.type === ty && ((l.a === a && l.b === b) || (ty !== '1N' && l.a === b && l.b === a)); }
  function connect(S, a, b) {
    var ty = S.fig.dataset.rel;
    if (S.lines.some(function (l) { return same(l, a, b, ty); })) { say(S, S.d.m.same, true); return; }
    S.lines.push({ a: a, b: b, type: ty }); draw(S); say(S, fmt(S.d.m.made, { a: a, b: b }));
  }
  function check(S) {
    var m = S.d.m, T = S.d.tables, out = [], bad = false, miss = [];
    S.d.order.forEach(function (k) { if (!S.tabs[k]) miss.push(k); });
    if (miss.length) { say(S, fmt(m.notable, { t: miss.join(', ') }), true); return; }
    var used = {};
    S.d.expect.forEach(function (e) {
      var one = e[0], many = e[1], info = { one: one, many: many, oko: T[one].ko, mko: T[many].ko }, ok = false, rev = false, kind = false;
      S.lines.forEach(function (l, i) {
        if (l.type === '1N' && l.a === one && l.b === many) { ok = true; used[i] = 1; }
        else if (l.type === '1N' && l.a === many && l.b === one) { rev = true; used[i] = 1; }
        else if ((l.a === one && l.b === many) || (l.a === many && l.b === one)) { kind = true; used[i] = 1; }
      });
      if (ok) out.push('✓ ' + fmt(m.ok, info));
      else if (rev) { out.push('✗ ' + fmt(m.rev, info)); bad = true; }
      else if (kind) { out.push('✗ ' + fmt(m.kind, info)); bad = true; }
      else { out.push('· ' + fmt(m.todo, info)); bad = true; }
    });
    var nm = S.lines.some(function (l) { return (l.a === 'ZSTUDENT' && l.b === 'ZSUBJECT') || (l.a === 'ZSUBJECT' && l.b === 'ZSTUDENT'); });
    if (nm) { out.push('✗ ' + m.nm); bad = true; }
    else if (S.lines.some(function (l, i) { return !used[i]; })) { out.push('✗ ' + m.extra); bad = true; }
    if (!bad) out = [m.done];
    S.msg.innerHTML = ''; S.msg.className = 'erd-msg' + (bad ? '' : ' is-ok');
    out.forEach(function (t) { var p = document.createElement('span'); p.textContent = t; S.msg.appendChild(p); });
  }
  function answer(S) {
    S.lines = []; S.pick = null;
    S.d.order.forEach(function (k) { if (!S.tabs[k]) addTable(S, k, SLOT[k], 50); else move(S, k, SLOT[k], 50); });
    S.lines.push({ a: 'ZCLASS', b: 'ZSTUDENT', type: '1N' }, { a: 'ZSTUDENT', b: 'ZENROLL', type: '1N' }, { a: 'ZSUBJECT', b: 'ZENROLL', type: '1N' });
    draw(S); mark(S); say(S, S.d.m.answer);
  }
  function reset(S) { Object.keys(S.tabs).forEach(function (k) { removeTable(S, k); }); S.lines = []; draw(S); say(S, S.d.m.reset); }
  function clickTable(S, k) {
    if (S.pick === null) { S.pick = k; mark(S); say(S, fmt(S.d.m.pick, { a: k })); return; }
    if (S.pick === k) { S.pick = null; mark(S); say(S, S.d.m.start); return; }
    var a = S.pick; S.pick = null; mark(S); connect(S, a, k);
  }
  var drag = null;
  function svgPoint(S, e) {
    var pt = S.svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    var m = S.svg.getScreenCTM(); return m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 };
  }
  document.addEventListener('pointerdown', function (e) {
    var g = e.target.closest && e.target.closest('.erdlab .erd-t'); if (!g) return;
    var S = setup(g.closest('.erdlab')), k = g.dataset.t, p = svgPoint(S, e), t = S.tabs[k];
    drag = { S: S, k: k, ox: p.x - t.x, oy: p.y - t.y, sx: e.clientX, sy: e.clientY, moved: false };
    try { g.setPointerCapture(e.pointerId); } catch (x) { /* ignore */ }
    e.preventDefault();
  });
  document.addEventListener('pointermove', function (e) {
    if (!drag) return;
    if (!drag.moved && Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy) < 5) return;
    drag.moved = true; var p = svgPoint(drag.S, e); move(drag.S, drag.k, p.x - drag.ox, p.y - drag.oy);
  });
  function endDrag() { if (!drag) return; var d = drag; drag = null; if (!d.moved) clickTable(d.S, d.k); }
  document.addEventListener('pointerup', endDrag);
  document.addEventListener('pointercancel', function () { drag = null; });
  document.addEventListener('click', function (e) {
    var t = e.target; if (!t.closest) return;
    var fig = t.closest('.erdlab'); if (!fig) return;
    var S = setup(fig), b;
    if ((b = t.closest('.erd-add'))) {
      var k = b.dataset.t; if (S.tabs[k]) removeTable(S, k); else { addTable(S, k, SLOT[k], 50); } return;
    }
    if ((b = t.closest('.erd-rels button'))) {
      fig.dataset.rel = b.dataset.rel;
      Array.prototype.forEach.call(b.parentNode.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', String(x === b)); }); return;
    }
    if ((b = t.closest('.erd-hit'))) { S.lines.splice(parseInt(b.dataset.i, 10), 1); draw(S); say(S, S.d.m.start); return; }
    if (t.closest('.erd-check')) { check(S); return; }
    if (t.closest('.erd-answer')) { answer(S); return; }
    if (t.closest('.erd-reset')) { reset(S); return; }
    if (t.closest('.erd-svg') && !t.closest('.erd-t') && S.pick) { S.pick = null; mark(S); say(S, S.d.m.start); }
  });
})();

/* 15부: data round-trip figure follows the scroll */
(function () {
  'use strict';
  var flow = document.getElementById('fb-flow');
  if (!flow) return;
  var N = 7;
  var $ = function (id) { return document.getElementById('fb-' + id); };
  var capItems = flow.querySelectorAll('.fb-cap-item'), dotBtns = flow.querySelectorAll('.fb-dots button'), lbl = flow.querySelector('.fb-lbl');
  var dotBars = flow.querySelectorAll('.fb-dots button span');
  Array.prototype.forEach.call(dotBtns, function (b) {
    b.addEventListener('click', function () {
      var i = parseInt(b.dataset.i, 10), top = flow.getBoundingClientRect().top + window.scrollY, dist = flow.offsetHeight - window.innerHeight;
      window.scrollTo({ top: top + dist * ((i + 0.55) / N), behavior: 'smooth' });
    });
  });
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function set(id, attrs) { var e = $(id); for (var k in attrs) e.setAttribute(k, attrs[k]); }
  function hl(id, on, color) {
    var e = $(id); e.setAttribute('stroke', on ? color : 'var(--line-strong)'); e.setAttribute('stroke-width', on ? 2 : 1);
  }

  var last = -1, svg = $('svg'), narrow = false;
  function render(p) {
    var k = clamp(Math.floor(p * N), 0, N - 1), t = p * N - k;   // current step and progress inside it
    var s = function (i) { return clamp(p * N - i, 0, 1); };       // progress of step i (0 before, 1 after)

    /* captions and progress bars */
    if (k !== last) { for (var i = 0; i < N; i++) capItems[i].classList.toggle('on', i === k); last = k; }
    for (var j = 0; j < N; j++) dotBars[j].style.width = (s(j) * 100) + '%';
    lbl.textContent = (k + 1) + ' / ' + N;

    /* narrow screens: the camera follows the action (left half = browser, right half = SAP server) */
    if (narrow) {
      var pan = ease(seg(s(1), .4, .95)) - ease(seg(s(5), .05, .8));
      svg.setAttribute('viewBox', (8 + pan * 326).toFixed(1) + ' 0 338 380');
    } else svg.setAttribute('viewBox', '0 0 680 380');

    /* 1. cursor moves to the button and clicks */
    var s1 = s(0), mv = ease(seg(s1, .05, .6));
    set('cursor', { opacity: p < 0.02 ? seg(p, 0, .02) : (s1 < 1 ? 1 : 1 - seg(s(1), 0, .3)), transform: 'translate(' + lerp(150, 200, mv) + ',' + lerp(210, 94, mv) + ')' });
    var press = seg(s1, .62, .8);
    set('btn-r', { fill: press > 0 && press < 1 ? 'var(--accent-ink)' : 'var(--accent)' });
    set('ripple', { r: 6 + press * 26, opacity: press > 0 && s(1) < .4 ? (1 - press) * .9 + (press >= 1 ? 0 : 0) : 0 });
    hl('btn-r', k === 0, 'var(--accent-ink)');

    /* 2. controller -> model -> request packet travels right */
    var ctrl = $('c-ctrl').firstElementChild, model = $('c-model').firstElementChild, view = $('c-view').firstElementChild;
    [ctrl, model, view].forEach(function (r) { r.style.stroke = ''; r.style.strokeWidth = ''; r.style.fill = ''; var u = r.parentNode.querySelector('use'); if (u) u.style.color = 'var(--muted)'; });
    function chipOn(r) { r.style.stroke = 'var(--accent)'; r.style.strokeWidth = '2'; r.style.fill = '#f0f9ff'; var u = r.parentNode.querySelector('use'); if (u) u.style.color = 'var(--accent-ink)'; }
    if (k === 1) chipOn(t < .35 ? ctrl : model);
    var go = ease(seg(s(1), .35, .95));
    var reqVis = s(1) > .3 && s(2) < .35;
    var rx = s(1) < .35 ? 226 : lerp(226, 452, go), ry = s(1) < .35 ? 333 : (go < .15 ? lerp(333, 116, go / .15) : 116);
    if (s(2) > 0) { rx = lerp(452, 549, ease(seg(s(2), 0, .3))); ry = lerp(116, 104, ease(seg(s(2), 0, .3))); }
    set('req', { opacity: reqVis ? (s(2) > 0 ? 1 - seg(s(2), .2, .35) : 1) : 0, transform: 'translate(' + rx + ',' + ry + ')' });

    /* 3. ABAP receives and prepares SQL */
    hl('abap-r', k === 2 || k === 3, 'var(--be)');
    var typ = seg(s(2), .35, .95);
    var l1 = 'SELECT * FROM zstudent', l2 = '  INTO TABLE @lt_std.';
    $('abap-l1').textContent = s(2) > 0 ? l1.slice(0, Math.round(l1.length * clamp(typ * 1.6, 0, 1))) : '';
    $('abap-l2').textContent = s(2) > 0 ? l2.slice(0, Math.round(l2.length * clamp(typ * 1.6 - .6, 0, 1))) : '';
    $('abap-ok').textContent = s(2) > .3 ? '요청 받음' : '';

    /* 4. ABAP -> DB, rows light up */
    hl('db-r', k === 3, 'var(--be)');
    set('qpath', { opacity: s(3) > 0 && s(4) < .2 ? 1 : 0, 'stroke-dashoffset': -s(3) * 40 });
    for (var r = 0; r < 3; r++) {
      var lit = seg(s(3), .3 + r * .2, .45 + r * .2);
      set('dr' + r, { fill: lit > 0 ? 'var(--be)' : '#e5e7eb', opacity: lit > 0 ? .35 + .65 * lit : 1 });
    }

    /* 5. rows fly into the internal table */
    hl('itab-r', k === 4, 'var(--be)');
    for (var f = 0; f < 3; f++) {
      var ft = ease(seg(s(4), .1 + f * .22, .45 + f * .22));
      var sx = 479, sy = 254 + f * 13, ex = 587, ey = 238 + f * 18;
      var flying = ft > 0 && ft < 1;
      set('f' + f, { x: lerp(sx, ex, ft), y: lerp(sy, ey, ft) - Math.sin(ft * Math.PI) * 26, opacity: flying ? 1 : 0 });
      set('ir' + f, { opacity: ft >= 1 ? .85 : 0 });
    }

    /* 6. response packet travels back to the model */
    var back = ease(seg(s(5), .05, .75));
    var resVis = s(5) > 0 && s(5) < .95;
    var bx = back < .12 ? lerp(602, 418, back / .12) : (back < .85 ? lerp(418, 262, (back - .12) / .73) : lerp(262, 160, (back - .85) / .15));
    var by = back < .12 ? lerp(302, 290, back / .12) : (back < .85 ? 290 : lerp(290, 333, (back - .85) / .15));
    set('res', { opacity: resVis ? 1 - seg(s(5), .8, .95) : 0, transform: 'translate(' + bx + ',' + by + ')' });
    if (k === 5 && t > .7) chipOn(model);
    $('model-val').textContent = s(5) > .8 ? '3명' : '';

    /* 7. binding updates the table */
    var b7 = s(6);
    set('bind', { opacity: b7 > 0 ? 1 : 0, 'stroke-dashoffset': -b7 * 60 });
    if (k === 6) chipOn(view);
    $('auto').setAttribute('opacity', seg(b7, .5, .7));
    hl('tbl-r', k === 6, 'var(--accent)');
    for (var q = 0; q < 3; q++) {
      var rt = seg(b7, .2 + q * .2, .4 + q * .2);
      set('tr' + q, { opacity: rt, transform: 'translate(' + (1 - rt) * -16 + ',0)' });
    }
    $('tbl-empty').setAttribute('opacity', b7 > .2 ? 0 : 1);
  }

  var ticking = false;
  function update() {
    ticking = false;
    if (!flow.offsetParent) return;
    narrow = svg.parentNode.clientWidth < 560;
    var r = flow.getBoundingClientRect(), dist = flow.offsetHeight - window.innerHeight;
    if (dist > 0) render(clamp(-r.top / dist, 0, .9999));
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  window.addEventListener('hashchange', function () { setTimeout(onScroll, 0); });
  onScroll();
})();

// Diagrams wider than the screen: show a swipe hint and fade the cut edge
(function () {
  var AR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M3 12h18"/></svg>';
  var all = document.querySelectorAll('.diagram-scroll');
  var check = function () {
    Array.prototype.forEach.call(all, function (d) {
      if (!d.offsetParent) return;
      var over = d.scrollWidth > d.clientWidth + 4;
      d.classList.toggle('can-scroll', over);
      d.classList.toggle('at-end', over && d.scrollLeft + d.clientWidth >= d.scrollWidth - 4);
      var h = d.nextElementSibling && d.nextElementSibling.classList.contains('scroll-hint') ? d.nextElementSibling : null;
      if (over && !h) { h = document.createElement('p'); h.className = 'scroll-hint'; h.innerHTML = AR + '옆으로 밀면 나머지가 보여요'; d.parentNode.insertBefore(h, d.nextSibling); }
      if (h) h.hidden = !over;
    });
  };
  Array.prototype.forEach.call(all, function (d) {
    d.addEventListener('scroll', function () { d.classList.toggle('at-end', d.scrollLeft + d.clientWidth >= d.scrollWidth - 4); }, { passive: true });
  });
  window.addEventListener('resize', check);
  window.addEventListener('hashchange', function () { setTimeout(check, 50); });
  document.addEventListener('click', function () { setTimeout(check, 50); });
  check(); setTimeout(check, 400);
})();


// ABAP syntax switch: one click changes every code box in the book, and is remembered
(function () {
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-set-syn]');
    if (!b) return;
    var v = b.getAttribute('data-set-syn'), root = document.documentElement;
    if ((root.dataset.syn || 'new') === v) return;
    var before = b.getBoundingClientRect().top;
    if (v === 'old') root.dataset.syn = 'old'; else delete root.dataset.syn;
    try { localStorage.setItem('abapSyn', v); } catch (err) { /* ignore */ }
    var after = b.getBoundingClientRect().top;
    if (after !== before) window.scrollBy(0, after - before);
  });
})();
