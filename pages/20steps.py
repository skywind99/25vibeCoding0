import streamlit as st
import openai

# OpenAI API 키 입력
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧠 ChatGPT 스무고개 상담 AI")

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_count = 0
    st.session_state.last_question = "당신의 고민을 맞혀볼게요! 첫 질문입니다: 이 고민은 인간관계와 관련 있나요?"

# 이전 대화 보여주기
for idx, (q, a) in enumerate(st.session_state.history, start=1):
    st.markdown(f"**Q{idx}:** {q}  \n**A:** {a}")

# 질문 출력
st.markdown(f"### 🤖 {st.session_state.last_question}")

# 사용자 응답 받기
answer = st.radio("당신의 대답은?", ("예", "아니오", "모르겠음"), key=st.session_state.question_count)

if st.button("답변 제출"):
    st.session_state.history.append((st.session_state.last_question, answer))
    st.session_state.question_count += 1

    if st.session_state.question_count >= 20:
        st.markdown("🎉 20번의 질문이 끝났어요. 이제 고민에 대한 조언을 드릴게요!")
        prompt = "다음은 사용자의 고민을 예측하고 조언을 제공하는 상담 AI입니다.\n"
        for q, a in st.session_state.history:
            prompt += f"Q: {q}\nA: {a}\n"
        prompt += "이 고민은 무엇이며, 어떤 조언을 해주면 좋을까요?"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.success(response.choices[0].message.content)
    else:
        # 다음 질문 생성
        prompt = "당신은 고민을 추론하는 AI입니다. 지금까지 질문과 답변을 참고하여 다음 질문을 예/아니오로 답할 수 있도록 만들어주세요.\n"
        for q, a in st.session_state.history:
            prompt += f"Q: {q}\nA: {a}\n"
        prompt += "다음 질문은?"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.session_state.last_question = response.choices[0].message.content
        st.experimental_rerun()
