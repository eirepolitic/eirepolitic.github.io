---
layout: default
title: Home
---

<section class="home-hero">
  <p class="home-eyebrow">Eire Politic Knowledge Base</p>
  <h1>Technical documentation for repositories, systems, data, and development work.</h1>
  <p>This site is the working reference for Eire Politic projects and High Director-assisted development. It records implementation details, operating procedures, architecture decisions, and historical work.</p>
  <div class="home-actions">
    <a class="button-primary" href="{{ '/docs/' | relative_url }}">Browse documentation</a>
    <a class="button-secondary" href="{{ '/docs/high-director/' | relative_url }}">High Director</a>
  </div>
</section>

<section class="home-section">
  <div class="home-section-heading">
    <div>
      <p class="home-eyebrow">Knowledge base</p>
      <h2>Documentation sections</h2>
    </div>
    <a href="{{ '/docs/' | relative_url }}">View all</a>
  </div>

  <div class="home-card-grid">
    {% assign sections = site.data.docs_sections | sort: 'order' %}
    {% for section in sections %}
      {% assign section_docs = site.docs | where: 'section', section.id %}
      <a class="home-card" href="{{ '/docs/' | append: section.id | append: '/' | relative_url }}">
        <h3>{{ section.title }}</h3>
        <p>{{ section.description }}</p>
        <span>{{ section_docs.size }} document{% unless section_docs.size == 1 %}s{% endunless %}</span>
      </a>
    {% endfor %}
  </div>
</section>

<section class="home-section home-two-column">
  <div>
    <div class="home-section-heading">
      <div>
        <p class="home-eyebrow">Recent work</p>
        <h2>Recently updated</h2>
      </div>
    </div>

    {% assign recent_docs = site.docs | where_exp: 'doc', "doc.visibility != 'private'" | sort: 'updated' | reverse %}
    <ul class="home-recent-list">
      {% for doc in recent_docs limit: 6 %}
        <li>
          <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
          <span>{{ doc.updated | date: '%Y-%m-%d' }}{% if doc.status %} · {{ doc.status }}{% endif %}</span>
        </li>
      {% endfor %}
    </ul>
  </div>

  <aside class="home-reference-panel">
    <p class="home-eyebrow">Development continuity</p>
    <h2>High Director</h2>
    <p>Agent operating guidance, build plans, standards, and the context required to continue development safely across chats.</p>
    <a href="{{ '/docs/high-director/' | relative_url }}">Open High Director documentation</a>
  </aside>
</section>

<section class="home-section">
  <div class="home-section-heading">
    <div>
      <p class="home-eyebrow">Public outputs</p>
      <h2>Articles and published content</h2>
    </div>
  </div>
  <div class="home-output-links">
    <a href="{{ '/articles/' | relative_url }}"><strong>Articles</strong><span>Findings, updates, and written outputs.</span></a>
    <a href="{{ '/content/' | relative_url }}"><strong>Content</strong><span>Power BI reports and published media.</span></a>
  </div>
</section>
