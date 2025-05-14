import streamlit.components.v1 as components

with open("periodic_simulator_fixed.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=700, scrolling=True)
