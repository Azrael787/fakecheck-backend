import cv2
import numpy as np

def analyze_color(image_bytes: bytes) -> float:
    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )
    b, g, r = cv2.split(img)
    corr = np.corrcoef(r.flatten(), g.flatten())[0, 1]
    return 0.7 if corr > 0.98 else 0.3
