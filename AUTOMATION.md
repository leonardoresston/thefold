# The Fold Automation Notes

## Readwise Reader

Save only one Reader document per edition.

- Use the permanent archive URL: `https://leonardoresston.github.io/thefold/archive/YYYY/MM-DD.html`.
- Do not save the front page URL for daily editions.
- Before creating a Reader document, list recent documents tagged `the fold`.
- Reuse an existing Reader document when its `source_url`, `url`, or title already matches the current edition.
- Call `reader_create_document` at most once per run.
- If Reader creation returns an error, list Reader documents again before retrying. Reader can create a document even when the connector returns an error.
- If category `rss` is rejected, save as `article` only after the second duplicate check, while keeping the `rss` tag.
