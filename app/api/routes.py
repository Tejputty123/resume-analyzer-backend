from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.models.models import Resume, Analysis
from app.schemas.schemas import ResumeResponse, AnalysisRequest, AnalysisResponse
from app.services.resume_parser import extract_text_from_pdf, extract_skills_basic
from app.services.ai_analyzer import extract_skills_with_ai, analyze_resume_vs_job

router = APIRouter()

@router.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)
    
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    
    # Try AI extraction, fall back to basic
    try:
        skills = extract_skills_with_ai(raw_text)
    except Exception:
        skills = extract_skills_basic(raw_text)
    
    resume = Resume(
        filename=file.filename,
        raw_text=raw_text,
        extracted_skills=json.dumps(skills)
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return ResumeResponse(
        id=resume.id,
        filename=resume.filename,
        extracted_skills=skills,
        created_at=resume.created_at
    )

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    
    try:
        result = analyze_resume_vs_job(resume.raw_text, request.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")
    
    analysis = Analysis(
        resume_id=resume.id,
        job_description=request.job_description,
        ats_score=result.get("ats_score", 0),
        matched_skills=json.dumps(result.get("matched_skills", [])),
        missing_skills=json.dumps(result.get("missing_skills", [])),
        suggestions=json.dumps(result.get("suggestions", []))
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return AnalysisResponse(
        id=analysis.id,
        resume_id=analysis.resume_id,
        ats_score=analysis.ats_score,
        matched_skills=json.loads(analysis.matched_skills),
        missing_skills=json.loads(analysis.missing_skills),
        suggestions=json.loads(analysis.suggestions),
        created_at=analysis.created_at
    )


@router.get("/resumes")
async def list_resumes(db: Session = Depends(get_db)):
    raise HTTPException(status_code=403, detail="This endpoint is currently disabled.")