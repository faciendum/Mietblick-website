# Mietblick Website

Statische Website für Mietblick unter https://mietblick-app.de. Alle HTML-Seiten, Illustrationen, Fonts und Inhalte liegen in diesem Repository. Die Website lädt keine externen Fonts, Skripte oder Analytics-Dienste.

## Inhalt

- 26 Funktionsbereiche: 25 eigenständige Fachseiten und Mobil als Companion-Bereich.
- Acht ausführliche Vermieter-Ratgeber mit Inhaltsverzeichnis, Checklisten, FAQ und Originalquellen.
- iPhone & iPad Companion mit Geräte-Reitern, zwei Detailseiten und eigener redaktioneller Quelle.
- Mac-Startseite mit der Häuserillustration, Arbeitsweise Immobilien → Mietvertrag → Mietkonto und konkreten Vermieter-Anwendungsfällen.
- Fünf Navigationsziele: Funktionen, Arbeitsweise, Wobei hilft Mietblick?, iPhone & iPad und Ratgeber. Separat bedienbares Funktionsmenü, App-Store-CTA, lokale Suche und Kategorienfilter.
- 42 HTML-Seiten insgesamt; 39 indexierbare URLs in der Sitemap.
- Farbschema-Steuerung für System, Hell und Dunkel im Header und mobilen Menü. Die Auswahl wird lokal gespeichert; der Systemmodus folgt der Geräteeinstellung.
- Lokale Inter-Schrift mit OFL-Lizenz und Illustrationen in Mietblick-Farben.

Die Website beschreibt den vollständigen Produktumfang mit fertigen Funktions- und Companion-Texten. Die Inhalte sind nach Themen gegliedert und durch passende Verknüpfungen verbunden.

## Inhalte bearbeiten und Website neu erzeugen

Die redaktionellen Quellen liegen in `content/features.json`, `content/guides.json` und `content/mobile.json`. Die Startseite, Symbole und Rechtstexte liegen unter `templates/`. Der Generator rendert statisches HTML sowie Titel, Beschreibungen, Canonicals, Social-Metadaten, JSON-LD und Sitemap gemeinsam:

```sh
python3 scripts/build-site.py
python3 scripts/check-site.py
node --check assets/site.js
node --check assets/content.js
node --check assets/theme.js
```

`configure-seo.py` ruft denselben Generator auf. Die ausgelieferte Website funktioniert ohne Laufzeit-Build, Paketmanager oder JavaScript-Abhängigkeiten. JavaScript verbessert Tabs, Filter, Menü und Animationen; die redaktionellen Texte und Links stehen vollständig im HTML.

## Lokale Vorschau

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Danach http://127.0.0.1:4173 öffnen.

Der zentrale Wert `APP_STORE_URL` in `scripts/build-site.py` steuert die Store-Buttons. Bis zum Mietblick-Listing führen sie zur allgemeinen Mac-App-Store-Seite.
