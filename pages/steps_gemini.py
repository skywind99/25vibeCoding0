import streamlit as st
import google.generativeai as genai

# Gemini API 키 설정
genai.configure(api_key="AIzaSyAoOn5okbLOLYXUeqwTWTuGg7aPKLGdmYs")  # <- 여기에 본인의 API 키 입력

# 모델 선택
model = genai.GenerativeModel("gemini-pro")

# Streamlit 웹앱 UI 구성
st.title("🌤️ Gemini에게 날씨 물어보기")

# 사용자 입력
user_input = st.text_input("날씨가 궁금한 지역이나 질문을 입력하세요", "오늘 서울 날씨 어때?")

# 버튼 누르면 응답 생성
if st.button("확인"):
    if user_input:
        with st.spinner("Gemini가 정보를 찾고 있어요..."):
            try:
                response = model.generate_content(f"{user_input} 날씨 알려줘. 최신 정보로 대답해줘.")
                st.markdown("### 📡 Gemini의 답변")
                st.write(response.text)
            except Exception as e:
                st.error(f"에러 발생: {e}")
    else:
        st.warning("먼저 질문을 입력해주세요.")
