#!/usr/bin/env python3
"""Build feed.xml (RSS 2.0) from the newest archive editions.

Usage: python3 scripts/build_feed.py

Writes feed.xml at the repo root with the 30 newest editions in archive/,
newest first. Each item's guid is its permanent archive URL, so rebuilding
never creates duplicates in readers.
"""
import html
import re
from datetime import datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://leonardoresston.github.io/thefold/"
LONDON = ZoneInfo("Europe/London")
MAX_ITEMS = 30


def editions():
    found = []
    for path in ROOT.glob("archive/[0-9][0-9][0-9][0-9]/[0-9][0-9]-[0-9][0-9].html"):
        y = int(path.parent.name)
        m, d = (int(x) for x in path.stem.split("-"))
        found.append((datetime(y, m, d).date(), path))
    return sorted(found, reverse=True)[:MAX_ITEMS]


def meta(doc, name):
    m = re.search(r'<meta\s+(?:name|property)="%s"\s+content="([^"]*)"' % re.escape(name), doc)
    return html.unescape(m.group(1)) if m else ""


def body(doc):
    m = re.search(r"<main\b.*?</main>", doc, re.S)
    content = m.group(0) if m else doc
    return content.replace("]]>", "]]]]><![CDATA[>")


def pub_date(day):
    return format_datetime(datetime.combine(day, time(4, 0), LONDON).astimezone(timezone.utc), usegmt=True)


def item(day, path):
    doc = path.read_text(encoding="utf-8")
    url = f"{BASE_URL}archive/{day:%Y}/{day:%m-%d}.html"
    summary = meta(doc, "description") or meta(doc, "og:description")
    return f"""    <item>
      <title>The Fold — {day:%Y-%m-%d}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{pub_date(day)}</pubDate>
      <description>{html.escape(summary, quote=False)}</description>
      <content:encoded><![CDATA[{body(doc)}]]></content:encoded>
    </item>"""


def main():
    eds = editions()
    items = "\n".join(item(d, p) for d, p in eds)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Fold</title>
    <link>{BASE_URL}</link>
    <atom:link href="{BASE_URL}feed.xml" rel="self" type="application/rss+xml"/>
    <description>A daily morning briefing from the UK and the world.</description>
    <language>en-gb</language>
    <lastBuildDate>{pub_date(eds[0][0]) if eds else ''}</lastBuildDate>
{items}
  </channel>
</rss>
"""
    (ROOT / "feed.xml").write_text(xml, encoding="utf-8")
    print(f"feed.xml: {len(eds)} items, newest {eds[0][0] if eds else 'none'}")


if __name__ == "__main__":
    main()
