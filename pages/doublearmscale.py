import streamlit as st
import random

# 초기 설정
if 'minerals' not in st.session_state:
    colors = ['빨강', '노랑', '초록', '파랑', '보라']
    minerals = []
    for color in colors:
        for i in range(2):
            weight = 10 if color == '노랑' and i < 3 else random.randint(1, 20)
            minerals.append({'color': color, 'id': f'{color}{i+1}', 'weight': weight})
    st.session_state.minerals = minerals
    st.session_state.left = []
    st.session_state.right = []

# 선택 UI
st.title("양팔저울 광물 무게 추리 게임")
selected = st.selectbox("광물을 선택하세요", [m['id'] for m in st.session_state.minerals])
side = st.radio("어느 저울에 올릴까요?", ["왼쪽", "오른쪽"])

if st.button("올리기"):
    if selected:
        mineral = next(m for m in st.session_state.minerals if m['id'] == selected)
        if side == "왼쪽":
            st.session_state.left.append(mineral)
        else:
            st.session_state.right.append(mineral)
        st.session_state.minerals = [m for m in st.session_state.minerals if m['id'] != selected]

# 저울 무게 계산
left_weight = sum(m['weight'] for m in st.session_state.left)
right_weight = sum(m['weight'] for m in st.session_state.right)

st.subheader(f"⚖️ 왼쪽: {left_weight}g vs 오른쪽: {right_weight}g")
if left_weight == right_weight:
    st.success("저울이 균형을 이룹니다!")
else:
    st.warning("저울이 기울어졌습니다.")

# 현재 저울 위 광물
st.markdown("### 🔴 왼쪽 저울")
st.write([m['id'] for m in st.session_state.left])
st.markdown("### 🔵 오른쪽 저울")
st.write([m['id'] for m in st.session_state.right])
