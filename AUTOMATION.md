# The Fold Automation Notes

## Edition output

- Follow `EDITORIAL_STYLE.md`, including the approximately 3,000-word target, looser conversational flow, and Matter-compatible semantic HTML.
- Do not fetch or publish the former BTC-GBP, BRL-GBP, or VWRP market snapshot.
- Publish the same final HTML to both `index.html` and the permanent dated archive path.

## Template and checks

- Build every edition from `TEMPLATE.html`. This replaces any instruction to use `index.html` or older archives as the visual template: those pages are previous outputs, and archives before 17 October 2026 use the retired design.
- Copy the template's `<head>` font links and `<style>` block exactly, keep `<meta name="fold-template" content="2026-10">`, and replace every `{{PLACEHOLDER}}`.
- Keep the `<title>` and `og:title` exactly `The Fold — YYYY-MM-DD`; the Matter de-duplication below searches for that title.
- After writing both files and before committing, run `python3 scripts/check_edition.py index.html`.
  - Any `ERROR` blocks publication: fix the edition and run the check again.
  - Review each `WARNING` (word count, contrast formulas, meta-comments, attribution scaffolding) and rewrite the flagged sentence unless it is a false positive.
- Include the checker's final summary line in the run report.

## Matter

Save exactly one Matter item per edition using the installed CLI at `/Users/leonardoresston/.matter/bin/matter`.

- Use the permanent archive URL: `https://leonardoresston.github.io/thefold/archive/YYYY/MM-DD.html`.
- Do not save the front page URL for daily editions.
- Before saving, run `matter account` and stop if authentication, Matter Pro access, or write access is unavailable.
- List all Matter items with `matter items list --status all --all` and compare their URL fields against the exact permanent archive URL.
- Also search Matter for the exact title `The Fold — YYYY-MM-DD`; compare any result's URL against the permanent archive URL.
- Reuse an existing item whenever its URL matches. Never save a second copy of the same permanent archive URL.
- If no match exists, call `matter items save --url "PERMANENT_ARCHIVE_URL" --status queue` exactly once and capture the returned item ID.
- Apply these tags to the saved or reused item with `matter tags add --item ITEM_ID --name "TAG"`: `The Fold`, `newsletter`, `rss`, `daily-briefing`, and `github-pages`. Adding an existing tag is acceptable.
- After saving, fetch the returned item with `matter items get ITEM_ID` and confirm that its URL matches the permanent archive URL.
- If `matter items save` returns an error, do not immediately retry. Repeat the all-items URL check and exact-title search first; save again only if both checks confirm that no matching item exists.
