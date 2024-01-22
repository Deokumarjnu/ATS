from dotenv import load_dotenv

load_dotenv() ## Load all the environment variables

import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

genai.configure(api_key=os.getenv('API_KEY'))

# Get gemeini response from the input
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro') ## gemini-pro-vision can be used when it's image, for text gemini-pro is good
    response = model.generate_content(input)
    return response.text

# Convert pdf to text

def convert_pdf_to_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# Prompt temapltes
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""


## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit and uploaded_file is not None:
    text=convert_pdf_to_text(uploaded_file)
    response=get_gemini_response(input_prompt)
    st.subheader(response)
    