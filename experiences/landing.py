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


def _card_presentation(entry: dict, *, default_button_label: str) -> dict:
    """Resolve optional catalogue presentation metadata with plain-card fallbacks."""
    return {
        "title": entry.get("card_title", entry["name"]),
        "summary": entry.get("card_summary", entry["summary"]),
        "audience_badge": entry.get("audience_badge"),
        "thumbnail": entry.get("thumbnail"),
        "thumbnail_caption": entry.get("thumbnail_caption"),
        "button_label": entry.get("card_button_label", default_button_label),
    }


def _render_catalog_card(entry: dict, *, button_label: str, button_key: str, open_experience) -> None:
    """Render one generic landing card from optional catalogue presentation metadata."""
    presentation = _card_presentation(entry, default_button_label=button_label)
    with st.container(border=True):
        if presentation["audience_badge"]:
            st.badge(presentation["audience_badge"], color="gray")
        if presentation["thumbnail"]:
            st.image(
                Path(__file__).resolve().parent.parent / presentation["thumbnail"],
                caption=presentation["thumbnail_caption"],
                width="stretch",
            )
        st.markdown(f"### {presentation['title']}")
        if presentation["summary"]:
            st.write(presentation["summary"])
        st.button(
            presentation["button_label"],
            key=button_key,
            width="stretch",
            on_click=open_experience,
            args=(entry["name"],),
        )


def render(data: pd.DataFrame, open_experience) -> None:
    st.title(HERO_HOOK)
    hero_text, hero_visual = st.columns([3, 2], gap="large")
    with hero_text:
        st.markdown(f"### {SHORT_NAME}")
        st.write("A reusable reference for introducing a dataset, guiding an investigation and making room for open exploration.")
        st.write(LANDING_ORIENTATION)
    with hero_visual:
        st.image(Path(__file__).resolve().parent.parent / "assets" / "starter-hero.svg", caption="Replace with a contextual image for your resource.", width="stretch")

    st.markdown("## Choose an investigation")
    st.write("Choose a guided route for a classroom or workshop.")

    experiences = [item for item in experience_catalog(enabled_only=True) if item["name"] != EXPERIENCE_PLAYGROUND]
    for index in range(0, len(experiences), 2):
        columns = st.columns(2)
        for column, experience in zip(columns, experiences[index:index + 2]):
            with column:
                _render_catalog_card(
                    experience,
                    button_label="Open experience →",
                    button_key=f"open_{experience['name']}",
                    open_experience=open_experience,
                )

    st.markdown("## Explore the data")
    st.write("Choose variables, inspect the evidence and follow a question that interests you.")
    playground = next(item for item in experience_catalog(enabled_only=True) if item["name"] == EXPERIENCE_PLAYGROUND)
    _render_catalog_card(
        playground,
        button_label="Open exploration →",
        button_key="open_playground",
        open_experience=open_experience,
    )

    render_resource_context(getattr(config, "RESOURCE_ABOUT", {}), logo_path=config.ABOUT_INSTITUTIONAL_LOGO, logo_width=125)
