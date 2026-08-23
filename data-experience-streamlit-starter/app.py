"""Application shell for the reusable data-experience starter."""

from __future__ import annotations

import streamlit as st

from config import (
    APP_ICON,
    APP_TITLE,
    EXPERIENCE_CURIOUS,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_YEAR8,
    EXPERIENCE_YEAR10,
)
from data import load_data
from experiences import curious, data_playground, landing, router, year10, year8

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

data = load_data()
current = router.current_experience()

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    if current != router.LANDING:
        st.button("← All experiences", use_container_width=True, on_click=router.go_home)
        st.divider()
        st.toggle("Teacher view", key="teacher_view")
        st.caption(f"Current experience: **{current}**")

if current == router.LANDING:
    landing.render(data, router.open_experience)
elif current == EXPERIENCE_CURIOUS:
    curious.render(data)
elif current == EXPERIENCE_YEAR8:
    year8.render(data)
elif current == EXPERIENCE_YEAR10:
    year10.render(data)
elif current == EXPERIENCE_PLAYGROUND:
    data_playground.render(data)
