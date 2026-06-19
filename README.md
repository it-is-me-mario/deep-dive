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
uv run jupyter lab    # opens JupyterLab; then open notebooks/MARIO_course.ipynb
```

## 📓 The notebook

[`notebooks/MARIO_course.ipynb`](notebooks/MARIO_course.ipynb) is a self-contained notebook that
covers, with runnable cells + exercises:

| Part | Topics |
|---|---|
| **1 — Foundations** | IO concepts (Z, Y, X, V, E, Leontief), data parsing, inspection, matrix computation, indicator extraction (GDP), visualization, export |
| **2 — Transformations** | aggregation, extensions, shock/scenario analysis, adding/splitting sectors, SUT→IOT, MRIO→SRIO, Isard→Chenery-Moses |
| **3 — Advanced** | greenhouse gases (GHG), supply-chain analysis (trades, embodied, linkages), structural path analysis (SPA) |

The whole notebook runs on MARIO's **built-in test database**
(`mario.load_test("IOT")` / `"SUT"`): **no heavy downloads**, identical for everyone.
Every code cell was executed end-to-end without errors against **mariopy 1.0.2**.

## 🚀 How to use it (students)

1. **Set up the environment once** following [`SETUP.md`](SETUP.md) (`uv sync`).
2. Launch JupyterLab from the course folder: `uv run jupyter lab`.
3. Open [`notebooks/MARIO_course.ipynb`](notebooks/MARIO_course.ipynb) and run the cells from top to
   bottom (`Shift + Enter`). The first cell just checks that MARIO is available.
4. Complete the 🧩 **Exercise** cells.

> ⚠️ The package on PyPI is called **`mariopy`**, but in Python you import it as **`mario`**.

## 🗄️ Real-world databases (EXIOBASE, EORA, FIGARO…)

Real databases are too large to download live in a classroom: they must be **downloaded separately
and loaded from local files**. The notebook shows the pattern (`download_*` + `parse_*`) in
section 3.2. Working locally, you just point the `path=` argument at the folder where you downloaded
the files — no uploads needed.

## 🔧 For the instructor / regenerating the notebook

The notebook is generated from a versioned script, so it is easy to maintain and review. The `dev`
dependency group adds the notebook tooling:

```bash
uv sync --group dev                       # install instructor tooling
uv run python tools/build_notebook.py     # regenerates notebooks/MARIO_course.ipynb
```

To re-validate that all cells run without errors:

```bash
uv run jupyter nbconvert --to notebook --execute --allow-errors \
  --output executed_check.ipynb notebooks/MARIO_course.ipynb
```

## 📚 Resources

- User guide: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- Documentation: <https://mario-suite.readthedocs.io/>
- Source code: <https://github.com/it-is-me-mario/MARIO>
