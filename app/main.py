from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(
    title="CloudOps Sentinel API",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "application": "CloudOps Sentinel",
        "message": "API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }