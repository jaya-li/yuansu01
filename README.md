# Progetto onboarding (italiano)

## File nel progetto

- `index.html`: file principale dell'app demo (struttura, stili e logica interattiva).
- `download_assets.py`: scarica le risorse remote usate nell'HTML e aggiorna i riferimenti a percorsi locali.

## Apertura in locale

Apri direttamente nel browser:

- `file:///Users/bytedance/Desktop/yuansu01/index.html`

## Pubblicazione su GitHub e apertura su altri dispositivi

1. Entra nella cartella del progetto:
   - `cd "/Users/bytedance/Desktop/yuansu01"`
2. Localizza prima le risorse:
   - `python3 download_assets.py`
3. Lo script:
   - crea la cartella `assets/`
   - scarica immagini/video Figma usati dalla pagina
   - sostituisce automaticamente gli URL remoti con percorsi locali `./assets/...`
4. Carica l'intera cartella `yuansu01` su GitHub.
5. Sul dispositivo remoto, dopo il clone, apri `index.html`.

## Note

- Se non esegui `download_assets.py`, la pagina dipende ancora da risorse esterne (ad esempio Figma MCP) che potrebbero non essere disponibili altrove.
- Si consiglia di versionare anche la cartella `assets/` per garantire stabilita nel tempo.
