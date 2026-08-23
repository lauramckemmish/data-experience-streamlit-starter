"""Dataset-first introduction page for the reusable starter."""

from __future__ import annotations

import pandas as pd
import streamlit as st

import config
from config import (
    APP_SUBTITLE,
    APP_TITLE,
    DATASET_NAME,
    DATASET_SCOPE_NOTE,
    DATASET_SHORT_DESCRIPTION,
    DATASET_SOURCE_LABEL,
    DATASET_SOURCE_URL,
)
from experiences.catalog import experience_catalog

DATASET_CITATION = getattr(config, "DATASET_CITATION", None)


def render(data: pd.DataFrame, open_experience) -> None:
    st.title(APP_TITLE)
    st.markdown(f"### {APP_SUBTITLE}")

    with st.container(border=True):
        st.markdown(f"## {DATASET_NAME}")
        st.write(DATASET_SHORT_DESCRIPTION)
        st.caption(f"{len(data):,} rows × {len(data.columns)} columns in this app")
        st.info(f"**About this dataset:** {DATASET_SCOPE_NOTE}")

        source_bits = []
        if DATASET_SOURCE_URL:
            source_bits.append(f"[{DATASET_SOURCE_LABEL}]({DATASET_SOURCE_URL})")
        elif DATASET_SOURCE_LABEL:
            source_bits.append(DATASET_SOURCE_LABEL)
        if DATASET_CITATION:
            source_bits.append(DATASET_CITATION)
        if source_bits:
            st.markdown("**Source:** " + " · ".join(source_bits))

    st.markdown("## Choose an experience")
    st.write("Start with the experience that matches how you are using the dataset today.")

    experiences = experience_catalog(enabled_only=True)
    for index in range(0, len(experiences), 2):
        columns = st.columns(2)
        for column, experience in zip(columns, experiences[index:index + 2]):
            name = experience["name"]
            with column:
                with st.container(border=True):
                    st.markdown(f"### {name}")
                    st.write(experience["summary"])
                    st.button(
                        "Open experience →",
                        key=f"open_{name}",
                        use_container_width=True,
                        on_click=open_experience,
                        args=(name,),
                    )

    with st.expander("About the data"):
        st.write(DATASET_SCOPE_NOTE)
        if DATASET_SOURCE_URL:
            st.markdown(f"**Dataset source:** [{DATASET_SOURCE_LABEL}]({DATASET_SOURCE_URL})")
        elif DATASET_SOURCE_LABEL:
            st.markdown(f"**Dataset source:** {DATASET_SOURCE_LABEL}")
        if DATASET_CITATION:
            st.markdown(f"**Citation:** {DATASET_CITATION}")
