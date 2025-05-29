import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import fitz

from dotenv import load_dotenv
load_dotenv()


os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


##prompt

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an ATS (Applicant Tracking System) that analyzes a candidate's CV against a given job description. Your task is to:\n"
        "1. Assess the chances of the candidate's selection based on keyword matching and relevance. Output the result as [low, medium, or high].\n"
        "2. Identify and list the good (relevant) keywords found in the CV that match the job description.\n"
        "3. Identify and list the important missing keywords from the CV based on the job description.\n"
        "Ensure your responses are clear and concise.",
    ),
    ("human", "The CV content is: {cv}. The job description is: {job}."),
])


llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

out_inp=StrOutputParser()

chain=prompt|llm|out_inp




def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text



st.title("Applicant Tracking System")
st.subheader("Powered by Llama3")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
job=st.text_input("Enter Job Discription")


    
    
    
    
if uploaded_file is not None:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    

    if st.button("Scan"):
        
        st.write(chain.invoke(
        {
        "cv": pdf_text,
        "job": job,
        }
        ))