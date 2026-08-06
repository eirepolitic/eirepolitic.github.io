(() => {
  const input = document.querySelector('#search-input');
  const clear = document.querySelector('#search-clear');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  if (!input || !clear || !status || !results) return;

  let documents = [];
  const normalize = (value) => String(value || '').toLowerCase();
  const escapeHtml = (value) => String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const scoreDocument = (doc, terms) => {
    const title = normalize(doc.title);
    const summary = normalize(doc.summary);
    const repository = normalize(doc.repository);
    const metadata = normalize([doc.section, doc.doc_type, doc.status, ...(doc.technologies || []), ...(doc.tags || [])].join(' '));
    const content = normalize(doc.content);
    let score = 0;

    for (const term of terms) {
      if (!title.includes(term) && !summary.includes(term) && !repository.includes(term) && !metadata.includes(term) && !content.includes(term)) return 0;
      if (title.includes(term)) score += 12;
      if (summary.includes(term)) score += 7;
      if (repository.includes(term)) score += 6;
      if (metadata.includes(term)) score += 4;
      if (content.includes(term)) score += 1;
    }
    return score;
  };

  const render = () => {
    const query = input.value.trim();
    const terms = normalize(query).split(/\s+/).filter(Boolean);
    results.innerHTML = '';

    if (!terms.length) {
      status.textContent = `${documents.length} documents indexed. Enter search terms.`;
      return;
    }

    const matches = documents
      .map((doc) => ({ doc, score: scoreDocument(doc, terms) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || String(b.doc.updated).localeCompare(String(a.doc.updated)))
      .slice(0, 50);

    status.textContent = `${matches.length} result${matches.length === 1 ? '' : 's'} for “${query}”.`;
    for (const { doc } of matches) {
      const item = document.createElement('li');
      const technologies = Array.isArray(doc.technologies) ? doc.technologies.slice(0, 4).join(', ') : '';
      item.innerHTML = `
        <a href="${escapeHtml(doc.url)}">${escapeHtml(doc.title)}</a>
        <p>${escapeHtml(doc.summary || 'No summary available.')}</p>
        <div class="search-result-meta">
          ${doc.section ? `<span>${escapeHtml(doc.section)}</span>` : ''}
          ${doc.repository ? `<span>${escapeHtml(doc.repository)}</span>` : ''}
          ${technologies ? `<span>${escapeHtml(technologies)}</span>` : ''}
          ${doc.updated ? `<span>Updated ${escapeHtml(doc.updated)}</span>` : ''}
        </div>`;
      results.appendChild(item);
    }
  };

  fetch('/search-index.json')
    .then((response) => {
      if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      documents = Array.isArray(data) ? data : [];
      status.textContent = `${documents.length} documents indexed. Enter search terms.`;
      const query = new URLSearchParams(window.location.search).get('q');
      if (query) {
        input.value = query;
        render();
      }
    })
    .catch(() => {
      status.textContent = 'Search is temporarily unavailable.';
    });

  input.addEventListener('input', render);
  clear.addEventListener('click', () => {
    input.value = '';
    render();
    input.focus();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && document.activeElement !== input) {
      event.preventDefault();
      input.focus();
    }
    if (event.key === 'Escape' && document.activeElement === input) {
      input.value = '';
      render();
    }
  });
})();
