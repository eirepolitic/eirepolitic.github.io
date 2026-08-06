---
layout: default
title: Search
permalink: /search/
---

<section class="search-page">
  <p class="home-eyebrow">Knowledge base</p>
  <h1>Search documentation</h1>
  <p class="search-intro">Search titles, summaries, repositories, technologies, tags, and document text.</p>

  <form class="search-form" role="search" onsubmit="return false;">
    <label for="search-input">Search terms</label>
    <div class="search-control">
      <input id="search-input" type="search" autocomplete="off" placeholder="Example: S3 pipeline Athena" />
      <button id="search-clear" type="button">Clear</button>
    </div>
  </form>

  <p id="search-status" class="search-status" aria-live="polite">Loading search index…</p>
  <ol id="search-results" class="search-results"></ol>
</section>

<script src="{{ '/assets/js/search.js?v=' | append: site.github.build_revision | relative_url }}" defer></script>
