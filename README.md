# Spill the Tea / 今日瓜田

Kora Home's daily team news digest, published with GitHub Pages.

- `index.html` – the reading page (static, no build step, system fonts only so it also loads in mainland China)
- `data/index.json` – list of issues, newest first
- `data/days/YYYY-MM-DD.json` – one issue: `{ issue, items }`
- `data/meta.json` – topic names and the AI critic's name (no internal settings)

A scheduled Claude task writes a new `data/days/<date>.json`, updates `data/index.json`, commits, and posts the link to Slack each weekday morning. Settings stay private on claude.ai and are never committed here.
