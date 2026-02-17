---
layout: page
title: Documentation
permalink: /projects/
---
**DEBUG MARKER: projects/index.md is rendering**

## Pipelines
<ul>
{% for p in site.pages %}
  {% if p.path contains "projects/pipelines/" and p.title %}
    <li><a href="{{ p.url }}">{{ p.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

---

## Schemas
<ul>
{% for p in site.pages %}
  {% if p.path contains "projects/schemas/" and p.title %}
    <li><a href="{{ p.url }}">{{ p.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
