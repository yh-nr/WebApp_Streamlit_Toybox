import streamlit as st
from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF
from PIL import Image
import os
import io


# ファイルを読み込む
with open("docs/EighthCutPDF.md", "r") as file:
    content = file.read()

st.set_page_config(page_title='EighthCutPDF (PDFを八つ折りサイズに分割)')
st.markdown(content)

selected_angle = st.radio('角度補正', [0,90,180,270])

pdf_file = st.file_uploader("ファイルをアップロード", type=['pdf'])



# 新しいファイルがアップロードされたかどうかの状態を持つ
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# 新しいPDFファイルがアップロードされたか確認
if st.session_state.last_uploaded_file != pdf_file:
    st.session_state.slider_value = 0
    st.session_state.last_uploaded_file = pdf_file

if pdf_file is not None:

    pdf_file_name = pdf_file.name
    name_without_extension = os.path.splitext(pdf_file_name)[0]

    dpi = 300

    # PDFを読み込み
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    # PDFのページ毎に処理
    split_images = []
    for page_number in range(len(doc)):

        # PDFページの寸法を取得
        page = doc[page_number]
        rect = page.rect
        
        # DPIを設定 (デフォルトを150とする)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        
        # ページを新しいJPEGファイルとして保存
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Define the grid size for splitting (4 columns x 2 rows)
        grid_size = (2, 4)
        img_width, img_height = img.size

        # 補正角度の設定があれば補正する
        if selected_angle !=0:
            img = img.rotate(selected_angle, expand=True)
            img_width, img_height = img.size

        # もし横長であれば、縦長に変換する。
        if img_width > img_height:
            img = img.rotate(270, expand=True)
            img_width, img_height = img.size

        # Width and height of each split
        split_width = img_width // grid_size[0]
        split_height = img_height // grid_size[1]

        # Function to split the image
        def split_image(image, grid):
            row_images = []
            for col in range(grid[0]):
                col_images = []
                for row in range(grid[1]):
                    left = (grid[0] - col -1) * split_width
                    upper = (row) * split_height
                    # left = (col) * split_width
                    # upper = (row) * split_height
                    right = left + split_width
                    lower = upper + split_height

                    print(f'left:{left}upper:{upper}right:{right}lower:{lower}')

                    bbox = (left, upper, right, lower)
                    split_img = image.crop(bbox)
                    split_img_rotated = split_img.rotate(90, expand=True)
                    col_images.append(split_img_rotated)
                row_images.extend(col_images)
            return row_images

        # Split the image and save the pieces
        split_images.extend(split_image(img, grid_size))

        
    # Streamlitで画像を表示
    st.image(split_images[0], caption="PDFの1ページ目", use_column_width=True)



    # 変換後の画像をバイト列に変換
    buf = io.BytesIO()
    split_images[0].save(buf, format="PDF", quality=100, save_all=True, append_images=split_images[1:], optimize=True)
    byte_pdf = buf.getvalue()
    doc.close()

        # ダウンロードボタンを作成
    st.download_button(
        label="変換後の画像をダウンロード",
        data=byte_pdf,
        file_name=f"{name_without_extension}_8cut.pdf",
        mime="application/octet-stream" 
    )

else:
    st.warning("PDFファイルをアップロードして下さい")

