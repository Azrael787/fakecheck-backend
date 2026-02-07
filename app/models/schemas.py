from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class AnalysisStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class AnalysisResult(BaseModel):
    score: float
    verdict: str
    reasons: List[str]
    sources: Optional[List[str]] = None


class AnalysisStatusResponse(BaseModel):
    job_id: str
    status: AnalysisStatus
    result: Optional[AnalysisResult] = None
