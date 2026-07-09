# The Fold Automation Notes

## Readwise Reader

Save only one Reader document per edition.

- Use the permanent archive URL: `https://leonardoresston.github.io/thefold/archive/YYYY/MM-DD.html`.
- Do not save the front page URL for daily editions.
- Save as category `article` and apply the `rss` tag. Do not try category `rss` first.
- Before creating a Reader document, list recent documents without a tag filter and compare `source_url` and `url` against the permanent archive URL. Reader can create untagged scraper documents.
- Also search Reader by the exact title `The Fold — YYYY-MM-DD`.
- Reuse an existing Reader document when its `source_url`, `url`, or exact title already matches the current edition.
- If an existing document lacks the standard title, author, category, published date, or tags, normalize it with `reader_bulk_edit_document_metadata` instead of creating another document.
- Call `reader_create_document` at most once per run.
- After creation, list the returned Reader document by ID and repair missing metadata or tags with `reader_bulk_edit_document_metadata`.
- If Reader creation returns an error, list recent Reader documents and search by exact title again before retrying. Reader can create a document even when the connector returns an error.
