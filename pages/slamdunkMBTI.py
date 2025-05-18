
import streamlit as st
import os

st.set_page_config(page_title="슬램덩크 MBTI 테스트", layout="centered")

st.title("🏀 슬램덩크 MBTI 성향 테스트")
st.markdown("**슬램덩크 속 장면을 통해 당신의 성향을 알아보세요!**")

# 점수 초기화
# 점수 및 페이지 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

questions = [
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEihIbPosC0grMvcg6A7ofLIKJ3kDgYw2KiyaXth7gmqJgpvQkUWoah-Vg6fn-qQjYBUCTeLBeKcjJtO0PoqPsdcF9AuUHWZb6monRjHEvBmwWFw3WqV-MAWPrQhSt5gtDeeE9vnVfYw90B-/s1600/Slam+Dunk+01_011.jpg", "경기 첫 출전, 당신은?", ["무조건 돌진! 부딪히며 배운다", "분석하고 흐름을 읽는다"], ["E", "P"], ["I", "J"]),
    ("http://t1.daumcdn.net/brunch/service/user/c7d1/image/zVQHDoo7t1iTCgMRvIVsdOG8gjs.png", "혼자 남은 체육관에서?", ["조용히 연습하며 집중", "사람들과 함께하고 싶음"], ["I", "S"], ["E", "F"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjxY8WCL3kAIVX0KKlH8C75-3PVjY9bKK4xH7lJA0bDHDkKeIdpxhsPwD_INZt6VH1xmkK4aXv_3vi4xc1gLk0-rKd3V2AV6Cdw-eOmijnffrf2gZrk1lWscYne-F4q7XipypCHC6a2-nEW/s1600/Slam+Dunk+03_122.jpg", "팀이 위기에 빠졌을 때?", ["큰 소리로 독려", "조용히 작전 변경"], ["E", "T"], ["I", "F"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhlXLHZjQYEwkczfwTpGTGoTxZOW43ntSdz5Fd68GRw43gID6rKiSVAmOBlzUBffhd-aWj3L6goons5bRljucxRyGVSTNvN_JdzqiO_jWcEd-ZWamjJIXj8_8KBSS4MAmTpRhQqGbP8t11D/s1600/Slam+Dunk+02_032.jpg", "라이벌과 충돌!", ["경쟁심 활활", "협력하며 균형"], ["T", "J"], ["F", "P"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg0t9zNuOY2vfZcXqHuOwmMd01aEbj1uUoB7jPqj0ba-9mv3-eftTiievahEiO2umvFC5w0gl9F9djnRNRCCQTCQjpbKjgCd9r58cEwyrFQ_kwLWgOye0WY58ANWoDj2kZpVHCiJXqzpifK/s1600/Slam+Dunk+01_098.jpg", "감독에게 꾸중 들었다면?", ["말대꾸 & 반항", "묵묵히 증명"], ["E", "P"], ["I", "J"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi81HrF1UMzWqtByDx7t6unn3T2n1ZM-AjStbw7jP85YqjqBMuYRanwsO3gMLrDMgx9ledEEZLGhcJ0_qYctwI9grywCdstdfoe6CFm6o9mtVWYMdHGB3MmxI5cMtWu20QkDizwIPqEomhP/s1600/Slam+Dunk+01_101.jpg", "남는 시간 당신은?", ["체력 훈련", "작전 상상"], ["S", "J"], ["N", "P"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgIu6QzSBu3CtxeTmDtStOpDP1V4qlK-r3YaWR1oHbpJPdv_oKyiU9rMRKZ7PknhC4YV7oUpzNEr7t0Ej-_bDbYAgIN-jY_CSILSEREOAtryVX1xIJ-xUHWHKob07IQrEUNp71Jyz28e1qE/s1600/Slam+Dunk+02_089.jpg", "당신의 습관은?", ["루틴대로 움직임", "즉흥적으로 행동"], ["S", "J"], ["N", "P"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjoUtZ9bNbf3PbMnRTlVWyBXYvM7yJWRYs6hGM070b2cR1lmKFHGMmWWKH-KNfR2r8-YHFO3p7qRNUOSGnHvhIs66EfHFuxYU5Z66oQjZCDKSANf9wGTVNGrAjKlB40RBhEXrcZCRr9Zi3H/s1600/Slam+Dunk+02_101.jpg", "팀원과 싸웠을 때?", ["감정 바로 풀기", "생각 정리 후 대화"], ["F", "E"], ["T", "I"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTM-VhFjwlUDSIBtvIr_xungVRuhEUu_kujAoZ7tX_aw0-zt6Ghb9Bt36Ik_6aH0jkt88PFE5340kzz89_wqtsG6MG6RCFyjCXwVYJn-pFUVznivlZsjt0gPi91-g3Tr6dmNc3CCTKla0v/s1600/Slam+Dunk+13_121.jpg", "중요한 경기 전날?", ["계획 복습", "마음 편히 잠"], ["J", "T"], ["P", "F"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg5R5EfE-c2fW4oLMD3p1Vl7OE_sXWuubYhaXbsoiL8OV7kV5uCYOOi4rEwSe5H3zIsoO_H8gWt_NW4GkZlhHhrRTTiv1KfQPe3AF3OwvqZfZhomiMQSzy0BOxoXHXJmgmlSY-47WnQWi68/s1600/Slam+Dunk+01_062.jpg", "관중석에 누군가 왔다!", ["신경 쓰임", "경기에만 집중"], ["F", "E"], ["T", "I"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7uPfAlN4_Lbrq8AGFKC0A58TKDRyvpm4101PxPhU1wK0FnyDCiPVkx2nR3kfvs8A1BAfO1WwVmyb5NLLH0EzydIWS7rpm_Hie8AUFNy4D7QitwW9gH5skD8Omz7UyQ3CYocukGXf6LkI2/s1600/Slam+Dunk+09_072.jpg", "이긴 후 당신은?", ["함께 외치며 축하", "속으로 뿌듯"], ["E", "F"], ["I", "T"]),
    ("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVFlHJ7xyCm7BYFmirUSW0KO3ZCqlI3mNHWaDvaTbQs5CtNtx8ZhMvT1y_sCHCpUHKKpmyHKRgc3jHEF90Uk2z1sH6t8PZ6CGof7pU4grpWcMcX5sej-nqKOg_mERzmlFqRr_OFFQm87z_/s1600/Slam+Dunk+05_028.jpg", "졌을 때 당신은?", ["다음 각오 다짐", "멍 때리며 감정에 빠짐"], ["N", "J"], ["S", "F"])
]


q_count = len(questions)

if st.session_state.page < q_count:
    img, q, options, type_a, type_b = questions[st.session_state.page]

    if img.startswith("http"):
        st.image(img, use_container_width=True)
    elif os.path.exists(img):
        st.image(img, use_container_width=True)
    else:
        st.warning(f"이미지를 찾을 수 없습니다: {img}")

    ans = st.radio(f"**Q{st.session_state.page + 1}. {q}**", options, key=st.session_state.page)
    if st.button("다음"):
        st.session_state.answers.append(ans)
        if ans == options[0]:
            for t in type_a:
                st.session_state.score[t] += 1
        else:
            for t in type_b:
                st.session_state.score[t] += 1
        st.session_state.page += 1
        st.rerun()

result = {
    "ESTJ": [
        "채치수",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj-N-CWdlFyHhqkM3t_BDYIpGxGMkLx47goo5EbfsRp9h3747gXHmk9LJhDqI-wN_qjgjT42q2jQmVE7pC5ccJVf7q_hENiICnWxZhQxaKq3jwhCuFvs8U598tZhZS2IM35IBRH6QqYQXsJ/s1600/Slam+Dunk+22_042.jpg",
        "현실적이고 규칙 중심적인 리더. 항상 팀을 먼저 생각하고 원칙을 중시한다.",
        "“넌 기본이 안 돼 있어!”"
    ],
    "ISTJ": [
        "송태섭",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj-npzvdJqeUPsi6BeU0GM65OX02cdW8vK6XisqpGo7OiPrnWmDUzd-DfIU1Kurm59uI2QPmKcLfl-UKhqynM1S88e3gLrgaOlSKuA9GVLwNd7YW66yYFAhadHcFsrNkGLd9Smw1YeiDmj7/s1600/Slam+Dunk+09_098.jpg",
        "꼼꼼하고 신중한 성격의 수비 전문 플레이어. 항상 계산적인 경기 운영을 선호한다.",
        "“내가 막을게.”"
    ],
    "ESFJ": [
        "이한나",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjuI9bEnCDfLrnQ6Zazkv4_OOtfA2JluLSLMpG0XONVS1qP5kX4JkQZvFOX72Q2dwYPIpyfln9y_13_tyUL-I2vOzlvrMgEZxP8N__JR1sg5pGf_ouffwEGyLI_o2N4Aa73bLfkjFbqf4WL/s1600/Slam+Dunk+21_060.jpg",
        "팀원 하나하나를 세심히 챙기며 헌신하는 리더십을 발휘하는 조율자.",
        "“정대만! 그만해!!”"
    ],
    "ISFJ": [
        "채소연",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhVdwuzQQolg72em3h6HejaEwOpybtXJqoWwrfbOrV-tutGJVlHGMReBT3APrtk8c7pdixt2X8cazfXCHD_FA3Njt3twFFZOdysHbK1PluYYKrIUKtaPf0pFw9TwC_N_hR_rQ7n5pXyaxXy/s1600/Slam+Dunk+01_092.jpg",
        "배려심이 많고 조용히 응원하는 스타일. 주변을 따뜻하게 만든다.",
        "“강백호 군… 멋져요!”"
    ],
    "ENTJ": [
        "이정환",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhDtWRdYoSzH9amQM2c72lfoZ6QtSm_jp08pXbSsg2wjelYOLHo1akUgJo-fCEuNge1OZl_Vx0G39hZFtSJRLi5QPsIV-XEG5TOtxZ0IncbXy56X6srnZFYX3y2C4rdc7xxbHaAq54wLwL7/s1600/Slam+Dunk+09_090.jpg",
        "전략적인 사고로 경기를 이끄는 완벽주의 리더. 냉정하고 목표 지향적이다.",
        "“이 경기는 내가 끝낸다.”"
    ],
    "INTJ": [
        "정우성",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPIeMav1h3b4fLgIXmdXenrgqVAuAetn4ry6EHx_mOIp33QDugTbI0cqS4enB0P_3-lLtlS8rlYO33RQv4jr0tJSZZtXTGWtfnNu714nLpuPgG57gwUm34Sj_qloMyzl7kzw3mhJxjGYHN/s1600/Slam+Dunk+22_105.jpg",
        "경기 흐름을 예측하고 분석하는 전략가. 항상 이기는 방법을 계산한다.",
        "“흐름은 우리 쪽이다.”"
    ],
    "ENFJ": [
        "아야코",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgf_KP7FGGT6qUiCu4tH4bp3RCMTax1DpwmnuXLUkpDeqCEMVXi8EY0luuyI9J6m-zP3BkzhaXm26Wy2JerS5mvRvNyHrVXrF5KpeflNjMqWou6RR1luhHrQGjQvY4XOGLU7puRuWBPVYJD/s1600/Slam+Dunk+07_032.jpg",
        "감성적이고 따뜻한 리더. 팀의 분위기를 이끌며 감정적으로도 중심을 잡는다.",
        "“무리하지 마!”"
    ],
    "INFJ": [
        "정우성(내면)",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgKVqtHF8MjQBgNpxjo6pnxfIeHPrScoNiAj34j7FCgQ4o1sE_Yrir4WUJsZUosG6kcp7HiE9fxwURKaf_XH7UjB4UjPNhwD1rZmrNqB7Mrb0qcKrWMym7t2jNmXzB8v72moGXXt-Abll8J/s1600/Slam+Dunk+09_092.jpg",
        "강인한 외면 아래 팀과의 유대와 목표를 내면 깊이 간직한 이상주의자.",
        "“지금은 보여줄 때야.”"
    ],
    "ESTP": [
        "상양 센터",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjh7Ana_pDZsNQYqTbavOYktoRCaYah3no1QthWQMvrxsIMl6N8bJj5d6JsUtHyUD7UjnbQlDGjpYNTqi2xu5QbRk6hjfz6eAyTJySEx1HlA4gK3J11noaPRPuPXqZL9TMJLZ8JMz7FUQ3n/s1600/Slam+Dunk+01_059.jpg",
        "직감적이고 즉흥적인 플레이어. 본능적으로 움직이며 팀의 흐름을 뒤흔든다.",
        "“박살내주마.”"
    ],
    "ISTP": [
        "미츠이 히사시",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjyF4laJ3OaLiImGD__aUhSb8zbgUsNAxVSczWrkV6q2pUnPw_EQHZJbst9DhFmy-dSkgj92D_d09LPvg8wWpeOCUlUIJ3BKr6VW5ilZGRbVeMnWrQx0YXLL5dXr56Pfyq8lEBPBD_mVlMj/s1600/Slam+Dunk+07_033.jpg",
        "냉정하고 침착한 판단력의 소유자. 결정적 순간에 강한 현실적 승부사.",
        "“아직 농구가 하고 싶다.”"
    ],
    "ESFP": [
        "강백호(초기)",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRafrPkxp_gZH7UuXELmizEk1PgJ3TdLfl61SLuFypOkEe0hzOHlxBBt4sZVAMNWb5YO072r2f69xCwpcfuNHEr2Lc3bLY0PvpICd1COOmxsQSvJ7ErGRcFxrYiwNUxpO1JmjJ9JOAK9BZ/s1600/Slam+Dunk+08_088.jpg",
        "감정적이고 즉흥적인 행동파. 분위기 메이커이자 예측불가.",
        "“하루코씨~!!”"
    ],
    "ISFP": [
        "정대만",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj5r5X6H36inLtK6A3PQsPB2p1STXwd3v7RNIB2cpE9wzEgjz_CSVOAtelZ5W8auyxryQEhcYdsIWVaOSX-J7JbZSqJyzuc4iUdBafX2AxUL91wlT4-wR3fPBUHCHp1-gJHfZPZurc02lsv/s1600/Slam+Dunk+07_013.jpg",
        "감정을 드러내지 않지만 내면은 누구보다 뜨거운 이상주의자.",
        "“과거는 지우고 싶지 않다.”"
    ],
    "ENFP": [
        "강백호",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikxmuF1XGSvUFT6pkw0u_wecqKJ0b8LL8d9qSeqtbWxisFWS9k2Zfp3B2oJtGiHkgCH-8i8ibEFm4yqBD6J3l4E4BwjCFclHai18pLJcu3jPdSXg1otIYCFDQvUmUoptzGlz_5BQwE7oRQ/s1600/Slam+Dunk+07_113.jpg",
        "열정적이고 감성적인 플레이어. 실수도 많지만 누구보다 진심이다.",
        "“리바운드~!!”"
    ],
    "INFP": [
        "하나미치 팬",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEghdl8SrH4gsWckRaFOvLxmdNOrtyXpAEBDR3NBIoK59UKMs4dGWUk6Ouqis59azq2Bgpl2Shp07HNg9GEFt8mx41jJmQTbIVMYyyLKY_ojAAZAS3YAT_IARfvX4R0hZPqBnzbywtkvpooN/s1600/Slam+Dunk+11_122.jpg",
        "감성을 기반으로 농구를 사랑하는 순수한 열정의 인물.",
        "“강백호 최고야!”"
    ],
    "ENTP": [
        "안 감독",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg_cnkGF2LSvVcCQE_-B7oTvyICUH9QsIV7qfJfDaug1xZtDnsgF8IbIIhw4ZFzEHHK_2JgtVRsM8QNhIijdY_-fqfyL8_r9h206OWhyphenhyphengNbi2PMpSUJR_tIAr58rTLlLDvfKeB9o_fXVyOz/s1600/Slam+Dunk+01_114.jpg",
        "재치 있고 유쾌한 분위기 메이커. 상황을 전환하는 지략가형 감독.",
        "“넌 아직 멀었어.”"
    ]
}
else:
    score = st.session_state.score
    mbti = ""
    mbti += "E" if score["E"] >= score["I"] else "I"
    mbti += "S" if score["S"] >= score["N"] else "N"
    mbti += "T" if score["T"] >= score["F"] else "F"
    mbti += "J" if score["J"] >= score["P"] else "P"

    name, img_path, desc, quote = result.get(mbti, ("알 수 없음", "", "결과 없음", "명대사 없음"))

    st.markdown(f"## 당신의 MBTI 유형은: **{mbti} ({name})**")

    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    elif img_path.startswith("http"):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"결과 이미지가 없습니다: {img_path}")

    st.markdown("### 🧠 캐릭터 성향 설명")
    st.markdown(desc)
    st.markdown("### 🗣️ 명대사")
    st.markdown(f"> {quote}")

    if st.button("🔁 다시 테스트하기"):
        st.session_state.page = 0
        st.session_state.score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.session_state.answers = []
        st.rerun()
