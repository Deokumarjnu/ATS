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

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit and uploaded_file is not None:
    resume=convert_pdf_to_text(uploaded_file)
    # Prompt temapltes
    formattedPrompt = '''
       Follow the instructions carefully to conduct a meticulous comparison between the job description and the provided resume within the specified context, adhering to the outlined style guidelines.

        **INSTRUCTIONS:**
        As a proficient ATS (Applicant Tracking System) scanner with a deep understanding of any provided job description and ATS functionality, your task is to thoroughly evaluate the resume against the provided job description.

        **CONTEXT:**
        Provide the percentage match if the resume aligns with the job description, focusing specifically on the required technical skills outlined in the job description: {jd}.

        **GUIDELINES:**
        1. Responses should directly address both the job description: {jd} and the resume: {resume}.
        2. Pay special attention to the Technical Skills Required section of the job description: {jd} to ensure a precise match with the resume: {resume}.
        3. If Resume does not explicitly mention any skills listed in the missing keywords Required section.
        4. The response should be in the form of a percentage match, identification of missing keywords related to technical skills, and final thoughts.
        5. Response percentage should be based on the skills in the resume: {resume} that match the job description: {jd}.

    '''

    # Using format method to substitute values
    formatted_string = formattedPrompt.format(jd=jd, resume=resume)

    response=get_gemini_response(formatted_string)
    st.subheader(response)
    