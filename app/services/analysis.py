from app.services.metadata import analyze_metadata
from app.services.visual import analyze_visual_artifacts
from app.services.statistical import analyze_pixel_statistics
from app.models.schemas import AnalysisResult, AnalysisSignal

def run_full_analysis(image_bytes: bytes, filename: str) -> AnalysisResult:
    signals: list[AnalysisSignal] = []

    # 1. Метаданные
    meta = analyze_metadata(image_bytes)
    signals.append(meta)

    # 2. Визуальные артефакты (без ML)
    visual = analyze_visual_artifacts(image_bytes)
    signals.append(visual)

    # 3. Статистические паттерны
    stats = analyze_pixel_statistics(image_bytes)
    signals.append(stats)

    # Итоговая вероятность
    score = sum(s.score for s in signals) / len(signals)

    return AnalysisResult(
        filename=filename,
        probability_ai_generated=round(score, 3),
        signals=signals,
        verdict="likely_ai" if score > 0.6 else "likely_real"
    )
