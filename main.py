import streamlit as st

# 🎨 이모지 아이콘 포함한 직업 추천 데이터
mbti_jobs = {
    "INTJ": ["🧠 데이터 과학자", "🧬 연구원", "📊 전략 컨설턴트"],
    "INTP": ["💻 프로그래머", "📚 철학자", "🔍 시스템 분석가"],
    "ENTJ": ["🧑‍💼 CEO", "🚀 스타트업 창업가", "📈 경영 컨설턴트"],
    "ENTP": ["📈 마케팅 기획자", "🎤 방송인", "🛠️ 발명가"],
    
    "INFJ": ["🧘 심리상담사", "📖 작가", "🌍 NGO 활동가"],
    "INFP": ["🎨 일러스트레이터", "✍️ 시인/작가", "🎼 음악가"],
    "ENFJ": ["🗣️ 강연가", "👨‍🏫 교사", "👥 인사담당자"],
    "ENFP": ["🎭 배우", "🌈 브랜드 디자이너", "🎮 게임 기획자"],
    
    "ISTJ": ["📑 행정공무원", "💼 회계사", "⚖️ 법무사"],
    "ISFJ": ["👩‍⚕️ 간호사", "🏫 초등교사", "🗂️ 사무직"],
    "ESTJ": ["📋 프로젝트 매니저", "🏢 기업 관리자", "📊 통계 분석가"],
    "ESFJ": ["💬 고객 서비스 담당자", "🏥 의료보조원", "🎓 교육 코디네이터"],
    
    "ISTP": ["🔧 정비사", "🚓 경찰관", "🧗 탐험가"],
    "ISFP": ["📷 사진작가", "🎨 순수미술가", "🧴 아로마 테라피스트"],
    "ESTP": ["🚗 자동차 딜러", "🎤 이벤트 MC", "🛍️ 세일즈 마케터"],
    "ESFP": ["🎬 배우", "🎶 가수", "🎉 이벤트 플래너"]
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
