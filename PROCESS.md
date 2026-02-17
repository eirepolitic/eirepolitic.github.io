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

## New Article Workflow
1. Copy `_templates/post-template.md`
2. Save in `_posts/` as:
   `YYYY-MM-DD-short-title.md`
3. If assets are needed:
   create folder in:
   `assets/articles/YYYY-MM-DD-short-title/`
4. Add embeds or asset links
5. Commit and push to publish

## New Project Workflow
1. Create file in `projects/`:
   `project-slug.md`
2. Add frontmatter:
   - layout: page
   - title:
   - permalink: /projects/project-slug/
3. Add link to `projects/index.md`
4. If assets needed:
   create folder in `assets/projects/project-slug/`
5. Commit and publish
