from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from app.models.schemas import AnalysisResponse, AnalysisStatusResponse, AnalysisStatus, AnalysisResult
from app.services.analysis import analyze_file, create_job, get_job

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job = create_job(filename=file.filename, content_type=file.content_type)
    background_tasks.add_task(analyze_file, job.job_id, file)
    return AnalysisResponse(job_id=job.job_id, status=job.status)


@router.get("/analyze/{job_id}", response_model=AnalysisStatusResponse)
def analyze_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return AnalysisStatusResponse(
        job_id=job.job_id,
        status=job.status,
        result=job.result,
        error=job.error,
    )
