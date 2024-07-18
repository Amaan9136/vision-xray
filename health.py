'''
cd backend/healthapp
streamlit run health.py
'''

import textwrap

import google.generativeai as genai
import streamlit as st
from IPython.display import Markdown
from PIL import Image

genai.configure(api_key="AIzaSyBIa2tTioiCDmpwzwRqniuIHL37IL3HFFs")

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def get_gemini_response_vision(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

st.set_page_config(page_title="Combined App")

app_mode = st.sidebar.selectbox("Choose the Model",
    ["Health Plus XVC AI", "Health Plus AI"])

# page - Health Plus XVC AI
if app_mode == "Health Plus XVC AI":
    st.header("Health Plus XVC AI")

    input = st.text_input("Input Prompt:", key="input", placeholder='Enter the prompt', value='What can you see in this xray scan?')

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""   
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Generate Response")

    input_prompt = """
    Consider yourself as a specialized in medical aspects and you can analyse X-ray images. 
    present your observations, diagnosis, and recommended course of action in a clear and structured format. 
    Utilize bullet points or numbers to organize your findings systematically.
    """

    if submit:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response_vision(input_prompt, image_data, input)
        st.subheader("The Response is")
        st.write(response)

# page - Health Plus AI
elif app_mode == "Health Plus AI":
    st.header("Health Plus AI")

    input = st.text_input("Input:", key="input", value='Can you say the reason behind my fever and cough?')

    input_prompt = """
    Consider yourself as a specialized in medical aspects. 
    and recommended what should i do : 

    """

    submit = st.button("Ask the question")

    if submit:
        combined_prompt = f"{input_prompt} {input}"

        response = get_gemini_response(combined_prompt)
        st.subheader("The Response is")
        st.write(response)
