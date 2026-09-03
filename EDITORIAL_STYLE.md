# The Fold Editorial Style

The Fold should feel like a substantial, conversational morning read, not a summary of feeds or a rigid newspaper digest. Aim for approximately 3,000 words per edition.

## Length and Selection

- Target approximately 3,000 words of editorial copy per edition. A range of 2,700–3,300 words is acceptable when the day's news warrants it; do not count navigation, metadata, source labels, or footer text toward the target.
- Let the strength and complexity of the day's news determine the number of stories. Do not pad thin items or force a rigid story quota merely to reach the word target.
- Select the stories that most reward the reader's attention instead of padding the edition or trying to represent every feed or category equally.
- Give important developments enough context to explain why they matter. The lead can run to three or four short paragraphs; other major items can use two.
- Keep paragraphs digestible and combine closely related developments when that produces a clearer read.

## Voice

- Write the news in The Fold's own voice.
- Use a natural, conversational pace: vary sentence length, favour plain language, and let one idea lead smoothly into the next.
- Sound informed and companionable without becoming chatty, jokey, or opinionated.
- Treat RSS items as reporting inputs, not as the subject of the article.
- Do not write meta-comments about the feed list, the RSS window, the source mix, the newsletter format, or the act of synthesis.
- Do not say that a source "reported", "said", "wrote", "framed", "focused on", or "carried" a story unless the source's own action is itself the news.
- Do not quote source language unless a direct quote is essential to the story.
- Place linked source credit in parentheses at the end of the relevant paragraph, in the Meio style: `(<a href="...">Guardian</a>, <a href="...">BBC</a>)`.

## Sentence Style

Avoid contrast formulas that sound like analysis scaffolding, especially:

- "It is not X, it is Y."
- "This is not just X, but Y."
- "This is less about X than Y."
- "It is not only X, rather Y."
- "The point is not X, but Y."

Prefer direct declarative news sentences:

- "The government faces a new test over..."
- "The decision leaves..."
- "The case raises..."
- "The result sends..."

## Sections

- Keep the established visual identity, but use a looser editorial flow with fewer visible dividers.
- Do not force every story into the standing sections or include a section merely to complete a template.
- Use only the broad headings that genuinely help the reader navigate that day's edition. Prefer 2–4 sections in total, drawn from News, Economy, Technology, Culture, Sports, Lifestyle, and Gaming.
- It is fine to place a related technology, gaming, culture, or lifestyle item after another without introducing a new heading for a single story.
- For sports, focus only on the configured teams and leagues: World Cup, Champions League, Premier League, and Sao Paulo FC. If there is no relevant match or significant news, omit sports entirely.

## Economy

- Cover meaningful economic and business news when it earns a place in the edition.
- Do not include a recurring market check, price grid, or routine updates for BTC, BRL, VWRP, currencies, cryptoassets, or funds.

## Matter Import

- Produce clean, self-contained HTML that imports well into Matter's article reader.
- Use one `<main>` containing one `<article>`, with a single `<h1>` title followed by a clear hierarchy of `<h2>` and `<h3>` headings.
- Keep the edition's reading order meaningful without CSS. Put story text in ordinary `<p>` elements and source credits at the end of the relevant paragraph.
- Use absolute `https://` URLs for the canonical page, source links, and any images.
- Include a descriptive `<title>`, canonical link, author, publication date, description, and Open Graph article metadata in `<head>`.
- Avoid JavaScript, tables, multi-column layouts, price cards, decorative text that interrupts extraction, and essential information supplied only through CSS.
- Keep inline CSS modest and mobile-friendly; Matter should still extract a complete, readable article if it ignores the styling.

## Editorial Model

Use Canal Meio's latest edition as inspiration for rhythm and sourcing: report the news directly in short paragraphs, then credit sources in linked parentheses. Keep The Fold's existing design and archive workflow.
