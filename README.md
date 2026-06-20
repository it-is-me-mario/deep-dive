# Hands-on course on MARIO — Input-Output Analysis with Python

Teaching material to learn how to use **[MARIO](https://mario-suite.readthedocs.io/)**
(*Multifunctional Analysis of Regions through Input-Output*), the Python package from
Politecnico di Milano / eNextGen for building and analysing Input-Output Tables (IOT) and
Supply & Use Tables (SUT).

The course is built from the [official user guide](https://mario-suite.readthedocs.io/en/latest/user_guide/index.html)
and runs in a **local, isolated Python environment** managed with [uv](https://docs.astral.sh/uv/),
opened in **JupyterLab**. Setting up that environment — cleanly and reproducibly, the same on every
machine — is itself part of the training.

## ⚡ Quick start

**New to Python / the terminal? Read [`SETUP.md`](SETUP.md) — it walks you through everything from
scratch (5 minutes).** The short version, once [uv](https://docs.astral.sh/uv/) is installed:

```bash
git clone https://github.com/it-is-me-mario/deep-dive.git
cd deep-dive
uv sync               # builds the exact environment (downloads Python too, if needed)
uv run jupyter lab    # opens JupyterLab; then open the notebooks/ folder
```

## 📓 The notebooks

The course is split into **three notebooks**, meant to be followed in order:

| # | Notebook | Data | Topics |
|---|---|---|---|
| **1** | [`Foundations (test database)`](notebooks/1.%20Foundations%20(test%20database).ipynb) | built-in toy DB (no download) | IO concepts (Z, Y, X, V, E, Leontief), parsing, inspection, matrix computation, GDP, visualization; SUT → single-region SUT and **SUT → IOT** |
| **2** | [`Real databases (EXIOBASE)`](notebooks/2.%20Real%20databases%20(EXIOBASE).ipynb) | **real EXIOBASE** (large download) | hybrid HSUT and the mixed-units peculiarity; monetary IOT; aggregation to ~7 sectors / 6 macro-regions keeping value added + CO₂ + water; visualization; export to coefficients + a parquet snapshot |
| **3** | [`Add sectors and shocks (AI scenarios)`](notebooks/3.%20Add%20sectors%20and%20shocks%20(AI%20scenarios).ipynb) | parquet snapshot from NB 2 | a transparent final-demand shock; **adding a new "Hyperscalers AI" sector**; the scenario where EU services swap high-skill labour for AI tokens; winners & losers |

Notebook **1** runs entirely on MARIO's **built-in test database**
(`mario.load_test("IOT")` / `"SUT"`): **no downloads**, identical for everyone, and every cell is
executed end-to-end against **mariopy 1.0.2**. Notebooks **2 and 3** use real EXIOBASE data
(several GB), so they are meant to be run on your own machine after editing the local data paths at
the top — they are not pre-executed.

## 🚀 How to use it (students)

1. **Set up the environment once** following [`SETUP.md`](SETUP.md) (`uv sync`).
2. Launch JupyterLab from the course folder: `uv run jupyter lab`.
3. Open the notebooks in `notebooks/` and run the cells from top to bottom (`Shift + Enter`),
   starting with **Notebook 1**.
4. Complete the 🧩 **Exercise** cells.

> ⚠️ The package on PyPI is called **`mariopy`**, but in Python you import it as **`mario`**.

## 🗄️ Real-world databases (EXIOBASE, EORA, FIGARO…)

Real databases are too large to download live in a classroom: they must be **downloaded separately
and loaded from local files**. Notebooks 2 and 3 show the full pattern (`download_*` + `parse_*` +
aggregation + scenarios). Working locally, you just point the `path=` arguments at the folders where
you downloaded the files — no uploads needed.

## 📚 Resources

- User guide: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- Documentation: <https://mario-suite.readthedocs.io/>
- Source code: <https://github.com/it-is-me-mario/MARIO>
