import streamlit.components.v1 as components
import os

# 현재 파일 기준으로 HTML 경로 잡기
current_dir = os.path.dirname(__file__)  # pages/
html_path = os.path.join(current_dir, "periodic_simulator_fixed.html")

with open(html_path, "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=700, scrolling=True)
