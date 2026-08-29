# Data Experiences Starter — architecture contract

This repository is a reusable master scaffold for educational data-science experiences.

This document governs reusable application and software architecture. Cross-resource design knowledge belongs in `playbook/`; individual resources retain local pedagogy and may deliberately deviate where their audience, science, data or delivery context warrants it.

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

### Shared content roles

The shell depends on a small semantic contract in `config.py`: `SHORT_NAME` is
the compact sidebar identity, `DESCRIPTIVE_NAME` is the formal About identity,
`HERO_HOOK` is the learner-facing landing hook, and `RESOURCE_DESCRIPTION`
explains the resource in its trust/context section. Dataset/source status and
landing orientation remain operational/context roles; stewardship and
positionality express accountability; contributors, development, feedback and
support express provenance and intellectual context. These roles explain
placement, not fixed wording or appearance, so derived resources can retain
their own science, pedagogy and visual character.

This repository is currently a UNSW/CURIOUS work product, not an
institution-neutral public starter. A derived resource inherits the technical
shell, semantic design contract, reusable components and authoring guidance,
but does not inherit UNSW branding permission, scientific or educational
approval, stewardship, provenance, contributor attribution, partnerships,
funding, support claims, local pedagogy or scientific framing. Those must be
established for each resource. A separate institution-neutral derivative may be
considered only after real-resource testing demonstrates a need for it; that
future translation is out of scope here.

## Code ownership

- `data.py` — loading, cleaning, variable metadata, filtering helpers and preparation of usable rows.
- `charts.py` — reusable visualisation functions. Do not put Streamlit interface controls here.
- `models.py` — add this in a topic-specific project when modelling/fitting is substantial enough to deserve its own layer.
- `ui_helpers.py` — reusable interface components.
- `experiences/*.py` — Streamlit controls, learning sequence and interface for one experience only.

## Shared authoring boundary

The shared layer owns semantic interaction machinery, reusable state and
progression behaviour, canonical visual treatment, generic data-literacy
presentation, and Teacher-view visibility. Experience modules own the
scientific question, learner wording, sequence, explanations, facilitation
advice, and dataset-specific interpretation. The data layer owns calculations,
filtering, usable-row counts, missing-data logic, and transformations.

Shared semantic meaning should have shared visual meaning, while native
Streamlit primitives remain preferred where they already work well. Visual
hierarchy should keep optional, data-literacy, and teacher support quieter than
the main learner evidence and tasks. Yellow is institutional/brand emphasis,
not generic interaction decoration.

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
