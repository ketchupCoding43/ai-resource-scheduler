from datetime import datetime
from app.profiler.workload_profiler import classify_workload
import time

from fastapi import FastAPI

from app.monitoring.service import monitoring_service

from app.database.database import engine, SessionLocal
from app.database.models import Base, SystemMetrics
from app.database.llm_models import LLMExecution

from app.llm.schemas import GenerateRequest
from app.llm.ollama_client import generate_response


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


@app.get("/llm/history")
def llm_history(limit: int = 10):

    db = SessionLocal()

    try:

        records = (
            db.query(LLMExecution)
            .order_by(LLMExecution.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": row.id,
                "timestamp": row.timestamp,

                "prompt_length": row.prompt_length,
                "response_length": row.response_length,

	        "workload_class": row.workload_class,

                "latency_seconds": row.latency_seconds,

                "cpu_before": row.cpu_before,
                "cpu_after": row.cpu_after,

                "ram_before": row.ram_before,
                "ram_after": row.ram_after,

                "gpu_before": row.gpu_before,
                "gpu_after": row.gpu_after,

                "vram_before": row.vram_before,
                "vram_after": row.vram_after,

                "temperature_before": row.temperature_before,
                "temperature_after": row.temperature_after,

                "power_before": row.power_before,
                "power_after": row.power_after
            }
            for row in records
        ]

    finally:
        db.close()


@app.post("/llm/generate")
def generate(request: GenerateRequest):

    before_metrics = monitoring_service.get_metrics()

    start_time = time.time()

    result = generate_response(
        prompt=request.prompt
    )

    latency = round(
        time.time() - start_time,
        3
    )

    workload_class = classify_workload(
    	latency_seconds=latency,
    	response_length=len(result["response"])
)

    after_metrics = monitoring_service.get_metrics()

    db = SessionLocal()

    try:

        execution = LLMExecution(
            prompt=request.prompt,

            prompt_length=len(request.prompt),

            response_length=len(
                result["response"]
            ),

	    workload_class=workload_class,

            latency_seconds=latency,

            cpu_before=before_metrics["cpu"]["usage_percent"],
            cpu_after=after_metrics["cpu"]["usage_percent"],

            ram_before=before_metrics["memory"]["usage_percent"],
            ram_after=after_metrics["memory"]["usage_percent"],

            gpu_before=before_metrics["gpu"]["usage_percent"],
            gpu_after=after_metrics["gpu"]["usage_percent"],

            vram_before=before_metrics["gpu"]["memory_used_mb"],
            vram_after=after_metrics["gpu"]["memory_used_mb"],

            temperature_before=before_metrics["gpu"]["temperature_c"],
            temperature_after=after_metrics["gpu"]["temperature_c"],

            power_before=before_metrics["gpu"]["power_watts"],
            power_after=after_metrics["gpu"]["power_watts"]
        )

        db.add(execution)
        db.commit()

    finally:
        db.close()

    return {
    "timestamp": datetime.utcnow(),
    "response": result["response"],
    "latency_seconds": latency,
    "workload_class": workload_class
}