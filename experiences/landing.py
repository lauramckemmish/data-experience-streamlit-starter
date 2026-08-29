"""Dataset-first introduction page for the reusable starter."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from pathlib import Path

import config
from config import (
    HERO_HOOK,
    LANDING_ORIENTATION,
    SHORT_NAME,
    EXPERIENCE_PLAYGROUND,
)
from experiences.catalog import experience_catalog
from visual_system import render_resource_context

def render(data: pd.DataFrame, open_experience) -> None:
    hero_text, hero_visual = st.columns([3, 2], gap="large")
    with hero_text:
        st.title(HERO_HOOK)
        st.markdown(f"### {SHORT_NAME}")
        st.caption("Use the short name for persistent navigation; use the hook for the learner-facing idea or question.")
        st.write("This starter shows how an interactive data-science resource can introduce a scientific dataset, guide learners through structured investigations, and provide space for more open exploration.")
        st.write(LANDING_ORIENTATION)
        st.caption("Orientation should give enough scientific or data context to begin, without becoming full provenance documentation.")
    with hero_visual:
        st.image(Path(__file__).resolve().parent.parent / "assets" / "starter-hero.svg", caption="Replace with a contextual image for your resource.", width="stretch")

    st.markdown("## Choose an investigation")
    st.write("Follow a guided investigation designed for a classroom or workshop.")

    experiences = [item for item in experience_catalog(enabled_only=True) if item["name"] != EXPERIENCE_PLAYGROUND]
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
                        width="stretch",
                        on_click=open_experience,
                        args=(name,),
                    )

    st.markdown("## Explore the data")
    st.write("Follow a question or dataset that interests you.")
    playground = next(item for item in experience_catalog(enabled_only=True) if item["name"] == EXPERIENCE_PLAYGROUND)
    with st.container(border=True):
        st.markdown(f"### {playground['name']}")
        st.write(playground["summary"])
        st.button("Open exploration →", key="open_playground", width="stretch", on_click=open_experience, args=(EXPERIENCE_PLAYGROUND,))

    render_resource_context(getattr(config, "RESOURCE_ABOUT", {}), logo_path=Path(__file__).resolve().parent.parent / "assets" / "unsw-sydney-logo-portrait.png")
