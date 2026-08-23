# Data Experiences Streamlit Starter

A neutral, deployable Streamlit starter for educational data experiences. It keeps the application architecture and visual/navigation pattern separate from any one scientific topic or dataset.

## Included experiences

- **CURIOUS** — guided facilitator-led sequence with neutral step placeholders.
- **Year 8** — routed two-lesson classroom shell, intentionally not designed yet.
- **Year 10** — routed two-lesson classroom shell, intentionally not designed yet.
- **Data Playground** — open-ended exploration kept architecturally separate from CURIOUS.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Put it on GitHub and Streamlit Community Cloud

1. Create a new empty GitHub repository.
2. Upload or push the contents of this folder to the repository root.
3. In Streamlit Community Cloud, create a new app from that repository.
4. Choose the branch containing these files.
5. Set the main file path to `app.py`.
6. Deploy.

No secrets are required for the bundled sample dataset.

## Adapt it to a new dataset

1. Replace `data/sample_data.csv` with your dataset (or update `DEFAULT_DATA_PATH` in `data.py`).
2. Update names and short branding text in `config.py`.
3. Build the guided workshop in `experiences/curious.py`.
4. Put reusable plots/analysis in `charts.py`, not in the experience module.
5. Develop `experiences/year8.py` and `experiences/year10.py` when their pedagogy is ready.
6. Keep general multivariate / parallel-coordinate exploration in `experiences/data_playground.py`.

## Architecture

```text
app.py                      application shell
config.py                   names and small project configuration
data.py                     loading and shared data helpers
charts.py                   plotting / analysis logic
ui_helpers.py               reusable teaching UI
experiences/
  landing.py                experience catalogue
  router.py                 routing and navigation state
  curious.py                guided CURIOUS lesson
  classroom_shell.py        common two-lesson shell
  year8.py                  Year 8 route
  year10.py                 Year 10 route
  data_playground.py        open-ended exploration
```

The intended workflow is to keep this starter stable, then fork/copy it for a topic-specific project and replace the neutral data and content.


## Dataset metadata

The sidebar includes a shared dataset section with a raw-data viewer, CSV download, and provenance information. Update `DATASET_NAME`, `DATASET_SOURCE_LABEL`, `DATASET_SOURCE_URL`, and `DATASET_SOURCE_NOTE` in `config.py` whenever you adapt the starter to a new dataset.
