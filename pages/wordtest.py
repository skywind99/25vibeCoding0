import streamlit as st
import easyocr
from PIL import Image
import pandas as pd

# 초기 세션 상태
if 'words' not in st.session_state:
    st.session_state.words = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'mode' not in st.session_state:
    st.session_state.mode = 'list'

st.title("📸 사진으로 만드는 단어장 & 테스트")

# 📤 업로드 or 📸 촬영
st.markdown("### 이미지를 업로드하거나 사진을 찍어주세요")
img_file = st.camera_input("카메라 촬영 (모바일)") or st.file_uploader("또는 이미지 업로드 (jpg/png)", type=["jpg", "jpeg", "png"])

if img_file:
    image = Image.open(img_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    with st.spinner("OCR 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'])  # 언어: 한글 + 영어
        result = reader.readtext(np.array(image), detail=0)
        text = "\n".join(result)

    st.subheader("📄 인식된 텍스트")
    st.text(text)

    # 단어와 뜻 구분
    lines = [line.strip() for line in text.split('\n') if '-' in line]
    word_list = []
    for line in lines:
        try:
            word, meaning = line.split('-', 1)
            word_list.append({"단어": word.strip(), "뜻": meaning.strip()})
        except:
            continue

    if word_list:
        st.session_state.words = word_list
        df = pd.DataFrame(word_list)
        st.subheader("📘 단어장")
        st.dataframe(df)

        # 단어 숨기기 복습
        if st.checkbox("뜻만 보고 단어 맞히기"):
            for row in df.itertuples():
                with st.expander(f"뜻: {row.뜻}"):
                    st.markdown(f"**단어:** ||{row.단어}||")

        # CSV 저장
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 단어장 CSV 저장", csv, "vocab_list.csv", "text/csv")

# 단어 테스트 시작
if st.session_state.mode == 'list' and st.session_state.words:
    if st.button("📝 단어 테스트 시작"):
        st.session_state.mode = 'quiz'
        st.session_state.current_index = 0
        st.session_state.answers = []

# 테스트 모드
elif st.session_state.mode == 'quiz':
    if st.session_state.current_index < len(st.session_state.words):
        index = st.session_state.current_index
        word_data = st.session_state.words[index]
        st.subheader(f"단어 {index + 1} / {len(st.session_state.words)}")
        st.markdown(f"**단어:** {word_data['단어']}")

        user_answer = st.text_input("뜻을 입력하세요:", key=f"answer_{index}")
        if st.button("확인"):
            correct = user_answer.strip() == word_data["뜻"]
            st.session_state.answers.append({
                "단어": word_data["단어"],
                "입력한 뜻": user_answer.strip(),
                "정답": word_data["뜻"],
                "결과": "정답" if correct else "오답"
            })
            st.session_state.current_index += 1
            st.experimental_rerun()

# 결과 보기
elif st.session_state.mode == 'result':
    st.subheader("📊 테스트 결과")

    df = pd.DataFrame(st.session_state.answers)
    st.dataframe(df)

    wrong_df = df[df["결과"] == "오답"]
    if not wrong_df.empty:
        st.warning("❌ 틀린 단어")
        st.dataframe(wrong_df[["단어", "입력한 뜻", "정답"]])
    else:
        st.success("🎉 모두 맞췄습니다!")

    if st.button("🔁 다시 테스트하기"):
        st.session_state.mode = 'list'
        st.session_state.current_index = 0
        st.session_state.answers = []
