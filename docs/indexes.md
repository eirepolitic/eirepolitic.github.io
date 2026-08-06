---
layout: docs
title: Documentation Indexes
summary: Browse documentation by repository, technology, document type, lifecycle status, or update date.
permalink: /docs/indexes/
---

## Repositories

{% assign repository_groups = site.docs | where_exp: 'doc', "doc.visibility != 'private'" | where_exp: 'doc', 'doc.repository' | group_by: 'repository' | sort: 'name' %}
{% if repository_groups.size > 0 %}
<div class="index-groups">
{% for group in repository_groups %}
  <section>
    <h3>{{ group.name }}</h3>
    <ul>
    {% for doc in group.items %}
      <li><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></li>
    {% endfor %}
    </ul>
  </section>
{% endfor %}
</div>
{% else %}
<p>No repository metadata has been added yet.</p>
{% endif %}

## Technologies

{% assign technology_values = site.docs | map: 'technologies' | join: '|' | split: '|' | uniq | sort %}
<div class="tag-index">
{% for technology in technology_values %}
  {% assign cleaned = technology | strip %}
  {% unless cleaned == '' %}
    <a href="{{ '/search/?q=' | append: cleaned | uri_escape | relative_url }}">{{ cleaned }}</a>
  {% endunless %}
{% endfor %}
</div>

## Document types

{% assign type_groups = site.docs | where_exp: 'doc', "doc.visibility != 'private'" | group_by: 'doc_type' | sort: 'name' %}
<div class="index-groups">
{% for group in type_groups %}
  {% unless group.name == '' %}
  <section>
    <h3>{{ group.name | replace: '-', ' ' | capitalize }}</h3>
    <ul>
    {% for doc in group.items %}
      <li><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></li>
    {% endfor %}
    </ul>
  </section>
  {% endunless %}
{% endfor %}
</div>

## Lifecycle status

{% assign status_groups = site.docs | where_exp: 'doc', "doc.visibility != 'private'" | group_by: 'status' | sort: 'name' %}
<div class="index-groups">
{% for group in status_groups %}
  {% unless group.name == '' %}
  <section>
    <h3><span class="status-badge status-{{ group.name }}">{{ group.name }}</span></h3>
    <ul>
    {% for doc in group.items %}
      <li><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></li>
    {% endfor %}
    </ul>
  </section>
  {% endunless %}
{% endfor %}
</div>

## Recently updated

{% assign recent_docs = site.docs | where_exp: 'doc', "doc.visibility != 'private'" | sort: 'updated' | reverse %}
<ul class="docs-list">
{% for doc in recent_docs limit: 25 %}
  <li>
    <a href="{{ doc.url | relative_url }}">{{ doc.title }}</a>
    {% if doc.summary %}<p>{{ doc.summary }}</p>{% endif %}
    <div class="docs-list-meta">
      {% if doc.section %}<span>{{ doc.section }}</span>{% endif %}
      {% if doc.updated %}<span>Updated {{ doc.updated | date: '%Y-%m-%d' }}</span>{% endif %}
    </div>
  </li>
{% endfor %}
</ul>
