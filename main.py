import streamlit as st
import pypdf

import pytesseract

markdown = '''
# PDFファイルから画像抽出
### 説明
* PDFファイルから画像を抽出して表示します。

'''
st.set_page_config(page_title='PDF内画像OCR')
st.markdown(markdown)

pdf_file = st.file_uploader("ファイルをアップロード", type='pdf')
# PDFファイルのメタデータを取得する
# pdf_info = pdf_reader.metadata



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
        col1, col2, col3 = st.columns(3)


        value = st.session_state.get("slider_value", 0)


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

        txt = st.text_area('OCR結果',value=pytesseract.image_to_string(image_list[slider].image, lang='jpn'))
    
    else:
        st.warning("PDFファイルに画像がありません")

else:
    st.warning("PDFファイルをアップロードして下さい")

