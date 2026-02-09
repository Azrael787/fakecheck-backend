from app.services.ensemble import run_ensemble

def analyze_image(image_bytes: bytes, filename: str):
    result = run_ensemble(image_bytes)
    return {
        "filename": filename,
        "verdict": result["verdict"],
        "confidence": int(result["score"] * 100),
        "signals": result["signals"]
    }
