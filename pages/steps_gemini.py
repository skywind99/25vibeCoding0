import streamlit as st
import google.generativeai as genai
import os

# Gemini API 키 가져오기
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

st.title("Gemini 스무고개 AI")

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_count = 0
    st.session_state.last_question = "이 고민은 인간관계와 관련 있나요?"

# 이전 대화 표시
for q, a in st.session_state.history:
    st.markdown(f"**Q:** {q}  \n**A:** {a}")

st.markdown(f"### 🤖 {st.session_state.last_question}")
answer = st.radio("답변:", ("예", "아니오", "모르겠음"))

if st.button("답변 제출"):
    st.session_state.history.append((st.session_state.last_question, answer))
    st.session_state.question_count += 1

    if st.session_state.question_count >= 20:
        prompt = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.history])
        prompt += "\n이 고민은 무엇이고 어떤 조언을 주면 좋을까?"

        response = model.generate_content(prompt)
        st.success(response.text)

    else:
        prompt = "다음은 상담 AI의 대화입니다.\n"
        prompt += "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.history])
        prompt += "\n다음 예/아니오 질문 하나만 생성해줘."

        response = model.generate_content(prompt)
        st.session_state.last_question = response.text.strip()
        st.experimental_rerun()
