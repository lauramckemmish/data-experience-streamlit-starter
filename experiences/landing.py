"""Neutral landing page for the reusable starter."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import APP_SUBTITLE, APP_TITLE, DEVELOPMENT_NOTE, PROJECT_LABEL
from experiences.catalog import experience_catalog


def render(data: pd.DataFrame, open_experience) -> None:
    st.title(APP_TITLE)
    st.markdown(f"### {APP_SUBTITLE}")

    count, columns = st.columns([1, 3])
    with count:
        st.metric("Sample records", f"{len(data):,}")
    with columns:
        st.write(
            "This starter is intentionally dataset-neutral. It provides the application shell, "
            "navigation and reusable learning-experience structure; replace the sample data and "
            "experience content for a new topic."
        )

    st.markdown(f"**{PROJECT_LABEL}**")
    st.info(DEVELOPMENT_NOTE)

    st.markdown("## Choose an experience")
    st.write("Each experience is a separate route so guided lessons and open exploration do not become coupled.")

    experiences = experience_catalog()
    for index in range(0, len(experiences), 2):
        columns = st.columns(2)
        for column, (name, summary) in zip(columns, experiences[index:index + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"### {name}")
                    st.write(summary)
                    st.button(
                        "Open experience →",
                        key=f"open_{name}",
                        use_container_width=True,
                        on_click=open_experience,
                        args=(name,),
                    )

    with st.expander("How to adapt this starter"):
        st.markdown(
            "1. Replace `data/sample_data.csv` with your teaching dataset.\n"
            "2. Update project names in `config.py`.\n"
            "3. Build guided teaching content in `experiences/curious.py`.\n"
            "4. Develop Year 8 and Year 10 independently when ready.\n"
            "5. Put open-ended multivariate exploration in `experiences/data_playground.py`, not in CURIOUS."
        )
