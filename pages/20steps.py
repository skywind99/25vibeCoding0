import streamlit as st
import openai

# API 키 불러오기

api_key = os.getenv("STREAMLIT_KEY")

st.set_page_config(page_title="스무고개 상담AI", page_icon="🧠")
st.title("🧠 ChatGPT 스무고개 상담 AI")

# 세션 초기화
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_count = 0
    st.session_state.last_question = "당신의 고민을 맞혀볼게요! 첫 질문입니다: 이 고민은 인간관계와 관련 있나요?"

# 이전 질문/답변 표시
for i, (q, a) in enumerate(st.session_state.history, 1):
    st.markdown(f"**Q{i}:** {q}  \n**A:** {a}")

# 현재 질문
st.markdown(f"### 🤖 {st.session_state.last_question}")

# 사용자 응답 받기
answer = st.radio("당신의 대답은?", ("예", "아니오", "모르겠음"), key=st.session_state.question_count)

if st.button("답변 제출"):
    st.session_state.history.append((st.session_state.last_question, answer))
    st.session_state.question_count += 1

    # 20번 끝났을 때
    if st.session_state.question_count >= 20:
        st.markdown("🎯 20번의 질문이 끝났어요. 고민에 대한 조언을 드릴게요!")
        prompt = "다음은 상담 AI의 대화입니다:\n"
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
        prompt = "지금까지 사용자와 나눈 Q/A를 바탕으로 다음 질문을 하나 만들어주세요. 반드시 예/아니오로 대답할 수 있어야 해요.\n\n"
        for q, a in st.session_state.history:
            prompt += f"Q: {q}\nA: {a}\n"
        prompt += "다음 질문은?"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.session_state.last_question = response.choices[0].message.content
        st.experimental_rerun()
