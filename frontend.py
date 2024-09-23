import streamlit as st
import PyPDF2
from backend import score_cv, filter_toxic_content
from PIL import Image
from transformers import pipeline
import time
import base64

# Set page config as the first Streamlit command
st.set_page_config(page_title="CV Evaluator", page_icon="📄")

@st.cache_resource
def load_toxicity_detector():
    return pipeline("text-classification", model="unitary/toxic-bert")

toxicity_detector = load_toxicity_detector()

col1, col2 = st.columns([1, 4])

logo = Image.open("static/logo.png")
col1.image(logo, width=100)  # Adjust width as needed
col2.title("CV Insight Pro: Your Path to Career Success")

uploaded_file = st.file_uploader("Upload your CV (PDF format, max size: 1 MB)", type="pdf")
job_description = st.text_area("Enter Job Role Description", height=200)

def highlight_keywords(text, keywords):
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword}**")
    return text

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
                        time.sleep(0.05)  # Simulate processing time
                        progress_bar.progress(i + 1)
                    result = score_cv(cv_content, job_description)
                
                # Filter toxic content
                filtered_result = filter_toxic_content(result)
                
                st.subheader("Evaluation Result:")
                st.write(filtered_result)

                # Extract and highlight keywords
                keywords = [word.strip() for word in filtered_result.split("Matching Keywords")[-1].split(",")]
                highlighted_cv = highlight_keywords(cv_content, keywords)
                st.subheader("CV with Highlighted Keywords:")
                st.markdown(highlighted_cv)

                # Download button for evaluation result
                b64 = base64.b64encode(filtered_result.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="evaluation_result.txt">Download Evaluation Result</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Evaluate toxicity of the result
                toxicity_chunks = [filtered_result[i:i+512] for i in range(0, len(filtered_result), 512)]
                toxicity_scores = [toxicity_detector(chunk)[0]['score'] for chunk in toxicity_chunks]
                avg_toxicity = sum(toxicity_scores) / len(toxicity_scores)
                
                st.subheader("Toxicity Analysis in generated content above:")
                st.write(f"Toxicity Score: {avg_toxicity:.2f}")
                if avg_toxicity > 0.5:
                    st.warning("The evaluation may contain some inappropriate content. It has been filtered for professionalism.")
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
- **Keyword Highlighting**: See which keywords in your CV match the job description, helping you understand your CV's strengths.
- **Content Filtering**: We ensure all feedback remains professional and respectful.

Unlock your career potential with a resume that truly reflects your skills and experiences!
""")
