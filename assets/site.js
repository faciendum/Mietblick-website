(() => {
  'use strict';
  const root = document.documentElement;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionButton = document.querySelector('.motion-toggle');
  let manualPaused = false;
  const updateMotion = () => {
    const paused = manualPaused || reduced.matches;
    root.classList.toggle('motion-paused', paused);
    if (motionButton) {
      motionButton.hidden = false;
      motionButton.setAttribute('aria-pressed', String(paused));
      motionButton.textContent = reduced.matches ? 'Bewegung im System reduziert' : paused ? 'Animationen fortsetzen ▶' : 'Animationen pausieren Ⅱ';
      motionButton.disabled = reduced.matches;
    }
    document.querySelectorAll('[data-parallax]').forEach(el => {
      if (paused) { el.style.removeProperty('--pointer-x'); el.style.removeProperty('--pointer-y'); }
    });
  };
  motionButton?.addEventListener('click', () => { manualPaused = !manualPaused; updateMotion(); });
  reduced.addEventListener('change', updateMotion);
  updateMotion();
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObserver.unobserve(entry.target); }
    }), { threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
    const motionObserver = new IntersectionObserver(entries => entries.forEach(entry => entry.target.classList.toggle('offscreen', !entry.isIntersecting)), { rootMargin: '80px' });
    document.querySelectorAll('.hero-art,.feature-explorer,.closing').forEach(el => motionObserver.observe(el));
    root.classList.add('motion-ready');
  }

  const header = document.querySelector('.site-header');
  const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 12);
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();
  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-nav');
  const closeMenu = () => {
    if (!menuButton || !menu) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Menü öffnen');
    menu.hidden = true;
  };
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(expanded));
    menuButton.setAttribute('aria-label', expanded ? 'Menü schließen' : 'Menü öffnen');
    menu.hidden = !expanded;
  });
  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu && !menu.hidden) { closeMenu(); menuButton.focus(); }
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

  document.querySelectorAll('[data-tabs]').forEach(explorer => {
    const tabs = Array.from(explorer.querySelectorAll('[role="tab"]'));
    const activate = (tab, focus = false) => {
      tabs.forEach(item => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
        const panel = document.getElementById(item.getAttribute('aria-controls'));
        panel.hidden = !selected;
      });
      if (focus) tab.focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
      });
    });
  });

  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('[data-parallax]').forEach(art => {
      art.addEventListener('pointermove', event => {
        if (root.classList.contains('motion-paused')) return;
        const bounds = art.getBoundingClientRect();
        art.style.setProperty('--pointer-x', `${((event.clientX - bounds.left) / bounds.width - .5) * 10}px`);
        art.style.setProperty('--pointer-y', `${((event.clientY - bounds.top) / bounds.height - .5) * 8}px`);
      });
      art.addEventListener('pointerleave', () => {
        art.style.setProperty('--pointer-x', '0px'); art.style.setProperty('--pointer-y', '0px');
      });
    });
  }

  const navLinks = Array.from(document.querySelectorAll('.desktop-nav a'));
  if ('IntersectionObserver' in window && navLinks.length) {
    const sectionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) navLinks.forEach(link => link.classList.toggle('active', link.hash === `#${entry.target.id}`));
    }), { rootMargin: '-15% 0px -60% 0px' });
    navLinks.forEach(link => { const section = document.querySelector(link.hash); if (section) sectionObserver.observe(section); });
  }
})();
