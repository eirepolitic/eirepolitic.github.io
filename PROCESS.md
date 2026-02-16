# Content Process

## New Article
- Location: `_posts/`
- Filename: `YYYY-MM-DD-short-title.md`
- Start from: `_templates/post-template.md`
- Assets: `assets/YYYY-MM-DD-short-title/`
- Publish: commit + push

## New Project Doc
- Location: `projects/`
- Add `permalink: /projects/<slug>/`
- Add link to: `projects/index.md`
- Publish: commit + push

## Outputs
- Prefer embeds when possible
- Store local files in `assets/` when needed

### Checklist
- [ ] Filename is `YYYY-MM-DD-short-title.md`
- [ ] Frontmatter includes `layout: post` and `title:`
- [ ] Add embeds under “Outputs” section
- [ ] If adding files, create `assets/YYYY-MM-DD-short-title/`
- [ ] Preview by opening the live Articles page after publish
