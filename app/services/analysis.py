import uuid
from typing import Dict, Optional

from fastapi import UploadFile

from app.models.schemas import AnalysisResult, AnalysisStatus

_JOBS: Dict[str, AnalysisResult] = {}


def create_job() -> str:
    job_id = str(uuid.uuid4())
    _JOBS[job_id] = AnalysisResult(
        score=0.0,
        verdict="pending",
        reasons=[],
        sources=[]
    )
    return job_id


def get_job(job_id: str) -> Optional[AnalysisResult]:
    return _JOBS.get(job_id)


def analyze_file(job_id: str, file: UploadFile) -> None:
    job = _JOBS[job_id]
    job.verdict = "processing"
    _ = file.file.read()
    job.verdict = "done"
