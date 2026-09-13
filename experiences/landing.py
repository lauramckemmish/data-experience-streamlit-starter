"""Dataset-first introduction page for the reusable starter."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from pathlib import Path

import config
from config import (
    HERO_HOOK,
    LANDING_ORIENTATION,
    DATASET_NAME,
    DATASET_SCOPE_NOTE,
    DATASET_SHORT_DESCRIPTION,
    EXPERIENCE_PATTERN_REFERENCE,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_TEMPLATE,
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


def _render_catalog_collection(entries: list[dict], *, open_experience) -> None:
    """Render destination cards in a compact two-column collection."""
    for index in range(0, len(entries), 2):
        columns = st.columns(2)
        for column, entry in zip(columns, entries[index:index + 2]):
            with column:
                _render_catalog_card(
                    entry,
                    button_label="Open →",
                    button_key=f"open_{entry['name']}",
                    open_experience=open_experience,
                )


def render(data: pd.DataFrame, open_experience) -> None:
    st.title(HERO_HOOK)
    hero_text, hero_visual = st.columns([3, 2], gap="large")
    with hero_text:
        st.markdown(f"### {DATASET_NAME}")
        st.write(DATASET_SHORT_DESCRIPTION)
        st.caption(DATASET_SCOPE_NOTE)
        st.write(LANDING_ORIENTATION)
    with hero_visual:
        st.image(Path(__file__).resolve().parent.parent / "assets" / "starter-hero.svg", caption="Replace with a contextual image for your resource.", width="stretch")

    st.markdown("## Choose a starting point")
    st.write("Begin with a guided investigation, explore the data openly, or inspect the shared reference patterns.")

    entries = experience_catalog(enabled_only=True)
    template = [item for item in entries if item["name"] == EXPERIENCE_TEMPLATE]
    playground = [item for item in entries if item["name"] == EXPERIENCE_PLAYGROUND]
    reference = [item for item in entries if item["name"] == EXPERIENCE_PATTERN_REFERENCE]

    st.markdown("### Guided investigation")
    _render_catalog_collection(template, open_experience=open_experience)
    st.markdown("### Explore the data")
    _render_catalog_collection(playground, open_experience=open_experience)
    st.markdown("### Reference patterns")
    _render_catalog_collection(reference, open_experience=open_experience)

    render_resource_context(getattr(config, "RESOURCE_ABOUT", {}), logo_path=config.ABOUT_INSTITUTIONAL_LOGO, logo_width=125)
