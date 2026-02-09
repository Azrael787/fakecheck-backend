from PIL import Image
from PIL.ExifTags import TAGS
import io
import hashlib
import numpy as np
import datetime

AI_KEYWORDS = ["midjourney", "stable diffusion", "dall-e", "firefly", "ai"]

def analyze_metadata(image_bytes: bytes) -> float:
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_raw = img._getexif() or {}
        exif = {TAGS.get(k, k): v for k, v in exif_raw.items()}
    except:
        return 0.3

    score = 0.0

    software = str(exif.get("Software", "")).lower()
    if any(k in software for k in AI_KEYWORDS):
        score += 1.0

    if not exif.get("Make") and not exif.get("Model"):
        score += 0.6

    if not exif.get("DateTimeOriginal"):
        score += 0.3

    if not img.info.get("icc_profile"):
        score += 0.3

    arr = np.array(img.convert("RGB"))
    if np.std(arr) < 20:
        score += 0.4

    return min(score / 3, 1.0)
