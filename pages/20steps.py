import streamlit as st
import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🧠 GPT-4o 스무고개 상담 AI")

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_count = 0
    st.session_state.last_question = "이 고민은 인간관계와 관련 있나요?"

# 과거 Q&A 표시
for i, (q, a) in enumerate(st.session_state.history, 1):
    st.markdown(f"**Q{i}:** {q}  \n**A:** {a}")

st.markdown(f"### 🤖 {st.session_state.last_question}")
answer = st.radio("당신의 대답은?", ("예", "아니오", "모르겠음"), key=st.session_state.question_count)

if st.button("답변 제출"):
    st.session_state.history.append((st.session_state.last_question, answer))
    st.session_state.question_count += 1

    if st.session_state.question_count >= 20:
        full_prompt = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.history])
        full_prompt += "\n이 고민은 무엇이고, 어떤 조언을 줄 수 있을까?"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}]
        )
        st.success(response.choices[0].message.content)

    else:
        followup_prompt = "지금까지 대화를 기반으로, 예/아니오로 답할 수 있는 다음 질문 하나만 만들어줘:\n"
        for q, a in st.session_state.history:
            followup_prompt += f"Q: {q}\nA: {a}\n"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": followup_prompt}]
        )
        st.session_state.last_question = response.choices[0].message.content
        st.experimental_rerun()
