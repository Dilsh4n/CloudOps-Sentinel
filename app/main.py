from datetime import UTC, datetime

from fastapi import FastAPI

testapp = FastAPI(
    title="CloudOps Sentinel API",
    version="0.1.0"
)

@testapp.get("/")
def home():
    return {
        "application": "CloudOps Sentinel",
        "message": "API is running"
    }

@testapp.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat()
    }

@testapp.get("/version")
def version():
    return {
        "version": "v 0.0.1",
        "timestamp": datetime.now(UTC).isoformat()
    }