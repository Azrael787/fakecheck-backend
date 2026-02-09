from pydantic import BaseModel
from typing import List, Dict, Any

class AnalysisSignal(BaseModel):
    name: str
    score: float
    details: Dict[str, Any]

class AnalysisResult(BaseModel):
    filename: str
    probability_ai_generated: float
    verdict: str
    signals: List[AnalysisSignal]
