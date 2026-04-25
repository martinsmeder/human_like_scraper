# Repository Guidelines

## Project Structure & Module Organization

This repository is intentionally small and task-focused. `scrapethissite.py` is the current main Python entrypoint and contains the Camoufox automation logic for `https://www.scrapethissite.com/pages/`. `buttonclick.py` is older Camoufox practice code. Local HTML snapshots such as `scrapethissite.html`, `countries.html`, and `hockey-teams.html` are available for inspecting page structure, selectors, pagination controls, and table fields before editing the scraper. `README.md` is minimal project metadata, and `notes.txt` holds working notes rather than production code. Keep generated files such as `__pycache__/` out of commits, and keep the local virtual environment in `venv/`.

## Collaboration Notes

The user runs browser automation scripts locally so they can watch the browser and report runtime behavior. Agents should handle code edits, selector inspection, lightweight validation, and syntax checks, but should not run the full scraper unless the user explicitly asks. Prefer `python3 -m py_compile scrapethissite.py` for quick validation after edits.

## Build, Test, and Development Commands

Set up the local environment before editing:

```bash
source venv/bin/activate
```

Run the automation script locally:

```bash
python3 scrapethissite.py
```

Perform a quick syntax check before committing:

```bash
python3 -m py_compile scrapethissite.py
```

If Camoufox is not installed yet, install it inside the virtual environment and fetch the browser binary as required by the upstream docs.

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation and keep the code direct and minimal. Prefer standard-library modules unless an external dependency is required for browser automation. Use `snake_case` for variables and functions, and keep filenames descriptive and lowercase, for example `buttonclick.py`. Avoid overengineering: this repo favors short scripts over framework-heavy structure.

## Testing Guidelines

There is no formal test suite yet. For now, validate changes with `python3 -m py_compile scrapethissite.py`. Manual browser runs are normally performed by the user. Use the local HTML snapshots to reason about selectors and expected data before asking the user to run the scraper. If tests are added later, place them under a `tests/` directory and name files `test_*.py` so they are easy to discover with standard Python tooling.

## Commit & Pull Request Guidelines

The existing history uses short, imperative commit messages, for example `Initial commit`. Follow that pattern with concise summaries such as `Add Camoufox click loop`. Pull requests should describe the behavior change, mention any manual verification performed, and include screenshots only when the UI or browser behavior materially changes.

## Security & Configuration Tips

Do not commit `venv/`, local notes, credentials, or browser profiles. Keep configuration local unless it is required for reproduction.
