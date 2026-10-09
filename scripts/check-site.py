#!/usr/bin/env python3
"""Validate the shipping site's internal URLs, images, IDs and SVG assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist' if (ROOT / 'dist').is_dir() else ROOT
errors = []
titles, descriptions, canonicals = set(), set(), set()
indexable = set()

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.references = path, set(), [], []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids: errors.append(f'{self.path.name}: duplicate ID {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'img' and 'alt' not in attrs: errors.append(f'{self.path.name}: image without alt')
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])
        for key in ('aria-controls', 'aria-labelledby'):
            self.references.extend(attrs.get(key, '').split())

pages = {path.resolve(): Page(path) for path in DIST.glob('*.html')}
for path, page in pages.items():
    source = path.read_text()
    for attribute,seen,pattern in [('title',titles,r'<title>(.*?)</title>'),('description',descriptions,r'<meta name="description" content="([^"]+)">'),('canonical',canonicals,r'<link rel="canonical" href="([^"]+)">')]:
        match = re.search(pattern, source, re.S)
        if not match: errors.append(f'{path.name}: missing {attribute}')
        elif match[1] in seen: errors.append(f'{path.name}: duplicate {attribute}')
        else: seen.add(match[1])
    if 'content="index,follow' in source: indexable.add(path.name)
    for block in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', source, re.S):
        try: json.loads(block)
        except json.JSONDecodeError: errors.append(f'{path.name}: invalid JSON-LD')
    if len(re.findall(r'<h1\b', source)) != 1: errors.append(f'{path.name}: expected one H1')
    if len(re.findall(r'rel="canonical"', source)) != 1: errors.append(f'{path.name}: expected one canonical URL')
    if 'https://mietblick-app.de/' not in source: errors.append(f'{path.name}: missing production domain')
    for ref in page.references:
        if ref not in page.ids: errors.append(f'{path.name}: missing ARIA target {ref}')
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        target = ((DIST / unquote(url.path).lstrip('/')) if url.path.startswith('/') else (path.parent / unquote(url.path))).resolve() if url.path else path
        if not target.exists(): errors.append(f'{path.name}: missing {link}')
        if url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{path.name}: missing fragment {link}')
for svg in DIST.rglob('*.svg'):
    try: ET.parse(svg)
    except ET.ParseError as exc: errors.append(f'{svg.name}: {exc}')
try:
    sitemap = ET.parse(DIST / 'sitemap.xml')
    sitemap_pages = set()
    for location in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        url = urlsplit(location.text)
        filename = url.path.lstrip('/') or 'index.html'
        sitemap_pages.add(filename)
        if url.netloc != 'mietblick-app.de' or not (DIST / filename).exists(): errors.append(f'Invalid sitemap URL: {location.text}')
    if sitemap_pages != indexable: errors.append('Sitemap and indexable pages differ')
except ET.ParseError: errors.append('Invalid sitemap XML')
if (ROOT / 'content/features.json').exists():
    features=json.loads((ROOT / 'content/features.json').read_text())
    requirements={f'R{i:02d}' for i in range(1,27)}-{'R23'}
    if {f['roadmap_id'] for f in features} != requirements: errors.append('Feature coverage incomplete')
    if len(features) != 25 or len({f['slug'] for f in features}) != 25: errors.append('Feature pages incomplete or duplicated')
    guides=json.loads((ROOT / 'content/guides.json').read_text())
    for guide in guides:
        text=guide['intro']+' '+' '.join(' '.join(s['paragraphs'])+' '+' '.join(s.get('bullets',[])) for s in guide['sections'])
        if len(re.sub(r'<[^>]*>','',text).split()) < 650: errors.append(f'{guide["slug"]}: guide too short')
        if not guide['sources']: errors.append(f'{guide["slug"]}: missing original sources')
        page_path=DIST/(guide['slug']+'.html')
        if not page_path.exists(): errors.append(f'{guide["slug"]}: missing article')
if not (DIST / 'assets/social-preview.png').exists(): errors.append('Missing social preview image')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, links, ARIA references, SVGs, JSON-LD, canonical URLs, H1s, social image and sitemap.')
