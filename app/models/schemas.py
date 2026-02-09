from pydantic import BaseModel
from typing import Dict, Any, List

class AnalysisSignal(BaseModel):
    name: str
    score: float
    details: Dict[str, Any]

class AnalysisResult(BaseModel):
    filename: str
    verdict: str
    confidence: int
    signals: List[AnalysisSignal]
