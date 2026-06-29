from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    raw_text = Column(Text)
    extracted_skills = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    analyses = relationship("Analysis", back_populates="resume")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description = Column(Text)
    ats_score = Column(Float)
    matched_skills = Column(Text)   # JSON string
    missing_skills = Column(Text)   # JSON string
    suggestions = Column(Text)      # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resume = relationship("Resume", back_populates="analyses")