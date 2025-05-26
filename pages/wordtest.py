import streamlit as st
from google.oauth2 import service_account
from google.cloud import vision
import pandas as pd
from PIL import Image
import io

st.title("📸 Streamlit Cloud용 단어장 앱 (Google OCR 사용)")

# Google Vision API 클라이언트 생성
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["google"]
)
client = vision.ImageAnnotatorClient(credentials=credentials)

# 이미지 업로드 or 촬영
st.markdown("### 📤 이미지를 업로드하거나 사진을 찍으세요")
img_file = st.camera_input("모바일은 카메라 촬영 가능") or st.file_uploader("또는 이미지 업로드", type=["jpg", "jpeg", "png"])

if img_file:
    image = Image.open(img_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    # Google Vision API로 OCR
    with st.spinner("OCR 처리 중..."):
        content = io.BytesIO()
        image.save(content, format='PNG')
        image_bytes = content.getvalue()

        image_vision = vision.Image(content=image_bytes)
        response = client.text_detection(image=image_vision)
        texts = response.text_annotations

    if texts:
        raw_text = texts[0].description
        st.subheader("📄 인식된 텍스트")
        st.text(raw_text)

        # 단어 - 뜻 분리
        lines = [line.strip() for line in raw_text.split('\n') if '-' in line]
        word_list = []
        for line in lines:
            try:
                word, meaning = line.split('-', 1)
                word_list.append({"단어": word.strip(), "뜻": meaning.strip()})
            except:
                continue

        if word_list:
            df = pd.DataFrame(word_list)
            st.session_state.words = word_list
            st.subheader("📘 단어장")
            st.dataframe(df)

            # 테스트 기능
            if st.button("📝 단어 테스트 시작"):
                st.session_state.mode = 'quiz'
                st.session_state.current_index = 0
                st.session_state.answers = []
        else:
            st.warning("'-' 로 구분된 단어와 뜻이 없습니다.")
    else:
        st.error("OCR에 실패했습니다.")
