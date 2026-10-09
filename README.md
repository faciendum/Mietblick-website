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

## GitHub Pages

GitHub Pages veröffentlicht direkt vom Branch `main` und dem Hauptverzeichnis `/`. Jeder Push auf `main` startet die integrierte Pages-Veröffentlichung. `.nojekyll` kennzeichnet die fertige statische Website. Prüfe Änderungen vor dem Push mit den obigen Befehlen.

Die benutzerdefinierte Domain lautet `mietblick-app.de` und steht in `CNAME`. Das TLS-Zertifikat wird von GitHub Pages verwaltet. Voraussetzung sind die korrekten DNS-Einträge; anschließend wird HTTPS in den Pages-Einstellungen erzwungen.

DNS für die Hauptdomain:

- A `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- Optional AAAA `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
- CNAME `www`: `faciendum.github.io`

Alte abweichende A-/AAAA-Einträge werden ersetzt. Die Domain bleibt kanonisch unter `https://mietblick-app.de` erreichbar. Bei eingeschränkten CAA-Einträgen muss `letsencrypt.org` erlaubt sein.

[GitHub: eigene Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) · [GitHub: HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
