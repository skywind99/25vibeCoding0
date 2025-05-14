import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide")

html_path = os.path.join(os.path.dirname(__file__), "periodic_simulator_fixed.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=800, width=0, scrolling=True)
