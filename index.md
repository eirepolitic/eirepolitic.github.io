---
layout: default
title: Irish Politics Analytics
---

# Irish Politics Analytics

Portfolio + documentation for my Irish Politics Analytics work.

## Navigation
- [Projects](/projects/)
- Articles below

---

## Articles
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} — {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
