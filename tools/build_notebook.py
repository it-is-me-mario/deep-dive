# -*- coding: utf-8 -*-
"""Build the teaching notebook for the MARIO course.

Run:      python tools/build_notebook.py
Produces: notebooks/MARIO_course.ipynb

The content targets the real API of mariopy 1.0.2 (verified locally).
"""
import json
import os

CELLS = []


def _src(text):
    # nbformat expects a list of lines, each ending with \n except (possibly) the last
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
# 0. Title and introduction
# ---------------------------------------------------------------------------
md(r"""# Hands-on course on **MARIO** — Input-Output Analysis with Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/it-is-me-mario/deep-dive/blob/main/notebooks/MARIO_course.ipynb)

**MARIO** (*Multifunctional Analysis of Regions through Input-Output*) is a Python package
developed by Politecnico di Milano and eNextGen for building and analysing
**Input-Output Tables (IOT)** and **Supply & Use Tables (SUT)**, both single- and multi-regional,
in monetary or physical units.

This notebook is designed to be run on **Google Colab** by many students at the same time:
it uses MARIO's **built-in test database**, so it requires **no heavy data downloads** and
behaves identically for everyone.

---

### How to use this notebook (read before you start)

1. **Make your own copy**: menu `File ▸ Save a copy in Drive`. You will work on your own personal
   copy without disturbing the others.
2. Run the cells **one at a time**, from top to bottom (`Shift + Enter`).
3. Cells marked with 🧩 **Exercise** are for you: complete the code where you see `# TODO`.
4. Cells marked with ⚙️ **Advanced** show the API for workflows that need real-world data:
   read them, but they may not produce a meaningful numerical result on the tiny test database.

> Estimated time: 2–3 hours. Have fun! 🚀
""")

# ---------------------------------------------------------------------------
# 1. Setup
# ---------------------------------------------------------------------------
md(r"""## 1. Installation and setup

We install the latest version of MARIO published on PyPI. ⚠️ Note: the package on PyPI is called
**`mariopy`**, but the module you import in Python is called **`mario`**.

> ### 🟥 You WILL see red warnings — this is normal, don't panic!
>
> MARIO pins specific versions of `pandas` and `numpy`. When pip installs them you will see
> messages like *"pip's dependency resolver … dependency conflicts … google-colab … gradio …
> numba …"*. **These warnings are harmless**: they refer to other packages pre-installed by Colab
> (gradio, google-colab, numba…) that have nothing to do with MARIO. You can ignore them.
>
> Because `numpy`/`pandas` get upgraded, **Colab needs to restart the runtime once**. The cell
> below does it **automatically**: you will see *"Your session crashed/restarted"* — that is
> **intended**. After the restart, simply continue from the **next** cell (the `import mario` one)
> and **do not re-run** the install cell.
""")

code(r"""# Install MARIO (course version). Run this cell ONCE.
%pip install -q mariopy==1.0.2

# On Colab, upgrading numpy/pandas requires a one-time runtime restart so the new
# versions load cleanly. We trigger it automatically here. This is NORMAL:
# after the restart, just continue from the NEXT cell (do not re-run this one).
try:
    import google.colab  # noqa: F401  (present only on Colab)
    print("\n✅ MARIO installed. Restarting the runtime to load the new numpy/pandas...")
    print("   This is expected. After it restarts, run the NEXT cell. Do NOT re-run this one.")
    import IPython
    IPython.Application.instance().kernel.do_shutdown(True)
except ImportError:
    # Not on Colab (e.g. local Jupyter): no restart needed.
    print("✅ MARIO installed (no runtime restart needed outside Colab).")""")

code(r"""import mario
import pandas as pd
import numpy as np

print("MARIO version:", mario.__version__)

# Reduce log verbosity to keep the notebook output clean
try:
    mario.set_log_verbosity("ERROR")
except Exception:
    pass""")

# ---------------------------------------------------------------------------
# 2. Core concepts
# ---------------------------------------------------------------------------
md(r"""## 2. Input-Output concepts (in 5 minutes)

An **Input-Output** table describes the economic flows of a system:

- **Z** — *intermediate transactions* matrix: how much sector *i* sells to sector *j*.
- **Y** — *final demand* (household consumption, investments, exports…).
- **X** — *total output* of each sector.
- **V** — *factors of production* / value added (wages, taxes, capital…).
- **E** — *satellite accounts* / environmental and social extensions (CO₂, employment…).

From these "flow" matrices MARIO computes the "**coefficient**" matrices and the models:

| MARIO symbol | Meaning |
|---|---|
| `z` | technical coefficients (Z normalised by output) |
| `v`, `e` | value-added / satellite-account coefficients |
| `w` | Leontief inverse, `w = (I − z)⁻¹` |
| `f` | footprint intensities of satellite accounts |
| `m` | multipliers |
| `p` | price indices |

> In MARIO **uppercase = absolute flows** (Z, V, E, Y, X) and
> **lowercase = coefficients** (z, v, e, w, f, m, p). We will use this constantly.

You don't need to memorise everything: MARIO computes the matrices **automatically** when needed.
""")

# ---------------------------------------------------------------------------
# 3. Parsing / loading data
# ---------------------------------------------------------------------------
md(r"""## 3. Loading data (parsing)

MARIO can read dozens of databases (EXIOBASE, EORA, FIGARO, WIOD, OECD, EUROSTAT…) as well as
custom databases from Excel/CSV/Parquet. To learn, we will use the **built-in test database**,
which loads in a single line and represents a toy economy with 2 regions and 3 sectors.
""")

code(r"""# Load a test Input-Output table
db = mario.load_test("IOT")

print(db)        # summary: name, table type, scenarios, size of each set
print("\nTable type:", db.table_type)
print("Multi-regional?", db.is_multi_region)""")

md(r"""### 3.1 Custom database from Excel

If you have your own data in an Excel sheet formatted according to MARIO's schema, you load it
like this:

```python
db = mario.parse_from_excel(
    path="my_table.xlsx",
    table="IOT",      # or "SUT"
    mode="flows",     # "flows" (absolute values) or "coefficients"
)
```

To get an empty, ready-to-fill **template**:

```python
mario.write_parse_template(...)   # see help(mario.write_parse_template)
```
""")

md(r"""### 3.2 "Large" databases (EXIOBASE, EORA, FIGARO…)

Real databases range from hundreds of MB to several GB: they **must be downloaded separately and
loaded from local files**, not on-the-fly in a classroom of 20 people. The typical flow is:

```python
# 1) Download once (takes time and disk space)
mario.download_exiobase_monetary(path="exiobase_data")   # example

# 2) Load from the downloaded files
db = mario.parse_exiobase(
    table="IOT",
    unit="Monetary",
    path="exiobase_data",
)
```

> 💡 In Colab you can upload the downloaded files with `from google.colab import files; files.upload()`
> or by mounting Google Drive (`from google.colab import drive; drive.mount('/content/drive')`).
> For the rest of the course we stick with the test database, which behaves just like a real one.
""")

# ---------------------------------------------------------------------------
# 4. Basic inspection
# ---------------------------------------------------------------------------
md(r"""## 4. Basic inspection

Before computing anything, let's explore *what the database contains*.
""")

code(r"""# Which "sets" (dimensions) does the database have?
print("Available sets:", db.sets)

# Which scenarios? (by default there is only one: 'baseline')
print("Scenarios:", db.scenarios)

# List the items of a set
print("\nRegions :", list(db.get_index("Region")))
print("Sectors :", list(db.get_index("Sector")))
print("Factors :", list(db.get_index("Factor of production")))
print("Satellite accounts:", list(db.get_index("Satellite account")))""")

code(r"""# Search a label by name (handy on real databases with thousands of sectors)
print("Search results for 'Agri':", db.search("Sector", "Agri"))

# Full index of every set in one go
db.get_index("all")""")

# ---------------------------------------------------------------------------
# 5. Computing matrices
# ---------------------------------------------------------------------------
md(r"""## 5. Computing the matrices

The heart of MARIO. The method `calc_all([...])` computes the requested matrices, **automatically
resolving all dependencies** (e.g. `w` needs `z`, `z` needs `Z` and `X`…). The computed matrices
are then accessible as attributes (`db.X`, `db.z`, `db.w`, …) and are plain `pandas.DataFrame`.
""")

code(r"""# Compute the main matrices
db.calc_all(["X", "z", "Z", "Y", "v", "e", "w"])

# Now they are accessible as pandas DataFrames
print("X (total output) shape:", db.X.shape)
print("z (technical coefficients) shape:", db.z.shape)
print("w (Leontief inverse) shape:", db.w.shape)

db.z   # display the technical coefficients""")

code(r"""# Total output by sector and region
db.X""")

code(r"""# 'explain' describes in words how MARIO computes a matrix
print(db.explain("w"))""")

md(r"""> ⚙️ **On large databases** the Leontief inversion can be heavy. MARIO lets you control the
> computation strategy with `mario.ComputeOptions(...)` passed to
> `db.resolve("w", compute_options=...)`. Not needed for the test database.
""")

# ---------------------------------------------------------------------------
# 6. Extracting data and indicators
# ---------------------------------------------------------------------------
md(r"""## 6. Extracting data and indicators

Beyond the raw matrices, MARIO offers high-level methods to extract analysis-ready data and
economic indicators such as **GDP**.
""")

code(r"""# GDP by region (sum of value added)
db.GDP()""")

code(r"""# get_data: extracts one or more matrices in "long" (tidy) form, handy for pandas/plotting
data = db.get_data(["X", "Y"])
type(data), len(data)""")

# ---------------------------------------------------------------------------
# 7. Visualization
# ---------------------------------------------------------------------------
md(r"""## 7. Visualization

MARIO has interactive plotting functions (built on Plotly). On Colab, MARIO's interactive figures
are **saved as HTML files** you can download. For an immediate **inline** chart, we will also use
`matplotlib` on the DataFrames returned by MARIO.
""")

code(r"""import matplotlib.pyplot as plt

gdp = db.GDP()
gdp.plot(kind="bar", legend=False, title="GDP by region")
plt.ylabel("GDP")
plt.tight_layout()
plt.show()""")

code(r"""# Native MARIO plot: saves an interactive HTML (does not open the browser on Colab)
try:
    db.plot_gdp(path="gdp.html", auto_open=False)
    print("Interactive chart saved to 'gdp.html'.")
    print("On Colab you can download it with:  from google.colab import files; files.download('gdp.html')")
except Exception as exc:
    print("Native plot not available in this environment:", exc)""")

# ---------------------------------------------------------------------------
# 8. Exporting
# ---------------------------------------------------------------------------
md(r"""## 8. Exporting results

You can save a database (with all its matrices and metadata) to Excel, Parquet or text, and
reload it later (*round-trip*).
""")

code(r"""# Export to Excel (a folder with the database sheets)
db.to_excel(path="database_export", flows=True, coefficients=True)
print("Exported to 'database_export'.")

# On Colab you can download the generated files with:
# from google.colab import files; files.download('...')""")

md(r"""---
## 🧩 Exercise 1 — Exploration

Use the cells above as a reference and complete the code.
""")

code(r"""# 🧩 EXERCISE 1
# a) Load a NEW SUT test table into a variable called `sut`
# b) Print its table type and its sets
# c) Print the list of Commodities

# TODO: write your code here
sut = ...
""")

# ---------------------------------------------------------------------------
# 9. Transformations
# ---------------------------------------------------------------------------
md(r"""# Part 2 — Transformations

MARIO is not only for *reading* data, but for **transforming** it: aggregating sectors/regions,
adding extensions, applying shocks, converting SUT↔IOT and MRIO→SRIO.
""")

md(r"""## 9. Aggregation

Aggregating = grouping regions, sectors, factors or satellite accounts into broader categories.
The flow in MARIO is:

1. generate an **Excel template** with `get_aggregation_excel(...)`;
2. in the template, for each item, write in the **`Aggregation`** column the name of the target
   group;
3. apply with `db.aggregate("template.xlsx")`.

Here we fill the template **from code** (with pandas) to make the cell reproducible, but in a real
case you could edit it by hand in Excel and re-upload it.
""")

code(r"""# Work on a copy so we don't alter the original database
db_agg = mario.load_test("IOT")

# 1) Generate the aggregation template
db_agg.get_aggregation_excel(path="aggregation.xlsx", overwrite=True)

# 2) Fill the template: keep everything unchanged, but rename the 3 sectors
#    into 2 macro-sectors (Primary / Services).
sheets = pd.read_excel("aggregation.xlsx", sheet_name=None)
sector_map = {"Agriculture": "Primary", "Industry": "Primary", "Services": "Services"}

with pd.ExcelWriter("aggregation.xlsx", engine="openpyxl") as writer:
    for sheet_name, df in sheets.items():
        df = df.copy()
        # 'Aggregation' must be filled with the target name
        df["Aggregation"] = df["Unnamed: 0"]
        if sheet_name == "Sector":
            df["Aggregation"] = df["Unnamed: 0"].map(sector_map)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# 3) Apply the aggregation
db_agg.aggregate("aggregation.xlsx")
print("Sectors after aggregation:", list(db_agg.get_index("Sector")))""")

md(r"""## 10. Adding extensions (satellite accounts)

With `add_extensions(...)` you can add new satellite-account rows (e.g. a new pollutant, a social
indicator) starting from your own matrix.

```python
db.add_extensions(
    io=my_matrix,          # DataFrame with the new satellite accounts
    matrix="E",            # which block to add them to
    units=my_units,        # DataFrame with the units of measure
    inplace=True,
)
```
⚙️ Requires data consistent with the database dimensions; we show it as an API reference.
""")

md(r"""## 11. Shock analysis (scenarios)

A **shock** modifies one or more coefficients (e.g. +10% intensity of an input) and recomputes the
system in a **new scenario**, leaving the `baseline` intact for comparison.

Flow: generate the template with `get_shock_excel(...)`, fill the `z`/`v`/`e`/`Y` sheets, then
apply with `shock_calc(...)` specifying the new scenario.
""")

code(r"""db_shock = mario.load_test("IOT")

# 1) Shock template with 1 row
db_shock.get_shock_excel(path="shock.xlsx", num_shock=1)

# 2) Fill the shock on the 'z' sheet: +20% on the coefficient
#    from (Reg1, Agriculture) to (Reg1, Industry)
sheets = pd.read_excel("shock.xlsx", sheet_name=None)
sheets["z"].loc[0] = ["Reg1", "Agriculture", "Reg1", "Industry", "Percentage", 20]

with pd.ExcelWriter("shock.xlsx", engine="openpyxl") as writer:
    for sheet_name, df in sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# 3) Apply the shock creating the 'shock_agri' scenario
db_shock.shock_calc("shock.xlsx", z=True, scenario="shock_agri")
print("Scenarios now available:", db_shock.scenarios)""")

code(r"""# Compare output X between baseline and the shock scenario
comparison = db_shock.get_data(["X"], scenarios=["baseline", "shock_agri"])
comparison""")

md(r"""## 12. Adding or splitting sectors

`add_sectors(...)` lets you introduce a new sector or **split** an existing sector into several
sub-sectors (a typical workflow to disaggregate a technology). It requires a dedicated template
(`get_add_sectors_excel(...)`) with the input/output data of the new sector.

⚙️ This is an advanced workflow that depends heavily on the data: we flag it as a reference.
```python
db.get_add_sectors_excel(path="new_sectors.xlsx")    # generate the template
db.add_sectors("new_sectors.xlsx")                   # apply
```
""")

md(r"""## 13. SUT → IOT conversion

A **Supply & Use** table can be converted into a symmetric **Input-Output** table with
`to_iot(method)`. The classic methods are `'A'`/`'B'`/`'C'`/`'D'` (technology/market assumptions).
""")

code(r"""sut = mario.load_test("SUT")
print("Before:", sut.table_type, "| sets:", sut.sets)

# Convert the SUT into an IOT (technology assumption 'B' = product technology)
sut.to_iot("B")
print("After :", sut.table_type)""")

md(r"""## 14. From multi-regional (MRIO) to single-region (SRIO)

With `to_single_region(...)` you "cut out" a single region from the multi-regional database,
treating the other regions as the rest of the world (imports/exports). With `to_region_subset(...)`
you instead keep a subset of regions.
""")

code(r"""db_mrio = mario.load_test("IOT")
print("MRIO regions:", list(db_mrio.get_index("Region")))

# Extract Reg1 only as a single-region database (on a copy)
srio = db_mrio.to_single_region("Reg1", inplace=False)
print("SRIO regions:", list(srio.get_index("Region")))""")

md(r"""## 15. Isard → Chenery-Moses methodology

`to_chenery_moses(...)` converts a database from the *Isard* representation (full inter-regional
trade) to the *Chenery-Moses* one (trade coefficients), widely used in MRIO models.

```python
db.to_chenery_moses()      # ⚙️ advanced: depends on the inter-regional trade structure
```
""")

# ---------------------------------------------------------------------------
# 16-18. Advanced workflows
# ---------------------------------------------------------------------------
md(r"""# Part 3 — Advanced workflows

Environmental indicators, supply-chain analysis and *structural path analysis*.
""")

md(r"""## 16. Greenhouse gas (GHG) calculation

`calc_ghg(...)` aggregates the different greenhouse gases present in the satellite accounts into a
single CO₂-equivalent indicator, using the IPCC GWP (Global Warming Potential) factors.

```python
db.calc_ghg(gwp=my_gwp_profile, label="GHG", ipcc_report="AR6", time_horizon=100)
```
⚙️ Requires the database to contain the individual greenhouse gases: on the tiny test database
(which only has "CO2") it serves only as an API reference. On real databases (e.g. EXIOBASE) it
works fully.
""")

md(r"""## 17. Supply-chain analysis

MARIO provides a family of `calc_trades*` and `calc_embodied_*` methods to study trade and the
"embodied" content of an indicator (e.g. CO₂, employment) along supply chains, plus
`calc_linkages` for backward/forward linkages (Rasmussen-Hirschman).
""")

code(r"""db_sc = mario.load_test("IOT")

# Backward/forward linkages per sector
linkages = db_sc.calc_linkages()
linkages""")

code(r"""# CO2 embodied in imports — example of a supply-chain indicator
emb = db_sc.calc_embodied_imports(indicator="CO2", item="Industry")
print(type(emb).__name__)
emb""")

md(r"""## 18. Structural Path Analysis (SPA)

**SPA** decomposes the total impact of an indicator (e.g. CO₂) into the individual **paths** of the
production chain, ranked by importance. Useful to understand *exactly where* in the supply chain an
impact is generated.
""")

code(r"""db_spa = mario.load_test("IOT")

# Top paths contributing to CO2 emissions (max depth 3)
paths = db_spa.calc_spa("CO2", max_depth=3, top_n=15, plot=None, show_plot=False)
paths.head(15)""")

# ---------------------------------------------------------------------------
# Final exercises
# ---------------------------------------------------------------------------
md(r"""---
# 🧩 Final exercises

Let's put together what we learned. Try to solve them with the documentation at hand.
""")

code(r"""# 🧩 EXERCISE 2 — Full pipeline
# 1) Load a test IOT
# 2) Compute X, z and w
# 3) Print GDP by region
# 4) Export the database to Excel in a folder called 'my_export'

# TODO: your code here
""")

code(r"""# 🧩 EXERCISE 3 — Scenario
# 1) Load a new test IOT
# 2) Generate a shock template and apply a +15% to the z coefficient
#    from (Reg2, Services) to (Reg2, Industry), in a scenario called 'my_shock'
# 3) Compare X between 'baseline' and 'my_shock' with get_data

# TODO: your code here
""")

code(r"""# 🧩 EXERCISE 4 — Regional aggregation
# 1) Load a test IOT
# 2) Generate the aggregation template
# 3) Aggregate the two regions Reg1 and Reg2 into a single region 'World'
# 4) Verify there is now a single region

# TODO: your code here
""")

# ---------------------------------------------------------------------------
# Footer / resources
# ---------------------------------------------------------------------------
md(r"""---
## 📚 Resources and next steps

- **Official user guide**: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- **Full documentation**: <https://mario-suite.readthedocs.io/>
- **Source code (GitHub)**: <https://github.com/it-is-me-mario/MARIO>
- **Scientific paper**: *MARIO: A Versatile and User-Friendly Software for Building Input-Output
  Models* (Journal of Open Research Software)

### What to do after the course
1. Download a real database (e.g. EXIOBASE) and repeat the workflows with real data.
2. Build your own policy scenario (shock) and quantify its effects on GDP and emissions.
3. Dive into structural path analysis to find supply-chain hotspots.

> Found a bug or a command that doesn't work? Note the version (`mario.__version__`) and report it
> to the instructor. Good luck! 🎓
""")

# ---------------------------------------------------------------------------
# Notebook dump
# ---------------------------------------------------------------------------
NB = {
    "cells": CELLS,
    "metadata": {
        "colab": {"name": "MARIO_course.ipynb", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebooks")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "MARIO_course.ipynb")
with open(OUT_PATH, "w", encoding="utf-8") as fh:
    json.dump(NB, fh, ensure_ascii=False, indent=1)

print(f"Notebook generated: {OUT_PATH}  ({len(CELLS)} cells)")
