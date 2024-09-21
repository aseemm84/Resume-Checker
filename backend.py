import os
from dotenv import load_dotenv
import cohere

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def score_cv(cv_content, job_description):
    # Define a prompt to evaluate the CV based on best practices and job role
    prompt = f"""
You are an expert CV evaluation assistant.
Your task is to rigorously evaluate the provided CV content {cv_content} based on best practices for creating an effective and ATS-friendly resume.
Apply a strict grading standard, similar to tough marking in an exam.

Consider these steps, each contributing to the overall score based on specified weightage.
Be critical and thorough in your assessment:

1. **Structure and Formatting (20% weightage in total score):**
   - Critically examine the format for clarity and consistency.
   - Ensure all section headings such as "Education," "Experience," and "Skills" are prominently and correctly used.
   - Strictly check for standard font usage, appropriate margins, and effective bullet points.
   - Penalize any deviation from these norms.

2. **Content Quality (10% weightage in total score):**
   - Rigorously evaluate if all necessary sections are included, such as contact information, education, work experience, and skills.
   - Assess the use of strong action verbs at the beginning of each bullet point to emphasize achievements and skills.
   - Deduct points for lack of quantifiable accomplishments.

3. **ATS Compatibility (15% weightage in total score):**
   - Ensure strict avoidance of complex formatting like tables or graphics that can confuse ATS software.
   - Confirm inclusion of keywords relevant to the job description naturally throughout the CV.
   - Penalize any missing critical keywords.

4. **Match with Job Role (55% weightage in total score):**
   - Extract required skills from the job description: {job_description}.
   - Extract required experience from the job description: {job_description}.
   - Extract required education from the job description: {job_description}.
   - Meticulously compare skills (25%), experience (20%) and education (10%) listed in the CV with those required in the job description: {job_description}.
   - Identify any gaps or matches in skills and experiences, focusing on alignment with job requirements.
   - Deduct points for significant mismatches or omissions.

5. **Suggestions for Improvement:**
   - Provide detailed and actionable feedback on enhancing CV effectiveness and ATS-friendliness.
   - Suggest incorporating more industry-specific keywords or rephrasing certain sections for clarity.
   - Recommend changes to improve overall presentation, such as reorganizing sections or adjusting formatting.

Based on these criteria, provide a detailed score out of 100 and comprehensive suggestions for improvement.
The evaluated total score should be sumation of scores calculated for 1, 2, 3 and 4 steps.
Ensure consistency in scoring by strictly following these guidelines.
"""

    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=0
        )
        
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
