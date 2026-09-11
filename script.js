/* ONEFLOW landing — interactions */
(function () {
  'use strict';

  /* ---- sticky header ---- */
  var header = document.getElementById('header');
  var onScroll = function () {
    header.classList.toggle('is-stuck', window.scrollY > 12);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- mobile menu ---- */
  var burger = document.getElementById('burger');
  var menu = document.getElementById('mobile-menu');

  var setMenu = function (open) {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    menu.hidden = !open;
  };
  setMenu(false);

  burger.addEventListener('click', function () {
    setMenu(burger.getAttribute('aria-expanded') !== 'true');
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setMenu(false);
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth > 1080) setMenu(false);
  });

  /* ---- reveal on scroll ---- */
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.style.transitionDelay = Math.min(i, 4) * 70 + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---- node wires: drawn from the real port positions ---- */
  var canvas = document.querySelector('.canvas');
  var svg = document.querySelector('.wires');
  var links = [
    ['n-img', 'n-gen'],
    ['n-gen', 'n-size'],
    ['n-size', 'n-o1'],
    ['n-size', 'n-o2'],
    ['n-size', 'n-o3']
  ];

  function drawWires() {
    if (!canvas || !svg) return;
    if (getComputedStyle(svg).display === 'none') return;

    var box = canvas.getBoundingClientRect();
    if (!box.width) return;
    svg.setAttribute('viewBox', '0 0 ' + box.width + ' ' + box.height);

    var d = links.map(function (pair) {
      var from = document.getElementById(pair[0]);
      var to = document.getElementById(pair[1]);
      if (!from || !to) return '';

      var a = from.querySelector('.port--r');
      var b = to.querySelector('.port--l');
      if (!a || !b) return '';

      var ra = a.getBoundingClientRect();
      var rb = b.getBoundingClientRect();
      var x1 = ra.left + ra.width / 2 - box.left;
      var y1 = ra.top + ra.height / 2 - box.top;
      var x2 = rb.left + rb.width / 2 - box.left;
      var y2 = rb.top + rb.height / 2 - box.top;
      var c = Math.max(28, (x2 - x1) * 0.55);

      return '<path d="M' + x1 + ' ' + y1 +
        ' C' + (x1 + c) + ' ' + y1 + ', ' + (x2 - c) + ' ' + y2 + ', ' + x2 + ' ' + y2 + '"/>';
    }).join('');

    svg.innerHTML = d;
  }

  var raf;
  function scheduleDraw() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(drawWires);
  }

  scheduleDraw();
  window.addEventListener('resize', scheduleDraw);
  window.addEventListener('load', scheduleDraw);
  if ('ResizeObserver' in window && canvas) new ResizeObserver(scheduleDraw).observe(canvas);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleDraw);
})();
