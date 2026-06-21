from fastapi import FastAPI

from app.monitoring.collector import get_system_metrics

app = FastAPI(
    title="AI Resource Scheduler"
)


@app.get("/")
def root():
    return {"message": "running"}


@app.get("/metrics")
def metrics():
    return get_system_metrics()


@app.get("/health")
def health():
    return {"status": "healthy"}