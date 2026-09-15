"""Experience routing and navigation state."""

from __future__ import annotations

import streamlit as st

from config import EXPERIENCE_PATTERN_REFERENCE, EXPERIENCE_PLAYGROUND, EXPERIENCE_TEMPLATE
from experiences.catalog import enabled_experience_names

LANDING = "Home"


def valid_experiences() -> list[str]:
    return enabled_experience_names()


def navigation_options() -> list[str]:
    return [LANDING, *valid_experiences()]


def open_experience(name: str) -> None:
    if name not in navigation_options():
        go_home()
        return
    st.session_state["experience"] = name
    st.session_state["experience_navigation"] = name
    if name == EXPERIENCE_TEMPLATE:
        st.session_state["curious_part"] = 0
        st.session_state.pop("curious_step_selector", None)
        st.session_state["curious_scroll_to_top"] = True


def go_home() -> None:
    open_experience(LANDING)


def current_experience() -> str:
    selected = st.session_state.get("experience", LANDING)
    return selected if selected in navigation_options() else LANDING


def _sync_navigation() -> None:
    selected = st.session_state.get("experience_navigation", LANDING)
    if selected in navigation_options():
        open_experience(selected)
    else:
        go_home()


def render_sidebar_navigation() -> None:
    """Render the persistent experience navigator in the sidebar."""
    current = current_experience()
    options = navigation_options()
    if st.session_state.get("experience_navigation") not in options:
        st.session_state["experience_navigation"] = current
    elif st.session_state.get("experience_navigation") != current:
        st.session_state["experience_navigation"] = current

    st.button("🏠 Start here", type="primary" if current == LANDING else "secondary",
              use_container_width=True, disabled=current == LANDING,
              on_click=go_home)
    for section_label, name in (
        ("Learn", EXPERIENCE_TEMPLATE),
        ("Explore data", EXPERIENCE_PLAYGROUND),
        ("Reference", EXPERIENCE_PATTERN_REFERENCE),
    ):
        st.markdown(f"#### {section_label}")
        selected = name == current
        st.button(
            name,
            type="primary" if selected else "secondary",
            use_container_width=True,
            disabled=selected,
            on_click=open_experience,
            args=(name,),
        )
