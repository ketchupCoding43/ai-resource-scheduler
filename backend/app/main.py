from fastapi import FastAPI

from app.monitoring.service import monitoring_service

app = FastAPI(
    title="AI Resource Scheduler"
)


@app.on_event("startup")
def startup_event():
    monitoring_service.start()


@app.get("/")
def root():
    return {
        "message": "AI Resource Scheduler Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/metrics")
def metrics():
    return monitoring_service.get_metrics()