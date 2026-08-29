# Data Experiences Streamlit Starter v4

A deployable, dataset-neutral Streamlit master scaffold for CURIOUS-style educational data-science resources.

This repository contains both reusable technical architecture and a shared design playbook for educational data-science experiences. See [ARCHITECTURE.md](ARCHITECTURE.md) for the application design contract and [playbook/README.md](playbook/README.md) for reusable cross-resource design knowledge.

## Stable core experiences

- **CURIOUS** — guided facilitator-led workshop.
- **Year 8** — scaffolded two-lesson classroom pathway.
- **Year 10** — deeper two-lesson classroom pathway.
- **Data Exploration Playground** — open exploration using a stable one-variable / two-variable / three-variable structure.

## What v4 stabilises

- A **dataset-first introduction page** above the experience catalogue.
- Dataset name, scope and provenance visible on both Home and the global sidebar.
- Raw-data viewing and CSV download remain globally accessible.
- Teacher view stays at the top-right of guided/classroom experiences.
- The Data Exploration Playground uses **1 / 2 / 3 variables** as its stable conceptual structure.
- Dataset-specific tools such as filtering, modelling or fitting can be added without changing the master experience architecture.
- Development should proceed **one experience at a time**.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy with GitHub + Streamlit Community Cloud

1. Create a GitHub repository and put the contents of this folder at the repository root.
2. Create a Streamlit Community Cloud app from that repository.
3. Set the main file path to `app.py`.
4. Deploy.

No secrets are required for the bundled sample dataset.

## Adapt to a scientific dataset

1. Replace `data/sample_data.csv` (or update the path/loading logic in `data.py`).
2. Update the dataset identity, scope, source and citation fields in `config.py`.
3. Design the CURIOUS pedagogy before changing `experiences/curious.py`.
4. Keep reusable data preparation in `data.py` and reusable plots in `charts.py`.
5. Add `models.py` if the topic has substantial fitting/modelling logic.
6. Develop Year 8 and Year 10 independently when their pedagogy is ready.
7. Keep the Data Exploration Playground structurally stable and add only scientifically justified dataset-specific tools.

## Architecture

```text
app.py                      application shell
config.py                   dataset identity + small project configuration
data.py                     loading and shared data helpers
charts.py                   plotting / analysis logic
ui_helpers.py               reusable teaching UI
ARCHITECTURE.md             master design contract
playbook/                   reusable cross-resource design decisions
templates/                  short workflows for applying playbook decisions
experiences/
  landing.py                dataset-first introduction + experience catalogue
  router.py                 routing and navigation state
  curious.py                guided CURIOUS lesson
  classroom_shell.py        common two-lesson shell
  year8.py                  Year 8 route
  year10.py                 Year 10 route
  data_playground.py        Data Exploration Playground
```
