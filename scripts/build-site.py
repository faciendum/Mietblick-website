#!/usr/bin/env python3
"""Render the complete, buildless Mietblick website from reviewed content."""
from pathlib import Path
from html import escape
from datetime import date
import json
import hashlib
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist' if (ROOT / 'dist').is_dir() else ROOT
DOMAIN = 'https://mietblick-app.de'
UPDATED = '2026-10-09'
# Replace the general Store destination with Mietblick's listing URL at release.
APP_STORE_URL = 'https://apps.apple.com/de/mac/discover'
FEATURES = json.loads((ROOT / 'content/features.json').read_text())
GUIDES = json.loads((ROOT / 'content/guides.json').read_text())
MOBILE = json.loads((ROOT / 'content/mobile.json').read_text())
BY_FEATURE = {item['slug']: item for item in FEATURES}
BY_GUIDE = {item['slug']: item for item in GUIDES}
SYMBOLS = (ROOT / 'templates/symbols.html').read_text()
META = {}

def e(value):
    return escape(str(value), quote=True)

def icon(name):
    if name not in SYMBOLS:
        name = 'i-property'
    return f'<svg class="icon" aria-hidden="true" focusable="false"><use href="#{e(name)}"/></svg>'

def brand():
    return '<a class="brand" href="index.html" aria-label="Mietblick Startseite"><span class="brand-symbol"><img src="assets/favicon.png" alt="" width="132" height="132"></span><span>Mietblick</span></a>'

def header(current):
    active_features = current == 'funktionen.html' or current.removesuffix('.html') in BY_FEATURE
    active_mobile = current in ('mobil.html','iphone-companion.html','ipad-companion.html')
    active_guides = current == 'ratgeber.html' or current.removesuffix('.html') in BY_GUIDE
    groups = [
        ('Bestand & Mietverhältnisse', [('immobilienverwaltung','Immobilien & Einheiten','Deinen Bestand strukturiert erfassen.'),('mietvertraege','Mietverträge','Vertragspartner, Laufzeiten und Mietentwicklung.')]),
        ('Mietkonten & Kosten', [('mietzahlungen','Mietzahlungen','Forderungen, Eingänge und offene Beträge.'),('kostenverwaltung','Kosten & Belege','Rechnungen und Objektanteile nachvollziehen.')]),
        ('Unterlagen & Daten', [('dokumentenverwaltung','Dokumente','Originale im richtigen Zusammenhang.'),('datensicherung','Datensicherung','Deinen lokalen Bestand sichern und exportieren.')])
    ]
    mega = ''.join('<div class="mega-column"><h2>'+e(label)+'</h2>'+''.join(f'<a href="{slug}.html">{icon(BY_FEATURE[slug]["icon"])}<span><strong>{e(name)}</strong><small>{e(copy)}</small></span><span class="mega-link-arrow" aria-hidden="true">↗</span></a>' for slug,name,copy in items)+'</div>' for label,items in groups)
    feature_current = ' aria-current="page"' if current == 'funktionen.html' else ''
    return f'''<header class="site-header"><div class="nav-shell container">{brand()}
      <nav class="desktop-nav" aria-label="Hauptnavigation"><div class="nav-dropdown{' nav-section-active' if active_features else ''}" data-nav-dropdown><div class="nav-dropdown-control"><a class="nav-link" href="funktionen.html"{feature_current}>Funktionen</a><button class="nav-dropdown-toggle" type="button" aria-expanded="false" aria-controls="feature-menu" aria-label="Funktionsmenü" hidden><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button></div><div class="mega-menu" id="feature-menu" hidden><div class="mega-heading"><div><span class="mini-label">MIETBLICK FÜR MAC</span><strong>Deine Mietverwaltung im Detail.</strong></div><a class="text-link" href="funktionen.html">Alle Funktionen <span aria-hidden="true">↗</span></a></div><div class="mega-grid">{mega}</div><div class="mega-footer"><span>Immobilien, Mietverhältnisse und Mietkonten. Klar verbunden.</span><a href="funktionen.html">Alle 26 Funktionsbereiche <span aria-hidden="true">↗</span></a></div></div></div><a class="nav-link" href="index.html#arbeitsweise">Arbeitsweise</a><a class="nav-link" href="index.html#wobei-hilft-mietblick">Wobei hilft Mietblick?</a><a class="nav-link{' nav-section-active' if active_mobile else ''}" href="mobil.html"{' aria-current="page"' if current == 'mobil.html' else ''}>iPhone & iPad</a><a class="nav-link{' nav-section-active' if active_guides else ''}" href="ratgeber.html"{' aria-current="page"' if current == 'ratgeber.html' else ''}>Ratgeber</a></nav>
      <a class="button button-small header-cta app-store-link" href="{APP_STORE_URL}" target="_blank" rel="noopener" aria-label="App Store öffnen">Im App Store <span aria-hidden="true">↗</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menü öffnen"><span></span><span></span></button></div>
      <nav id="mobile-nav" class="mobile-nav container" aria-label="Mobile Navigation" hidden><a href="index.html">Mietblick für Mac</a><a href="funktionen.html">Funktionen</a><a href="index.html#arbeitsweise">Arbeitsweise</a><a href="index.html#wobei-hilft-mietblick">Wobei hilft Mietblick?</a><a href="mobil.html">iPhone & iPad Companion</a><a href="ratgeber.html">Ratgeber für Vermieter</a><div class="mobile-shortcuts"><a href="immobilienverwaltung.html">Immobilien & Einheiten</a><a href="mietzahlungen.html">Mietzahlungen</a><a href="kostenverwaltung.html">Kosten & Belege</a><a href="datensicherung.html">Datensicherung</a></div><a class="mobile-store-link" href="{APP_STORE_URL}" target="_blank" rel="noopener" aria-label="App Store öffnen">Im App Store laden ↗</a></nav></header>'''

def footer():
    return f'''<footer class="footer container"><div class="footer-main"><div>{brand()}<p>Einfach vermieten. Alles im Blick.<br>Für private Vermieter. Von Justanothercoder.</p></div><div><strong>Mietblick</strong><a href="index.html#arbeitsweise">Arbeitsweise</a><a href="index.html#wobei-hilft-mietblick">Wobei hilft Mietblick?</a><a href="funktionen.html">Alle Funktionen</a><a href="immobilienverwaltung.html">Immobilienverwaltung</a><a href="mietvertraege.html">Mietverträge</a><a href="mietzahlungen.html">Mietzahlungen</a><a href="kostenverwaltung.html">Kosten & Belege</a><a href="mobil.html">iPhone & iPad Companion</a></div><div><strong>Wissen & Antworten</strong><a href="ratgeber.html">Alle Ratgeber</a><a href="ratgeber-mietkonto.html">Mietkonto führen</a><a href="ratgeber-nebenkostenabrechnung.html">Nebenkosten vorbereiten</a><a href="ratgeber-wohnungsuebergabe.html">Wohnungsübergabe</a><a href="datenschutz.html">Datenschutz</a><a href="impressum.html">Impressum</a></div><div><strong>Im Gespräch bleiben</strong><a href="mailto:hallo@justanothercoder.de?subject=Hallo%20Mietblick">hallo@justanothercoder.de ↗</a><a href="https://www.justanothercoder.de/" target="_blank" rel="noopener">Justanothercoder ↗</a><button class="motion-toggle" aria-pressed="false" hidden>Animationen pausieren <span aria-hidden="true">Ⅱ</span></button></div></div><div class="footer-bottom"><span>© 2026 Mietblick · Justanothercoder</span><span>Mit Klarheit gestaltet. Mit Sorgfalt entwickelt.</span><a href="#top">Nach oben ↑</a></div></footer>'''

def canonical(filename):
    return DOMAIN + ('/' if filename == 'index.html' else '/' + filename)

def schema(filename, title, description, breadcrumbs, kind, article=None, collection=None):
    url = canonical(filename)
    org = {'@type':'Organization','@id':DOMAIN+'/#organization','name':'Mietblick','url':DOMAIN+'/', 'email':'hallo@justanothercoder.de'}
    site = {'@type':'WebSite','@id':DOMAIN+'/#website','name':'Mietblick','url':DOMAIN+'/', 'inLanguage':'de-DE','publisher':{'@id':org['@id']}}
    page = {'@type':kind,'@id':url+'#webpage','url':url,'name':title,'description':description,'inLanguage':'de-DE','isPartOf':{'@id':site['@id']}}
    graph = [org, site, page]
    if breadcrumbs:
        graph.append({'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':canonical(target)} for i,(name,target) in enumerate(breadcrumbs)]})
    if article:
        article_node = {'@type':'Article','@id':url+'#article','headline':article['title'],'description':description,'mainEntityOfPage':{'@id':page['@id']},'author':{'@id':org['@id']},'publisher':{'@id':org['@id']},'datePublished':UPDATED+'T12:00:00+02:00','dateModified':UPDATED+'T12:00:00+02:00','inLanguage':'de-DE','image':[DOMAIN+'/assets/social-preview.png'],'citation':[source['url'] for source in article['sources']]}
        page['mainEntity'] = {'@id':article_node['@id']}
        graph.append(article_node)
    elif filename not in ('impressum.html','datenschutz.html','404.html'):
        app = {'@type':'SoftwareApplication','@id':DOMAIN+'/#app','name':'Mietblick','url':DOMAIN+'/','applicationCategory':'BusinessApplication','operatingSystem':'macOS 14+','inLanguage':'de-DE','description':'Native Mietverwaltung mit lokalen Immobilien, Mietverhältnissen, Mietforderungen, Zahlungen, Kosten und Originaldateien.','featureList':[feature['short_title'] for feature in FEATURES]+['iPhone & iPad Companion'],'publisher':{'@id':org['@id']}}
        graph.append(app)
        page['about'] = {'@id':app['@id']}
    if collection:
        page['mainEntity'] = {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':label,'url':canonical(target)} for i,(label,target) in enumerate(collection)]}
    return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2)

def write_page(filename, title, description, body, breadcrumbs=None, kind='WebPage', article=None, collection=None, indexable=True):
    url = canonical(filename)
    META[filename] = (title,description,indexable)
    tags = [f'<meta name="description" content="{e(description)}">',f'<link rel="canonical" href="{url}">',f'<meta name="robots" content="{"index,follow,max-image-preview:large" if indexable else "noindex,follow"}">']
    values = {'type':'article' if article else 'website','locale':'de_DE','site_name':'Mietblick','title':title,'description':description,'url':url,'image':DOMAIN+'/assets/social-preview.png','image:width':'1200','image:height':'630','image:alt':'Mietblick · Mietverwaltung. Auf deinem Mac.'}
    tags += [f'<meta property="og:{key}" content="{e(value)}">' for key,value in values.items()]
    tags += [f'<meta name="twitter:{key}" content="{e(value)}">' for key,value in {'card':'summary_large_image','title':title,'description':description,'image':DOMAIN+'/assets/social-preview.png'}.items()]
    if article:
        tags += [f'<meta property="article:published_time" content="{UPDATED}T12:00:00+02:00">',f'<meta property="article:modified_time" content="{UPDATED}T12:00:00+02:00">']
    head = '\n'.join(tags)
    structured = schema(filename,title,description,breadcrumbs,kind,article,collection)
    html = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="color-scheme" content="light"><meta name="theme-color" content="#18324A"><link rel="icon" href="assets/favicon.png" type="image/png" sizes="132x132"><link rel="preload" href="assets/fonts/InterVariable.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="assets/tokens.css"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/content.css"><link rel="stylesheet" href="assets/home.css"><script src="assets/site.js" defer></script><script src="assets/content.js" defer></script>{head}<script type="application/ld+json">{structured}</script><noscript><style>.feature-tabs,.menu-toggle{{display:none!important}}.feature-panel[hidden]{{display:grid!important}}.mobile-nav[hidden]{{display:grid!important}}@media(min-width:1161px){{.mobile-nav[hidden]{{display:none!important}}}}@media(max-width:1160px){{.site-header{{position:static}}}}</style></noscript></head><body id="top"><a class="skip-link" href="#inhalt">Zum Inhalt springen</a>{SYMBOLS}{header(filename)}{body}{footer()}</body></html>'''
    html = re.sub(r'((?:href|src)="assets/[^"?]+\.(?:css|js))"', lambda match: match[1]+'?v='+hashlib.sha256((DIST/match[1].split('="',1)[1]).read_bytes()).hexdigest()[:10]+'"', html)
    if filename == '404.html':
        html = re.sub(r'(href|src)="((?!https?:|mailto:|#|/)[^"]+)"', r'\1="/\2"', html)
    (DIST / filename).write_text(html)

def breadcrumb(items):
    return '<nav class="breadcrumb" aria-label="Brotkrümelnavigation">'+''.join((('<span aria-hidden="true">/</span>' if i else '')+ (f'<span aria-current="page">{e(name)}</span>' if i == len(items)-1 else f'<a href="{target}">{e(name)}</a>')) for i,(name,target) in enumerate(items))+'</nav>'

def feature_card(item, filterable=False):
    attrs = f' data-directory-card data-category="{e(item["category"])}" data-search="{e((item["short_title"]+" "+item["description"]).lower())}"' if filterable else ''
    return f'''<a class="directory-card reveal" href="{item['slug']}.html"{attrs}><div class="card-top">{icon(item['icon'])}</div><span class="mini-label">{e(item['category'])}</span><h3>{e(item['short_title'])}</h3><p>{e(item['description'])}</p><span class="card-link">Mehr erfahren <span aria-hidden="true">↗</span></span></a>'''

def guide_card(item):
    return f'''<a class="guide-card reveal" href="{item['slug']}.html"><div class="guide-card-art" aria-hidden="true">{icon('i-documents')}<span>{e(item['category'])}</span><i></i><i></i><i></i></div><div class="guide-card-copy"><span class="mini-label">{e(item['category'])} · {e(item['read_minutes'])} MIN. LESEZEIT</span><h3>{e(item['title'])}</h3><p>{e(item['description'])}</p><span class="card-link">Ratgeber lesen <span aria-hidden="true">↗</span></span></div></a>'''

def faq(items):
    return '<section class="detail-faq" id="fragen"><span class="mini-label">GUT ZU WISSEN</span><h2>Häufige Fragen</h2><div class="faq-list">'+''.join(f'<details><summary>{e(item["question"])}<span aria-hidden="true">+</span></summary><div><p>{item["answer"]}</p></div></details>' for item in items)+'</div></section>'

def toc(sections, extra=None):
    links = [(s['id'],s['title']) for s in sections]+(extra or [])
    return '<aside class="article-toc"><nav aria-label="Inhaltsverzeichnis"><span class="mini-label">AUF DIESER SEITE</span>'+''.join(f'<a href="#{e(id_)}">{e(label)}</a>' for id_,label in links)+'</nav><div class="toc-note">Einfach vermieten.<br>Alles im Blick.</div></aside>'

def section_html(section):
    return f'<section class="prose-section" id="{e(section["id"])}"><h2>{e(section["title"])}</h2>'+''.join(f'<p>{p}</p>' for p in section['paragraphs'])+('<ul class="article-checklist">'+''.join(f'<li>{b}</li>' for b in section['bullets'])+'</ul>' if section.get('bullets') else '')+'</section>'

def related_features(slugs):
    items=[BY_FEATURE[s] for s in slugs if s in BY_FEATURE]
    if not items: return ''
    return '<section class="section container"><div class="section-heading"><h2>Das passt dazu.</h2><p>Die richtigen Verbindungen machen deine Mietverwaltung übersichtlicher.</p></div><div class="directory-grid">'+''.join(feature_card(i) for i in items[:3])+'</div></section>'

def related_guides(slugs, heading='Wissen für deinen Alltag.'):
    items=[BY_GUIDE[s] for s in slugs if s in BY_GUIDE]
    if not items: return ''
    return f'<section class="section container"><div class="section-heading"><h2>{heading}</h2><a class="text-link" href="ratgeber.html">Alle Ratgeber ↗</a></div><div class="guide-grid">'+''.join(guide_card(i) for i in items[:3])+'</div></section>'

def feature_visual(item):
    nodes = item['benefits'][:3]
    return f'''<figure class="feature-visual reveal" data-parallax><div class="visual-orbit" aria-hidden="true"><div class="visual-center">{icon(item['icon'])}<strong>{e(item['short_title'])}</strong></div>{''.join(f'<div class="visual-node node-{i}">{icon(["i-property","i-leases","i-selected"][i])}<span>{e(n["title"])}</span></div>' for i,n in enumerate(nodes))}<svg class="visual-connections" viewBox="0 0 500 400"><path d="M250 200 105 70M250 200 415 150M250 200 220 335"/></svg><span class="visual-dot dot-one"></span><span class="visual-dot dot-two"></span></div><figcaption>Illustration · {e(item['short_title'])} im Zusammenhang.</figcaption></figure>'''

def feature_page(item):
    slug=item['slug']; filename=slug+'.html'
    crumbs=[('Mietblick','index.html'),('Funktionen','funktionen.html'),(item['short_title'],filename)]
    sections=[dict(s,id=f'abschnitt-{i+1}') for i,s in enumerate(item['sections'])]
    body=f'''<main id="inhalt"><section class="detail-hero container">{breadcrumb(crumbs)}<div class="detail-hero-grid"><div><span class="pill">{e(item['category'])}</span><h1>{e(item['title'])}</h1><p class="detail-lead">{item['intro']}</p><div class="detail-actions"><a class="button" href="#ueberblick">Im Detail entdecken ↓</a><a class="text-link" href="funktionen.html">Alle Funktionen ↗</a></div></div>{feature_visual(item)}</div></section><section class="benefit-strip container" id="ueberblick">{''.join(f'<article class="reveal"><span class="benefit-number">0{i+1}</span><h2>{e(b["title"])}</h2><p>{e(b["text"])}</p></article>' for i,b in enumerate(item['benefits'][:3]))}</section><div class="article-layout container">{toc(sections, [('fragen','Häufige Fragen')])}<div class="article-prose">{''.join(section_html(s) for s in sections)}{faq(item['faq'])}<div class="article-cta"><strong>Deine Vermietung. Gut organisiert.</strong><p>Entdecke die Funktionen von Mietblick im Zusammenhang.</p><a class="button" href="funktionen.html">Zur Funktionsübersicht ↗</a></div></div></div>{related_features(item['related'])}{related_guides(item['guide_slugs'])}</main>'''
    write_page(filename,item['title']+' | Mietblick',item['description'],body,crumbs)

def guide_page(item):
    filename=item['slug']+'.html'
    crumbs=[('Mietblick','index.html'),('Ratgeber','ratgeber.html'),(item['title'],filename)]
    sources='<section class="article-sources" id="quellen"><h2>Quellen & Grundlagen</h2><p>Amtliche Informationen und praktische Grundlagen zum Nachlesen. Rechtsstand der verlinkten Grundlagen: 9. Oktober 2026.</p><ul>'+''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["title"])} ↗</a></li>' for s in item['sources'])+'</ul><p class="editorial-note">Dieser Ratgeber vermittelt allgemeine Informationen zur Organisation deiner Vermietung. Bei rechtlichen oder steuerlichen Einzelfragen kommt es auf den konkreten Sachverhalt an.</p></section>'
    others=[g['slug'] for g in GUIDES if g['slug']!=item['slug']][:3]
    body=f'''<main id="inhalt"><div class="reading-progress" aria-hidden="true"><span></span></div><header class="article-header container">{breadcrumb(crumbs)}<span class="pill">Ratgeber · {e(item['category'])}</span><h1>{e(item['title'])}</h1><p class="article-intro">{item['intro']}</p><div class="article-meta"><span>Von Mietblick</span><time datetime="{UPDATED}">Aktualisiert am 9. Oktober 2026</time><span>{item['read_minutes']} Minuten Lesezeit</span></div></header><div class="article-layout container" data-reading-article>{toc(item['sections'],[('fragen','Häufige Fragen'),('quellen','Quellen & Grundlagen')])}<article class="article-prose">{''.join(section_html(s) for s in item['sections'])}{faq(item['faq'])}{sources}<div class="article-cta"><strong>Wissen in Ordnung bringen.</strong><p>Mietblick verbindet Immobilien, Mietkonten, Kosten und Originalbelege in einer lokalen Vermieter-App.</p><a class="button" href="funktionen.html">Mietblick kennenlernen ↗</a></div></article></div>{related_features(item['related_features'])}{related_guides(others,'Weiterlesen. Weiterdenken.')}</main>'''
    write_page(filename,item['title']+' | Mietblick Ratgeber',item['description'],body,crumbs,article=item)

def overview():
    categories=list(dict.fromkeys(f['category'] for f in FEATURES))
    filters=''.join(f'<button type="button" data-filter="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in categories)
    groups=''.join(f'<div data-card-group><div class="directory-group-heading"><div><span class="mini-label">MIETBLICK IM DETAIL</span><h2>{e(category)}</h2></div></div><div class="directory-grid">'+''.join(feature_card(f,True) for f in FEATURES if f['category']==category)+'</div></div>' for category in categories)
    body=f'''<main id="inhalt"><section class="directory-hero container">{breadcrumb([('Mietblick','index.html'),('Funktionen','funktionen.html')])}<span class="pill">Die Funktionsübersicht</span><h1>Für jedes Detail.<br>Ein <span class="teal">guter Zusammenhang.</span></h1><p>Vom ersten Objekt bis zur geordneten Abrechnung: Entdecke die Funktionen von Mietblick. Immobilien, Mietverhältnisse, Zahlungen und Unterlagen greifen ineinander – am Mac und beim Termin vor Ort.</p><div class="overview-stats"><span><strong>26</strong> Funktionsbereiche</span><span>Mac · iPhone · iPad</span><span>{icon('i-privacy')} Lokal & ohne Mietblick-Konto</span></div></section><section class="directory-section container" data-directory><span id="ausblick" hidden></span><div class="directory-controls" hidden><div class="filter-chips" role="group" aria-label="Funktionsbereiche filtern"><button type="button" data-filter="all" aria-pressed="true">Alle Bereiche</button>{filters}</div><label class="directory-search"><span>Funktion suchen</span><input type="search" placeholder="z. B. Kosten, Mietkonto, Dokumente" autocomplete="off" data-directory-search></label><p class="directory-result" aria-live="polite" aria-atomic="true"></p></div>{groups}<p class="directory-empty" hidden>Für diese Suche gibt es keinen passenden Bereich. Wähle „Alle Bereiche“ oder ändere deinen Suchbegriff.</p></section><section class="mobile-promo container reveal"><div><span class="mini-label">IPHONE & IPAD COMPANION</span><h2>Dein Bestand.<br>Auch vor Ort im Blick.</h2><p>Objektakten, Dokumente und Aufgaben begleiten dich zum Termin. Fotos, Zählerstände und Übergaben erfasst du auf iPhone und iPad direkt am Objekt.</p><a class="button" href="mobil.html">iPhone & iPad entdecken ↗</a></div><img src="assets/illustrations/companion.svg" alt="Illustration eines iPhones und iPads mit Immobilien-, Dokument- und Aufgabensymbolen" width="700" height="480" loading="lazy"></section>{related_guides([g['slug'] for g in GUIDES[:3]])}</main>'''
    collection=[(f['short_title'],f['slug']+'.html') for f in FEATURES]+[('iPhone & iPad Companion','mobil.html')]
    write_page('funktionen.html','Alle Funktionen der Vermieter-App für Mac | Mietblick','Alle Funktionen von Mietblick: Immobilien, Mietverträge, Mietkonten, Kosten, Abrechnungen, Dokumente und Übergaben. Mit Companion-Apps für iPhone und iPad.',body,[('Mietblick','index.html'),('Funktionen','funktionen.html')],kind='CollectionPage',collection=collection)

def guide_overview():
    body=f'''<main id="inhalt"><section class="directory-hero container">{breadcrumb([('Mietblick','index.html'),('Ratgeber','ratgeber.html')])}<span class="pill">Wissen für private Vermieter</span><h1>Gut vorbereitet.<br><span class="teal">Klar vermieten.</span></h1><p>Praktische Ratgeber für deine Mietverwaltung. Mit nachvollziehbaren Abläufen, hilfreichen Checklisten und verlinkten Originalquellen – vom Mietkonto bis zur Wohnungsübergabe.</p></section><section class="container guide-library"><div class="guide-grid">{''.join(guide_card(g) for g in GUIDES)}</div></section><section class="editorial-panel container"><div>{icon('i-documents')}<h2>Wissen, das im Alltag hilft.</h2></div><p>Die Ratgeber werden von Mietblick anhand der angegebenen amtlichen Quellen zusammengestellt. Jeder Artikel nennt seinen Aktualisierungsstand und erklärt die Schritte unabhängig von einer bestimmten Software. Bei rechtlichen und steuerlichen Einzelfragen ist eine individuelle Prüfung erforderlich.</p><a class="text-link" href="mailto:hallo@justanothercoder.de?subject=Hinweis%20zum%20Mietblick-Ratgeber">Hinweis zu einem Ratgeber senden ↗</a></section></main>'''
    write_page('ratgeber.html','Ratgeber für private Vermieter: Mietkonto, Kosten & Übergabe | Mietblick','Praktische Vermieter-Ratgeber zu Mietverwaltung, Mietkonto, Nebenkosten, Wohnungsübergabe, Kosten, Kaution, Zählerständen und Datensicherung. Mit Originalquellen.',body,[('Mietblick','index.html'),('Ratgeber','ratgeber.html')],kind='CollectionPage',collection=[(g['title'],g['slug']+'.html') for g in GUIDES])

def companion_art(device):
    if device == 'iPhone':
        return f'<div class="mobile-device-art phone-art" aria-hidden="true"><div class="device-shell"><span class="device-camera"></span><span class="mini-label">MIETBLICK</span>{icon("i-property")}<strong>Dein Objekt</strong><div class="device-row">{icon("i-documents")}<span>Unterlagen</span></div><div class="device-row">{icon("i-tasks")}<span>Aufgaben</span></div><div class="device-row">{icon("i-leases")}<span>Mietverhältnisse</span></div></div><span class="device-float">Ein kurzer Blick. ↗</span></div>'
    return f'<div class="mobile-device-art tablet-art" aria-hidden="true"><div class="device-shell"><span class="device-camera"></span><aside>{icon("i-property")}{icon("i-leases")}{icon("i-documents")}{icon("i-tasks")}</aside><div><span class="mini-label">MIETBLICK</span><strong>Deine Objektakte</strong><div class="tablet-cards"><span>{icon("i-property")}Einheiten</span><span>{icon("i-documents")}Unterlagen</span></div><div class="tablet-lines"><i></i><i></i><i></i></div></div></div><span class="device-float">Mehr Platz für Details.</span></div>'

def mobile():
    item=MOBILE['overview']
    crumbs=[('Mietblick','index.html'),('iPhone & iPad','mobil.html')]
    tabs=''.join(f'<button role="tab" id="tab-{tab["id"]}" aria-controls="panel-{tab["id"]}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{e(tab["label"])}</button>' for i,tab in enumerate(item['tabs']))
    panels=''.join(f'''<div class="feature-panel" id="panel-{tab['id']}" role="tabpanel" aria-labelledby="tab-{tab['id']}" tabindex="0"{'' if i==0 else ' hidden'}><div class="panel-copy"><span class="mini-label">{e(tab['eyebrow'])}</span><h3>{tab['heading']}</h3><p>{tab['text']}</p><ul class="check-list">{''.join('<li>'+e(check)+'</li>' for check in tab['checks'])}</ul><a class="text-link panel-detail-link" href="{e(tab['href'])}">{e(tab['link_label'])} ↗</a></div>{companion_art(tab['device'])}</div>''' for i,tab in enumerate(item['tabs']))
    benefits=''.join(f'<article class="reveal">{icon(benefit["icon"])}<h3>{e(benefit["title"])}</h3><p>{e(benefit["text"])}</p></article>' for benefit in item['benefits'])
    principles=''.join(f'<div><strong>{e(principle["title"])}</strong><p>{e(principle["text"])}</p></div>' for principle in item['principles'])
    body=f'''<main id="inhalt"><section class="detail-hero container">{breadcrumb(crumbs)}<div class="detail-hero-grid"><div><span class="pill">iPhone & iPad Companion</span><h1>{item['heading']}</h1><p class="detail-lead">{item['introduction']}</p><div class="detail-actions"><a class="button" href="#geraete">iPhone & iPad entdecken ↓</a><a class="text-link" href="funktionen.html">Alle Funktionen ↗</a></div></div><figure class="companion-hero reveal"><img src="assets/illustrations/companion.svg" width="700" height="480" alt="Illustration eines iPhones und eines iPads mit abstrakten Immobilienakten"><figcaption>Illustration · Mietverwaltung am Ort des Geschehens.</figcaption></figure></div></section><section class="container mobile-tabs-section" id="geraete"><div class="section-heading"><h2>{item['tabs_heading']}</h2><p>{item['tabs_introduction']}</p></div><div class="feature-explorer mobile-explorer" data-tabs><div class="feature-tabs" role="tablist" aria-label="Companion-Geräte">{tabs}</div>{panels}</div></section><section class="section container"><div class="section-heading"><h2>{item['benefits_heading']}</h2><p>{item['benefits_introduction']}</p></div><div class="benefit-strip mobile-benefits">{benefits}</div></section><section class="mobile-principles"><div class="container"><span class="mini-label">NATIV. BEWUSST. KLAR.</span><h2>{item['principles_heading']}</h2><div class="device-notes">{principles}</div></div></section>{related_features(['immobilienverwaltung','dokumentenverwaltung','aufgaben-fristen'])}{related_guides(['ratgeber-wohnungsuebergabe','ratgeber-zaehlerstaende','ratgeber-datensicherung'])}</main>'''
    write_page('mobil.html',item['title'],item['description'],body,crumbs)
    for device in ['iphone','ipad']:
        device_page(MOBILE[device])

def device_page(item):
    filename=item['filename']; device=item['device']; sections=item['sections']
    crumbs=[('Mietblick','index.html'),('iPhone & iPad','mobil.html'),(device+' Companion',filename)]
    body=f'<main id="inhalt"><section class="article-header container">{breadcrumb(crumbs)}<span class="pill">{e(device)} Companion</span><h1>{item["heading"]}</h1><p class="article-intro">{item["intro"]}</p><img class="companion-detail-image" src="assets/illustrations/companion.svg" alt="Illustration: iPhone und iPad als mobile Begleiter für Immobilien und Unterlagen" width="700" height="480"></section><div class="article-layout container">{toc(sections)}<article class="article-prose">'+''.join(section_html(section) for section in sections)+'<div class="article-cta"><strong>Beide Companion-Geräte entdecken.</strong><p>iPhone und iPad im Vergleich – für deine Termine vor Ort.</p><a class="button" href="mobil.html">Zu iPhone & iPad ↗</a></div></article></div>'+related_guides(['ratgeber-wohnungsuebergabe','ratgeber-zaehlerstaende'])+'</main>'
    write_page(filename,item['title'],item['description'],body,crumbs)

def home():
    body=(ROOT/'templates/home.html').read_text().replace('https://apps.apple.com/de/', APP_STORE_URL)
    write_page('index.html','Die Vermieter-App für Mac: Mietverwaltung lokal organisieren | Mietblick','Mietblick ist die native Vermieter-App für Mac. Immobilien, Mietverträge, Mietkonten, Kosten und Belege strukturiert verwalten. Lokal und ohne Mietblick-Konto.',body)


for feature in FEATURES:
    feature_page(feature)
for guide in GUIDES:
    guide_page(guide)
overview()
guide_overview()
mobile()
home()
for filename,label,description in [('datenschutz.html','Datenschutz','Informationen zum Datenschutz der Mietblick-Website und zur lokalen Datenspeicherung der App.'),('impressum.html','Impressum','Anbieterkennzeichnung und Kontakt für Mietblick von Justanothercoder.')]:
    write_page(filename,label+' | Mietblick',description,(ROOT/f'templates/{filename}').read_text(),[('Mietblick','index.html'),(label,filename)],indexable=False)
write_page('404.html','Seite nicht gefunden | Mietblick','Diese Seite wurde nicht gefunden. Entdecke die Funktionen und Ratgeber von Mietblick.', '<main id="inhalt" class="container not-found"><span class="pill">404 · Seite nicht gefunden</span><h1>Hier geht es<br><span class="teal">weiter.</span></h1><p>Die gesuchte Seite ist unter dieser Adresse nicht vorhanden. Über die Funktionsübersicht oder die Ratgeber findest du den passenden Einstieg.</p><div class="detail-actions"><a class="button" href="funktionen.html">Alle Funktionen ↗</a><a class="text-link" href="ratgeber.html">Zu den Ratgebern ↗</a></div></main>',indexable=False)
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
urlset=ET.Element(ns+'urlset')
for filename,(_,_,indexable) in META.items():
    if indexable:
        node=ET.SubElement(urlset,ns+'url')
        ET.SubElement(node,ns+'loc').text=canonical(filename)
        ET.SubElement(node,ns+'lastmod').text=UPDATED
ET.indent(urlset)
(DIST/'sitemap.xml').write_bytes(ET.tostring(urlset,encoding='utf-8',xml_declaration=True))
(DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
print(f'Rendered {len(META)} pages, {len(FEATURES)} feature details, {len(GUIDES)} guides and SEO metadata.')
