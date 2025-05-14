import streamlit as st
import streamlit.components.v1 as components

# 수정된 경로로 HTML 파일 읽기
with open("/periodic_simulator_fixed.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Streamlit에 HTML 렌더링
components.html(html_code, height=700, scrolling=True)
