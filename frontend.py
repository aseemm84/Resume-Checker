import streamlit as st
import PyPDF2
from backend import score_cv
from PIL import Image
from transformers import pipeline

toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")
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
                    result = score_cv(cv_content, job_description)
                st.subheader("Evaluation Result:")
                st.write(result)

                # Evaluate toxicity of the result
                toxicity_result_1 = toxicity_detector(result[:512])
                toxicity_result_2 = toxicity_detector(result[513:1024])
                toxicity_result_3 = toxicity_detector(result[1025:1536])  # Truncate to max length for model compatibility
                total_toxicity = (toxicity_result_1[0]['score'] + toxicity_result_2[0]['score'] + toxicity_result_3[0]['score'])
                toxicity_score = total_toxicity / 3
                st.subheader("Toxicity Analysis in generated content above:")
                st.write(f"Toxicity Score: {toxicity_score:.2f}")
                if toxicity_score > 0.5:
                    st.warning("The evaluation may contain toxic content. Please review.")
            else:
                st.error("Could not extract text from the PDF.")
    else:
        st.error("Please upload a CV and enter a job description.")


st.sidebar.title("About")
st.sidebar.info("""
Welcome to the CV Mastery Evaluator, your expert assistant for crafting a standout and ATS-friendly resume!

This tool rigorously analyzes your CV against industry best practices and specific job requirements, ensuring it meets the highest standards.

Key Features:
- **Comprehensive Evaluation**: Our tool assesses your CV across multiple dimensions, including structure, content quality, ATS compatibility, and alignment with job roles.
- **Rigorous Scoring**: Receive a detailed score out of 100, reflecting a rigorous evaluation process akin to tough marking in an exam.
- **Actionable Insights**: Obtain personalized suggestions to enhance your CV's effectiveness and ATS-friendliness, helping you optimize for success in today's competitive job market.

Unlock your career potential with a resume that truly reflects your skills and experiences!
""")