(() => {
  'use strict';
  const root = document.documentElement;
  const storageKey = 'mietblick-theme';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const buttons = Array.from(document.querySelectorAll('[data-theme-set]'));
  const parse = value => value === 'light' || value === 'dark' ? value : 'system';
  let preference = parse(root.getAttribute('data-theme'));

  const apply = () => {
    if (preference === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', preference);
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.themeSet === preference)));
    const dark = preference === 'dark' || (preference === 'system' && system.matches);
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#18324A' : '#ffffff');
  };

  buttons.forEach(button => button.addEventListener('click', () => {
    preference = parse(button.dataset.themeSet);
    apply();
    try {
      if (preference === 'system') localStorage.removeItem(storageKey);
      else localStorage.setItem(storageKey, preference);
    } catch { /* The current selection still works when browser storage is unavailable. */ }
  }));
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key !== storageKey && event.key !== null) return;
    preference = parse(event.newValue);
    apply();
  });
  document.querySelectorAll('[data-theme-controls]').forEach(control => { control.hidden = false; });
  apply();
})();
