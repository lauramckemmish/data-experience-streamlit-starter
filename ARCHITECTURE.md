# Data Experiences Starter — architecture contract

This repository is a reusable master scaffold for educational data-science experiences.

## Stable core experience structure

The four core routes are deliberately stable:

1. **CURIOUS** — a guided facilitator-led workshop.
2. **Year 8** — a scaffolded two-lesson classroom pathway.
3. **Year 10** — a deeper two-lesson classroom pathway.
4. **Data Exploration Playground** — open exploration organised around one, two and three variables.

A topic-specific project may add an extra experience only when the dataset genuinely warrants it. Do not add dataset-specific experiences to the master scaffold.

## Stable interface rules

- **Introduction/Home:** dataset identity, short scope statement and provenance are prominent above the experience choices.
- **Sidebar:** experience navigation, raw dataset access/download and source/provenance.
- **Top-right of guided/classroom pages:** Teacher view.
- **Main experience page:** only the teaching or exploration content relevant to that experience.

## Code ownership

- `data.py` — loading, cleaning, variable metadata, filtering helpers and preparation of usable rows.
- `charts.py` — reusable visualisation functions. Do not put Streamlit interface controls here.
- `models.py` — add this in a topic-specific project when modelling/fitting is substantial enough to deserve its own layer.
- `ui_helpers.py` — reusable interface components.
- `experiences/*.py` — Streamlit controls, learning sequence and interface for one experience only.

## Data-science progression

The reusable toolkit may include:

- inspecting raw data and provenance
- one-variable distributions
- two-variable relationships
- three-variable colour/grouping
- constrained filtering
- missing data
- scale/transformations
- fitting/modelling when scientifically meaningful

Not every dataset needs every technique. Add a technique when it helps answer a scientific question, not merely because the software can do it.

## Development rule

Work on one experience at a time. Change that experience plus only the shared modules genuinely required by the change. Do not opportunistically redesign other experiences in the same implementation pass.
