# Setup guide — installing the MARIO course environment

This guide takes you from **a computer with nothing installed** to **JupyterLab open with the
course notebook running**. No prior Python or command-line experience is assumed: follow the steps
in order and copy–paste the commands exactly.

When you are done you will have:

- **uv** — a single, fast tool that manages Python and packages for you.
- An **isolated environment** (the `.venv` folder) containing the *exact* versions the course needs,
  identical on every machine, with no risk of breaking anything else on your computer.
- **JupyterLab**, launched with one command, with the course notebook ready to run.

---

## The whole thing in 4 commands

If you are comfortable with a terminal, this is the entire setup. The sections below explain each
step for everyone else.

```bash
# 1. Install uv      (Windows: run in PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
#                    (macOS / Linux: run in Terminal)
# curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Get the course files, then enter the folder
git clone https://github.com/it-is-me-mario/deep-dive.git
cd deep-dive

# 3. Build the exact environment (uv downloads Python too, if needed)
uv sync

# 4. Launch JupyterLab
uv run jupyter lab
```

---

## Step 1 — Install **uv**

`uv` is the only thing you install "globally". It will take care of Python and every package, so you
**do not** need to install Python, Anaconda, or pip yourself.

### Windows

1. Open the **Start menu**, type `PowerShell`, and click **Windows PowerShell**.
2. Paste this line and press **Enter**:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. When it finishes, **close PowerShell and open a new one** (so it picks up the new `PATH`).

### macOS / Linux

1. Open the **Terminal** app.
2. Paste this line and press **Enter**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Close the Terminal and open a new one.**

### Check it worked

In a **new** terminal, run:

```bash
uv --version
```

You should see something like `uv 0.11.8`. If instead you get *"command not found"* / *"not
recognized"*, see [Troubleshooting](#troubleshooting).

> 💡 You will **not** install Python separately. `uv sync` (Step 3) downloads the correct Python
> version automatically into uv's own storage — it won't interfere with anything else.

---

## Step 2 — Get the course files

You need the course folder on your computer. Pick **one** of the two options.

### Option A — Download the ZIP (simplest, no extra tools)

1. Go to <https://github.com/it-is-me-mario/deep-dive>.
2. Click the green **`< > Code`** button ▸ **Download ZIP**.
3. **Unzip** it somewhere easy to find, e.g. your **Documents** folder. You will get a folder named
   `deep-dive` (or `deep-dive-main`).

### Option B — Clone with git (recommended if you have, or want, git)

```bash
git clone https://github.com/it-is-me-mario/deep-dive.git
```

### Then: open a terminal **inside** that folder

All the next commands must run from inside the course folder (the one containing `pyproject.toml`).

- **Windows:** open the `deep-dive` folder in File Explorer, then in the address bar type `powershell`
  and press **Enter** — a PowerShell opens already pointing at that folder.
- **macOS:** right-click the folder ▸ **New Terminal at Folder** (or `cd` into it).

To confirm you are in the right place, run `ls` (macOS/Linux) or `dir` (Windows): you should see
`pyproject.toml`, `uv.lock`, `README.md` and the `notebooks` folder.

---

## Step 3 — Build the environment

From inside the course folder, run:

```bash
uv sync
```

This single command:

1. reads `pyproject.toml` and `uv.lock` (the exact recipe of the environment);
2. **downloads the right Python** if you don't already have it;
3. creates an isolated environment in a `.venv` folder **inside the course folder**;
4. installs MARIO and everything it needs, at the *exact* versions everyone else in the class has.

The first run downloads a few hundred MB and takes a couple of minutes. It is fully automatic — wait
for the prompt to come back. You never need to "activate" anything by hand.

> ✅ When it finishes you have a complete, isolated, reproducible environment. If it ever gets into a
> weird state, you can delete the `.venv` folder and run `uv sync` again to rebuild it from scratch.

---

## Step 4 — Launch JupyterLab and open the notebook

Still inside the course folder, run:

```bash
uv run jupyter lab
```

`uv run` runs JupyterLab **inside** the course environment, so MARIO is available with no extra
steps. Your web browser will open automatically at JupyterLab.

1. In the **left-hand file browser**, open the `notebooks` folder.
2. Double-click **`MARIO_course.ipynb`**.
3. If asked to **Select Kernel**, choose the Python kernel from this project (it will mention
   `.venv` or "Python 3"). 
4. Run the cells one at a time with **`Shift + Enter`**, from top to bottom. The first code cell just
   checks that MARIO imported correctly and prints its version.

To **stop** JupyterLab: go back to the terminal and press `Ctrl + C` (confirm with `y` if asked).

---

## Day-to-day use (after the first setup)

You only do Steps 1–3 once. From then on, every time you want to work on the course:

```bash
# open a terminal inside the course folder, then:
uv run jupyter lab
```

That's it. If the course files were updated, run `uv sync` again first to pick up any changes.

---

## Alternative editors (optional)

JupyterLab is the path we use in class, but the **same environment** works with other tools — uv
already created `.venv`, you just point your editor at it.

- **VS Code:** install the *Python* and *Jupyter* extensions, open the course folder, open the
  `.ipynb`, and when prompted to select a kernel choose **`.venv`** (Python from the project).
- **Spyder:** if you prefer a MATLAB-like IDE, run it from the environment with
  `uv run spyder` after adding it: `uv add --group dev spyder`. (Heavier; JupyterLab is recommended
  for this course.)

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uv: command not found` / `'uv' is not recognized` | You didn't open a **new** terminal after installing uv. Close it and open a fresh one. If it still fails, the installer prints the folder it used (e.g. `%USERPROFILE%\.local\bin`); add that folder to your `PATH`, or just restart the computer. |
| `warning: VIRTUAL_ENV=...anaconda3... does not match the project environment` | Harmless. You have Anaconda active in your shell; uv ignores it and correctly uses the project's `.venv`. You can ignore the warning. |
| `uv sync` fails to download Python or packages | Usually a network/proxy/firewall issue. Retry on a stable connection. Behind a corporate proxy, set the `HTTPS_PROXY` environment variable first. |
| JupyterLab opens but the notebook shows **"No Kernel" / kernel not found** | Use **Kernel ▸ Change Kernel** and pick the project's Python (the one in `.venv`). The environment already includes `ipykernel`. |
| `Port 8888 is already in use` | Another Jupyter is running. Either use the link it offers, or launch on another port: `uv run jupyter lab --port 8889`. |
| `import mario` fails with *ModuleNotFoundError* | You launched Jupyter outside the environment. Always start it with **`uv run jupyter lab`** from inside the course folder. |
| Everything is broken and you want a clean slate | Delete the `.venv` folder inside the course folder and run `uv sync` again. Your notebook and files are untouched. |

---

## For instructors — regenerating / validating the notebook

The `dev` dependency group adds the notebook tooling:

```bash
uv sync --group dev                       # install instructor tooling
uv run python tools/build_notebook.py     # regenerate notebooks/MARIO_course.ipynb

# re-validate that every cell runs end-to-end:
uv run jupyter nbconvert --to notebook --execute --allow-errors \
  --output executed_check.ipynb notebooks/MARIO_course.ipynb
```
