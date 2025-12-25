# ug-university-prototype

Prototype of the Math Department undergraduate pages in a “university site” style.

This repo is **not** the official Binghamton site. It is used to draft structure and wording before
migrating stable content into the university CMS.

## Content source
Stable UG content lives in the separate repo `ug-content` and is included here as a git submodule:

- `docs/content/`  ← `ug-content` (submodule)

Edits to track descriptions and other stable text should generally be made in `ug-content`, not here.

## Local preview (MkDocs)
Create/activate a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mkdocs
```
Run a local server:

```bash
mkdocs serve
```
Then open the local URL shown in the terminal.