import streamlit as st
from random import sample
import random
from collections import Counter

# ------------------- 초기 설정 -------------------
name = ['볼개', '노랑', '초롱', '파랑', '보라']

# Streamlit session state 초기화
if 'initialized' not in st.session_state:
    weights = sample(range(1, 10), 2) + sample(range(11, 21), 2) + [10]
    random.shuffle(weights)
    st.session_state.weights = weights
    st.session_state.dictionary = dict(zip(name, weights))
    st.session_state.Tdictionary = dict(zip(weights, name))
    st.session_state.mineral = dict.fromkeys(name, 2)
    st.session_state.mainleft = dict.fromkeys(name, 0)
    st.session_state.mainright = dict.fromkeys(name, 0)
    st.session_state.assisleft = dict.fromkeys(name, 0)
    st.session_state.assisright = dict.fromkeys(name, 0)
    st.session_state.initialized = True

# ------------------- UI -------------------
st.title("평행적인 양팔저울 그래픽 게임")

st.markdown(f"\n✨ 자명구도: **{st.session_state.Tdictionary[10]}** 가 3번째로 무게가 중간이며, 무게는 10g입니다.")

st.write("\n### 현재 보유 광물")
st.json(st.session_state.mineral)

st.subheader("1 — 저울에 올린 광물 선택")

ml = st.multiselect("해당: 메인저울 왼\u쪾", options=name, key="ml")
mr = st.multiselect("해당: 메인저울 오른왼", options=name, key="mr")
al = st.multiselect("해당: 보조저울 왼\u쪾", options=name, key="al")
ar = st.multiselect("해당: 보조저울 오른왼", options=name, key="ar")

if st.button("판정: 저울 다음 발생"):
    use_list = ml + mr + al + ar
    use_dict = dict(Counter(use_list))
    remain = st.session_state.mineral.copy()

    # 유효성 검사
    for k in use_dict:
        remain[k] -= use_dict[k]
    if any(v < 0 for v in remain.values()):
        st.error("혼범: 사용 가능 각 광물 수설을 넘어선 안됩니다.")
    elif Counter(ml) == Counter(mr):
        st.warning("메인저울 왼칸과 오른칸의 광물 구성이 같습니다.")
    elif len(use_list) < 2:
        st.warning("최소 2개 광물을 올린 필요가 있습니다.")
    else:
        for color in ml: st.session_state.mainleft[color] += 1
        for color in mr: st.session_state.mainright[color] += 1
        for color in al: st.session_state.assisleft[color] += 1
        for color in ar: st.session_state.assisright[color] += 1
        st.session_state.mineral = remain

        # 저울 계산
        d = st.session_state.dictionary
        mlw = sum(st.session_state.mainleft[c] * d[c] for c in name)
        mrw = sum(st.session_state.mainright[c] * d[c] for c in name)
        alw = sum(st.session_state.assisleft[c] * d[c] for c in name)
        arw = sum(st.session_state.assisright[c] * d[c] for c in name)

        st.subheader("테스트 결과")
        st.markdown(f"**메인저울** \n\n← {mlw}g   |   {mrw}g →")
        st.markdown(f"**보조저울** \n\n← {alw}g   |   {arw}g →")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style='text-align:center;font-size:30px;'>
                📊 저울 그래픽
                <br>
                <span style='font-size:48px;'>🔹 ⚖️ 🔸</span>
                </div>
            """, unsafe_allow_html=True)

        # 정답 맞추기
        if mlw == mrw:
            guess = st.text_input("호칭: 광물 무게 예시 - 1,10,3,15,20")
            if st.button("정답 제출"):
                try:
                    answer = list(map(int, guess.split(',')))
                    if answer == st.session_state.weights:
                        st.success("✔️ 정답입니다! 반사합니다.")
                    else:
                        st.error("❌ 정답이 아니입니다.")
                except:
                    st.error("인수 5개를 쉽게 구분해 입력해주세요.")
