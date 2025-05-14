# Streamlit 앱: 주기율표 시각화 + 조합 시뮬레이터 (그리드 스타일)
import streamlit as st
import pandas as pd

# 원소 데이터: 일부 예시만 사용 (전체는 CSV/JSON로 확장 가능)
elements = [
    {"symbol": "H", "name": "Hydrogen", "group": 1, "period": 1},
    {"symbol": "He", "name": "Helium", "group": 18, "period": 1},
    {"symbol": "Li", "name": "Lithium", "group": 1, "period": 2},
    {"symbol": "Be", "name": "Beryllium", "group": 2, "period": 2},
    {"symbol": "B", "name": "Boron", "group": 13, "period": 2},
    {"symbol": "C", "name": "Carbon", "group": 14, "period": 2},
    {"symbol": "N", "name": "Nitrogen", "group": 15, "period": 2},
    {"symbol": "O", "name": "Oxygen", "group": 16, "period": 2},
    {"symbol": "F", "name": "Fluorine", "group": 17, "period": 2},
    {"symbol": "Ne", "name": "Neon", "group": 18, "period": 2},
    {"symbol": "Na", "name": "Sodium", "group": 1, "period": 3},
    {"symbol": "Mg", "name": "Magnesium", "group": 2, "period": 3},
    {"symbol": "Al", "name": "Aluminium", "group": 13, "period": 3},
    {"symbol": "Si", "name": "Silicon", "group": 14, "period": 3},
    {"symbol": "P", "name": "Phosphorus", "group": 15, "period": 3},
    {"symbol": "S", "name": "Sulfur", "group": 16, "period": 3},
    {"symbol": "Cl", "name": "Chlorine", "group": 17, "period": 3},
    {"symbol": "Ar", "name": "Argon", "group": 18, "period": 3},
]

# 세션 상태 초기화
if "selected_elements" not in st.session_state:
    st.session_state.selected_elements = []

st.set_page_config(layout="wide")
st.title("🧪 화학식 시뮬레이터")

# 그리드 크기
max_group = 18
max_period = 7

# 그리드 생성용 딕셔너리
grid = [[None for _ in range(max_group)] for _ in range(max_period)]
for element in elements:
    g = element["group"] - 1
    p = element["period"] - 1
    grid[p][g] = element

# 주기율표 출력
st.subheader("주기율표")
for row in grid:
    cols = st.columns(max_group)
    for idx, el in enumerate(row):
        if el:
            if cols[idx].button(el["symbol"]):
                st.session_state.selected_elements.append(el)
        else:
            cols[idx].markdown(" ")

# 선택된 원소 표시
st.subheader("선택된 원소")
if st.session_state.selected_elements:
    for el in st.session_state.selected_elements:
        st.markdown(f"**{el['symbol']}** - {el['name']}")
else:
    st.info("원소를 선택하세요.")

# 화합물 조합
def generate_formula(elements):
    count = {}
    for el in elements:
        symbol = el['symbol']
        count[symbol] = count.get(symbol, 0) + 1
    return ''.join(f"{k}{'' if v == 1 else v}" for k, v in sorted(count.items()))

known_combinations = {
    "H2O": "물 (H₂O)",
    "CO2": "이산화탄소 (CO₂)",
    "CH4": "메테인 (CH₄)",
}

if st.button("🔬 화합물 조합 시도"):
    formula = generate_formula(st.session_state.selected_elements)
    result = known_combinations.get(formula, "알 수 없는 조합입니다.")
    st.markdown(f"### 🧪 결과: {result}")

if st.button("🔄 초기화"):
    st.session_state.selected_elements = []
