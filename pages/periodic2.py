import streamlit.components.v1 as components

# HTML 파일이 현재 같은 폴더(pages/) 안에 있으므로 경로 그대로
with open("periodic_simulator_fixed.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=700, scrolling=True)
