import fitz  # PyMuPDF
import json
import re

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from PDF bytes."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_skills_basic(text: str) -> list[str]:
    """Basic skill extraction using keyword matching."""
    common_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "Django",
        "FastAPI", "Flask", "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas",
        "NumPy", "Scikit-learn", "REST API", "GraphQL", "HTML", "CSS",
        "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
        "Data Analysis", "Power BI", "Tableau", "Excel", "Spark", "Kafka",
        "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible"
    ]
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))