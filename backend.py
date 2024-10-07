import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import re

groq = st.secrets["Groq_API_Key"]



llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    groq_api_key=groq,
    temperature=0
    # other params...
)

def check_for_rate_limit_error(response_content):
    """Checks if the response content contains a Groq rate limit error."""
    error_pattern = r"Rate limit reached.*in (\d+m\d+\.\d+s)"
    match = re.search(error_pattern, response_content)
    if match:
        wait_time = match.group(1)
        st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")
        return True
    return False

def CVstruct_prompt(cv_content):
    template = """
            You are an expert CV evaluation assistant.
            Your task is to rigorously evaluate the provided CV content {cv_content} for the CV Structure and Formatting Best Practices.
            Focus on consistency in font style, section headers, use of bullet points, margins, and alignment.
            Assess whether the layout is clean and easy to read, including the proper usage of reverse chronological order for experiences.
            Provide suggestions for improvements if any formatting inconsistencies or readability issues are found.
            Following are some examples of structure and formatting best practices:
            1. Ensure uniformity in font style, bullet points, and section headers. Use bold and italics sparingly for emphasis.
            2. Recommended fonts include Times New Roman, Arial, Helvetica, or Calibri in 10-12 point size, with 0.5-1 inch margins.
            3. Include standard sections like Education, Experience, Skills, and Contact Information.
            Optional sections like Leadership and Technical Skills can be included based on relevannce.
            4. Use concise bullet points starting with action verbs to highlight achievements.
            Keep the format consistent across all entries.
            5. List experiences in reverse chronological order, starting with the most recent position.
               
            Apply a strict grading standard, similar to tough marking in an exam.

            The result should be following format:
            1. Overall Structure an Formatting: Numbered list with detailed analysis
            2. Section-by-section analysis: Numbered list with detailed analysis
            3. Suggestions for Improvement: Numbered list with detailed suggestions
            4. Score: A score out of 100 (e.g. Score: 65/100)
            """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({"cv_content": cv_content})
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")

def actVerb_prompt(cv_content, job_description):
    template = """
            You are an expert CV evaluation assistant.
            Your task is to rigorously evaluate the provided CV content {cv_content} for Action Verbs Usage best practices.
            Analyze the usage of action verbs throughout the CV.
            Ensure that each bullet point begins with a strong, dynamic action verb that effectively conveys the candidate's skills and achievements.
            Check if the action verbs vary and are tailored to highlight leadership, technical, or communication skills.
            Suggest improvements if any passive language or repetitive verbs are detected.
            Following are some examples of action verb usage best practices:
            1. Use varied and impactful action verbs to begin each bullet point, showcasing specific actions taken (e.g., developed, managed, coordinated).
            2. Replace generic phrases like “responsible for” or “duties include” with dynamic action verbs.
            3. Align choice of verbs with the industry or job role {job_description} for which the CV {cv_content} will be used to apply (e.g., "engineered" for technical roles, "negotiated" for management).
            4. Diversify your verb usage to cover different skills such as leadership, communication, problem-solving, and technical expertise.
               
            Apply a strict grading standard, similar to tough marking in an exam.

            The result should be following format:
            1. Overall Action Verb Usage: Numbered list with detailed analysis
            2. Section-by-section analysis: Numbered list with detailed analysis
            3. Suggestions for Improvement: Numbered list with detailed suggestions
            4. Score: A score out of 100 (e.g. Score: 65/100)
            """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({"cv_content": cv_content, "job_description": job_description})
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")

def CVcontent_prompt(cv_content, job_description):
    template = """
            You are an expert CV evaluation assistant.
            Your task is to rigorously evaluate the provided CV content {cv_content} for CV content quality best practices.
            Examine the quality of the CV content, focusing on how effectively the candidate highlights accomplishments rather than listing job responsibilities.
            Check for the use of quantifiable results where applicable, relevance of listed experiences, and the inclusion of industry-specific keywords.
            Ensure the content is concise and avoids unnecessary personal details or pronouns.
            Recommend ways to enhance the focus on achievements and relevance.
            Following are some examples of CV Content Quality best practices:
            1. Where possible, use numbers to describe the scale or impact of your accomplishments (e.g., increased sales by 20%).
            2. Highlight specific outcomes and contributions rather than listing job responsibilities.
            3. Incorporate industry-specific terms and keywords from the job description {job_description} to improve relevance.
            4. Write in the third person without using "I," "me," or "my".
            5. Keep content brief and to the point, focusing only on the most relevant experiences for the position.

            Apply a strict grading standard, similar to tough marking in an exam.

            The result should be following format:
            1. Overall CV Content Quality Analysis: Numbered list with detailed analysis
            2. Section-by-section analysis: Numbered list with detailed analysis
            3. Suggestions for Improvement: Numbered list with detailed suggestions
            4. Score: A score out of 100 (e.g. Score: 65/100)
            """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({"cv_content": cv_content, "job_description": job_description})
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")

def ATS_prompt(cv_content, job_description):
    template = """
            You are an expert CV evaluation assistant.
            Your task is to rigorously evaluate the provided CV content {cv_content} for ATS compatibility best practices.
            Assess the CV's compatibility with Applicant Tracking Systems (ATS).
            Ensure that it uses simple formatting without complex tables, columns, or images.
            Verify that appropriate keywords from the job description {job_description} or industry standards are incorporated, and that the file is likely to be parsed correctly by ATS.
            Suggest any necessary changes to improve ATS readability, such as modifying section headings or avoiding special characters.
            Following are some examples of ATS compatibility best practices:
            1. Avoid unusual fonts, images, or special characters that could confuse Applicant Tracking Systems (ATS).
            2. Tailor the CV by incorporating keywords and phrases from the job description to ensure it ranks higher in ATS.
            3. Use simple formats, avoiding text boxes, columns, and tables, which might not be readable by ATS.
            4. Stick to conventional headings like “Work Experience” and “Education” to ensure ATS systems can easily parse your resume.

            Apply a strict grading standard, similar to tough marking in an exam.

            The result should be following format:
            1. Overall ATS Compatibility Analysis: Numbered list with detailed analysis
            2. Section-by-section analysis: Numbered list with detailed analysis
            3. Suggestions for Improvement: Numbered list with detailed suggestions
            4. Score: A score out of 100 (e.g. Score: 65/100)
            """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({"cv_content": cv_content, "job_description": job_description})
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")

def jobRole_prompt(cv_content, job_description):
    template = """
            You are an expert CV evaluation assistant.
            Your task is to rigorously evaluate the provided CV content {cv_content} for the provided job role description {job_description}.
            Evaluate the alignment of the CV with the specific job role description.
            Compare the candidate's skills, education, and experience with the requirements of the role.
            Focus on how well the listed qualifications match the job description, including relevant keywords, skills, and achievements.
            Identify gaps in relevance or opportunities to better tailor the CV for the job application.
            Following are some examples of matching the CV content with the job role description:
            1. Meticulously compare Matching Skills, skills, experience and education listed in the CV with those required in the job description: {job_description}.
            2. Identify any gaps or matches in skills and experiences, focusing on alignment with job requirements.
            3. Deduct points for significant mismatches or omissions.

            Apply a strict grading standard, similar to tough marking in an exam.
            Extract the skills from {cv_content} and required skills from the {job_description} and provide a numbered list of skills that are matching between {cv_content} and {job_description}

            The result should be following format:
            1. Overall Job Role Compatibility: Numbered list with detailed analysis
            2. Section-by-section analysis: Numbered list with detailed analysis
            3. Suggestions for Improvement: Numbered list with detailed suggestions
            4. Matching Skills: A numbered list of skills that are matching between {cv_content} and {job_description}
            4. Score: A score out of 100 (e.g. Score: 65/100)

            """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({"cv_content": cv_content, "job_description": job_description})
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")
    

def draft_new(cv_content, job_description, suggest1, suggest2, suggest3, suggest4, suggest5):
    template = """
            Draft a New CV based on following:
            1. Old CV: {cv_content}
            2. Job Role Description: {job_description}
            3. Old CV Structuring and Formatting Suggestions: {suggest1}
            4. Old CV Action Verb Usage Suggestions: {suggest2}
            5. Old CV Content Quality Suggestions: {suggest3}
            6. Old CV ATS Compatibility Suggestions: {suggest4}
            7. Old CV Job Role Description: {suggest5}
            """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    try:
        response = chain.invoke({
            "cv_content": cv_content, 
            "job_description": job_description, 
            "suggest1": suggest1, 
            "suggest2": suggest2, 
            "suggest3": suggest3, 
            "suggest4": suggest4, 
            "suggest5": suggest5
        })
        # Check for rate limit error in the response content
        if check_for_rate_limit_error(response.content):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return response.content
    except Exception as e:
        if check_for_rate_limit_error(str(e):
            return st.error(f"This app uses free Groq API. API call Rate limit exceeded. Please try again in {wait_time}.")  # or some other indicator of failure
        else: 
            return st.error(f"An error occurred: {e}")
