import cv2
import numpy as np

def analyze_edges(image_bytes: bytes) -> float:
    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_GRAYSCALE
    )
    edges = cv2.Canny(img, 100, 200)
    density = edges.mean()
    return 0.7 if density < 0.02 else 0.3
