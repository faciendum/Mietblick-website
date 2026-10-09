(() => {
  'use strict';
  const disclosure = document.querySelector('.nav-disclosure');
  const closeDisclosure = () => { if (disclosure) disclosure.open = false; };
  document.addEventListener('click', event => {
    if (disclosure?.open && !disclosure.contains(event.target)) closeDisclosure();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && disclosure?.open) {
      closeDisclosure();
      disclosure.querySelector('summary').focus();
    }
  });
  disclosure?.addEventListener('focusout', () => {
    requestAnimationFrame(() => {
      if (!disclosure.contains(document.activeElement)) closeDisclosure();
    });
  });
  document.querySelectorAll('[data-directory]').forEach(directory => {
    const controls = directory.querySelector('.directory-controls');
    controls.hidden = false;
    const buttons = Array.from(directory.querySelectorAll('[data-filter]'));
    const input = directory.querySelector('[data-directory-search]');
    const cards = Array.from(directory.querySelectorAll('[data-directory-card]'));
    const result = directory.querySelector('.directory-result');
    let selected = 'all';
    const apply = () => {
      const query = input.value.trim().toLocaleLowerCase('de-DE');
      let count = 0;
      cards.forEach(card => {
        const visible = (selected === 'all' || card.dataset.category === selected) && card.dataset.search.includes(query);
        card.hidden = !visible;
        if (visible) { count++; card.classList.add('visible'); }
      });
      directory.querySelectorAll('[data-card-group]').forEach(group => {
        group.hidden = !Array.from(group.querySelectorAll('[data-directory-card]')).some(card => !card.hidden);
      });
      directory.querySelector('.directory-empty').hidden = count !== 0;
      result.textContent = `${count} ${count === 1 ? 'passender Funktionsbereich' : 'passende Funktionsbereiche'} · Mobil findest du weiter unten.`;
    };
    buttons.forEach(button => button.addEventListener('click', () => {
      selected = button.dataset.filter;
      buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      apply();
    }));
    input.addEventListener('input', apply);
    apply();
  });
  const toc = document.querySelector('.article-toc');
  if (toc && 'IntersectionObserver' in window) {
    const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
    const sections = links.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
    const activate = id => links.forEach(link => {
      const active = link.hash === `#${id}`;
      link.classList.toggle('toc-active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) activate(visible[0].target.id);
    }, { rootMargin: '-105px 0px -65% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
    links.forEach(link => link.addEventListener('click', () => activate(link.hash.slice(1))));
  }
  const article = document.querySelector('[data-reading-article]');
  const progress = document.querySelector('.reading-progress span');
  if (article && progress) {
    let scheduled = false;
    const update = () => {
      const bounds = article.getBoundingClientRect();
      const range = Math.max(1, bounds.height - window.innerHeight);
      const fraction = Math.min(1, Math.max(0, -bounds.top / range));
      progress.style.transform = `scaleX(${fraction})`;
      scheduled = false;
    };
    window.addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
  }
})();
