import streamlit as st
import cv2
import pytesseract
from PIL import Image
import pandas as pd
import io

# OCR 설정
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Windows는 tesseract 설치 경로로 수정

# 세션 상태 초기화
if 'words' not in st.session_state:
    st.session_state.words = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'mode' not in st.session_state:
    st.session_state.mode = 'list'  # list, quiz, result

st.title("📸 사진으로 만드는 단어장 & 테스트")

# 1. 사진 업로드 or 카메라 촬영
img_file = st.camera_input("사진을 찍거나 이미지를 업로드하세요") or st.file_uploader("또는 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if img_file:
    image = Image.open(img_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    # 2. OCR로 텍스트 추출
    text = pytesseract.image_to_string(image, lang='eng+kor')
    st.subheader("추출된 텍스트")
    st.text(text)

    # 3. 단어와 뜻 구분 (기본적으로 "단어 - 뜻" 형식이라고 가정)
    lines = [line.strip() for line in text.split('\n') if '-' in line]
    word_list = []
    for line in lines:
        try:
            word, meaning = line.split('-', 1)
            word_list.append({"단어": word.strip(), "뜻": meaning.strip()})
        except:
            continue

    if word_list:
        # 단어장
        st.session_state.words = word_list
        df = pd.DataFrame(word_list)
        st.subheader("단어장")
        st.dataframe(df)

        # 4. 복습 퀴즈 (단어 숨기기)
        if st.checkbox("단어 숨기고 뜻 보고 맞춰보기"):
            for index, row in df.iterrows():
                with st.expander(f"뜻: {row['뜻']}"):
                    st.markdown(f"**단어:** ||{row['단어']}||")

        # 5. 다운로드 기능
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("단어장 CSV로 저장", csv, "vocab_list.csv", "text/csv")

# 단어 테스트 모드
if st.session_state.mode == 'list' and st.session_state.words:
    if st.button("테스트 시작"):
        st.session_state.mode = 'quiz'
        st.session_state.current_index = 0
        st.session_state.answers = []

# 퀴즈 모드
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

            if st.session_state.current_index >= len(st.session_state.words):
                st.session_state.mode = 'result'

# 결과 보기
elif st.session_state.mode == 'result':
    st.subheader("📊 테스트 결과")

    df = pd.DataFrame(st.session_state.answers)
    st.dataframe(df)

    wrong_df = df[df["결과"] == "오답"]
    if not wrong_df.empty:
        st.warning("틀린 단어 목록")
        st.dataframe(wrong_df[["단어", "입력한 뜻", "정답"]])
    else:
        st.success("모든 단어를 맞췄습니다! 잘했어요!")

    if st.button("다시 테스트하기"):
        st.session_state.mode = 'list'
        st.session_state.current_index = 0
        st.session_state.answers = []
