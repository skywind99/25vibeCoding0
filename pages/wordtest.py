import streamlit as st
import pandas as pd

# 예시 단어장 데이터
default_data = [
    {"단어": "apple", "뜻": "사과"},
    {"단어": "run", "뜻": "달리다"},
    {"단어": "book", "뜻": "책"},
    {"단어": "computer", "뜻": "컴퓨터"},
    {"단어": "pencil", "뜻": "연필"}
]

# 세션 상태 초기화
if 'words' not in st.session_state:
    st.session_state.words = default_data
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'mode' not in st.session_state:
    st.session_state.mode = 'list'  # list, quiz, result

st.title("📘 단어장 테스트 웹앱")

# 단어장 전체 목록 보기
if st.session_state.mode == 'list':
    st.subheader("전체 단어 목록")
    st.dataframe(pd.DataFrame(st.session_state.words))

    if st.button("테스트 시작"):
        st.session_state.mode = 'quiz'
        st.session_state.current_index = 0
        st.session_state.answers = []

# 퀴즈 모드
elif st.session_state.mode == 'quiz':
    index = st.session_state.current_index
    word_data = st.session_state.words[index]
    st.subheader(f"단어 {index + 1} / {len(st.session_state.words)}")
    st.markdown(f"**단어:** {word_data['단어']}")

    user_answer = st.text_input("뜻을 입력하세요:", key=f"answer_{index}")
    if st.button("확인"):
        correct = user_answer.strip() == word_data["뜻"]
        st.session_state.answers.append({
            "단어": word_data["단어"],
            "입력한 뜻": user_answer.strip(),
            "정답": word_data["뜻"],
            "결과": "정답" if correct else "오답"
        })

        st.session_state.current_index += 1

        if st.session_state.current_index >= len(st.session_state.words):
            st.session_state.mode = 'result'

        st.experimental_rerun()

# 결과 보기
elif st.session_state.mode == 'result':
    st.subheader("📊 테스트 결과")

    df = pd.DataFrame(st.session_state.answers)
    st.dataframe(df)

    wrong_df = df[df["결과"] == "오답"]
    if not wrong_df.empty:
        st.warning("틀린 단어 목록")
        st.dataframe(wrong_df[["단어", "입력한 뜻", "정답"]])
    else:
        st.success("모든 단어를 맞췄습니다! 잘했어요!")

    if st.button("다시 테스트하기"):
        st.session_state.mode = 'list'
        st.session_state.current_index = 0
        st.session_state.answers = []
