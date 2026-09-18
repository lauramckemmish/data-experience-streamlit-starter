# Data Experiences Starter — architecture contract

This repository is a reusable master scaffold for educational data-science experiences.

This document governs reusable application and software architecture. Cross-resource design knowledge belongs in `playbook/`; individual resources retain local pedagogy and may deliberately deviate where their audience, science, data or delivery context warrants it.

## Stable reference-surface structure

The three reference surfaces are deliberately stable:

1. **Template Experience** — a small, coherent, guided learner journey.
2. **Data Playground** — open exploration organised around one, two and three variables.
3. **Pattern Reference** — a non-narrative home for selected canonical shared-pattern examples.

The starter is broad and representative, not comprehensive. A shared helper does
not automatically need a rendered exemplar; keep one only where it supports
authoring, design, testing or auditing.

## Stable interface rules

- **Introduction/Home:** dataset identity, short scope statement and provenance are prominent above the experience choices.
- **Sidebar:** experience navigation, raw dataset access/download and source/provenance.
- **Top-right shell control:** Facilitator notes, available across the learner journey.
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
presentation, and Facilitator-notes visibility. Experience modules own the
scientific question, learner wording, sequence, explanations, facilitation
advice, and dataset-specific interpretation. The data layer owns calculations,
filtering, usable-row counts, missing-data logic, and transformations.

Shared semantic meaning should have shared visual meaning, while native
Streamlit primitives remain preferred where they already work well. Visual
hierarchy should keep optional, data-literacy, and facilitator support quieter than
the main learner evidence and tasks. Yellow is institutional/brand emphasis,
not generic interaction decoration.

### Shared interaction distinctions

- **Semantic prompts** name the cognitive job—Notice, Compare, Predict, Explain, Conclude, Revise or Recall—and are non-blocking. A generic Think cue is discouraged because it hides the intended intellectual work.
- **Self-check** is collapsed formative feedback for comparing a learner's reading or thinking. It is non-gating and distinct from optional enrichment.
- **Soft reveal** offers optional supporting or enrichment information and never blocks progression.
- **Hard reveal** protects consequential evidence when seeing it early would undermine prior reasoning or action. It blocks Continue until revealed, but does not imply prediction specifically.
- **Completion gates** block Continue only for a meaningful required learner action; they remain separate from reveals and prompts.
- **Facilitator notes** are optional adult-support content, visible through the shared shell toggle and independent of learner state. Stage-local preparation and compact live cues use shared treatments; experience modules own when and what to say.
- Experience modules own the particular cognitive job, learner wording, and whether a check or reveal is appropriate. Prompt choice and progression choice are separate design decisions.

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

## Data Playground field capabilities

Shared Playground machinery consumes a small, experience-supplied per-field
contract in `data.py`: internal name, learner label, kind, concise meaning,
analytical role, and one-/two-variable eligibility. Optional capabilities cover
units, log display, filtering, grouping, and a modest categorical cardinality
guardrail. Pandas dtype alone does not establish scientific or pedagogical
eligibility. Missingness is calculated from the source dataframe, never stored
in field configuration. A local experience may also suppress one otherwise
valid variable pair with a short configured reason. Experiences may omit
unsupported analytical routes and retain their own science, local wording, and
pedagogy.

The canonical opening journey is **Start here → Know your data → One variable
→ Two variables**. One- and two-variable representations dispatch from the
configured field kinds rather than a learner-facing chart menu. Later routes
remain capability-dependent: an experience may omit them when its data cannot
support a truthful analysis, while retaining local science and pedagogy.

## Development rule

Work on one surface at a time. Change that surface plus only the shared modules genuinely required by the change. Do not opportunistically redesign other surfaces in the same implementation pass.
