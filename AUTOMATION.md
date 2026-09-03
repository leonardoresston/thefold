# The Fold Automation Notes

## Edition output

- Follow `EDITORIAL_STYLE.md`, including the approximately 3,000-word target, looser conversational flow, and Matter-compatible semantic HTML.
- Do not fetch or publish the former BTC-GBP, BRL-GBP, or VWRP market snapshot.
- Publish the same final HTML to both `index.html` and the permanent dated archive path.

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
