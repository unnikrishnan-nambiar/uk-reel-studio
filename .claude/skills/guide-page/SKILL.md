---
name: guide-page
description: Make the free DM guide page that matches a reel's comment keyword, on his website repo uk_speaks.ai. Use when he asks for a guide, a link for a keyword, or after a reel with a new keyword.
---

# Guide pages (website repo)

Repo: `github.com/unnikrishnan-nambiar/uk_speaks.ai` (GitHub Pages, main branch). Clone it next to this project if missing. Its own `CLAUDE.md` has the full rules — read it.

Key points:
- Each guide: `g/<keyword-slug>/index.html`, copied from an existing guide (e.g. `g/ppt/`, `g/excel/`). `noindex, nofollow`, relative links, never linked publicly.
- Structure: intro card with keyword chip + 3 quick steps → copyable prompt cards (`data-copy-target`, copy.js) → visuals (`assets/img/guides/<slug>/`, WebP) → "Need help? Full steps" numbered cards → Points to be noted → black closer card.
- OG image `assets/og/og-<slug>.png` (1200×630) and absolute og:url/og:image with BASE_URL `https://unnikrishnan-nambiar.github.io/uk_speaks.ai/`.
- Check at 390 px wide (no horizontal scroll), commit, push, give him `https://unnikrishnan-nambiar.github.io/uk_speaks.ai/g/<slug>/`.
- Facts on the page (plan limits, prices, features) must be checked on the web first; add a Sources list in your reply.
