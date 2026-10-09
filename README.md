# Mietblick Website

Statische Produktwebsite für **https://mietblick-app.de**, veröffentlicht mit GitHub Pages.

## Website-Dateien

Das Repository enthält alle HTML-Seiten, Illustrationen, Fonts und Assets direkt im Hauptverzeichnis. Es gibt keine Laufzeit-Abhängigkeit von Node, einem Backend oder einem CDN. Inter ist lokal einschließlich OFL-Lizenz enthalten.

## Lokal ansehen und prüfen

```sh
python3 -m http.server 4173 --bind 127.0.0.1
python3 scripts/check-site.py
node --check assets/site.js
```

Die Vorschau ist unter `http://127.0.0.1:4173` erreichbar. SEO-Metadaten lassen sich mit `python3 scripts/configure-seo.py` aktualisieren. Für das optionale Neurendern der Social-Grafik benötigt `scripts/generate-share-image.cjs` Node und `sharp`; alle fertigen Assets liegen bereits in `assets/`.


