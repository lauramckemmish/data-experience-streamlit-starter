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

## Classroom concurrency release check

Before releasing a facilitated classroom app, run a small browser-based smoke
test to check that the app remains usable when learners act together. This is a
release-readiness gate, not a performance-engineering framework: if it passes
comfortably, stop. Investigate only a failure or marginal result.

Install the one browser runtime once, then run the check:

```bash
python -m playwright install chromium
python tools/classroom_concurrency.py
```

The default levels are **1 → 20 → 30** independent sessions: one session,
the expected class size, and a small safety margin. The test starts and stops
its own local Streamlit server, gives the initial class arrival a bounded
startup allowance, then sends three synchronized interactions per level. It
fails on failed sessions, browser/page errors, interaction timeouts or a server
exit. It intentionally does not profile or diagnose allocator high-water use.

`tools/classroom_concurrency.py` is the generic mechanism. A derived
repository supplies `classroom_smoke_adapter.py`, whose small contract defines
the Streamlit launch command, representative route, synchronized interaction
and usable-page assertion. Override levels when needed, for example:

```bash
python tools/classroom_concurrency.py --sessions 1 --sessions 20 --sessions 30
```

The Starter adapter uses the existing Data Exploration Playground's dataset-preview
disclosure, because this dataset-neutral reference has no more
meaningful subject-specific class stage. For Exoplanets, the adapter should
navigate to **Planet Shopping → Combine** and perform its representative
Combine interaction. Another resource should similarly supply one stable,
real learner route and interaction rather than add testing UI or invent
pedagogy.

## Deploy with GitHub + Streamlit Community Cloud

1. Create a GitHub repository and put the contents of this folder at the repository root.
2. Create a Streamlit Community Cloud app from that repository.
3. Set the main file path to `app.py`.
4. Deploy.

No secrets are required for the bundled demo dataset.

## Adapt to a scientific dataset

1. Replace `data/taylor_swift_demo_dataset.csv` (or update the path/loading logic in `data.py`).
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

When adapting the starter, replace the resource-owned hero, dataset orientation,
About text, stewardship and relevant positionality, contributors, development
status, feedback, review, support and partnership content. Stewardship is
split between UNSW identity/permission stewardship and local scientific or
educational responsibility; neither is automatically inherited. Keep
“Choose an investigation” for structured guided experiences and “Explore the
data” for open-ended exploration. Use the established contribution vocabulary
and credit distinctive perspectives that materially shaped the resource; see
[`playbook/decisions/contributor-credit.md`](playbook/decisions/contributor-credit.md).

The Starter is a worked authoring reference, not an empty scaffold. Its
rendered landing page demonstrates the decisions a future author needs to make;
replace the guidance with verified scientific, pedagogical and provenance
content for the derived resource.

The default resource steward is Dr Laura McKemmish, UNSW Chemistry, with the
descriptor “Computational astrochemist · 10+ years creating research-connected
science experiences and data-rich investigations for school students”. This
establishes resource stewardship only: scientific/domain review is an additional
local claim, and “Resource stewardship and scientific review” should be used
only when relevant disciplinary expertise is established. Stewardship is also
separate from contributor credit.

### Shared pattern map

Use these worked examples when authoring a new experience. Shared structure and
presentation live in `ui_helpers.py`; data counts and field profiles live in
`data.py`; wording and sequence remain in the experience module.

| Pattern | Purpose and important distinction | Worked example |
| --- | --- | --- |
| Think prompt | Non-blocking cue for prediction, noticing or reasoning. | `experiences/curious.py`, CURIOUS → Welcome |
| Hard reveal | Withholds meaningful downstream evidence; render that content only when the helper returns `True`. | `experiences/curious.py`, CURIOUS → 1 · Context |
| Learner response | Persistent writable response, but not a gate by itself. | `experiences/curious.py`, CURIOUS → 1 · Context |
| Completion gate | Controls progression separately from reveal semantics. | `experiences/curious.py`, CURIOUS → 1 · Context |
| Soft reveal | Optional, non-blocking supporting content. | `experiences/curious.py`, CURIOUS → 1 · Context |
| Choice reveal | Optional learner-selected exploration; no natural Starter exemplar yet. | Shared helper only: `ui_helpers.py` |
| Graph support | Quiet guidance placed beside a real graph-reading task. | `experiences/data_playground.py`, 2 variables |
| Variable card | Explains a selected field’s meaning, units or interpretation. | `experiences/data_playground.py`, 1 variable |
| Sample note | Reports usable rows for the displayed analysis; calculations stay in the data layer. | `experiences/data_playground.py`, 1 and 2 variables |
| Teacher guidance | Shared visibility/presentation; the experience owns the facilitator content. | `experiences/curious.py`, CURIOUS → 1 · Context |

The content contract in `config.py` separates `SHORT_NAME` (compact shell
identity), `DESCRIPTIVE_NAME` (formal About identity), `HERO_HOOK` (learner-facing
main idea), and `RESOURCE_DESCRIPTION` (what the resource is). Keep dataset
status, landing orientation, stewardship/positionality, contributor
perspectives, and development/feedback as separate roles because they serve
different jobs; their exact wording and visual character remain resource-owned.

### Propagating shared-shell changes

When adopting the shell, transfer the complete dependency set: shared code and
helpers, theme/configuration, required local assets, and local relative asset
references. The current shell asset dependencies are declared in `config.py`;
copy only the assets required by the adopted components. The downstream app
must remain self-contained and must not depend on this Starter at runtime.

Before committing a downstream adoption:

1. Identify adopted components/helpers and their assets/configuration.
2. Copy required assets and update references to local paths.
3. Check for runtime paths back to the Starter.
4. Run syntax and asset-path checks, then visually inspect the app.
5. Commit and push only after those checks pass.

If a real resource exposes a generally useful shell improvement, generalise and
stabilise it in the Starter first, then propagate the canonical version back
downstream. Do not copy shared machinery directly between resource repositories.
