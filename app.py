"""Application shell for the reusable data-experience starter."""

from __future__ import annotations

from pathlib import Path
import streamlit as st

import config
from config import (
    APP_ICON,
    SHORT_NAME,
    DATASET_NAME,
    DATASET_SOURCE_LABEL,
    DATASET_SOURCE_NOTE,
    DATASET_SOURCE_URL,
    EXPERIENCE_CURIOUS,
    EXPERIENCE_PLAYGROUND,
    EXPERIENCE_YEAR8,
    EXPERIENCE_YEAR10,
)
from data import load_data
from experiences import curious, data_playground, landing, router, year10, year8
from visual_system import apply_visual_system, sidebar_data_source, sidebar_identity

DATASET_CITATION = getattr(config, "DATASET_CITATION", None)

st.set_page_config(page_title=SHORT_NAME, page_icon=APP_ICON, layout="wide")
apply_visual_system()

data = load_data()
current = router.current_experience()

UNSW_LOGO_PATH = Path(__file__).resolve().parent / "assets" / "unsw-sydney-logo-portrait.png"

with st.sidebar:
    sidebar_identity(SHORT_NAME, UNSW_LOGO_PATH)
    sidebar_data_source(len(data), len(data.columns), DATASET_SOURCE_LABEL)
    router.render_sidebar_navigation()

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
