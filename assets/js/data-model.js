(() => {
  const catalogue = document.querySelector('.data-model-catalogue');
  if (!catalogue) return;

  const wraps = [...catalogue.querySelectorAll('.data-table-wrap')];
  wraps.forEach((wrap, index) => {
    if (wrap.closest('.table-browser')) return;

    const browser = document.createElement('div');
    browser.className = 'table-browser';

    const toolbar = document.createElement('div');
    toolbar.className = 'table-toolbar';

    const hint = document.createElement('span');
    hint.className = 'table-hint';
    hint.textContent = 'Browse columns with ← / → or expand the table.';

    const actions = document.createElement('div');
    actions.className = 'table-toolbar-actions';

    const makeButton = (label, title) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.title = title;
      return button;
    };

    const left = makeButton('←', 'Scroll table left');
    const right = makeButton('→', 'Scroll table right');
    const expand = makeButton('Full width', 'Expand this table to fill the screen');

    const scrollAmount = () => Math.max(280, Math.round(wrap.clientWidth * 0.75));
    left.addEventListener('click', () => wrap.scrollBy({ left: -scrollAmount(), behavior: 'smooth' }));
    right.addEventListener('click', () => wrap.scrollBy({ left: scrollAmount(), behavior: 'smooth' }));

    const setExpanded = (expanded) => {
      browser.classList.toggle('is-expanded', expanded);
      document.body.classList.toggle('table-browser-open', expanded);
      expand.textContent = expanded ? 'Close full width' : 'Full width';
      expand.setAttribute('aria-expanded', String(expanded));
      if (expanded) wrap.focus({ preventScroll: true });
    };

    expand.setAttribute('aria-expanded', 'false');
    expand.addEventListener('click', () => setExpanded(!browser.classList.contains('is-expanded')));

    browser.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && browser.classList.contains('is-expanded')) setExpanded(false);
      if (event.key === 'ArrowLeft' && event.altKey) {
        event.preventDefault();
        wrap.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
      }
      if (event.key === 'ArrowRight' && event.altKey) {
        event.preventDefault();
        wrap.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
      }
    });

    wrap.tabIndex = 0;
    wrap.setAttribute('aria-label', `Scrollable data table ${index + 1}`);
    actions.append(left, right, expand);
    toolbar.append(hint, actions);
    wrap.parentNode.insertBefore(browser, wrap);
    browser.append(toolbar, wrap);
  });
})();
