# Corso pratico su MARIO — Analisi Input-Output con Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/it-is-me-mario/deep-dive/blob/main/notebooks/Corso_MARIO.ipynb)

Materiale didattico per imparare a usare **[MARIO](https://mario-suite.readthedocs.io/)**
(*Multifunctional Analysis of Regions through Input-Output*), il pacchetto Python del
Politecnico di Milano / eNextGen per costruire e analizzare tabelle Input-Output (IOT) e
Supply & Use (SUT).

Il corso è costruito a partire dalla [user guide ufficiale](https://mario-suite.readthedocs.io/en/latest/user_guide/index.html)
ed è pensato per essere svolto su **Google Colab** da 10–20 studenti contemporaneamente.

## 📓 Il notebook

[`notebooks/Corso_MARIO.ipynb`](notebooks/Corso_MARIO.ipynb) è un notebook autoconsistente che copre,
in italiano e con celle eseguibili + esercizi:

| Parte | Argomenti |
|---|---|
| **1 — Fondamenti** | concetti IO (Z, Y, X, V, E, Leontief), parsing dei dati, ispezione, calcolo delle matrici, estrazione indicatori (PIL), visualizzazione, esportazione |
| **2 — Trasformazioni** | aggregazione, estensioni, analisi di shock/scenari, aggiunta/split di settori, SUT→IOT, MRIO→SRIO, Isard→Chenery-Moses |
| **3 — Avanzato** | gas serra (GHG), analisi delle catene di fornitura (trades, embodied, linkages), structural path analysis (SPA) |

Tutto il notebook gira sul **database di test integrato** in MARIO
(`mario.load_test("IOT")` / `"SUT"`): **nessun download pesante**, funziona identico per tutti.
Ogni cella di codice è stata eseguita end-to-end senza errori contro **mariopy 1.0.2**.

## 🚀 Come usarlo (studenti)

1. Apri il notebook su Colab (carica il file `.ipynb` su <https://colab.research.google.com>,
   oppure usa il pulsante *Open in Colab* dopo che il repo è su GitHub).
2. `File ▸ Salva una copia in Drive` per avere la tua copia personale.
3. Esegui le celle dall'alto verso il basso (`Shift + Invio`). La prima installa MARIO.
4. Completa le celle 🧩 **Esercizio**.

> ⚠️ Il pacchetto su PyPI si chiama **`mariopy`**, ma in Python si importa come **`mario`**.

## 🗄️ Database reali (EXIOBASE, EORA, FIGARO…)

I database reali sono troppo grandi per essere scaricati live in aula: vanno **scaricati a parte
e caricati da file locali**. Il notebook mostra il pattern (`download_*` + `parse_*`) nella
sezione 3.2. Su Colab si possono caricare con `google.colab.files.upload()` o montando Drive.

## 🔧 Per il docente / rigenerare il notebook

Il notebook è generato da uno script versionato, così è facile da mantenere e rivedere:

```bash
pip install -r requirements.txt
python tools/build_notebook.py        # rigenera notebooks/Corso_MARIO.ipynb
```

Per ri-validare che tutte le celle eseguano senza errori:

```bash
jupyter nbconvert --to notebook --execute --allow-errors \
  --output executed_check.ipynb notebooks/Corso_MARIO.ipynb
```

## 📚 Risorse

- User guide: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- Documentazione: <https://mario-suite.readthedocs.io/>
- Codice sorgente: <https://github.com/it-is-me-mario/MARIO>
