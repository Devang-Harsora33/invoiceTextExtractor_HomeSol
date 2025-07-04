# from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="HomeSol")

st.header("HomeSol Application")
input=st.text_input("Input Prompt: ",key="input")

# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     if st.button("Extract All Details"):
#         input = "Extract all the data from the image like company name, GST number, invoice number, dates, billed items, tax info, and totals, etc."
# with col2:
#     if st.button("Extract Date"):
#         input = "What is the invoice date?"
        
# with col3:
#     if st.button("Extract Invoice Number"):
#         input = "What is the invoice number?"
        
# with col4:
#     if st.button("Extract Total Amount"):
#         input = "What is the total amount on the invoice?"
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)


submit=st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
