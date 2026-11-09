# The Fold Automation Notes

## Edition output

- Follow `EDITORIAL_STYLE.md`, including the approximately 3,000-word target, looser conversational flow, and Matter-compatible semantic HTML.
- Do not fetch or publish the former BTC-GBP, BRL-GBP, or VWRP market snapshot.
- Publish the same final HTML to both `index.html` and the permanent dated archive path.

## Template and checks

- Build every edition from `TEMPLATE.html`. This replaces any instruction to use `index.html` or older archives as the visual template: those pages are previous outputs, and archives before 17 October 2026 use the retired design.
- Copy the template's `<head>` font links and `<style>` block exactly, keep `<meta name="fold-template" content="2026-10">`, and replace every `{{PLACEHOLDER}}`.
- Keep the `<title>` and `og:title` exactly `The Fold — YYYY-MM-DD`; RSS readers and the checker rely on it.
- After writing both files and before committing, run `python3 scripts/check_edition.py index.html`.
  - Any `ERROR` blocks publication: fix the edition and run the check again.
  - Review each `WARNING` (word count, contrast formulas, meta-comments, attribution scaffolding) and rewrite the flagged sentence unless it is a false positive.
- Include the checker's final summary line in the run report.

## Feed (RSS)

Editions reach Leo's Feed app through Feedbin, by RSS. There is no Matter step any more.

- After the check passes, run `python3 scripts/build_feed.py`. It rebuilds `feed.xml` from the 30 newest archive editions, newest first, with the full edition HTML in `content:encoded`.
- Each item's `guid` is the permanent archive URL. Never change it for a published edition. Feedbin de-duplicates on it, so rebuilding is safe.
- Commit `feed.xml` in the same commit as the edition, then push.
- After pushing, check `xmllint --noout feed.xml`. Report the feed URL `https://leonardoresston.github.io/thefold/feed.xml` and the edition's guid in the run report.

## Daily run

`scripts/run_daily.sh` runs the whole job on the Mac Mini. Gemini 4 Argon (via `agy`) writes the edition from `scripts/daily_prompt.md`. The script then runs the check (sending any errors back to Gemini, for up to two fix rounds), rebuilds `feed.xml`, commits and pushes. launchd runs it at 04:00 London time. The log is in `~/Library/Logs/thefold-daily.log`.
