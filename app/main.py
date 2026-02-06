from fastapi import FastAPI

from app.api.routes import router as api_router

app = FastAPI(title="FakeCheck API", version="0.1")

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
