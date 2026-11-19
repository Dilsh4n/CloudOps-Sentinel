from datetime import UTC, datetime
from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(
    title="CloudOps Sentinel API",
    version="0.1.0"
)

# Count HTTP requests by method, route and status code.
HTTP_REQUESTS = Counter(
    "sentinel_http_requests_total",
    "Total number of HTTP requests",
    ["method", "route", "status"],
)

# Record the duration of HTTP requests in seconds.
HTTP_DURATION = Histogram(
    "sentinel_http_request_duration_seconds",
    "Duration of HTTP requests in seconds",
    ["method", "route"],
)


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start = perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        route_object = request.scope.get("route")
        route = getattr(route_object, "path", "unmatched")

        # Don't count Prometheus scraping itself as API traffic.
        if route != "/metrics":
            duration = perf_counter() - start

            HTTP_REQUESTS.labels(
                method=request.method,
                route=route,
                status=str(status_code),
            ).inc()

            HTTP_DURATION.labels(
                method=request.method,
                route=route,
            ).observe(duration)


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
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
        "timestamp": datetime.now(UTC).isoformat()
    }

@app.get("/version")
def version():
    return {
        "version": "v 0.0.1",
        "timestamp": datetime.now(UTC).isoformat()
    }