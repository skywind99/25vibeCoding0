import streamlit as st
import google.generativeai as genai
import os

# API 키 환경변수에서 읽기
GOOGLE_API_KEY = os.getenv("AIzaSyAoOn5okbLOLYXUeqwTWTuGg7aPKLGdmYs")

# 키 없으면 에러 처리
if not GOOGLE_API_KEY:
    st.error("❌ 환경변수 'GOOGLE_API_KEY'가 설정되지 않았습니다.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

    # 모델 초기화
    model = genai.GenerativeModel("gemini-pro")

    # UI
    st.title("🌦️ Gemini 날씨 질문 앱")
    user_input = st.text_input("날씨 질문을 입력하세요", "오늘 부산 날씨 어때?")

    if st.button("질문하기"):
        if user_input:
            with st.spinner("Gemini가 답변 중..."):
                try:
                    response = model.generate_content(user_input)
                    st.markdown("### 🤖 Gemini의 답변")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"에러 발생: {e}")
