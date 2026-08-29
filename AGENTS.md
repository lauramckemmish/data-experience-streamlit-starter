# Repository Guidelines

## Project Structure & Module Organization

This repository is a dataset-neutral Streamlit educational application. The entry point is `app.py`. Shared configuration and data concerns live in `config.py` and `data.py`; reusable charts belong in `charts.py`, and reusable interface/teaching components belong in `ui_helpers.py`. Experience-specific Streamlit pages are isolated under `experiences/` (`curious.py`, `year8.py`, `year10.py`, and `data_playground.py`), with routing and shared classroom structure in `router.py` and `classroom_shell.py`. The bundled dataset is `data/sample_data.csv`. Read `ARCHITECTURE.md` before changing the stable experience structure.

## Local-first Development

For learner-facing, visual, or interactive work, develop and review locally before creating a Git checkpoint. Use this loop:

**inspect → bounded change → run locally → visually inspect → iterate → inspect diff → commit when coherent**

1. Start the app locally with:

```bash
python -m streamlit run app.py
```

2. Keep the Streamlit server running during iteration where practical.
3. Open the localhost URL reported by the running Streamlit process in the Codex in-app browser so the app can be inspected without leaving Codex. The port may vary; use the reported URL rather than assuming a fixed port.
4. Reuse that browser tab during subsequent iterations where practical.
5. Let Streamlit auto-reload after edits when possible.
6. Do not open Chrome or another external browser unless explicitly requested or the in-app browser cannot perform the required check.
7. Do not deploy publicly merely for visual inspection.

## Git Checkpoints

Git is the safety net and history, not a required step after every micro-edit or visual iteration. Make multiple local iterations when they belong to the same coherent change, then commit at a useful, inspectable checkpoint. Push when that checkpoint is worth preserving remotely or sharing. Do not commit or push merely to make visual inspection possible. Keep commits bounded enough to remain understandable and reversible, and always inspect the diff before committing.

## Build and Run Commands

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The first command installs the pinned-compatible Streamlit, pandas, and Plotly dependencies. The second starts the local app. There is no compiled build step.

## Coding Style & Naming Conventions

Use Python with four-space indentation, clear snake_case names for modules, functions, and variables, and descriptive names for learner-facing controls. Keep data preparation in `data.py`, plotting logic in `charts.py`, and page UI/learning sequences in the relevant `experiences/*.py` file. Avoid putting Streamlit controls in chart helpers. Keep the four core experiences and the dataset-first landing/sidebar contract stable unless the change is explicitly architectural. Match existing formatting and keep changes focused.

## Testing and Verification Guidelines

Use the smallest relevant check for the change. No automated test framework or coverage requirement is configured.

- Documentation-only: inspect the diff; no Streamlit run is required.
- Pure data or scientific logic: run the smallest relevant test or check, including empty, missing, or filtered-row cases where applicable.
- Learner-facing or UI change: run Streamlit locally and inspect the affected route.
- Shared navigation or shell change: inspect the relevant routes locally.
- Deployment-related change: verify the deployed environment separately when needed.

Do not require broad regression testing after every small local iteration.

## Deployment Verification

Local preview in the Codex in-app browser verifies the learning experience and interface. Public deployment is a separate verification step only when a resource is intended for public or classroom deployment; do it at an appropriate checkpoint to catch environment, dependency, path, or hosting differences. Do not confuse routine visual verification with deployment verification.

## Commit & Pull Request Guidelines

Recent commits use short, imperative, sentence-style summaries (for example, `Centralize experience visibility in catalogue`). Follow that pattern and keep each commit focused. Pull requests should explain the user-facing or architectural impact, identify affected experiences/modules, describe manual verification, and include screenshots for meaningful UI changes. Mention any dataset, configuration, or provenance changes explicitly.

## Data & Configuration Notes

When adapting the scaffold, update dataset identity, scope, source, and citation fields in `config.py` alongside the data path or schema changes. Do not add secrets; the bundled sample dataset requires none. Develop one experience at a time and change shared modules only when genuinely required.
