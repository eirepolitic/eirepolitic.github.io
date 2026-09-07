from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

SOURCE_URL = "https://raw.githubusercontent.com/eirepolitic/eirepolitic-data-pipeline/previews/data-model/index.html"
OUTPUT = Path("_docs/data/irish-politics-data-model.md")

FRONT_MATTER = """---
title: Irish Politics Data Model
summary: Practical catalogue of the current EirePolitic production political datasets, including purpose, sources, transformations, relationships, schemas and real example rows.
section: data
doc_type: reference
status: active
created: 2026-09-07
updated: {today}
last_verified: {today}
owner: Eire Politic
repository: eirepolitic-data-pipeline
system: Unified Oireachtas Data Platform
order: 20
permalink: /projects/data/irish-politics-data-model/
tags:
  - oireachtas
  - data-model
  - schemas
  - parquet
  - polling
related:
  - /projects/data/oireachtas-canonical-data-product-catalogue/
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/repositories/eirepolitic-data-pipeline/
---
"""


def fetch_source() -> str:
    request = Request(SOURCE_URL, headers={"User-Agent": "EirePolitic-docs-refresh/1.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def clean_fragment(source_html: str) -> str:
    soup = BeautifulSoup(source_html, "html.parser")
    main = soup.find("main")
    if main is None:
        raise RuntimeError("Source catalogue does not contain <main>")

    hero = main.find("section", class_="hero")
    if hero is None:
        raise RuntimeError("Source catalogue does not contain hero metadata")

    hero_text = hero.find("p")
    badges = [b.get_text(" ", strip=True) for b in hero.select(".badge")]

    out = BeautifulSoup("<div class='data-model-catalogue'></div>", "html.parser")
    container = out.div

    summary = out.new_tag("section")
    h2 = out.new_tag("h2")
    h2.string = "Summary"
    summary.append(h2)
    if hero_text:
        p = out.new_tag("p")
        p.string = hero_text.get_text(" ", strip=True)
        summary.append(p)
    if badges:
        ul = out.new_tag("ul")
        for badge in badges:
            li = out.new_tag("li")
            li.string = badge
            ul.append(li)
        summary.append(ul)
    container.append(summary)

    for section in main.find_all("section", recursive=False):
        if "hero" in (section.get("class") or []):
            continue

        # Keep native article headings/content, but remove standalone-page navigation chrome.
        for back in section.select(".back"):
            back.decompose()
        for eyebrow in section.select(".eyebrow"):
            eyebrow.decompose()

        for table_wrap in section.select(".table-wrap, .schema-wrap"):
            existing = table_wrap.get("class") or []
            table_wrap["class"] = [c for c in existing if c not in {"table-wrap", "schema-wrap"}] + ["data-table-wrap"]

        for cell in section.select(".cell"):
            cell["class"] = ["data-cell"]

        # The docs layout already provides the page title. Dataset/overview headings remain native.
        container.append(section.extract())

    # Remove standalone-page class names that would otherwise imply special card/post styling.
    for tag in container.find_all(True):
        classes = tag.get("class") or []
        classes = [c for c in classes if c not in {"overview", "dataset", "appendix", "section-head", "facts", "sample-note", "muted", "schema-details", "group-card", "grid", "index", "schema"}]
        if classes:
            tag["class"] = classes
        elif tag.has_attr("class"):
            del tag["class"]

    return str(container)


def main() -> None:
    source = fetch_source()
    fragment = clean_fragment(source)
    today = date.today().isoformat()
    content = FRONT_MATTER.format(today=today) + "\n# Irish Politics Data Model\n\n" + fragment + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
