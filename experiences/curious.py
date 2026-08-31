"""Blank guided CURIOUS experience.

This module owns the facilitator-led lesson sequence. It deliberately contains
neutral placeholders rather than subject-specific pedagogy.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui_helpers import (
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
        st.write("A compact reference sequence for separating reasoning from evidence.")
        placeholder_callout(
            "Information",
            "This demonstration dataset is synthetic. Use it to practise data questions, not to make claims about the named artists.",
        )
        think_prompt("Before looking at evidence, what pattern would you expect between two variables? What would count as evidence for it?")
        evidence_revealed = hard_reveal(
            "State a prediction, then identify the pattern you would look for in a scatter plot.",
            "curious_context_evidence",
            reveal_label="Reveal an evidence example",
            revealed_content="Example evidence statement: the points trend upward overall, but the spread shows that the relationship is not exact.",
            pre_reveal_label="Think first",
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
        with soft_reveal("What makes an observation useful"):
            st.write("Make it specific enough that someone else could find it too.")
    elif part == 2:
        st.write("Inspect what one row represents and what the key variables measure.")
        st.dataframe(data.head(6), use_container_width=True, hide_index=True)
    elif part == 3:
        st.write("Use the first graph to investigate one purposeful question.")
        placeholder_callout("Reference pattern", "One graph, one question and one key idea. Keep chart logic in charts.py.")
    elif part == 4:
        st.write("Make a comparison that advances the investigation.")
        placeholder_callout("Reference pattern", "Compare groups, conditions, scales or representations only when the comparison helps answer the question.")
    elif part == 5:
        st.write("Use the most useful interactive investigation here.")
        placeholder_callout("Boundary", "Keep open-ended exploration across several variables in the separate Data Playground.")
    else:
        st.write("Return to the central question and state what the evidence supports.")
        placeholder_callout("Take-away", "Name the two or three evidence-based ideas learners should leave with.")

    step_buttons(
        STEP_LABELS,
        "curious_step_selector",
        "curious_part",
        "curious_scroll_to_top",
        part,
        "curious",
    )
