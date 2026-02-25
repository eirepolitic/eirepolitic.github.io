---
layout: default
title: AutoDoc
permalink: /autodoc/
sitemap: false
wide: true
---

<style>
  /* ============================
     TUNABLE VARIABLES (edit here)
     ============================ */
  :root {
    --autodoc-page-max-width: 1400px; /* try: 1200px, 1400px, 1600px */
    --autodoc-iframe-height: 110vh;    /* try: 78vh, 85vh, 92vh */
    --autodoc-iframe-min-height: 1100px; /* try: 720px, 840px, 960px */
  }

  /* Page-scoped "hacker" styling (only affects this page content) */
  .autodoc-shell {
    max-width: var(--autodoc-page-max-width);
    margin: 0 auto;

    background: #050b07;
    border: 1px solid rgba(0, 255, 120, 0.25);
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow:
      0 0 0 1px rgba(0, 255, 120, 0.10),
      0 0 24px rgba(0, 255, 120, 0.10);
    position: relative;
    overflow: hidden;
  }

  /* Subtle scanline effect */
  .autodoc-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      to bottom,
      rgba(0, 255, 120, 0.05),
      rgba(0, 255, 120, 0.05) 1px,
      rgba(0, 0, 0, 0) 3px,
      rgba(0, 0, 0, 0) 6px
    );
    pointer-events: none;
    opacity: 0.35;
  }

  .autodoc-header {
    position: relative;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.75rem;
  }

  .autodoc-title {
    margin: 0;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    letter-spacing: 0.02em;
    color: #3CFF8F;
    text-shadow: 0 0 12px rgba(0, 255, 120, 0.25);
  }

  .autodoc-badge {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.85rem;
    color: rgba(60, 255, 143, 0.85);
    border: 1px solid rgba(0, 255, 120, 0.25);
    border-radius: 999px;
    padding: 0.25rem 0.6rem;
    background: rgba(0, 255, 120, 0.06);
    white-space: nowrap;
  }

  .autodoc-note {
    position: relative;
    margin: 0 0 1rem 0;
    color: rgba(200, 255, 220, 0.85);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    line-height: 1.5;
  }

  .autodoc-wrap {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(0, 255, 120, 0.22);
    background: #000;
  }

  .autodoc-embed {
    width: 100%;
    height: var(--autodoc-iframe-height);
    min-height: var(--autodoc-iframe-min-height);
    border: 0;
    display: block;
  }

  @media (max-width: 768px) {
    .autodoc-shell { padding: 1rem; }
    .autodoc-header { flex-direction: column; align-items: flex-start; }

    /* Keep mobile sane while still using your variables */
    .autodoc-embed {
      height: min(90vh, var(--autodoc-iframe-height));
      min-height: 760px;
    }
  }
</style>

<div class="autodoc-shell">
  <div class="autodoc-header">
    <h2 class="autodoc-title">AutoDoc Console</h2>
    <span class="autodoc-badge">PUBLIC · UNLINKED</span>
  </div>

  <p class="autodoc-note">
    Embedded Appsmith app below. If it fails to load, check browser tracking protection / third-party cookies.
  </p>

  <div class="autodoc-wrap">
    <iframe
      class="autodoc-embed"
      title="AutoDoc (Appsmith)"
      src="https://app.appsmith.com/app/autodoc/submit-69962dc692e9da4ea5cd1e7a"
      loading="lazy"
      allow="clipboard-read; clipboard-write; fullscreen"
      referrerpolicy="no-referrer-when-downgrade"
      allowfullscreen="true">
    </iframe>
  </div>
</div>
