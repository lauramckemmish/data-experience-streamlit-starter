"""Blank guided CURIOUS experience.

This module owns the facilitator-led lesson sequence. It deliberately contains
neutral placeholders rather than subject-specific pedagogy.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui_helpers import (
    completion_gate,
    hard_reveal,
    page_header,
    placeholder_callout,
    response_box,
    scroll_to_top_if_requested,
    soft_reveal,
    step_buttons,
    step_tabs,
    teacher_guidance,
    think_prompt,
)

STEP_LABELS = [
    "Welcome",
    "1 · Context",
    "2 · Meet the data",
    "3 · First pattern",
    "4 · Compare",
    "5 · Investigate",
    "Conclusion",
]


def render(data: pd.DataFrame) -> None:
    part = int(st.session_state.get("curious_part", 0))
    part = max(0, min(part, len(STEP_LABELS) - 1))
    page_header("CURIOUS")
    _, selected = step_tabs(STEP_LABELS, "curious_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["curious_part"] = part
        st.session_state["curious_scroll_to_top"] = True
    scroll_to_top_if_requested("curious_scroll_to_top")

    teacher_guidance(
        STEP_LABELS[part],
        "Let learners make a quick prediction before revealing evidence. Listen for a specific observation or question, then let them compare it with what the data show.",
    )

    st.header(STEP_LABELS[part])
    if part == 0:
        st.write("Introduce the topic, the investigation question and why this dataset is interesting.")
        placeholder_callout("Today's challenge", "Replace this with the central question for the guided experience.")
        think_prompt("What would you like to find out?")
    elif part == 1:
        st.write("Establish the real-world or scientific context students need before seeing the data.")
        evidence_revealed = hard_reveal(
            "Predict first, then check the evidence.",
            "curious_context_evidence",
            reveal_label="Reveal the evidence",
            revealed_content="Now compare your prediction with the dataset.",
        )
        if evidence_revealed:
            response = response_box(
                "Record one observation or question.",
                "curious_context_response",
                sentence_starters="I notice… / I wonder…",
            )
            completion_gate(bool(response.strip()))
            with soft_reveal("What makes an observation useful"):
                st.write("Make it specific enough that someone else could find it too.")
    elif part == 2:
        st.write("Help students understand what one row represents and what the important variables mean.")
        st.dataframe(data.head(6), use_container_width=True, hide_index=True)
    elif part == 3:
        st.write("Introduce the first purposeful visualisation or pattern.")
        placeholder_callout("Add here", "One graph, one question and one key idea. Keep the chart logic in charts.py.")
    elif part == 4:
        st.write("Give students a comparison that advances the investigation rather than simply adding another chart.")
        placeholder_callout("Add here", "A comparison between groups, conditions, scales or representations.")
    elif part == 5:
        st.write("Use the strongest interactive investigation here.")
        placeholder_callout("Boundary", "Keep open-ended multivariate exploration in the separate Data Playground experience.")
    else:
        st.write("Return to the central question and make the evidence-based conclusion explicit.")
        placeholder_callout("Take-away", "Replace this with the 2–3 ideas students should leave with.")

    step_buttons(
        STEP_LABELS,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
    )
