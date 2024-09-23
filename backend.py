import os
from dotenv import load_dotenv
import cohere

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define maximum scores for each category
max_scores = {
    'Structure and Formatting': 20,
    'Content Quality': 10,
    'ATS Compatibility': 15,
    'Match with Job Role': 55
}

def validate_and_adjust_scores(category_scores):
    adjusted_scores = {}
    for category, score in category_scores.items():
        if score > max_scores[category]:
            adjusted_scores[category] = max_scores[category]
        else:
            adjusted_scores[category] = score
    return adjusted_scores

def construct_prompt(cv_content, job_description):
    return f"""
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

Additionally, provide a list of keywords from the CV that match the job description.

Important: Ensure that the score for each category does not exceed its maximum allowed value:
Structure and Formatting: 20
Content Quality: 10
ATS Compatibility: 15
Match with Job Role: 55

Present the scores in a JSON format like this:
{{
    "Structure and Formatting": [score],
    "Content Quality": [score],
    "ATS Compatibility": [score],
    "Match with Job Role": [score],
    "Total Score": [total score],
    "Suggestions": "[detailed suggestions]",
    "Matching Keywords": "[list of matching keywords]"
}}
"""

def call_cohere_api(prompt):
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=0
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def score_cv(cv_content, job_description):
    prompt = construct_prompt(cv_content, job_description)
    result = call_cohere_api(prompt)
    
    # Parse the JSON response
    import json
    try:
        scores = json.loads(result)
        # Validate and adjust scores
        adjusted_scores = validate_and_adjust_scores({k: v for k, v in scores.items() if k in max_scores})
        
        # Recalculate total score
        total_score = sum(adjusted_scores.values())
        
        # Update the scores and total in the result
        for category, score in adjusted_scores.items():
            scores[category] = score
        scores['Total Score'] = total_score
        
        # Convert back to string for return
        return json.dumps(scores, indent=2)
    except json.JSONDecodeError:
        return result  # Return the original result if JSON parsing fails

def filter_toxic_content(text):
    # This is a placeholder function. In a real-world scenario, you'd implement
    # more sophisticated content filtering or rephrasing logic.
    toxic_words = ["terrible", "awful", "horrible", "stupid", "idiot"]
    for word in toxic_words:
        text = text.replace(word, "[inappropriate word]")
    return text
