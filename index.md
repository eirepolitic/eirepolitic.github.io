---
layout: default
title: Irish Politics Analytics
---
# Irish Politics Analytics

Short, neutral, 1–2 sentence summary of what this project does.

## Sections
- **[Projects](/projects/)** — documentation and build notes  
- **[Articles](/articles/)** — outputs, findings, and updates

## Latest articles
<ul>
  {% for post in site.posts limit:5 %}
    <li>
      <a href="{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} — {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
