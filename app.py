import streamlit as st
import json
from pathlib import Path
from src.mcqgenerator.utils import read_file
from src.mcqgenerator.main import *


def load_json(file_name):
    try:
        file_path = Path(file_name)
        if file_path.is_file():
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        else:
            return f"File {file_name} not found in the current directory."
    except Exception as e:
        return str(e)
    
json_file_name = 'response.json'
# Load the JSON file
RESPONSE_JSON = load_json(json_file_name)

st.title("MCQ Generator")

with st.form("User_Inputs"): 
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a text file", type=['txt','pdf'])
    SUBJECT = st.text_input("Topic Name :",value="Machine Learning")
    TONE = st.text_input("Tone :",value="Simple")
    NUMBER = st.number_input("Enter Number of Quizes :",value=3, min_value=0, max_value=6, step=1)
    button=st.form_submit_button("Create MCQ's")
    if button and uploaded_file is not None and NUMBER and TONE and SUBJECT:
        with st.spinner("Loading Wait Na >>>>>>>"):
            try:
                TEXT=read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                    {
                        "text": TEXT,
                        "number": NUMBER,
                        "subject":SUBJECT,
                        "tone": TONE,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                    )
                quiz_json = response['quiz']
                # Remove unnecessary text and extract only the JSON part
                quiz_json = quiz_json.replace('\n### RESPONSE_JSON\n', '')
                st.write(quiz_json)
            except Exception as e:
                st.error("Error")
            



    
