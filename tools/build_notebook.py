# -*- coding: utf-8 -*-
"""Genera il notebook didattico per il corso su MARIO.

Eseguire:  python tools/build_notebook.py
Produce:   notebooks/Corso_MARIO.ipynb

Il contenuto e' tarato sull'API reale di mariopy 1.0.2 (verificata localmente).
"""
import json
import os

CELLS = []


def _src(text):
    # nbformat vuole una lista di righe, ognuna con \n tranne (eventualmente) l'ultima
    return text.rstrip("\n").splitlines(keepends=True)


def md(text):
    CELLS.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": _src(text),
    })


def code(text):
    CELLS.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _src(text),
    })


# ---------------------------------------------------------------------------
# 0. Titolo e introduzione
# ---------------------------------------------------------------------------
md(r"""# Corso pratico su **MARIO** — Analisi Input-Output con Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/it-is-me-mario/deep-dive/blob/main/notebooks/Corso_MARIO.ipynb)

**MARIO** (*Multifunctional Analysis of Regions through Input-Output*) è un pacchetto Python
sviluppato dal Politecnico di Milano ed eNextGen per costruire e analizzare
**tabelle Input-Output (IOT)** e **tabelle Supply & Use (SUT)**, sia mono- che multi-regionali,
in unità monetarie o fisiche.

Questo notebook è pensato per essere eseguito su **Google Colab** da molti studenti
contemporaneamente: usa il **database di test integrato** in MARIO, quindi **non richiede
alcun download di dati pesanti** e funziona in modo identico per tutti.

---

### Come usare questo notebook (leggere prima di iniziare)

1. **Fai una copia tua**: menu `File ▸ Salva una copia in Drive`. Lavorerai sulla tua copia
   personale senza disturbare gli altri.
2. Esegui le celle **una alla volta**, dall'alto verso il basso (`Shift + Invio`).
3. Le celle marcate con 🧩 **Esercizio** sono per te: completa il codice dove vedi `# TODO`.
4. Le celle marcate con ⚙️ **Avanzato** mostrano l'API per workflow che richiedono dati reali:
   leggile, ma potrebbero non produrre un risultato numerico significativo sul mini-database di test.

> Tempo stimato: 2–3 ore. Buon lavoro! 🚀
""")

# ---------------------------------------------------------------------------
# 1. Setup
# ---------------------------------------------------------------------------
md(r"""## 1. Installazione e setup

Installiamo l'ultima versione di MARIO pubblicata su PyPI. ⚠️ Attenzione: il pacchetto su PyPI
si chiama **`mariopy`**, ma il modulo da importare in Python si chiama **`mario`**.

> La prima installazione richiede ~1 minuto. Se Colab chiede di **riavviare il runtime**
> (`Restart runtime`) dopo l'installazione, fallo e poi **riesegui** la cella di import.
""")

code(r"""# Installa MARIO (versione del corso) — eseguire una sola volta per sessione
%pip install -q mariopy==1.0.2""")

code(r"""import mario
import pandas as pd
import numpy as np

print("Versione di MARIO:", mario.__version__)

# Riduciamo la verbosità dei log per tenere pulito l'output del notebook
try:
    mario.set_log_verbosity("ERROR")
except Exception:
    pass""")

# ---------------------------------------------------------------------------
# 2. Concetti di base
# ---------------------------------------------------------------------------
md(r"""## 2. I concetti dell'analisi Input-Output (in 5 minuti)

Una tabella **Input-Output** descrive i flussi economici di un sistema:

- **Z** — matrice delle *transazioni intermedie*: quanto il settore *i* vende al settore *j*.
- **Y** — *domanda finale* (consumi delle famiglie, investimenti, esportazioni…).
- **X** — *produzione totale* di ogni settore.
- **V** — *fattori della produzione* / valore aggiunto (salari, tasse, capitale…).
- **E** — *conti satellite* / estensioni ambientali e sociali (CO₂, occupazione…).

Da queste matrici "di flusso" MARIO calcola le matrici "a **coefficienti**" e i modelli:

| Simbolo MARIO | Significato |
|---|---|
| `z` | coefficienti tecnici (Z normalizzata per la produzione) |
| `v`, `e` | coefficienti di valore aggiunto / conti satellite |
| `w` | inversa di Leontief, `w = (I − z)⁻¹` |
| `f` | intensità (footprint) dei conti satellite |
| `m` | moltiplicatori |
| `p` | indici di prezzo |

> In MARIO **le lettere maiuscole = flussi assoluti** (Z, V, E, Y, X) e
> **le minuscole = coefficienti** (z, v, e, w, f, m, p). Lo useremo continuamente.

Non serve ricordare tutto a memoria: MARIO calcola le matrici **automaticamente** quando servono.
""")

# ---------------------------------------------------------------------------
# 3. Parsing / caricamento dati
# ---------------------------------------------------------------------------
md(r"""## 3. Caricare i dati (parsing)

MARIO può leggere decine di database (EXIOBASE, EORA, FIGARO, WIOD, OECD, EUROSTAT…) oltre a
database personalizzati da Excel/CSV/Parquet. Per imparare useremo il **database di test integrato**,
che si carica con una sola riga e rappresenta un'economia giocattolo con 2 regioni e 3 settori.
""")

code(r"""# Carichiamo una tabella Input-Output di test
db = mario.load_test("IOT")

print(db)        # riepilogo: nome, tipo tabella, scenari, dimensioni di ogni set
print("\nTipo di tabella:", db.table_type)
print("Multi-regionale?", db.is_multi_region)""")

md(r"""### 3.1 Database personalizzato da Excel

Se hai i tuoi dati in un foglio Excel formattato secondo lo schema di MARIO, li carichi così:

```python
db = mario.parse_from_excel(
    path="mia_tabella.xlsx",
    table="IOT",      # oppure "SUT"
    mode="flows",     # "flows" (valori assoluti) o "coefficients"
)
```

Per ottenere un **template vuoto** già formattato da compilare:

```python
mario.write_parse_template(...)   # vedi help(mario.write_parse_template)
```
""")

md(r"""### 3.2 Database "grandi" (EXIOBASE, EORA, FIGARO…)

I database reali pesano da centinaia di MB a diversi GB: **vanno scaricati a parte e caricati da
file locali**, non on-the-fly in un'aula con 20 persone. Il flusso tipico è:

```python
# 1) Scarica una volta (richiede tempo e spazio su disco)
mario.download_exiobase_monetary(path="exiobase_data")   # esempio

# 2) Carica dai file scaricati
db = mario.parse_exiobase(
    table="IOT",
    unit="Monetary",
    path="exiobase_data",
)
```

> 💡 In Colab puoi caricare i file scaricati con `from google.colab import files; files.upload()`
> oppure montando Google Drive (`from google.colab import drive; drive.mount('/content/drive')`).
> Per il resto del corso restiamo sul database di test, che si comporta esattamente come uno reale.
""")

# ---------------------------------------------------------------------------
# 4. Ispezione di base
# ---------------------------------------------------------------------------
md(r"""## 4. Ispezione di base

Prima di calcolare qualsiasi cosa, esploriamo *cosa contiene* il database.
""")

code(r"""# Quali "set" (dimensioni) ha il database?
print("Set disponibili:", db.sets)

# Quali scenari? (di default ne esiste uno solo: 'baseline')
print("Scenari:", db.scenarios)

# Elenco degli elementi di un set
print("\nRegioni :", list(db.get_index("Region")))
print("Settori :", list(db.get_index("Sector")))
print("Fattori :", list(db.get_index("Factor of production")))
print("Conti satellite:", list(db.get_index("Satellite account")))""")

code(r"""# Cercare un'etichetta per nome (utile sui database reali con migliaia di settori)
print("Risultati ricerca 'Agri':", db.search("Sector", "Agri"))

# Indice completo di tutti i set in un colpo solo
db.get_index("all")""")

# ---------------------------------------------------------------------------
# 5. Calcolo delle matrici
# ---------------------------------------------------------------------------
md(r"""## 5. Calcolare le matrici

Il cuore di MARIO. Il metodo `calc_all([...])` calcola le matrici richieste **risolvendo
automaticamente tutte le dipendenze** (es. per `w` serve `z`, per `z` serve `Z` e `X`…).
Le matrici calcolate diventano poi accessibili come attributi (`db.X`, `db.z`, `db.w`, …) e
sono normali `pandas.DataFrame`.
""")

code(r"""# Calcoliamo le matrici principali
db.calc_all(["X", "z", "Z", "Y", "v", "e", "w"])

# Ora sono accessibili come DataFrame pandas
print("X (produzione totale) shape:", db.X.shape)
print("z (coefficienti tecnici) shape:", db.z.shape)
print("w (inversa di Leontief) shape:", db.w.shape)

db.z   # visualizziamo i coefficienti tecnici""")

code(r"""# La produzione totale per settore e regione
db.X""")

code(r"""# 'explain' spiega a parole come MARIO calcola una matrice
print(db.explain("w"))""")

md(r"""> ⚙️ **Su database grandi** l'inversione di Leontief può essere pesante. MARIO permette di
> controllare la strategia di calcolo con `mario.ComputeOptions(...)` passata a
> `db.resolve("w", compute_options=...)`. Per il database di test non serve.
""")

# ---------------------------------------------------------------------------
# 6. Estrazione dati e indicatori
# ---------------------------------------------------------------------------
md(r"""## 6. Estrarre dati e indicatori

Oltre alle matrici grezze, MARIO offre metodi di alto livello per estrarre dati pronti
all'analisi e indicatori economici come il **PIL**.
""")

code(r"""# PIL per regione (somma del valore aggiunto)
db.GDP()""")

code(r"""# get_data: estrae una o più matrici in forma "lunga" (tidy), comoda per pandas/plot
dati = db.get_data(["X", "Y"])
type(dati), len(dati)""")

# ---------------------------------------------------------------------------
# 7. Visualizzazione
# ---------------------------------------------------------------------------
md(r"""## 7. Visualizzazione

MARIO ha funzioni di plotting interattive (basate su Plotly). In Colab le figure interattive di
MARIO vengono **salvate come file HTML** che puoi scaricare. Per un grafico **inline immediato**,
useremo anche `matplotlib` sui DataFrame restituiti da MARIO.
""")

code(r"""import matplotlib.pyplot as plt

gdp = db.GDP()
gdp.plot(kind="bar", legend=False, title="PIL per regione")
plt.ylabel("PIL")
plt.tight_layout()
plt.show()""")

code(r"""# Plot nativo di MARIO: salva un HTML interattivo (non apre il browser su Colab)
try:
    db.plot_gdp(path="gdp.html", auto_open=False)
    print("Grafico interattivo salvato in 'gdp.html'.")
    print("Su Colab puoi scaricarlo con:  from google.colab import files; files.download('gdp.html')")
except Exception as exc:
    print("Plot nativo non disponibile in questo ambiente:", exc)""")

# ---------------------------------------------------------------------------
# 8. Esportazione
# ---------------------------------------------------------------------------
md(r"""## 8. Esportare i risultati

Puoi salvare un database (con tutte le matrici e i metadati) in Excel, Parquet o testo, e
ricaricarlo in seguito (*round-trip*).
""")

code(r"""# Esporta in Excel (una cartella con i fogli del database)
db.to_excel(path="database_export", flows=True, coefficients=True)
print("Esportato in 'database_export'.")

# In Colab puoi scaricare i file generati con:
# from google.colab import files; files.download('...')""")

md(r"""---
## 🧩 Esercizio 1 — Esplorazione

Usa le celle sopra come riferimento e completa il codice.
""")

code(r"""# 🧩 ESERCIZIO 1
# a) Carica una NUOVA tabella di test SUT in una variabile chiamata `sut`
# b) Stampa il suo tipo di tabella e i suoi set
# c) Stampa l'elenco delle Commodity

# TODO: scrivi qui il tuo codice
sut = ...
""")

# ---------------------------------------------------------------------------
# 9. Trasformazioni
# ---------------------------------------------------------------------------
md(r"""# Parte 2 — Trasformazioni

MARIO non serve solo a *leggere* i dati, ma a **trasformarli**: aggregare settori/regioni,
aggiungere estensioni, applicare shock, convertire SUT↔IOT e MRIO→SRIO.
""")

md(r"""## 9. Aggregazione

Aggregare = raggruppare regioni, settori, fattori o conti satellite in categorie più ampie.
Il flusso in MARIO è:

1. genera un **template Excel** con `get_aggregation_excel(...)`;
2. nel template, per ogni elemento scrivi nella colonna **`Aggregation`** il nome del gruppo di
   destinazione;
3. applica con `db.aggregate("template.xlsx")`.

Qui compiliamo il template **da codice** (con pandas) per rendere la cella riproducibile, ma in
un caso reale potresti modificarlo a mano in Excel e ricaricarlo.
""")

code(r"""# Lavoriamo su una copia per non alterare il database originale
db_agg = mario.load_test("IOT")

# 1) Genera il template di aggregazione
db_agg.get_aggregation_excel(path="aggregazione.xlsx", overwrite=True)

# 2) Compiliamo il template: teniamo tutto invariato, ma rinominiamo i 3 settori
#    in 2 macro-settori (Primario / Servizi).
fogli = pd.read_excel("aggregazione.xlsx", sheet_name=None)
mappa_settori = {"Agriculture": "Primario", "Industry": "Primario", "Services": "Servizi"}

with pd.ExcelWriter("aggregazione.xlsx", engine="openpyxl") as writer:
    for nome_foglio, df in fogli.items():
        df = df.copy()
        # 'Aggregation' di default va riempita con il nome di destinazione
        df["Aggregation"] = df["Unnamed: 0"]
        if nome_foglio == "Sector":
            df["Aggregation"] = df["Unnamed: 0"].map(mappa_settori)
        df.to_excel(writer, sheet_name=nome_foglio, index=False)

# 3) Applica l'aggregazione
db_agg.aggregate("aggregazione.xlsx")
print("Settori dopo l'aggregazione:", list(db_agg.get_index("Sector")))""")

md(r"""## 10. Aggiungere estensioni (conti satellite)

Con `add_extensions(...)` puoi aggiungere nuove righe di conti satellite (es. un nuovo
inquinante, un indicatore sociale) a partire da una matrice tua.

```python
db.add_extensions(
    io=mia_matrice,        # DataFrame con i nuovi conti satellite
    matrix="E",            # a quale blocco aggiungerli
    units=mie_unita,       # DataFrame con le unità di misura
    inplace=True,
)
```
⚙️ Richiede dati coerenti con le dimensioni del database; la mostriamo come riferimento API.
""")

md(r"""## 11. Analisi di shock (scenari)

Uno **shock** modifica uno o più coefficienti (es. +10% di intensità di un input) e ricalcola il
sistema in un **nuovo scenario**, lasciando intatto il `baseline` per il confronto.

Flusso: genera il template con `get_shock_excel(...)`, compila i fogli `z`/`v`/`e`/`Y`, poi
applica con `shock_calc(...)` indicando il nuovo scenario.
""")

code(r"""db_shock = mario.load_test("IOT")

# 1) Template di shock con 1 riga
db_shock.get_shock_excel(path="shock.xlsx", num_shock=1)

# 2) Compiliamo lo shock sul foglio 'z': +20% sul coefficiente
#    da (Reg1, Agriculture) verso (Reg1, Industry)
fogli = pd.read_excel("shock.xlsx", sheet_name=None)
fogli["z"].loc[0] = ["Reg1", "Agriculture", "Reg1", "Industry", "Percentage", 20]

with pd.ExcelWriter("shock.xlsx", engine="openpyxl") as writer:
    for nome_foglio, df in fogli.items():
        df.to_excel(writer, sheet_name=nome_foglio, index=False)

# 3) Applica lo shock creando lo scenario 'shock_agri'
db_shock.shock_calc("shock.xlsx", z=True, scenario="shock_agri")
print("Scenari ora disponibili:", db_shock.scenarios)""")

code(r"""# Confrontiamo la produzione X tra baseline e scenario di shock
confronto = db_shock.get_data(["X"], scenarios=["baseline", "shock_agri"])
confronto""")

md(r"""## 12. Aggiungere o dividere settori

`add_sectors(...)` permette di introdurre un nuovo settore o di **splittare** un settore esistente
in più sotto-settori (workflow tipico per disaggregare una tecnologia). Richiede un template
dedicato (`get_add_sectors_excel(...)`) con i dati di input/output del nuovo settore.

⚙️ È un workflow avanzato che dipende fortemente dai dati: lo segnaliamo come riferimento.
```python
db.get_add_sectors_excel(path="nuovi_settori.xlsx")   # genera il template
db.add_sectors("nuovi_settori.xlsx")                  # applica
```
""")

md(r"""## 13. Conversione SUT → IOT

Una tabella **Supply & Use** può essere convertita in una **Input-Output** simmetrica con
`to_iot(method)`. I metodi classici sono `'A'`/`'B'`/`'C'`/`'D'` (ipotesi tecnologiche/di mercato).
""")

code(r"""sut = mario.load_test("SUT")
print("Prima:", sut.table_type, "| set:", sut.sets)

# Converte la SUT in IOT (ipotesi tecnologica 'B' = product technology)
sut.to_iot("B")
print("Dopo :", sut.table_type)""")

md(r"""## 14. Da multi-regionale (MRIO) a mono-regionale (SRIO)

Con `to_single_region(...)` "ritagli" una singola regione dal database multi-regionale,
trattando le altre regioni come resto del mondo (import/export). Con `to_region_subset(...)`
tieni invece un sottoinsieme di regioni.
""")

code(r"""db_mrio = mario.load_test("IOT")
print("Regioni MRIO:", list(db_mrio.get_index("Region")))

# Estrai la sola Reg1 come database mono-regionale (su una copia)
srio = db_mrio.to_single_region("Reg1", inplace=False)
print("Regioni SRIO:", list(srio.get_index("Region")))""")

md(r"""## 15. Metodologia Isard → Chenery-Moses

`to_chenery_moses(...)` converte un database dalla rappresentazione *Isard* (commercio
inter-regionale pieno) a quella *Chenery-Moses* (coefficienti di commercio), molto usata nei
modelli MRIO.

```python
db.to_chenery_moses()      # ⚙️ avanzato: dipende dalla struttura del commercio inter-regionale
```
""")

# ---------------------------------------------------------------------------
# 16-18. Workflow avanzati
# ---------------------------------------------------------------------------
md(r"""# Parte 3 — Workflow avanzati

Indicatori ambientali, analisi delle catene di fornitura e *structural path analysis*.
""")

md(r"""## 16. Calcolo dei gas serra (GHG)

`calc_ghg(...)` aggrega i diversi gas serra presenti nei conti satellite in un unico indicatore
in CO₂-equivalente, usando i fattori GWP (Global Warming Potential) dell'IPCC.

```python
db.calc_ghg(gwp=mio_profilo_gwp, label="GHG", ipcc_report="AR6", time_horizon=100)
```
⚙️ Richiede che il database contenga i singoli gas serra: sul mini-database di test (che ha solo
"CO2") serve solo come riferimento API. Sui database reali (es. EXIOBASE) funziona pienamente.
""")

md(r"""## 17. Analisi delle catene di fornitura (supply chain)

MARIO offre una famiglia di metodi `calc_trades*` e `calc_embodied_*` per studiare il commercio e
i contenuti "incorporati" (embodied) di un indicatore (es. CO₂, occupazione) lungo le filiere,
più `calc_linkages` per i legami a monte/valle (Rasmussen-Hirschman).
""")

code(r"""db_sc = mario.load_test("IOT")

# Legami a monte/valle (backward/forward linkages) per settore
linkages = db_sc.calc_linkages()
linkages""")

code(r"""# CO2 "incorporata" nelle importazioni (embodied imports) — esempio di indicatore di filiera
emb = db_sc.calc_embodied_imports(indicator="CO2", item="Industry")
print(type(emb).__name__)
emb""")

md(r"""## 18. Structural Path Analysis (SPA)

La **SPA** scompone l'impatto totale di un indicatore (es. CO₂) nei singoli **percorsi** della
filiera produttiva, ordinandoli per importanza. Utile per capire *dove esattamente* nella catena
di fornitura si genera un impatto.
""")

code(r"""db_spa = mario.load_test("IOT")

# Primi percorsi che contribuiscono alle emissioni di CO2 (profondità max 3)
percorsi = db_spa.calc_spa("CO2", max_depth=3, top_n=15, plot=None, show_plot=False)
percorsi.head(15)""")

# ---------------------------------------------------------------------------
# Esercizi finali
# ---------------------------------------------------------------------------
md(r"""---
# 🧩 Esercizi finali

Mettiamo insieme quello che abbiamo imparato. Prova a risolverli con la documentazione alla mano.
""")

code(r"""# 🧩 ESERCIZIO 2 — Pipeline completa
# 1) Carica una IOT di test
# 2) Calcola X, z e w
# 3) Stampa il PIL per regione
# 4) Esporta il database in Excel nella cartella 'mio_export'

# TODO: il tuo codice qui
""")

code(r"""# 🧩 ESERCIZIO 3 — Scenario
# 1) Carica una nuova IOT di test
# 2) Genera un template di shock e applica un +15% al coefficiente z
#    da (Reg2, Services) verso (Reg2, Industry), in uno scenario 'mio_shock'
# 3) Confronta X tra 'baseline' e 'mio_shock' con get_data

# TODO: il tuo codice qui
""")

code(r"""# 🧩 ESERCIZIO 4 — Aggregazione regionale
# 1) Carica una IOT di test
# 2) Genera il template di aggregazione
# 3) Aggrega le due regioni Reg1 e Reg2 in un'unica regione 'Mondo'
# 4) Verifica che ora ci sia una sola regione

# TODO: il tuo codice qui
""")

# ---------------------------------------------------------------------------
# Footer / risorse
# ---------------------------------------------------------------------------
md(r"""---
## 📚 Risorse e prossimi passi

- **User guide ufficiale**: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- **Documentazione completa**: <https://mario-suite.readthedocs.io/>
- **Codice sorgente (GitHub)**: <https://github.com/it-is-me-mario/MARIO>
- **Articolo scientifico**: *MARIO: A Versatile and User-Friendly Software for Building
  Input-Output Models* (Journal of Open Research Software)

### Cosa fare dopo il corso
1. Scarica un database reale (es. EXIOBASE) e ripeti i workflow con dati veri.
2. Costruisci un tuo scenario di policy (shock) e quantificane gli effetti su PIL ed emissioni.
3. Approfondisci la *structural path analysis* per individuare gli hotspot delle filiere.

> Hai trovato un errore o un comando che non funziona? Annota la versione (`mario.__version__`)
> e segnalalo al docente. Buon lavoro! 🎓
""")

# ---------------------------------------------------------------------------
# Dump del notebook
# ---------------------------------------------------------------------------
NB = {
    "cells": CELLS,
    "metadata": {
        "colab": {"name": "Corso_MARIO.ipynb", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "Corso_MARIO.ipynb")
with open(OUT_PATH, "w", encoding="utf-8") as fh:
    json.dump(NB, fh, ensure_ascii=False, indent=1)

print(f"Notebook generato: {OUT_PATH}  ({len(CELLS)} celle)")
