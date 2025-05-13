import streamlit as st

# 🎨 이모지 아이콘 포함한 직업 추천 데이터
mbti_jobs = {
    "INTJ": ["🧠 데이터 과학자", "🧬 연구원", "📊 전략 컨설턴트"],
    "INFP": ["🎨 일러스트레이터", "✍️ 작가", "🌿 심리상담가"],
    "ENTP": ["📈 마케팅 기획자", "🎤 방송인", "🛠️ 스타트업 창업가"],
    "ISFJ": ["👩‍⚕️ 간호사", "🏫 교사", "📋 행정직"],
    "ESTJ": ["💼 관리자", "📊 회계사", "📦 프로젝트 매니저"],
    "ENFP": ["🎭 배우", "🌍 NGO 활동가", "🎮 게임 기획자"],
    # 기타 유형 생략 가능... 전체 16개 만들기 가능
}

# 💡 앱 제목과 설명
st.set_page_config(page_title="MBTI 직업 추천기", page_icon="🧩")
st.title("🧩 나의 MBTI로 알아보는 직업 추천")
st.write("MBTI 유형을 선택하면 어울리는 직업을 추천해드릴게요! 💼✨")

# 🎛️ 사이드바 꾸미기
st.sidebar.header("🌈 옵션")
mbti_type = st.sidebar.selectbox("당신의 MBTI를 선택하세요", list(mbti_jobs.keys()))

# 📢 추천 직업 출력
st.subheader(f"🧭 {mbti_type} 유형에게 추천하는 직업:")
if mbti_type in mbti_jobs:
    for job in mbti_jobs[mbti_type]:
        st.success(f"{job}")
else:
    st.warning("MBTI 유형을 선택해주세요!")

# 🌟 추가 꾸미기: 풍선, 눈, 이스터에그
if st.button("🎉 추천 직업 마음에 들어요!"):
    st.balloons()

st.markdown("---")
st.caption("Made with ❤️ by 컴게gpt")
