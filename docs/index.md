---
layout: page
title: Documentation
permalink: /docs/
---

# Documentation

{% assign published_docs = site.docs | where_exp: "doc", "doc.visibility != 'private'" | sort: "title" %}

{% if published_docs.size > 0 %}
<ul>
{% for doc in published_docs %}
  <li>
    <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
    {% if doc.summary %}<br><small>{{ doc.summary }}</small>{% endif %}
  </li>
{% endfor %}
</ul>
{% else %}
<p>Documentation migration is in progress. Existing pages remain available under the current Documentation section.</p>
{% endif %}
