from app.services.metadata import analyze_metadata
from app.services.noise import analyze_noise
from app.services.edges import analyze_edges
from app.services.color import analyze_color
from app.services.ml_stub import analyze_ml

WEIGHTS = {
    "metadata": 0.25,
    "noise": 0.2,
    "edges": 0.2,
    "color": 0.15,
    "ml": 0.2,
}

def run_ensemble(image_bytes: bytes) -> dict:
    scores = {
        "metadata": analyze_metadata(image_bytes),
        "noise": analyze_noise(image_bytes),
        "edges": analyze_edges(image_bytes),
        "color": analyze_color(image_bytes),
        "ml": analyze_ml(image_bytes),
    }

    final_score = sum(scores[k] * WEIGHTS[k] for k in scores)

    if final_score > 0.85:
        verdict = "High confidence AI-generated"
    elif final_score > 0.6:
        verdict = "Medium confidence"
    else:
        verdict = "Low confidence / likely real"

    return {
        "score": round(final_score, 3),
        "verdict": verdict,
        "signals": scores,
    }
