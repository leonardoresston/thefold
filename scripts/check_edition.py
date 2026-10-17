#!/usr/bin/env python3
"""Check a Fold edition before it is committed.

Usage: python3 scripts/check_edition.py [index.html]

Errors (exit 1) break the template, the Matter import or the Matter de-duplication.
Warnings are editorial-style flags to review; they can be false positives.
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://leonardoresston.github.io/thefold/"
TEMPLATE_VERSION = "2026-10"
SECTIONS = {"News", "Economy", "Technology", "Culture", "Sports", "Lifestyle", "Gaming"}
WORDS_MIN, WORDS_MAX = 2700, 3300

STYLE_FLAGS = [
    (r"\bnot just\b", "contrast formula: 'not just X, but Y'"),
    (r"\bnot only\b", "contrast formula: 'not only X, rather Y'"),
    (r"\bless about\b[^.]*\bthan\b", "contrast formula: 'less about X than Y'"),
    (r"\bthe point is not\b", "contrast formula: 'the point is not X'"),
    (r"\b(?:is|was|isn['’]t|wasn['’]t) not [^.;]{1,60}[,;] (?:it|this|that)(?:['’]s| is| was)\b", "contrast formula: 'it is not X, it is Y'"),
    (r"\b(?:it|this|that) (?:is|was)n['’]t [^.;]{1,60}[,;] (?:it|this|that)(?:['’]s| is| was)\b", "contrast formula: 'it isn't X, it's Y'"),
    (r"\bRSS\b|\bfeed list\b|\bsource mix\b|\bsynthesis\b|\bthis edition\b|\bthe feeds?\b(?! (?:for|of|on) )", "meta-comment about feeds or the newsletter"),
    (r"\b(?:Guardian|BBC|Folha|Verge|IGN|9to5Mac|MacStories|MacMagazine|Meio)\b[^.]{0,25}\b(?:reported|wrote|said|framed|focused on|carried)\b", "source-attribution scaffolding"),
]


class Edition(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = {}
        self.meta = {}
        self.links = []
        self.imgs = []
        self.h1 = []
        self.h2 = []
        self.title = ""
        self.canonical = None
        self.story_text = []
        self.brief_items = 0
        self._stack = []
        self._in = {"title": 0, "h1": 0, "h2": 0, "story": 0, "sources": 0, "brief_li": 0, "story_p": 0}
        self._buf = {"h1": "", "h2": ""}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.tags[tag] = self.tags.get(tag, 0) + 1
        flags = []
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.imgs.append(a)
        if tag == "title":
            flags.append("title")
        if tag in ("h1", "h2"):
            flags.append(tag)
            self._buf[tag] = ""
        if tag == "section" and "story" in cls:
            flags.append("story")
        if "sources" in cls:
            flags.append("sources")
        if tag == "li" and self._ancestor_has("in-brief"):
            flags.append("brief_li")
            self.brief_items += 1
        if tag == "p" and self._in["story"]:
            flags.append("story_p")
        if tag in ("meta", "link", "img", "br", "hr", "input", "source"):
            return
        for f in flags:
            self._in[f] += 1
        self._stack.append((tag, cls, flags))

    def _ancestor_has(self, cls_name):
        return any(cls_name in c for _, c, _ in self._stack)

    def handle_endtag(self, tag):
        while self._stack:
            t, _, flags = self._stack.pop()
            for f in flags:
                self._in[f] -= 1
                if f in ("h1", "h2"):
                    getattr(self, f).append(" ".join(self._buf[f].split()))
            if t == tag:
                break

    def handle_data(self, data):
        if self._in["title"]:
            self.title += data
        for h in ("h1", "h2"):
            if self._in[h]:
                self._buf[h] += data
        if self._in["story_p"] and not self._in["sources"]:
            self.story_text.append(data)


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "index.html")
    src = path.read_text(encoding="utf-8")
    ed = Edition()
    ed.feed(src)
    errors, warnings = [], []

    title = " ".join(html.unescape(ed.title).split())
    m = re.fullmatch(r"The Fold — (\d{4})-(\d{2})-(\d{2})", title)
    if not m:
        errors.append(f"<title> must be exactly 'The Fold — YYYY-MM-DD' (Matter de-duplication searches for it); found {title!r}")
        date = None
    else:
        y, mo, d = m.groups()
        date = f"{y}-{mo}-{d}"
        archive_url = f"{BASE_URL}archive/{y}/{mo}-{d}.html"
        if ed.meta.get("og:title") != f"The Fold — {date}":
            errors.append(f"og:title must be 'The Fold — {date}'")
        if ed.canonical != archive_url:
            errors.append(f"canonical must be {archive_url}; found {ed.canonical}")
        if ed.meta.get("og:url") != archive_url:
            errors.append(f"og:url must be {archive_url}")
        if not ed.meta.get("article:published_time", "").startswith(date):
            errors.append("article:published_time must start with the edition date")
        if ed.meta.get("publication_date") != date:
            errors.append("publication_date meta must match the edition date")
        archive_path = ROOT / "archive" / y / f"{mo}-{d}.html"
        index_path = ROOT / "index.html"
        if path.resolve() == index_path.resolve():
            if not archive_path.exists():
                errors.append(f"missing archive copy {archive_path.relative_to(ROOT)}")
            elif archive_path.read_bytes() != path.read_bytes():
                errors.append(f"index.html and {archive_path.relative_to(ROOT)} must be identical")

    if ed.meta.get("fold-template") != TEMPLATE_VERSION:
        errors.append(f"not built from TEMPLATE.html (missing <meta name=\"fold-template\" content=\"{TEMPLATE_VERSION}\">)")
    for key in ("author", "description", "og:description", "og:image", "og:type"):
        if not ed.meta.get(key):
            errors.append(f"missing meta {key}")
    if "{{" in src or "}}" in src:
        errors.append("unreplaced {{PLACEHOLDER}} left in the page")

    for tag, want in (("main", 1), ("article", 1), ("h1", 1)):
        if ed.tags.get(tag, 0) != want:
            errors.append(f"expected exactly {want} <{tag}>, found {ed.tags.get(tag, 0)}")
    for tag in ("script", "table", "iframe", "nav", "aside"):
        if ed.tags.get(tag):
            errors.append(f"<{tag}> is not allowed (Matter import)")
    if not 2 <= len(ed.h2) <= 4:
        warnings.append(f"{len(ed.h2)} section headings; the style guide prefers 2–4")
    for h in ed.h2:
        if h not in SECTIONS:
            errors.append(f"section heading {h!r} is not one of {sorted(SECTIONS)}")
    if 'class="story lead"' not in src:
        errors.append('the first story must use class="story lead"')
    if not 4 <= ed.brief_items <= 6:
        errors.append(f"'In this edition' needs 4–6 items; found {ed.brief_items}")

    for href in ed.links:
        if not href.startswith("https://"):
            errors.append(f"link is not absolute https: {href}")
    for img in ed.imgs:
        if not (img.get("src") or "").startswith("https://"):
            errors.append(f"image is not absolute https: {img.get('src')}")
        if not img.get("alt"):
            errors.append(f"image without alt text: {img.get('src')}")
    if not ed.meta.get("og:image", "").startswith("https://"):
        errors.append("og:image must be an absolute https URL")

    text = " ".join(" ".join(ed.story_text).split())
    words = len(text.split())
    if not WORDS_MIN <= words <= WORDS_MAX:
        warnings.append(f"{words} words of editorial copy; target {WORDS_MIN}–{WORDS_MAX}")
    for pattern, label in STYLE_FLAGS:
        for hit in re.finditer(pattern, text, re.I):
            start = max(0, hit.start() - 40)
            warnings.append(f"{label}: …{text[start:hit.end() + 40]}…")

    print(f"{path.name}: {date or 'unknown date'} · {words} words · {len(ed.h2)} sections · {ed.tags.get('figure', 0)} images · {len(ed.links)} links")
    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"WARNING {w}")
    print("FAILED" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
