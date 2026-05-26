"""Main entrypoint for Streamlit Cloud.

Run with: `streamlit run src/main.py`
"""
from pathlib import Path
import runpy
import os

# Ensure working directory resolution
here = Path(__file__).parent
app_path = here / "streamlit.py"

# Initialize minimal session state and run app
try:
    import streamlit as st
except Exception:
    from _stubs import st

# Initialize session state
try:
    from core.state import init_session_state
    init_session_state()
except Exception:
    # Fallback if state module unavailable
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

# Delegate to existing app implementation
runpy.run_path(str(app_path), run_name="__main__")
