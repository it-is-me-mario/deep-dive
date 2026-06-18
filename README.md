# Hands-on course on MARIO — Input-Output Analysis with Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/it-is-me-mario/deep-dive/blob/main/notebooks/MARIO_course.ipynb)

Teaching material to learn how to use **[MARIO](https://mario-suite.readthedocs.io/)**
(*Multifunctional Analysis of Regions through Input-Output*), the Python package from
Politecnico di Milano / eNextGen for building and analysing Input-Output Tables (IOT) and
Supply & Use Tables (SUT).

The course is built from the [official user guide](https://mario-suite.readthedocs.io/en/latest/user_guide/index.html)
and is designed to be run on **Google Colab** by 10–20 students at the same time.

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

1. Open the notebook in Colab (use the *Open in Colab* badge above, or upload the `.ipynb` file to
   <https://colab.research.google.com>).
2. `File ▸ Save a copy in Drive` to get your own personal copy.
3. Run the cells from top to bottom (`Shift + Enter`). The first one installs MARIO.
4. Complete the 🧩 **Exercise** cells.

> ⚠️ The package on PyPI is called **`mariopy`**, but in Python you import it as **`mario`**.

## 🗄️ Real-world databases (EXIOBASE, EORA, FIGARO…)

Real databases are too large to download live in a classroom: they must be **downloaded separately
and loaded from local files**. The notebook shows the pattern (`download_*` + `parse_*`) in
section 3.2. On Colab you can upload them with `google.colab.files.upload()` or by mounting Drive.

## 🔧 For the instructor / regenerating the notebook

The notebook is generated from a versioned script, so it is easy to maintain and review:

```bash
pip install -r requirements.txt
python tools/build_notebook.py        # regenerates notebooks/MARIO_course.ipynb
```

To re-validate that all cells run without errors:

```bash
jupyter nbconvert --to notebook --execute --allow-errors \
  --output executed_check.ipynb notebooks/MARIO_course.ipynb
```

## 📚 Resources

- User guide: <https://mario-suite.readthedocs.io/en/latest/user_guide/index.html>
- Documentation: <https://mario-suite.readthedocs.io/>
- Source code: <https://github.com/it-is-me-mario/MARIO>
