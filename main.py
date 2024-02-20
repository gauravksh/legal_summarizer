import streamlit as st
import os
from io import StringIO
import replicate
import pandas as pd
from PyPDF2 import PdfReader as rd
from streamlit_jupyter import StreamlitPatcher, tqdm
StreamlitPatcher().jupyter()
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


os.environ['REPLICATE_API_TOKEN']='r8_KDgE8tUvIS50GimL0ZspWeG2ZpwUc5t1K0X5C'
pr = "do extractive summarisation on the following text. make sure to clean the text as it was extracted from a pdf. text below : "
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file = rd(uploaded_file)
    for page in file.pages :
        data = page.extract_text()
        # data = st.text_area("Edit the extracted text", data)
        pr += data

    output = replicate.run(
      "meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0",
      input={
        "debug": False,
        "top_k": -1,
        "top_p": 1,
        "prompt": pr,
        "temperature": 0.75,
        "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Please   summarise the given text and extract important information from the text.",
        "max_new_tokens": 800,
        "min_new_tokens": -1,
        "repetition_penalty": 1
      }
    )

    response = ""
    for item in output :
        response += item

    st.code(response)