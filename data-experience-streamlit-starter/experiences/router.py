"""Experience routing and navigation state."""

from __future__ import annotations

import streamlit as st

from config import EXPERIENCE_CURIOUS, EXPERIENCE_PLAYGROUND, EXPERIENCE_YEAR8, EXPERIENCE_YEAR10

LANDING = "Home"
VALID_EXPERIENCES = [EXPERIENCE_CURIOUS, EXPERIENCE_YEAR8, EXPERIENCE_YEAR10, EXPERIENCE_PLAYGROUND]


def open_experience(name: str) -> None:
    st.session_state["experience"] = name
    st.session_state["teacher_view"] = False
    if name == EXPERIENCE_CURIOUS:
        st.session_state["curious_part"] = 0
        st.session_state.pop("curious_step_selector", None)
        st.session_state["curious_scroll_to_top"] = True


def go_home() -> None:
    st.session_state["experience"] = LANDING


def current_experience() -> str:
    selected = st.session_state.get("experience", LANDING)
    return selected if selected in [LANDING, *VALID_EXPERIENCES] else LANDING
