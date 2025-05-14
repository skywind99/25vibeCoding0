# Streamlit 앱: 주기율표 시각화 + 조합 시뮬레이터 (기본 기능 구현)
import streamlit as st
import pandas as pd
import json

# 원소 정보 불러오기 (간단화된 예시)
elements = [
    {"symbol": "H", "name": "Hydrogen", "atomic_number": 1},
    {"symbol": "He", "name": "Helium", "atomic_number": 2},
    {"symbol": "O", "name": "Oxygen", "atomic_number": 8},
    {"symbol": "C", "name": "Carbon", "atomic_number": 6},
    {"symbol": "N", "name": "Nitrogen", "atomic_number": 7},
    # 확장 가능: H~Og까지 전체 118개 추가 가능
]

# 선택된 원소 저장용 세션 상태 초기화
if "selected_elements" not in st.session_state:
    st.session_state.selected_elements = []

st.title("🧪 주기율표 시각화 + 조합 시뮬레이터")

# 주기율표 UI
st.subheader("원소 선택")
cols = st.columns(6)
for i, element in enumerate(elements):
    with cols[i % 6]:
        if st.button(f"{element['symbol']}"):
            st.session_state.selected_elements.append(element)

# 선택된 원소 보여주기
st.subheader("선택된 원소")
if st.session_state.selected_elements:
    for el in st.session_state.selected_elements:
        st.markdown(f"**{el['symbol']}** - {el['name']} (원자번호 {el['atomic_number']})")
else:
    st.write("아직 선택된 원소가 없습니다.")

# 조합 버튼 및 결과
if st.button("🔬 화합물 조합 시도"):
    symbols = sorted([el['symbol'] for el in st.session_state.selected_elements])
    formula = "".join(symbols)

    # 아주 간단한 룰 기반 반응 판단 예시
    known_combinations = {
        "HHO": "H₂O (물)",
        "COO": "CO₂ (이산화탄소)",
        "CHH": "CH₄ (메테인)",
    }

    result = known_combinations.get(formula, "알 수 없는 조합입니다.")
    st.markdown(f"### 🧪 결과: {result}")

# 초기화 버튼
if st.button("🔄 초기화"):
    st.session_state.selected_elements = []
