"""Canonical rendered examples of selected shared starter patterns."""

from __future__ import annotations

import config
import streamlit as st

from experiences import router
from ui_helpers import (
    key_idea,
    media_text_pair,
    page_header,
    role_image,
    scroll_to_top_if_requested,
    self_check,
    soft_reveal,
    step_buttons,
    step_tabs,
)


REFERENCE_LABELS = [
    "Prompts & reveals",
    "Key idea",
    "Images",
    "Media layout",
]


def render() -> None:
    """Render the small non-narrative pattern reference surface."""
    part = int(st.session_state.get("pattern_reference_part", 0))
    part = max(0, min(part, len(REFERENCE_LABELS) - 1))
    page_header("Pattern Reference", teacher_control=False)
    st.caption("Canonical shared-pattern examples.")
    _, selected = step_tabs(REFERENCE_LABELS, "pattern_reference_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["pattern_reference_part"] = part
        st.session_state["pattern_reference_scroll_to_top"] = True
    scroll_to_top_if_requested("pattern_reference_scroll_to_top")

    if part == 0:
        with self_check("Compare your observation"):
            st.write("A useful observation points to specific evidence and explains why it may matter.")

        with soft_reveal("Optional supporting detail"):
            st.write("This optional detail supports interpretation without changing what learners must do next.")

    elif part == 1:
        key_idea(
            "A key idea states what evidence supports; it is not a success or completion message."
        )

    elif part == 2:
        _, image_column, _ = st.columns([2, 1, 2])
        with image_column:
            role_image(
                config.ASSETS_DIR / "starter-hero.svg",
                role="context",
                caption="Context image treatment.",
                key="pattern_reference_context",
            )

    else:
        with media_text_pair(
            config.ASSETS_DIR / "starter-hero.svg",
            role="support",
            caption="Support media treatment.",
            key="pattern_reference_support",
        ):
            st.markdown("#### Associated explanation")
            st.write("Use this layout when supporting media and its explanation belong together.")

    step_buttons(
        REFERENCE_LABELS,
        "pattern_reference_step_selector",
        "pattern_reference_part",
        "pattern_reference_scroll_to_top",
        part,
        "pattern_reference",
        terminal_action=router.go_home,
        terminal_label="Back to experiences",
    )
