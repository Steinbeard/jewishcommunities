"""Build the player wiki with Python's standard library; no game files are modified.

Usage: python scripts/kehillah_build_wiki.py --output C:/workspace/kehillah-wiki
The output directory must be empty or contain only an earlier wiki build.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/wiki"
REPO = "https://github.com/Steinbeard/jewishcommunities"
REVIEWED = "2026-11-25"


def escape(value):
    return html.escape(str(value), quote=True)


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.text = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])

    def handle_data(self, data):
        self.text.append(data)


def plain(value):
    doc = Document()
    doc.feed(value)
    return " ".join(" ".join(doc.text).split())


def revision():
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


def source_is_dirty():
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "docs/wiki", "scripts/kehillah_build_wiki.py",
         "scripts/kehillah_library_catalog.json", "localization/english", "common/domiciles/buildings"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return bool(result.stdout.strip())


def localization():
    result = {}
    for path in sorted((ROOT / "localization/english").glob("*.yml")):
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = re.match(r'^\s*([\w.]+):\d*\s+"(.*)"\s*(?:#.*)?$', line)
            if match:
                result[match[1]] = match[2]
    return result


def clean_loc(value, loc, depth=0):
    if depth < 8:
        value = re.sub(r"\$([\w.]+)\$", lambda m: clean_loc(loc.get(m[1], m[1]), loc, depth + 1), value)
    value = re.sub(r"\[[^\]]*\]", "(campaign-dependent)", value)
    value = re.sub(r"#[\w;,=:.+-]+\s?|#!|@[\w]+!", "", value)
    return value.replace(r"\n", " ").replace(r'\"', '"').strip()


def make_books(loc):
    catalog = json.loads((ROOT / "scripts/kehillah_library_catalog.json").read_text(encoding="utf-8-sig"))
    works = []
    for key in catalog["order"]:
        work = catalog["works"][key]
        if key.startswith("work_authored_"):
            continue  # Empty procedural slots are not historical books.
        title = clean_loc(loc.get("kehillah_lib_name_" + key, key.removeprefix("work_").replace("_", " ")), loc)
        works.append((key, title, work))
    rows, entries = [], []
    genres = {"parshanut": "Parshanut", "talmudics": "Talmudics", "hashkafa": "Machshavah", "machshava": "Machshavah"}
    for key, title, work in works:
        genre = genres.get(work.get("genre"), work.get("genre", "Unspecified"))
        year = work.get("year", "Unspecified")
        language = work.get("language", work.get("lang", "Unspecified"))
        author = work.get("composer", "Unspecified")
        cells = [title, genre, author, year, language, work.get("place", "Unspecified")]
        dates = ["Yes" if isinstance(year, (int, float)) and year <= date else "Later / unspecified" for date in (867, 1066, 1178)]
        row = f'<tr id="{escape(key)}">' + "".join(f"<td>{escape(c)}</td>" for c in cells + dates) + "</tr>"
        rows.append(row)
        entries.append({"title": title, "url": "books.html#" + key,
                        "summary": f"{genre} · {author} · {year} · {language}",
                        "text": " ".join(map(str, cells))})
    headers = ["Work", "Discipline", "Attribution in the mod", "Configured year", "Language", "Place", "By 867", "By 1066", "By 1178"]
    body = ('<p>The catalog contains <strong>' + str(len(rows)) + '</strong> named works from this build. '
            'Empty procedural authored slots are excluded. Titles and metadata are generated from the mod, not retyped.</p>'
            '<p>Dates are the mod’s configured chronology, not independent scholarly datings. “By” columns compare '
            'only the configured year with a bookmark. They do not establish ownership, discovery, rite acceptance, '
            'or every in-game availability gate. Newly authored landmarks can change campaign history.</p>'
            '<p>Use the filter for a title, author, discipline, language, or place. Scroll horizontally for bookmark columns.</p>'
            '<label class="filter-label" for="reference-filter">Filter works</label>'
            '<input id="reference-filter" type="search" placeholder="e.g. Saadia, Aramaic, Machshavah" aria-controls="reference-table">'
            '<p id="filter-count" role="status"></p><div class="table-scroll"><table id="reference-table"><thead><tr>'
            + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table></div>')
    return {"slug": "books", "title": "Book catalog", "section": "Reference", "summary": "Every named work, with attribution, language, configured date, and bookmark chronology.",
            "body": body, "sources": ["scripts/kehillah_library_catalog.json", "localization/english/kehillah_library_panel_l_english.yml"]}, entries


def make_buildings(loc):
    path = ROOT / "common/domiciles/buildings/kehillah_domicile_buildings.txt"
    keys = re.findall(r"^(kehillah_\w+)\s*=\s*\{", path.read_text(encoding="utf-8-sig"), re.M)
    rows = []
    for key in keys:
        name_key = key + "_domicile_building"
        name = clean_loc(loc.get(name_key, key.replace("_", " ")), loc)
        desc = clean_loc(loc.get(name_key + "_desc", "No static description provided."), loc)
        rows.append(f'<tr id="{escape(key)}"><td>{escape(name)}</td><td>{escape(desc)}</td><td><code>{escape(key)}</code></td></tr>')
    body = ('<p>These <strong>' + str(len(keys)) + '</strong> top-level definitions are extracted from the Quarter building file. '
            'The table includes retained legacy definitions: it does not imply that every building is constructible in the current slot layout. '
            'Names and descriptions are generated from English localization.</p>'
            '<p>Construction tooltips in the game determine actual costs, prerequisites, charter permissions, tiers, and effects. '
            'Campaign-dependent description fragments are labelled accordingly. See <a href="quarter.html">the Quarter guide</a> for the current design.</p>'
            '<label class="filter-label" for="reference-filter">Filter buildings</label><input id="reference-filter" type="search" '
            'placeholder="e.g. Synagogue, scribe, wall" aria-controls="reference-table"><p id="filter-count" role="status"></p>'
            '<div class="table-scroll"><table id="reference-table"><thead><tr><th scope="col">Building / tier</th>'
            '<th scope="col">Description</th><th scope="col">Source ID</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
    return {"slug": "buildings", "title": "Building reference", "section": "Reference", "summary": "Building and annex definitions in the checked-out mod, including retained legacy entries.",
            "body": body, "sources": [str(path.relative_to(ROOT)).replace("\\", "/")]}


def render(article, articles, sha, dirty):
    nav = []
    for section in dict.fromkeys(a["section"] for a in articles):
        nav.append(f'<h2>{escape(section)}</h2><ul>')
        for item in articles:
            if item["section"] == section:
                current = ' aria-current="page"' if item["slug"] == article["slug"] else ''
                nav.append(f'<li><a href="{item["slug"]}.html"{current}>{escape(item["title"])}</a></li>')
        nav.append('</ul>')
    body = article["body"]
    headings = []
    def heading(match):
        text = plain(match[1])
        anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        if anchor in [h[0] for h in headings]:
            anchor += "-" + str(len(headings))
        headings.append((anchor, text))
        return f'<h2 id="{anchor}">{match[1]}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', heading, body)
    toc = '<nav class="toc" aria-label="On this page"><strong>On this page</strong><ul>' + ''.join(f'<li><a href="#{key}">{escape(text)}</a></li>' for key, text in headings) + '</ul></nav>' if headings else ''
    sources = ''.join(f'<li><a href="{REPO}/blob/{sha}/{escape(path)}">{escape(path)}</a></li>' for path in article["sources"])
    working_note = ' This preview includes uncommitted source changes; linked committed sources can differ.' if dirty else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(article['title'])} · Jewish Communities</title><meta name="description" content="{escape(article['summary'])}">
<link rel="stylesheet" href="assets/wiki.css"><script src="assets/wiki.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a><header class="masthead"><a class="brand" href="index.html">KEHILLAH <span>Jewish Communities Wiki</span></a>
<nav aria-label="External links"><a href="{REPO}">Repository</a><a href="{REPO}/issues">Report a bug</a></nav></header>
<div class="layout"><aside class="sidebar"><details open><summary>Wiki navigation</summary><label for="wiki-search">Search the wiki</label>
<input id="wiki-search" type="search" placeholder="Books, buildings, guides…" autocomplete="off" aria-controls="search-results">
<p id="search-status" role="status"></p><div id="search-results"></div><nav aria-label="Wiki articles">{''.join(nav)}</nav></details></aside>
<main id="main"><p class="eyebrow">{escape(article['section'])} · Pre-alpha development wiki</p><h1>{escape(article['title'])}</h1>
<p class="summary">{escape(article['summary'])}</p>{toc}<article>{body}</article>
<details class="sources"><summary>Sources and verification</summary><p>Editorial review: {REVIEWED}. Build base: <a href="{REPO}/commit/{sha}">{sha[:8]}</a>.{working_note} Source-built does not mean live-tested. <a href="status.html">About this wiki</a>.</p><ul>{sources}</ul></details>
<footer><a href="{REPO}/blob/master/docs/wiki/articles.json">Edit articles on GitHub</a><span>Jewish Communities · A Crusader Kings III mod</span></footer></main></div>
<script id="wiki-index" type="application/json">__SEARCH_INDEX__</script></body></html>'''


def validate(output):
    docs = {}
    for path in output.glob("*.html"):
        doc = Document()
        doc.feed(path.read_text(encoding="utf-8"))
        if len(doc.ids) != len(set(doc.ids)):
            raise ValueError(f"Duplicate HTML IDs: {path.name}")
        docs[path.resolve()] = doc
    for path, doc in docs.items():
        for link in doc.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not target.is_relative_to(output.resolve()) or not target.is_file():
                raise ValueError(f"Broken or escaping local link in {path.name}: {link}")
            if parts.fragment and target in docs and unquote(parts.fragment) not in docs[target].ids:
                raise ValueError(f"Broken anchor in {path.name}: {link}")
    return len(docs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT.is_relative_to(output) or output == SOURCE or output.is_relative_to(SOURCE):
        raise ValueError("Choose a separate build directory, not the repository or wiki source.")
    articles = json.loads((SOURCE / "articles.json").read_text(encoding="utf-8-sig"))
    sha = revision()
    dirty = source_is_dirty()
    loc = localization()
    book_page, book_entries = make_books(loc)
    articles.extend([book_page, make_buildings(loc)])
    slugs = [a["slug"] for a in articles]
    if len(slugs) != len(set(slugs)) or any(not re.fullmatch(r"[a-z0-9-]+", s) for s in slugs):
        raise ValueError("Invalid or duplicate article slug")
    for article in articles:
        for source in article["sources"]:
            if not (ROOT / source).is_file():
                raise ValueError(f"Missing evidence file for {article['slug']}: {source}")
    # Never clear arbitrary output paths; refuse unexpected pre-existing contents.
    allowed = {s + ".html" for s in slugs} | {"assets", "images", ".nojekyll", "build-info.json"}
    if output.exists() and any(p.name not in allowed for p in output.iterdir()):
        raise ValueError("Output contains non-wiki files; choose an empty directory")
    output.mkdir(parents=True, exist_ok=True)
    (output / "assets").mkdir(exist_ok=True)
    (output / "images").mkdir(exist_ok=True)
    for name in ("wiki.css", "wiki.js"):
        shutil.copyfile(SOURCE / name, output / "assets" / name)
    for name in ("jewish-quarter.jpg", "quarter-map.jpg", "library.jpg", "bet-din-sitting.jpg"):
        shutil.copyfile(ROOT / "docs/images" / name, output / "images" / name)
    search = [{"title": a["title"], "url": a["slug"] + ".html", "summary": a["summary"], "text": plain(a["body"])} for a in articles] + book_entries
    # Inline index keeps search usable from a local file as well as Pages.
    index = json.dumps(search, ensure_ascii=False).replace("<", r"\u003c")
    for article in articles:
        page = render(article, articles, sha, dirty).replace("__SEARCH_INDEX__", index)
        (output / (article["slug"] + ".html")).write_text(page, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    info = {"revision": sha, "uncommitted_source": dirty, "editorial_review": REVIEWED, "articles": len(articles), "named_works": len(book_entries)}
    (output / "build-info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    count = validate(output)
    print(json.dumps({**info, "validated_pages": count, "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
