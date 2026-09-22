(function(){
  'use strict';
  if (!window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.style.opacity = 1; el.style.transform = 'none'; });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('revealed'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15 });
  var items = document.querySelectorAll('.reveal');
  items.forEach(function (el, i) { el.style.setProperty('--i', i % 6); io.observe(el); });
  var sweepRaf = 0;
  function sweep() {
    sweepRaf = 0;
    var rest = document.querySelectorAll('.reveal:not(.revealed)');
    if (!rest.length) return;
    rest.forEach(function (el) {
      if (el.getBoundingClientRect().bottom < 0) { el.classList.add('revealed'); io.unobserve(el); }
    });
  }
  function onScroll() { if (!sweepRaf) sweepRaf = requestAnimationFrame(sweep); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();