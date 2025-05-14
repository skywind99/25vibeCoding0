import os
import streamlit.components.v1 as components

# HTML 파일 경로를 현재 파일 기준으로 정확히 설정
html_path = os.path.join(os.path.dirname(__file__), "..", "periodic_simulator_fixed.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=700, scrolling=True)
