from fastapi import FastAPI

app = FastAPI(title="FakeCheck API", version="0.1")

@app.get("/health")
def health_check():
    return {"status": "ok"}
