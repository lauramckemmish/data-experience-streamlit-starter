"""Canonical rendered examples of selected shared starter patterns."""

from __future__ import annotations

import config
import streamlit as st

from ui_helpers import key_idea, media_text_pair, page_header, role_image, self_check, soft_reveal


def render() -> None:
    """Render the small non-narrative pattern reference surface."""
    page_header("Pattern Reference", teacher_control=False)

    with self_check("Compare your observation"):
        st.write("A useful observation points to specific evidence and explains why it may matter.")

    with soft_reveal("Optional supporting detail"):
        st.write("This optional detail supports interpretation without changing what learners must do next.")

    key_idea(
        "A key idea states what evidence supports; it is not a success or completion message."
    )

    role_image(
        config.ASSETS_DIR / "starter-hero.svg",
        role="context",
        caption="Context image treatment: use a relevant image to establish the setting.",
        key="pattern_reference_context",
    )

    with media_text_pair(
        config.ASSETS_DIR / "starter-hero.svg",
        role="support",
        caption="Support media treatment: keep the explanation directly associated with the image.",
        key="pattern_reference_support",
    ):
        st.markdown("#### Associated explanation")
        st.write("Use this paired layout when supporting media and its explanation should be understood together.")
