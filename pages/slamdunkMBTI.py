
import streamlit as st
import os

st.set_page_config(page_title="슬램덩크 MBTI 테스트", layout="centered")

st.title("🏀 슬램덩크 MBTI 성향 테스트")
st.markdown("**슬램덩크 속 장면을 통해 당신의 성향을 알아보세요!**")

# 점수 초기화
score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

questions = [
    ("img/q1.png", "경기 첫 출전, 당신은?", ["무조건 돌진! 부딪히며 배운다", "분석하고 흐름을 읽는다"], ["E", "P"], ["I", "J"]),
    ("http://t1.daumcdn.net/brunch/service/user/c7d1/image/zVQHDoo7t1iTCgMRvIVsdOG8gjs.png", "혼자 남은 체육관에서?", ["조용히 연습하며 집중", "사람들과 함께하고 싶음"], ["I", "S"], ["E", "F"]),
    ("img/q3.png", "팀이 위기에 빠졌을 때?", ["큰 소리로 독려", "조용히 작전 변경"], ["E", "T"], ["I", "F"]),
    ("img/q4.png", "라이벌과 충돌!", ["경쟁심 활활", "협력하며 균형"], ["T", "J"], ["F", "P"]),
    ("img/q5.png", "감독에게 꾸중 들었다면?", ["말대꾸 & 반항", "묵묵히 증명"], ["E", "P"], ["I", "J"]),
    ("img/q6.png", "남는 시간 당신은?", ["체력 훈련", "작전 상상"], ["S", "J"], ["N", "P"]),
    ("img/q7.png", "당신의 습관은?", ["루틴대로 움직임", "즉흥적으로 행동"], ["S", "J"], ["N", "P"]),
    ("img/q8.png", "팀원과 싸웠을 때?", ["감정 바로 풀기", "생각 정리 후 대화"], ["F", "E"], ["T", "I"]),
    ("img/q9.png", "중요한 경기 전날?", ["계획 복습", "마음 편히 잠"], ["J", "T"], ["P", "F"]),
    ("img/q10.png", "관중석에 누군가 왔다!", ["신경 쓰임", "경기에만 집중"], ["F", "E"], ["T", "I"]),
    ("img/q11.png", "이긴 후 당신은?", ["함께 외치며 축하", "속으로 뿌듯"], ["E", "F"], ["I", "T"]),
    ("img/q12.png", "졌을 때 당신은?", ["다음 각오 다짐", "멍 때리며 감정에 빠짐"], ["N", "J"], ["S", "F"]),
]

for idx, (img, q, options, type_a, type_b) in enumerate(questions, 1):
    if img.startswith("http"):
        st.image(img, use_container_width=True)
    elif os.path.exists(img):
        st.image(img, use_container_width=True)
    else:
        st.warning(f"이미지가 없습니다: {img}")
    ans = st.radio(f"**Q{idx}. {q}**", options, key=idx)
    if ans == options[0]:
        for t in type_a:
            score[t] += 1
    else:
        for t in type_b:
            score[t] += 1

if st.button("결과 보기"):
    mbti = ""
    mbti += "E" if score["E"] >= score["I"] else "I"
    mbti += "S" if score["S"] >= score["N"] else "N"
    mbti += "T" if score["T"] >= score["F"] else "F"
    mbti += "J" if score["J"] >= score["P"] else "P"

    result = {
        "ESTJ": ("채치수", "img/result_estj.jpg", "현실적이고 팀 중심의 리더. 규율과 책임감이 강하고 팀을 끝까지 지키는 인물.", "“넌 기본이 안 돼 있어!”"),
        "ENFP": ("강백호", "img/result_enfp.jpg", "열정적이며 감성적. 실수도 많지만 진심이 있고 팀과 함께 성장하는 인물.", "“하루코 씨~!!”"),
        "ENFJ": ("정대만", "img/result_enfj.jpg", "감성적인 리더. 사람을 이끄는 능력이 있으며, 열정과 후회가 공존함.", "“3년간… 난 뭐 했지…”"),
        "ISTJ": ("서태웅", "img/result_istj.jpg", "조용하고 실력 중심. 말보다 행동으로 보여주는 냉정한 승부사.", "“너도 농구 좋아하잖아…”"),
        "ISFJ": ("채소연", "img/result_isfj.jpg", "상냥하고 배려심 깊은 감성형. 주변을 챙기며 조용히 응원하는 스타일.", "“강백호 군… 멋져요!”"),
        "INFJ": ("채치수(내면)", "img/result_infj.jpg", "겉으로는 강하지만 속마음은 팀 걱정뿐인 헌신형 리더. 외유내강.", "“포기란 말은 없다!”"),
        "INTJ": ("정우성", "img/result_intj.jpg", "계획적이고 분석적인 지휘자. 모든 상황을 계산하고 주도하는 전략가.", "상양전 작전 지시 장면"),
        "ISTP": ("정대만", "img/result_istp.jpg", "위기에 강한 현실주의자. 침착하고 빠른 판단력, 단호한 행동력의 소유자.", "“미안하다, 나 아직 농구가 하고 싶어.”"),
        "ISFP": ("정대만(내면)", "img/result_isfp.jpg", "말 없이 묵묵히 훈련에 임하는 스타일. 감정은 깊지만 잘 드러내지 않음.", "복귀 전 회상 장면"),
        "INFP": ("채치수 동생", "img/result_infp.jpg", "조용하고 감성적인 이상주의자. 이상과 신념이 뚜렷함.", "가족 응원 장면"),
        "INTP": ("서태웅(내면)", "img/result_intp.jpg", "말은 거의 하지 않지만 내면은 복잡하고 깊은 사고를 하는 선수. 경기 흐름과 위치를 계산하며, 자신의 세계에 몰입하는 스타일입니다.", "“…… (침묵이 가장 많은 말이다)”"),
        "ESTP": ("강백호(초기)", "img/result_estp.jpg", "행동파. 충동적이고 즉흥적이며, 분위기를 흔드는 천연 기질.", "“리바운드는 내가 왕이다!”"),
        "ESFP": ("강백호(연애모드)", "img/result_esfp.jpg", "유쾌하고 사교적. 모든 상황에 감정적으로 몰입하는 감성 행동형.", "“하루코 씨~!!”"),
        "ENTP": ("안 감독", "img/result_entp.jpg", "유쾌한 조련자. 비판에도 유머로 넘기고 문제해결에 능한 스타일.", "“넌 아직 멀었어.”"),
        "ESFJ": ("이한나", "img/result_esfj.jpg", "팀원 하나하나를 아끼고 돌보는 따뜻한 리더십의 조율자.", "“정대만! 그만해!!”"),
        "ENTJ": ("이정환", "img/result_entj.jpg", "경기 흐름을 통제하고, 팀 전체를 이끄는 천부적인 리더. 냉정하고 목표 지향적이며, 결정적인 순간 주저하지 않는 승부사입니다.", "“이 경기는 내가 끝낸다.”")
    }

    name, img_path, desc, quote = result.get(mbti, ("알 수 없음", "", "결과를 찾을 수 없습니다.", ""))

    st.markdown(f"## 당신의 MBTI 유형은: **{mbti} ({name})**")
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"결과 이미지가 없습니다: {img_path}")
    st.markdown("### 🧠 캐릭터 성향 설명")
    st.markdown(desc)
    st.markdown("### 🗣️ 명대사")
    st.markdown(f"> {quote}")
    st.markdown("---")
    st.button("🔁 다시 테스트하기", on_click=lambda: st.experimental_rerun())
