import os
import shutil
import uuid
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from utils.parsing import extract_text_from_file
from utils.matching import calculate_match_score

app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main upload form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_files(
    request: Request,
    job_description: UploadFile = File(...),
    resumes: List[UploadFile] = File(...),
    jd_title: str = Form(...)
):
    """Process uploaded job description and resumes"""
    # Create unique session ID for this upload
    session_id = str(uuid.uuid4())
    session_dir = os.path.join("uploads", session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    # Save job description
    jd_path = os.path.join(session_dir, f"jd_{job_description.filename}")
    with open(jd_path, "wb") as f:
        shutil.copyfileobj(job_description.file, f)
    
    # Extract text from job description
    jd_text = extract_text_from_file(jd_path)
    if not jd_text:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": "Could not extract text from job description"}
        )
    
    # Process each resume
    results = []
    for resume in resumes:
        # Save resume
        resume_path = os.path.join(session_dir, f"resume_{resume.filename}")
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        
        # Extract text from resume
        resume_text = extract_text_from_file(resume_path)
        if not resume_text:
            continue
        
        # Calculate match score
        score, keyword_score, semantic_score, matched_keywords = calculate_match_score(jd_text, resume_text)
        
        # Determine if shortlisted
        shortlisted = score >= 0.7  # 70% threshold
        
        results.append({
            "filename": resume.filename,
            "score": round(score * 100, 2),
            "keyword_score": round(keyword_score * 100, 2),
            "semantic_score": round(semantic_score * 100, 2),
            "shortlisted": shortlisted,
            "matched_keywords": matched_keywords
        })
    
    # Sort results by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return templates.TemplateResponse(
        "results.html", 
        {
            "request": request, 
            "results": results, 
            "jd_title": jd_title,
            "total_resumes": len(resumes),
            "shortlisted_count": sum(1 for r in results if r["shortlisted"])
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
