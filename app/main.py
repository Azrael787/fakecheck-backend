from fastapi import FastAPI, File, UploadFile
from app.analyze import analyze_image

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return analyze_image(image_bytes, file.filename)
