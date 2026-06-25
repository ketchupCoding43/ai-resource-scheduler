from app.scheduler.predictive_scheduler import (
    predictive_decision
)
from app.predictor.workload_predictor import (
    predict_workload
)
from app.scheduler.queue_manager import (
    enqueue,
    dequeue,
    queue_size
)
from app.scheduler.rule_scheduler import make_decision
from datetime import datetime
from app.profiler.workload_profiler import classify_workload
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup_event():
    monitoring_service.start()


@app.get("/queue")
def queue_status():

    return {
        "pending_requests": queue_size()
    }

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

@app.get("/workload/distribution")
def workload_distribution():

    db = SessionLocal()

    try:

        records = db.query(
            LLMExecution
        ).all()

        light = sum(
            1 for row in records
            if row.workload_class == "LIGHT"
        )

        medium = sum(
            1 for row in records
            if row.workload_class == "MEDIUM"
        )

        heavy = sum(
            1 for row in records
            if row.workload_class == "HEAVY"
        )

        return {
            "LIGHT": light,
            "MEDIUM": medium,
            "HEAVY": heavy,
            "TOTAL": len(records)
        }

    finally:
        db.close()

@app.get("/latency/stats")
def latency_stats():

    db = SessionLocal()

    try:

        records = db.query(
            LLMExecution
        ).all()

        if len(records) == 0:
            return {
                "average_latency_seconds": 0
            }

        average_latency = round(
            sum(
                row.latency_seconds
                for row in records
            ) / len(records),
            3
        )

        return {
            "average_latency_seconds": average_latency
        }

    finally:
        db.close()

@app.get("/resource/stats")
def resource_stats():

    db = SessionLocal()

    try:

        records = db.query(
            LLMExecution
        ).all()

        if len(records) == 0:

            return {
                "average_cpu": 0,
                "average_ram": 0,
                "average_gpu": 0
            }

        avg_cpu = round(
            sum(row.cpu_after or 0 for row in records)
            / len(records),
            2
        )

        avg_ram = round(
            sum(row.ram_after for row in records)
            / len(records),
            2
        )

        avg_gpu = round(
            sum(row.gpu_after for row in records)
            / len(records),
            2
        )

        return {
            "average_cpu": avg_cpu,
            "average_ram": avg_ram,
            "average_gpu": avg_gpu
        }

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
                "model_name": row.model_name,
                "predicted_class": row.predicted_class,
                "predicted_score": row.predicted_score,
                "prediction_correct": row.prediction_correct,
                "workload_class": row.workload_class,
                "workload_score": row.workload_score,
                "prompt_length": row.prompt_length,
                "response_length": row.response_length,
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

@app.get("/prediction/stats")
def prediction_stats():

    db = SessionLocal()

    try:

        records = db.query(
            LLMExecution
        ).all()

        total = len(records)

        if total == 0:
            return {
                "total_predictions": 0,
                "correct_predictions": 0,
                "accuracy_percent": 0
            }

        correct = sum(
            1
            for row in records
            if row.prediction_correct == 1
        )

        accuracy = round(
            (correct / total) * 100,
            2
        )

        return {
            "total_predictions": total,
            "correct_predictions": correct,
            "accuracy_percent": accuracy
        }

    finally:
        db.close()


@app.post("/llm/generate")
def generate(request: GenerateRequest):

    enqueue(request.prompt)

    position_before = queue_size()

    before_metrics = monitoring_service.get_metrics()

    prediction = predict_workload(
        request.prompt
    )

    predicted_class = prediction["class"]
    predicted_score = prediction["score"]

    predictive_result = predictive_decision(
        predicted_class=predicted_class,
        metrics=before_metrics,
        queue_size=queue_size()
    )

    if predictive_result["decision"] == "DELAY":

        dequeue()

        return {
            "timestamp": datetime.utcnow(),
            "scheduler_decision": "DELAY",
            "scheduler_reason": predictive_result["reason"],
            "predicted_class": predicted_class,
            "predicted_score": predicted_score,
            "queue_size": queue_size()
        }

    start_time = time.time()

    result = generate_response(
        prompt=request.prompt
    )

    dequeue()

    position_after = queue_size()

    latency = round(
        time.time() - start_time,
        3
    )

    after_metrics = monitoring_service.get_metrics()

    workload_result = classify_workload(
        prompt_length=len(request.prompt),
        response_length=len(result["response"]),
        latency_seconds=latency,
        gpu_usage=after_metrics["gpu"]["usage_percent"],
        vram_usage=after_metrics["gpu"]["memory_used_mb"]
    )

    workload_class = workload_result["class"]
    workload_score = workload_result["score"]

    prediction_correct = (
        predicted_class == workload_class
    )

    decision = make_decision(
        workload_class=workload_class,
        metrics=after_metrics,
        queue_size=queue_size()
    )

    db = SessionLocal()

    try:

        execution = LLMExecution(
            prompt=request.prompt,
            model_name=result["model"],

            prompt_length=len(request.prompt),
            response_length=len(result["response"]),

            predicted_class=predicted_class,
            predicted_score=predicted_score,
            prediction_correct=int(prediction_correct),

            workload_class=workload_class,
            workload_score=workload_score,

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
        "model_used": result["model"],

        "latency_seconds": latency,

        "predicted_class": predicted_class,
        "predicted_score": predicted_score,
        "prediction_correct": prediction_correct,

        "workload_class": workload_class,
        "workload_score": workload_score,

        "scheduler_decision": decision["decision"],
        "scheduler_reason": decision["reason"],

        "queue_position_before": position_before,
        "queue_size_after": position_after
    }
