import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
load_dotenv()

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Invoice Extractor")

st.header("Invoice Info Extractor")
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key="image")
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

system_prompt ='''
You are an expert at understanding invoices. You will recieve input images
as invoices and you will have to answer questions based on this invoice.
'''

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(system_prompt, image_data, input_prompt)

    st.subheader("Response: ")
    st.write(response)
    