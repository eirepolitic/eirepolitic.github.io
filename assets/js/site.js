(() => {
  const body = document.querySelector('.docs-body');
  const toc = document.querySelector('#page-toc');
  if (!body || !toc) return;

  const headings = [...body.querySelectorAll('h2, h3')];
  if (!headings.length) {
    const container = toc.closest('.docs-toc');
    if (container) container.hidden = true;
    return;
  }

  const usedIds = new Set();
  const slugify = (text) => text
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');

  headings.forEach((heading) => {
    let id = heading.id || slugify(heading.textContent || 'section');
    let uniqueId = id || 'section';
    let index = 2;
    while (usedIds.has(uniqueId)) {
      uniqueId = `${id}-${index}`;
      index += 1;
    }
    usedIds.add(uniqueId);
    heading.id = uniqueId;

    const link = document.createElement('a');
    link.href = `#${uniqueId}`;
    link.textContent = heading.textContent || uniqueId;
    if (heading.tagName === 'H3') link.classList.add('toc-h3');
    toc.appendChild(link);
  });
})();
