#!/usr/bin/env python3
"""Keep production SEO metadata, truthful structured data and sitemap in sync."""
import json
import re
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

DIST = Path(__file__).resolve().parents[1]
DOMAIN = 'https://mietblick-app.de'
PAGES = {
    'index.html': ('Vermieter-App für Mac, iPhone & iPad | Mietblick', 'Mietverwaltung für private Vermieter: Immobilien, Mietverträge, Mietzahlungen und Dokumente mit Mietblick auf Mac, iPhone und iPad verwalten. Lokal & ohne Konto.', 'Mietblick', True),
    'immobilienverwaltung.html': ('Immobilienverwaltung für private Vermieter | Mietblick', 'Immobilien und Wohnungen auf Mac, iPhone und iPad verwalten: Objekte, Einheiten, Flächen, Ausstattung und Mietverhältnisse mit Mietblick übersichtlich organisieren.', 'Immobilienverwaltung', True),
    'mietvertraege.html': ('Mietverträge verwalten auf Mac, iPhone & iPad | Mietblick', 'Mietverträge und Mietverhältnisse übersichtlich verwalten: Vertragspartner, Laufzeiten, Mietbestandteile, Mietänderungen und Originaldateien mit Mietblick organisieren.', 'Mietverträge', True),
    'mietzahlungen.html': ('Mietzahlungen verwalten & Mietkonto führen | Mietblick', 'Mietzahlungen und Mietforderungen im Blick: Zahlungseingänge, Teilzahlungen, Guthaben und Bank-CSV mit Mietblick auf Mac, iPhone und iPad nachvollziehen.', 'Mietzahlungen', True),
    'datenschutz.html': ('Datenschutz | Mietblick', 'Informationen zum Datenschutz der Mietblick-Website und zur lokalen Datenspeicherung deiner Vermieter-App.', 'Datenschutz', False),
    'impressum.html': ('Impressum | Mietblick', 'Anbieterkennzeichnung und Kontakt für Mietblick von Justanothercoder.', 'Impressum', False),
}
organization = {'@type':'Organization','@id':f'{DOMAIN}/#organization','name':'Mietblick','url':f'{DOMAIN}/','email':'hallo@justanothercoder.de'}
website = {'@type':'WebSite','@id':f'{DOMAIN}/#website','name':'Mietblick','alternateName':'Mietblick Vermieter-App','url':f'{DOMAIN}/','inLanguage':'de-DE','publisher':{'@id':f'{DOMAIN}/#organization'}}
app = {'@type':'SoftwareApplication','@id':f'{DOMAIN}/#app','name':'Mietblick','url':f'{DOMAIN}/','applicationCategory':'BusinessApplication','operatingSystem':'macOS 14+, iOS 17+, iPadOS 17+','inLanguage':'de-DE','description':'Native Mietverwaltung für private Vermieter mit Immobilien, Mietverhältnissen, Mietforderungen, Zahlungseingängen, Originaldateien und Aufgaben.','featureList':['Immobilien und Einheiten verwalten','Mietverhältnisse und Mietbestandteile organisieren','Monatliche Mietforderungen erzeugen','Zahlungseingänge und Teilzahlungen zuordnen','Bank-CSV importieren','Originaldateien ablegen','Aufgaben mit Fälligkeit verwalten','JSON- und CSV-Datenexport'],'publisher':{'@id':f'{DOMAIN}/#organization'}}
for filename,(title,description,label,indexable) in PAGES.items():
    path=DIST/filename
    if not path.exists(): raise SystemExit(f'Missing page: {filename}')
    content=path.read_text()
    content=re.sub(r'<title>.*?</title>',f'<title>{escape(title)}</title>',content,flags=re.S)
    content=re.sub(r'<meta\b[^>]*(?:name="(?:description|robots|twitter:[^"]+)"|property="og:[^"]+")[^>]*>', '', content)
    content=re.sub(r'<link\b[^>]*rel="(?:canonical|alternate)"[^>]*>', '', content)
    content=re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', content,flags=re.S)
    url=f'{DOMAIN}/' if filename=='index.html' else f'{DOMAIN}/{filename}'
    page={'@type':'WebPage','@id':f'{url}#webpage','url':url,'name':title,'description':description,'inLanguage':'de-DE','isPartOf':{'@id':f'{DOMAIN}/#website'},'about':{'@id':f'{DOMAIN}/#app'}}
    graph=[organization,website,app,page] if filename=='index.html' else [organization,website,page]
    if filename!='index.html':
        graph.append({'@type':'BreadcrumbList','@id':f'{url}#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Mietblick','item':f'{DOMAIN}/'},{'@type':'ListItem','position':2,'name':label,'item':url}]})
    tags=[f'<meta name="description" content="{escape(description,quote=True)}">',f'<link rel="canonical" href="{url}">',f'<meta name="robots" content="{"index,follow,max-image-preview:large" if indexable else "noindex,follow"}">']
    for key,value in {'type':'website','locale':'de_DE','site_name':'Mietblick','title':title,'description':description,'url':url,'image':f'{DOMAIN}/assets/social-preview.png','image:width':'1200','image:height':'630','image:alt':'Mietblick: Einfach vermieten. Alles im Blick. Illustration einer geordneten Immobilienwelt.'}.items():
        tags.append(f'<meta property="og:{key}" content="{escape(value,quote=True)}">')
    for key,value in {'card':'summary_large_image','title':title,'description':description,'image':f'{DOMAIN}/assets/social-preview.png'}.items():
        tags.append(f'<meta name="twitter:{key}" content="{escape(value,quote=True)}">')
    tags.append('<script type="application/ld+json">\n'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,indent=2)+'\n</script>')
    content=content.replace('</head>','\n'+'\n'.join(tags)+'\n</head>')
    path.write_text(content)

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
urlset=ET.Element(ns+'urlset')
for filename,(_,_,_,indexable) in PAGES.items():
    if not indexable: continue
    node=ET.SubElement(urlset,ns+'url')
    ET.SubElement(node,ns+'loc').text=f'{DOMAIN}/' if filename=='index.html' else f'{DOMAIN}/{filename}'
    ET.SubElement(node,ns+'lastmod').text='2026-10-09'
ET.indent(urlset)
(DIST/'sitemap.xml').write_bytes(ET.tostring(urlset,encoding='utf-8',xml_declaration=True))
(DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
print(f'SEO metadata, JSON-LD, sitemap and robots configured for {DOMAIN}.')
