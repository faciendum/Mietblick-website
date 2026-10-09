# Mietblick Website

Statische Website für Mietblick unter https://mietblick-app.de. Alle HTML-Seiten, Illustrationen, Fonts und Inhalte liegen in diesem Repository. Die Website lädt keine externen Fonts, Skripte oder Analytics-Dienste.

## Inhalt

- 26 Funktionsbereiche: 25 eigenständige Fachseiten und Mobil als Companion-Bereich.
- Acht ausführliche Vermieter-Ratgeber mit Inhaltsverzeichnis, Checklisten, FAQ und Originalquellen.
- iPhone & iPad Companion mit Geräte-Reitern und zwei Detailseiten.
- Fokussierte Mac-Startseite mit einer Produktillustration und dem Ablauf Immobilien → Mietvertrag → Mietkonto.
- Abgesetzter Header, direkter Funktionen-Link und separat bedienbares Menü; responsive Navigation, lokale Suche und Kategorienfilter.
- 42 HTML-Seiten insgesamt; 39 indexierbare URLs in der Sitemap.
- Lokale Inter-Schrift mit OFL-Lizenz und Illustrationen in Mietblick-Farben.

Die Funktionsseiten unterscheiden lokale Funktionen und Ausblick anhand des tatsächlichen Produktumfangs. Geplante OCR-, Abrechnungs-, Kautions- und Companion-Abläufe werden nicht als aktuell verfügbar beschrieben. App-Store-Download und geräteübergreifende Synchronisation werden nicht behauptet.

## Inhalte bearbeiten und Website neu erzeugen

Die redaktionellen Quellen liegen in `content/features.json` und `content/guides.json`. Die Startseite, Symbole und Rechtstexte liegen unter `templates/`. Der Generator rendert statisches HTML sowie Titel, Beschreibungen, Canonicals, Social-Metadaten, JSON-LD und Sitemap gemeinsam:

```sh
python3 scripts/build-site.py
python3 scripts/check-site.py
node --check assets/site.js
node --check assets/content.js
```

`configure-seo.py` ruft denselben Generator auf. Die ausgelieferte Website funktioniert ohne Laufzeit-Build, Paketmanager oder JavaScript-Abhängigkeiten. JavaScript verbessert Tabs, Filter, Menü und Animationen; die redaktionellen Texte und Links stehen vollständig im HTML.

## Lokale Vorschau

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Danach http://127.0.0.1:4173 öffnen.
