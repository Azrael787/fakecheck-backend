from PIL import Image
import io
import numpy as np
from app.models.schemas import AnalysisSignal

def analyze_visual_artifacts(image_bytes: bytes) -> AnalysisSignal:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(image)

    # Проверка симметрии шума
    left = arr[:, :arr.shape[1]//2]
    right = arr[:, arr.shape[1]//2:]
    symmetry_diff = abs(left.mean() - right.mean()) / 255

    score = min(symmetry_diff * 2, 1.0)

    return AnalysisSignal(
        name="visual_artifacts",
        score=score,
        details={
            "noise_symmetry_diff": symmetry_diff,
            "note": "AI часто даёт симметричный или неестественный шум"
        }
    )
