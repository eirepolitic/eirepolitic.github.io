#!/usr/bin/env python3
"""Validate Jekyll documentation metadata and internal references."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "_docs"

REQUIRED_FIELDS = {"title", "summary", "section", "doc_type", "status", "updated"}
ALLOWED_SECTIONS = {
    "repositories",
    "systems",
    "data",
    "runbooks",
    "decisions",
    "high-director",
    "notes",
    "archive",
}
ALLOWED_TYPES = {
    "repository",
    "system",
    "pipeline",
    "schema",
    "runbook",
    "decision",
    "agent",
    "reference",
    "note",
}
ALLOWED_STATUSES = {
    "planned",
    "active",
    "paused",
    "deprecated",
    "archived",
    "unknown",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")


def load_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    try:
        _, raw_yaml, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("malformed YAML front matter") from exc
    data = yaml.safe_load(raw_yaml) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter must be a mapping")
    return data, body


def permalink_for(path: Path, metadata: dict) -> str:
    if metadata.get("permalink"):
        return str(metadata["permalink"])
    relative = path.relative_to(DOCS_DIR).with_suffix("")
    return f"/docs/{relative.as_posix()}/"


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme or parsed.netloc or target.startswith(("mailto:", "tel:", "#", "{{")))


def target_exists(source: Path, target: str, known_urls: set[str]) -> bool:
    clean = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean or is_external(clean):
        return True
    if clean.startswith("/"):
        if clean in known_urls or clean.rstrip("/") + "/" in known_urls:
            return True
        candidate = ROOT / clean.lstrip("/")
    else:
        candidate = (source.parent / clean).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            return False
    return candidate.exists() or candidate.with_suffix(".md").exists() or (candidate / "index.md").exists()


def main() -> int:
    errors: list[str] = []
    docs: list[tuple[Path, dict, str]] = []
    permalinks: dict[str, Path] = {}

    if not DOCS_DIR.exists():
        print("ERROR: _docs directory does not exist")
        return 1

    for path in sorted(DOCS_DIR.rglob("*.md")):
        try:
            metadata, body = load_front_matter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        missing = sorted(REQUIRED_FIELDS - metadata.keys())
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing fields: {', '.join(missing)}")

        section = metadata.get("section")
        if section not in ALLOWED_SECTIONS:
            errors.append(f"{path.relative_to(ROOT)}: invalid section {section!r}")

        doc_type = metadata.get("doc_type")
        if doc_type not in ALLOWED_TYPES:
            errors.append(f"{path.relative_to(ROOT)}: invalid doc_type {doc_type!r}")

        status = metadata.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{path.relative_to(ROOT)}: invalid status {status!r}")

        for field in ("created", "updated", "last_verified", "archived_date"):
            value = metadata.get(field)
            if value is not None and not DATE_RE.match(str(value)):
                errors.append(f"{path.relative_to(ROOT)}: {field} must use YYYY-MM-DD")

        if status == "archived":
            for field in ("archived_date", "archive_reason"):
                if not metadata.get(field):
                    errors.append(f"{path.relative_to(ROOT)}: archived document missing {field}")
            if section != "archive":
                errors.append(f"{path.relative_to(ROOT)}: archived document must use section 'archive'")

        permalink = permalink_for(path, metadata)
        if not permalink.startswith("/") or not permalink.endswith("/"):
            errors.append(f"{path.relative_to(ROOT)}: permalink must start and end with '/' ({permalink})")
        if permalink in permalinks:
            errors.append(
                f"{path.relative_to(ROOT)}: duplicate permalink {permalink} also used by "
                f"{permalinks[permalink].relative_to(ROOT)}"
            )
        else:
            permalinks[permalink] = path

        docs.append((path, metadata, body))

    known_urls = set(permalinks)
    for page in ROOT.rglob("*.md"):
        if any(part in {".git", "vendor"} for part in page.parts):
            continue
        try:
            metadata, _ = load_front_matter(page)
        except Exception:
            continue
        if metadata.get("permalink"):
            known_urls.add(str(metadata["permalink"]))

    for path, metadata, body in docs:
        targets = MARKDOWN_LINK_RE.findall(body) + HTML_LINK_RE.findall(body)
        for target in targets:
            target = target.strip().split()[0].strip("<>\"'")
            if not target_exists(path, target, known_urls):
                errors.append(f"{path.relative_to(ROOT)}: broken local reference {target!r}")

        for related in metadata.get("related", []) or []:
            if not target_exists(path, str(related), known_urls):
                errors.append(f"{path.relative_to(ROOT)}: broken related URL {related!r}")

    if errors:
        print(f"Documentation validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Documentation validation passed for {len(docs)} document(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
