import streamlit as st
import pypdf

import pytesseract

# ファイルを読み込む
with open("docs/PDFimagesOCR.md", "r") as file:
    content = file.read()

st.set_page_config(page_title='PDF内画像OCR')
st.markdown(content)

img_file = st.file_uploader("ファイルをアップロード", type='jpg')

# 新しいファイルがアップロードされたかどうかの状態を持つ
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# 新しいPDFファイルがアップロードされたか確認
if st.session_state.last_uploaded_file != img_file:
    st.session_state.slider_value = 0
    st.session_state.last_uploaded_file = img_file

if img_file is not None:

    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = 0

    lang = st.radio("OCR言語", ("jpn", "eng"), horizontal=True)

    slider=st.slider("指定範囲", 0, len(image_list)-1, value)

    st.image(img_file)

    # スライダーの値をsession_stateに保存
    value = st.session_state.get("slider_value", 0)
    st.session_state.slider_value = value

    # txt = st.code('OCR結果',value=pytesseract.image_to_string(image_list[slider].image, lang=lang))
    txt = st.code(pytesseract.image_to_string(img_file, lang=lang))
    

else:
    st.warning("PDFファイルをアップロードして下さい")

