from fastapi import FastAPI

from app.monitoring.service import monitoring_service

from app.database.database import engine, SessionLocal
from app.database.models import Base, SystemMetrics

Base.metadata.create_all(bind=engine)

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


@app.get("/metrics/history")
def metrics_history(limit: int = 10):
    db = SessionLocal()

    try:
        records = (
            db.query(SystemMetrics)
            .order_by(SystemMetrics.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": row.id,
                "timestamp": row.timestamp,
                "cpu_usage": row.cpu_usage,
                "ram_usage": row.ram_usage,
                "gpu_usage": row.gpu_usage,
                "temperature_c": row.temperature_c,
                "power_watts": row.power_watts,
            }
            for row in records
        ]

    finally:
        db.close()