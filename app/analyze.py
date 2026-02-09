from app.services.analysis import run_full_analysis
from app.models.schemas import AnalysisResult

def analyze_image_bytes(image_bytes: bytes, filename: str) -> AnalysisResult:
    """
    Главная точка анализа изображения.
    """
    result = run_full_analysis(
        image_bytes=image_bytes,
        filename=filename
    )
    return result
