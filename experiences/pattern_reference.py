"""Canonical rendered examples of selected shared starter patterns."""

from __future__ import annotations

import config
import streamlit as st

from experiences import router
from ui_helpers import (
    curriculum_summary,
    curriculum_tags,
    facilitator_live_cue,
    facilitator_preparation,
    key_idea,
    media_text_pair,
    notice_prompt,
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
    "Facilitator support",
    "Images",
    "Media layout",
]


def render() -> None:
    """Render the small non-narrative pattern reference surface."""
    part = int(st.session_state.get("pattern_reference_part", 0))
    part = max(0, min(part, len(REFERENCE_LABELS) - 1))
    page_header("Pattern Reference")
    st.caption("Canonical shared-pattern examples.")
    _, selected = step_tabs(REFERENCE_LABELS, "pattern_reference_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["pattern_reference_part"] = part
        st.session_state["pattern_reference_scroll_to_top"] = True
    scroll_to_top_if_requested("pattern_reference_scroll_to_top")

    if part == 0:
        notice_prompt("Identify one feature of the evidence that you would inspect first.")

        with self_check("Compare your observation"):
            st.write("A useful observation points to specific evidence and explains why it may matter.")

        with soft_reveal("Optional supporting detail"):
            st.write("This optional detail supports interpretation without changing what learners must do next.")

        st.info("**Alert:** This neutral support treatment clarifies scope or a useful instruction.")
        st.success("**Success:** This treatment is reserved for a genuinely checkable response.")

    elif part == 1:
        key_idea(
            "A key idea states what evidence supports; it is not a success or completion message."
        )

    elif part == 2:
        st.caption("Illustrative curriculum-rendering example only; this starter does not claim a formal mapping.")
        curriculum_summary(
            "NSW curriculum — Stage 5 Data Science 2",
            "SC5-DA2-01",
            "Illustrative example: learners inspect data representations and use evidence to communicate a finding.",
            detailed_content_note=True,
        )
        st.markdown("#### Example stage: inspect a representation")
        curriculum_tags([("SC5-DA2-01.L5", "✓"), ("L6", "◐")], key="inspect_representation")
        facilitator_preparation(
            "Use this collapsed space only when preparation changes how a capable "
            "facilitator understands or enacts the stage."
        )
        facilitator_live_cue(
            "CORE LEARNING",
            "Protect the opportunity to compare evidence before moving to explanation.",
        )
        facilitator_live_cue(
            "STREAMLINE",
            "Invite a brief paired comparison, then collect one evidence-based observation.",
        )
        facilitator_live_cue(
            "EXTENSION",
            "Invite learners to test whether the pattern holds for another relevant grouping.",
        )
        facilitator_live_cue(
            "FACILITATION NOTE",
            "Use the displayed evidence to decide whether more shared observation time is useful.",
        )
        st.markdown("#### Example stage: explain a finding")
        curriculum_tags(
            [("SC5-DA2-01.L6", "◐"), ("SC5-WS-06.2", "✓")],
            key="explain_finding",
        )
        st.markdown("#### Example stage: communicate an evidence-based claim")
        curriculum_tags([("SC5-WS-06.2", "✓")], key="communicate_claim")

    elif part == 3:
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
