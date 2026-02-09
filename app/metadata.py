from PIL import Image
from PIL.ExifTags import TAGS
import io
import hashlib
import datetime
import numpy as np
import cv2

AI_SOFTWARE_KEYWORDS = [
    "midjourney", "stable diffusion", "dall-e",
    "firefly", "generative", "ai", "diffusion"
]

def extract_exif(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_raw = img._getexif()
        if not exif_raw:
            return {}
        return {TAGS.get(k, k): v for k, v in exif_raw.items()}
    except:
        return {}

def software_score(exif):
    software = str(exif.get("Software", "")).lower()
    return 1.0 if any(k in software for k in AI_SOFTWARE_KEYWORDS) else 0.0

def camera_chain_score(exif):
    return 0.8 if not exif.get("Make") and not exif.get("Model") else 0.0

def datetime_score(exif):
    dt = exif.get("DateTimeOriginal") or exif.get("DateTime")
    if not dt:
        return 0.4
    try:
        datetime.datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        return 0.0
    except:
        return 0.6

def compression_history_score(exif):
    return 0.3 if "Compression" not in exif else 0.0

def thumbnail_score(exif):
    return 0.4 if "JPEGThumbnail" not in exif else 0.0

def icc_profile_score(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return 0.4 if not img.info.get("icc_profile") else 0.0
    except:
        return 0.2

def bit_depth_uniformity_score(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(img)
    return 0.5 if np.std(arr) < 20 else 0.0

# 🔹 NEW SIGNALS

def noise_pattern_score(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    noise = img - cv2.GaussianBlur(img, (5, 5), 0)
    return 0.5 if np.std(noise) < 10 else 0.0

def edge_coherence_score(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)
    edge_density = np.mean(edges > 0)
    return 0.4 if edge_density < 0.02 else 0.0

def color_channel_correlation_score(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    corr_rg = np.corrcoef(r.flatten(), g.flatten())[0,1]
    corr_rb = np.corrcoef(r.flatten(), b.flatten())[0,1]
    corr_gb = np.corrcoef(g.flatten(), b.flatten())[0,1]
    avg_corr = np.mean([corr_rg, corr_rb, corr_gb])
    return 0.4 if avg_corr > 0.98 else 0.0

def hash_fingerprint(image_bytes):
    return hashlib.sha256(image_bytes).hexdigest()

def analyze_metadata(image_bytes):
    exif = extract_exif(image_bytes)

    signals = {
        "ai_software": software_score(exif),
        "camera_missing": camera_chain_score(exif),
        "datetime_anomaly": datetime_score(exif),
        "compression_missing": compression_history_score(exif),
        "thumbnail_missing": thumbnail_score(exif),
        "icc_missing": icc_profile_score(image_bytes),
        "bit_uniformity": bit_depth_uniformity_score(image_bytes),
        "noise_pattern": noise_pattern_score(image_bytes),
        "edge_coherence": edge_coherence_score(image_bytes),
        "color_correlation": color_channel_correlation_score(image_bytes),
    }

    score = round(sum(signals.values()) / len(signals), 2)

    return {
        "score": score,
        "signals": signals,
        "exif_present": bool(exif),
        "hash": hash_fingerprint(image_bytes)
    }
