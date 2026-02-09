import cv2
import numpy as np

def analyze_noise(image_bytes: bytes) -> float:
    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_GRAYSCALE
    )
    noise = img - cv2.GaussianBlur(img, (5, 5), 0)
    std = np.std(noise)
    return 0.8 if std < 10 else 0.3
