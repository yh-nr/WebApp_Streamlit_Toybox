import streamlit as st
import pypdf

import pytesseract

# ファイルを読み込む
with open("docs/PDFimagesOCR.md", "r") as file:
    content = file.read()

st.set_page_config(page_title='PDF内画像OCR')
st.markdown(content)

pdf_file = st.file_uploader("ファイルをアップロード", type='pdf')

# 新しいファイルがアップロードされたかどうかの状態を持つ
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# 新しいPDFファイルがアップロードされたか確認
if st.session_state.last_uploaded_file != pdf_file:
    st.session_state.slider_value = 0
    st.session_state.last_uploaded_file = pdf_file



if pdf_file is not None:

    pdf_reader = pypdf.PdfReader(pdf_file) 
    image_list = []

    for page in pdf_reader.pages:
        for image_file_object in page.images:
            image_list.append(image_file_object)

    if len(image_list):
        # セッションの状態を初期化
        if 'slider_value' not in st.session_state:
            st.session_state.slider_value = 0

        # 列を作成
        col1, col2, col3 = st.columns([3,1,1])
        value = st.session_state.get("slider_value", 0)

        lang = st.radio("OCR言語", ("jpn", "eng"), horizontal=True)

        # ボタンを作成
        with col2:
            if st.button("Prev"):
                value -= 1
                value = max(value, 0)  # 最小値は0に設定

        with col3:
            if st.button("Next"):
                value += 1
                value = min(value, len(image_list)-1)  # 最大値は100に設定

        with col1:
            slider=st.slider("指定範囲", 0, len(image_list)-1, value)

        st.text(image_list[slider].name)
        st.image(image_list[slider].image)

        # スライダーの値をsession_stateに保存
        st.session_state.slider_value = value

        txt = st.code('OCR結果',value=pytesseract.image_to_string(image_list[slider].image, lang=lang))
    
    else:
        st.warning("PDFファイルに画像がありません")

else:
    st.warning("PDFファイルをアップロードして下さい")

