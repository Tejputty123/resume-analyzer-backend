from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResumeResponse(BaseModel):
    id: int
    filename: str
    extracted_skills: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    resume_id: int
    job_description: str

class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    ats_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    created_at: datetime

    class Config:
        from_attributes = True