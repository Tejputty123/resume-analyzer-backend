import json
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.OPENAI_API_KEY)

def extract_skills_with_ai(resume_text: str) -> list[str]:
    prompt = f"""
    Extract all technical and professional skills from this resume text.
    Return ONLY a JSON array of skill strings. No explanation.
    
    Resume text:
    {resume_text[:3000]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def analyze_resume_vs_job(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an expert ATS and career coach.
    
    Analyze this resume against the job description and return a JSON object with:
    - "ats_score": number from 0-100
    - "matched_skills": array of skills present in both resume and job description
    - "missing_skills": array of skills in job description but missing from resume
    - "suggestions": array of 5 specific actionable improvement suggestions
    
    Return ONLY valid JSON. No explanation or markdown.
    
    RESUME:
    {resume_text[:2500]}
    
    JOB DESCRIPTION:
    {job_description[:1500]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)