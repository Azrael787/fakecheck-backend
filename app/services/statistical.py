import io
import numpy as np
from PIL import Image
from app.models.schemas import AnalysisSignal

def analyze_pixel_statistics(image_bytes: bytes) -> AnalysisSignal:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(image)

    # Энтропия
    hist, _ = np.histogram(arr.flatten(), bins=256, range=(0, 255), density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))

    # AI-изображения часто имеют "идеальную" энтропию
    score = min(abs(entropy - 7.5) / 3, 1.0)

    return AnalysisSignal(
        name="pixel_statistics",
        score=score,
        details={
            "entropy": round(float(entropy), 3),
            "note": "GAN/Diffusion дают аномально стабильную энтропию"
        }
    )
