from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import AnalysisResult
from app.services.analysis import create_job, analyze_file, get_job

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_image(file: UploadFile = File(...)):
    job_id = create_job()
    analyze_file(job_id, file)

    result = get_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")

    return result
