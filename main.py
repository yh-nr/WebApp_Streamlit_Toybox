import streamlit as st

# ファイルを読み込む
with open(r"readme.md", "r") as file:
    content = file.read()

st.set_page_config(page_title='メインページ')
st.markdown(content)
