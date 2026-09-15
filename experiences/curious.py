"""Small guided Template Experience.

This module owns the facilitator-led lesson sequence. It deliberately contains
neutral placeholders rather than subject-specific pedagogy.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from experiences import router
from ui_helpers import (
    hard_reveal,
    facilitator_preparation,
    notice_prompt,
    page_header,
    placeholder_callout,
    predict_prompt,
    response_box,
    scroll_to_top_if_requested,
    step_buttons,
    step_tabs,
)

STEP_LABELS = [
    "Welcome",
    "1 · Context",
    "2 · Meet the data",
]


def render(data: pd.DataFrame) -> None:
    part = int(st.session_state.get("curious_part", 0))
    part = max(0, min(part, len(STEP_LABELS) - 1))
    page_header("Template Experience")
    _, selected = step_tabs(STEP_LABELS, "curious_step_selector", part)
    if selected != part:
        part = selected
        st.session_state["curious_part"] = part
        st.session_state["curious_scroll_to_top"] = True
    scroll_to_top_if_requested("curious_scroll_to_top")

    facilitator_preparation(
        "Let learners make a quick prediction before revealing evidence. Listen for a specific observation or question, then let them compare it with what the data show.",
    )

    st.header(STEP_LABELS[part])
    if part == 0:
        st.write("A compact reference sequence for separating reasoning from evidence.")
        placeholder_callout(
            "Information",
            "This demonstration dataset is synthetic. Use it to practise data questions, not to make claims about the named artists.",
        )
        predict_prompt(
            "Before looking at evidence, what pattern would you expect between two variables? "
            "What would count as evidence for it?"
        )
        evidence_revealed = hard_reveal(
            "State a prediction, then identify the pattern you would look for in a scatter plot.",
            "curious_context_evidence",
            reveal_label="Reveal an evidence example",
            revealed_content="Example evidence statement: the points trend upward overall, but the spread shows that the relationship is not exact.",
            pre_reveal_label="Predict first",
            pre_reveal_guidance="Discuss or note your prediction before revealing the example.",
        )
        if evidence_revealed:
            response_box(
                "Optional: record one observation you would check against a chart.",
                "curious_context_response",
                sentence_starters="I predict… because… / I would look for…",
            )
    elif part == 1:
        st.write("Give learners the context they need to make sense of the investigation.")
        placeholder_callout("Context", "Keep only the background needed for the question and evidence ahead.")
        notice_prompt("What detail in this context will matter when you interpret the evidence later?")
    elif part == 2:
        st.write("Inspect what one row represents and what the key variables measure.")
        notice_prompt("What does one row represent, and which two fields could help answer a question?")
        st.dataframe(data.head(6), hide_index=True)
    step_buttons(
        STEP_LABELS,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
        terminal_action=router.go_home,
        terminal_label="Back to experiences",
    )
