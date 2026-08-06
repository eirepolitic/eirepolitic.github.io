---
layout: page
title: Documentation
permalink: /projects/
---

## Archive
<ul>
{% for p in site.pages %}
  {% if p.path contains "projects/pipelines/" and p.title %}
    <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

---

## High Director
<ul>
{% for p in site.pages %}
  {% if p.path contains "projects/high-director/" and p.title %}
    <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>

---

## Schemas
<ul>
{% for p in site.pages %}
  {% if p.path contains "projects/schemas/" and p.title %}
    <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
