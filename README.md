## SEARCH

Questo script Python permette di cercare file nel sistema con vari filtri e di aprirli automaticamente con uno dei programmi predefiniti per il tipo di file specificato. È stato progettato per funzionare in modo simile al comando `find` di Linux.

## Caratteristiche

- Filtra i file per tipo (immagine, video, documento, audio, archivio, server)
- Filtra i file per estensione
- Filtra i file per nome
- Filtra i file per data di modifica (ultime 24 ore, ultimo mese, ultimo anno)
- Cerca ricorsivamente o non ricorsivamente
- Apre i file trovati con programmi predefiniti

## Utilizzo

### Esempi d'uso:

- Cerca tutti i file nel percorso corrente:
  ```sh
  python search.py .
  ```

- Cerca tutti i file PDF nel percorso corrente e aprili:
  ```sh
  python search.py . -e .pdf
  ```

- Cerca tutti i file di tipo immagine nel percorso corrente e aprili:
  ```sh
  python search.py . -t immagine
  ```

- Cerca tutti i file di tipo immagine modificati nelle ultime 24 ore:
  ```sh
  python search.py . -t immagine -f 24h
  ```

- Cerca tutti i file che contengono "report" nel nome e aprili:
  ```sh
  python search.py . -n report
  ```

- Cerca tutti i file di tipo video non ricorsivamente e aprili:
  ```sh
  python search.py . -t video -r
  ```

- Cerca tutti i file di configurazione del server nel percorso corrente e aprili:
  ```sh
  python search.py . -t server
  ```

## Opzioni

- `--tipo-file` (`-t`): Filtra per tipo di file (es. immagine, video, documento, audio, archivio, server)
- `--estensione` (`-e`): Filtra i file per estensione (es. `.txt`, `.pdf`)
- `--nome` (`-n`): Filtra i file per nome (es. "report")
- `--no-ricorsivo` (`-r`): Cerca non ricorsivamente nelle directory (default è ricorsivo)
- `--filtro-data` (`-f`): Filtra i file per data di modifica (24h, mese, anno)

## Installazione

1. Clona il repository:
   ```sh
   git clone https://github.com/tuo-username/tuo-repository.git
   ```
2. Spostati nella directory del repository:
   ```sh
   cd tuo-repository
   ```
3. Esegui lo script:
   ```sh
   python search.py [opzioni]
   ```

## Requisiti

- Python 3.x

## Licenza

MIT