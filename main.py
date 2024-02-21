import streamlit as st
import tempfile
import os
from config import geminikey
import google.generativeai as genai
import pypdfium2 as pdfium
import easyocr
from PyPDF2 import PdfReader as rd
from streamlit_jupyter import StreamlitPatcher
StreamlitPatcher().jupyter()
st.set_page_config(layout="wide")

st.title("Summarizer")

st.markdown(
    """
    <style>
    .reportview-container {
        padding: 0 0 0 0;
        max-width: 100%;
    }
    .main {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

genai.configure(api_key=geminikey)
model = genai.GenerativeModel('gemini-pro')

def pdf_pil(file_path,page_num,up_scale):

    pdf = pdfium.PdfDocument(file_path)
    page = pdf.get_page(int(page_num)-1)
    bitmap = page.render(
        scale = int(up_scale),    # 72dpi resolution
        rotation = 0, # no additional rotation
        # ... further rendering options
    )
    pil_image = bitmap.to_pil()
    pil_image.save(f"image_{page_num}.png")
    
    return (f"image_{page_num}.png")

def ocrpdf(file_path,page_num):
    img1 = pdf_pil(file_path,page_num,3)
    lang=['kn']
    reader = easyocr.Reader(lang)
    bounds = reader.readtext(img1)
    
    this = ""
    for bound in bounds:
        this = (f'{this} \n{bound[1]}')
    return this    

os.environ['REPLICATE_API_TOKEN']='r8_KDgE8tUvIS50GimL0ZspWeG2ZpwUc5t1K0X5C'
pr = "do extractive summarisation on the following text. make sure to clean the text as it was extracted from a pdf. text below : "
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    pr = "Summarise the following kannada legal document in english to about 10-15 lines or less : "
    file = rd(uploaded_file)
    pages = len(file.pages)
    if pages > 1:
        pages = 2
    for page in range(1, pages+1):
        pr += ocrpdf(path, page)
        pr += " "

    response = model.generate_content(pr)

    st.code(response.text)