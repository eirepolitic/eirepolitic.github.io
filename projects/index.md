---
layout: page
title: Documentation
permalink: /projects/
---
**DEBUG MARKER: projects/index.md is rendering**


## Pipelines

<ul>
{% for page in site.pages %}
  {% if page.path contains "projects/pipelines/" and page.title %}
    <li>
      <a href="{{ page.url }}">{{ page.title }}</a>
    </li>
  {% endif %}
{% endfor %}
</ul>

---

## Schemas

<ul>
{% for page in site.pages %}
  {% if page.path contains "projects/schemas/" and page.title %}
    <li>
      <a href="{{ page.url }}">{{ page.title }}</a>
    </li>
  {% endfor %}
</ul>
