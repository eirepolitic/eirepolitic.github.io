---
layout: default
title: Irish Politics Analytics
---
## Overview

Eire Politic is a project looking at Irish political data with the aims of creating insightful & informative
content while developing my analytics & pipeline building skills. 

## Sections
- **[Documentation](/projects/)** — documentation and build notes  
- **[Articles](/articles/)** — outputs, findings, and updates

## Latest articles
<ul>
  {% for post in site.posts limit:5 %}
    <li>
      <a href="{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} — {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
