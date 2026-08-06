---
layout: docs
title: Documentation
summary: Technical knowledge base for repositories, systems, data, operations, decisions, and High Director-assisted development.
permalink: /docs/
---

<div class="docs-section-grid">
{% assign sections = site.data.docs_sections | sort: 'order' %}
{% for section in sections %}
  {% assign section_docs = site.docs | where: 'section', section.id %}
  <section>
    <h2><a href="{{ '/docs/' | append: section.id | append: '/' | relative_url }}">{{ section.title }}</a></h2>
    <p>{{ section.description }}</p>
    <small>{{ section_docs.size }} document{% unless section_docs.size == 1 %}s{% endunless %}</small>
  </section>
{% endfor %}
</div>
