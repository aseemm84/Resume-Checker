import streamlit as st
import PyPDF2
from backend import CVstruct_prompt, actVerb_prompt, CVcontent_prompt, ATS_prompt, jobRole_prompt, draft_new, overall_score
from PIL import Image
from transformers import pipeline
import time
import base64

# Set page config as the first Streamlit command
st.set_page_config(page_title="CV Evaluator", page_icon="📄")


col1, col2 = st.columns([1, 4])

logo = Image.open("static/logo.png")
col1.image(logo, width=100)  # Adjust width as needed
col2.title("CV Insight Pro: Your Path to Career Success")

uploaded_file = st.file_uploader("Upload your CV (PDF format, max size: 1 MB)", type="pdf")
job_description = st.text_area("Enter Job Role Description", height=200)


# Evaluate button
if st.button("Evaluate"):
    if uploaded_file is not None and job_description:
        if uploaded_file.size > 1 * 1024 * 1024:
            st.error("File size exceeds 1 MB limit.")
        else:
            # Read PDF content
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            cv_content = ""
            for page in pdf_reader.pages:
                cv_content += page.extract_text()

            if cv_content:
                with st.spinner("Evaluating your CV..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(2.5)  # Simulate processing time
                        progress_bar.progress(i + 1)
                    result_struct = CVstruct_prompt(cv_content)
                    result_verb = actVerb_prompt(cv_content, job_description)
                    result_content = CVcontent_prompt(cv_content, job_description)
                    result_ats = ATS_prompt(cv_content, job_description)
                    result_role = jobRole_prompt(cv_content, job_description)
                    new_cv = draft_new(cv_content, job_description, result_struct, result_verb, result_content, result_ats, result_role)
                    score = overall_score(result_struct, result_verb, result_content, result_ats, result_role)

                
                # Filter toxic content
                
                st.subheader("Evaluation Result:")
                st.subheader("1. Structure and Formatting")
                st.write(result_struct)
                st.subheader("2. Action Verbs Usage")
                st.write(result_verb)
                st.subheader("3. Content Quality")
                st.write(result_content)
                st.subheader("4. ATS Compatibility")
                st.write(result_ats)
                st.subheader("5. Job Role Match")
                st.write(result_role)
                st.subheader("Overal Score")
                st.write(score)
                st.subheader("6. New Draft CV Based on Above Suggestions:")
                st.write(new_cv)

                

st.sidebar.title("About")
st.sidebar.info("""
Welcome to the CV Mastery Evaluator, your expert assistant for crafting a standout and ATS-friendly resume!

This tool rigorously analyzes your CV against industry best practices and specific job requirements, ensuring it meets the highest standards.

Key Features:
- **Comprehensive Evaluation**: Our tool assesses your CV across multiple dimensions, including structure, content quality, ATS compatibility, and alignment with job roles.
- **Rigorous Scoring**: Receive a detailed CV analysis, reflecting a rigorous evaluation process akin to tough marking in an exam.
- **Actionable Insights**: Obtain personalized suggestions to enhance your CV's effectiveness and ATS-friendliness, helping you optimize for success in today's competitive job market.

Unlock your career potential with a resume that truly reflects your skills and experiences!
""")
