You are writing today's edition of The Fold, a daily morning briefing, in this repository (the current directory).

Edition date: {{DATE}} (today in Europe/London).

1. Read and follow, exactly: `EDITORIAL_STYLE.md`, `AUTOMATION.md` (sections "Edition output" and "Template and checks"), `TEMPLATE.html`, and `feeds.json`.
2. Fetch every feed in `feeds.json` (you may use curl). Use items from the last 24 hours. Open the underlying articles when you need facts. Choose the stories that most reward the reader.
3. Build the edition from `TEMPLATE.html`. Copy its `<head>` font links and `<style>` block exactly, keep `<meta name="fold-template" content="2026-10">`, and replace every `{{PLACEHOLDER}}`. `<title>` and `og:title` must be exactly `The Fold — {{DATE}}`. The canonical URL is `https://leonardoresston.github.io/thefold/archive/{{YEAR}}/{{MMDD}}.html`.
4. About 3,000 words (2,700–3,300). "In this edition": 4–6 plain lines. The lead story uses `class="story lead"` and has an image. Use 2–4 sections. Sports only for the World Cup, Champions League, Premier League, Arsenal and São Paulo FC. No market or price snapshot.
5. Write the identical final HTML to `index.html` and `archive/{{YEAR}}/{{MMDD}}.html`.
6. Run `python3 scripts/check_edition.py index.html`. Fix every ERROR, and rewrite sentences flagged by a WARNING unless it is a false positive. Re-run until it passes. If you change index.html, copy it to the archive file again.

Do NOT run git, commit, push, or edit any other files; the wrapper script does that. Finish with one line: the checker's final summary line.
