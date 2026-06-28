
from app.scheduler.predictive_scheduler import (
    predictive_decision
)
from app.predictor.workload_predictor import (
    predict_workload
)
from app.predictor.predictor_v2 import predict_workload_v2
from app.predictor.feature_extractor import extract_features
from app.predictor.confidence_engine import evaluate_response_confidence
from app.predictor.evaluator import evaluate_predictor
from app.scheduler.queue_manager import (
    enqueue,
    dequeue,
    queue_size
)
from app.scheduler.model_router import select_model
from app.scheduler.escalation_scheduler import should_escalate
from app.scheduler.rule_scheduler import make_decision
from app.scheduler.final_decision_engine import make_final_decision
from datetime import datetime
from app.profiler.workload_profiler import classify_workload, classify_runtime_workload
import time

from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.monitoring.service import monitoring_service

from app.database.database import engine, SessionLocal
from app.database.models import Base, SystemMetrics
from app.database.llm_models import LLMExecution

from app.llm.context_optimizer import choose_context_size
from app.llm.schemas import GenerateRequest
from app.llm.ollama_client import generate_response


Base.metadata.create_all(bind=engine)


def ensure_llm_execution_columns():
    with engine.connect() as connection:
        columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(llm_executions)"))
        }

        add_columns = [
            ("selected_model", "VARCHAR"),
            ("final_model", "VARCHAR"),
            ("routing_reason", "TEXT"),
            ("context_size", "INTEGER"),
            ("confidence_score", "FLOAT"),
            ("confidence_class", "VARCHAR"),
            ("escalated", "INTEGER"),
            ("escalation_reason", "TEXT"),
            ("vram_safe", "INTEGER"),
            ("context_reason", "TEXT"),
            ("prediction_confidence", "FLOAT"),
            ("prediction_intent", "VARCHAR"),
            ("expected_response_size", "VARCHAR"),
            ("complexity_score", "FLOAT"),
            ("estimated_cost", "FLOAT"),
        ]

        for column_name, column_type in add_columns:
            if column_name not in columns:
                connection.execute(
                    text(
                        f"ALTER TABLE llm_executions ADD COLUMN {column_name} {column_type}"
                    )
                )
                connection.commit()

app = FastAPI(
    title="AI Resource Scheduler"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    ensure_llm_execution_columns()
    monitoring_service.start()


@app.get("/prediction/features")
def prediction_features(prompt: str = Query(..., min_length=1)):
    features = extract_features(prompt)
    prediction = predict_workload_v2(prompt)
    return {
        **features,
        "predicted_workload": prediction["class"],
        "prediction_confidence": prediction["confidence"],
        "intent": prediction["intent"],
        "expected_response_size": prediction["expected_response_size"],
        "complexity_score": prediction["complexity_score"],
    }


@app.get("/prediction/analyze")
def prediction_analyze(prompt: str = Query(..., min_length=1)):
    prediction = predict_workload_v2(prompt)
    features = prediction["features"]
    return {
        "intent": prediction["intent"],
        "expected_response_size": prediction["expected_response_size"],
        "technical_keyword_count": features["technical_keyword_count"],
        "topic_count": features["topic_count"],
        "complexity_score": prediction["complexity_score"],
        "predicted_class": prediction["class"],
    }


@app.get("/prediction/evaluation")
def prediction_evaluation():
    return evaluate_predictor()


@app.get("/scheduler/escalation/stats")
def scheduler_escalation_stats():
    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()
        total_requests = len(records)
        escalated_requests = sum(1 for row in records if row.escalated == 1)
        draft_success_requests = total_requests - escalated_requests

        escalation_rate_percent = round((escalated_requests / total_requests) * 100, 2) if total_requests else 0
        draft_success_rate_percent = round((draft_success_requests / total_requests) * 100, 2) if total_requests else 0

        return {
            "total_requests": total_requests,
            "escalated_requests": escalated_requests,
            "draft_success_requests": draft_success_requests,
            "escalation_rate_percent": escalation_rate_percent,
            "draft_success_rate_percent": draft_success_rate_percent,
        }

    finally:
        db.close()


@app.get("/scheduler/context/stats")
def scheduler_context_stats():
    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()
        return {
            "1024": sum(1 for row in records if row.context_size == 1024),
            "2048": sum(1 for row in records if row.context_size == 2048),
            "4096": sum(1 for row in records if row.context_size == 4096),
        }

    finally:
        db.close()


@app.get("/scheduler/confidence/stats")
def scheduler_confidence_stats():
    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()
        total_requests = len(records)

        if total_requests == 0:
            return {
                "average_confidence": 0,
                "high_confidence": 0,
                "medium_confidence": 0,
                "low_confidence": 0,
            }

        confidence_values = [row.confidence_score or 0 for row in records]
        average_confidence = round(sum(confidence_values) / total_requests, 2)

        return {
            "average_confidence": average_confidence,
            "high_confidence": sum(1 for value in confidence_values if value >= 75),
            "medium_confidence": sum(1 for value in confidence_values if 50 <= value < 75),
            "low_confidence": sum(1 for value in confidence_values if value < 50),
        }

    finally:
        db.close()


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


@app.get("/model/distribution")
def model_distribution():

    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()

        return {
            "qwen2.5-coder:3b": sum(
                1 for row in records
                if (row.selected_model or row.model_name) == "qwen2.5-coder:3b"
            ),
            "qwen2.5-coder:7b": sum(
                1 for row in records
                if (row.selected_model or row.model_name) == "qwen2.5-coder:7b"
            )
        }

    finally:
        db.close()


@app.get("/cost/stats")
def cost_stats():
    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()
        total_requests = len(records)

        if total_requests == 0:
            return {
                "total_requests": 0,
                "actual_cost": 0,
                "baseline_cost": 0,
                "savings_percent": 0,
            }

        def row_cost(row):
            if row.estimated_cost is not None:
                return row.estimated_cost
            model_name = row.selected_model or row.model_name
            return 1.0 if model_name == "qwen2.5-coder:3b" else 3.0

        actual_cost = round(sum(row_cost(row) for row in records), 2)
        baseline_cost = total_requests * 3
        savings_percent = round(
            ((baseline_cost - actual_cost) / baseline_cost) * 100,
            2,
        ) if baseline_cost else 0

        return {
            "total_requests": total_requests,
            "actual_cost": actual_cost,
            "baseline_cost": baseline_cost,
            "savings_percent": savings_percent,
        }

    finally:
        db.close()


@app.get("/execution/trends")
def execution_trends(limit: int = 20):
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
                "latency": row.latency_seconds,
                "cpu": row.cpu_after,
                "ram": row.ram_after,
                "gpu": row.gpu_after,
            }
            for row in reversed(records)
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
                "prediction_confidence": row.prediction_confidence,
                "prediction_intent": row.prediction_intent,
                "expected_response_size": row.expected_response_size,
                "complexity_score": row.complexity_score,
                "selected_model": row.selected_model,
                "final_model": row.final_model,
                "routing_reason": row.routing_reason,
                "context_size": row.context_size,
                "context_reason": row.context_reason,
                "confidence_score": row.confidence_score,
                "confidence_class": row.confidence_class,
                "escalated": row.escalated,
                "escalation_reason": row.escalation_reason,
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

        aligned = sum(
            1 for row in records
            if row.prediction_correct == 1
        )

        alignment = round((aligned / total) * 100, 2)

        return {
            "total_predictions": total,
            "aligned_predictions": aligned,
            "prediction_execution_alignment_percent": alignment,
            "accuracy_percent": alignment,
        }

    finally:
        db.close()


@app.post("/llm/generate")
def generate(request: GenerateRequest):

    enqueue(request.prompt)

    position_before = queue_size()

    before_metrics = monitoring_service.get_metrics()

    try:
        prediction = predict_workload_v2(request.prompt)
    except Exception:
        fallback_prediction = predict_workload(request.prompt)
        prediction = {
            "class": fallback_prediction["class"],
            "score": fallback_prediction["score"],
            "confidence": 0,
            "intent": "GENERAL",
            "expected_response_size": "MEDIUM",
            "complexity_score": 0,
            "features": {},
        }

    predicted_class = prediction["class"]
    predicted_score = prediction["score"]
    prediction_confidence = prediction["confidence"]
    prediction_intent = prediction["intent"]
    expected_response_size = prediction["expected_response_size"]
    complexity_score = prediction["complexity_score"]
    routing = select_model(
        predicted_class=predicted_class,
        predicted_score=predicted_score,
        metrics=before_metrics
    )
    selected_model = routing["selected_model"]
    routing_reason = routing["routing_reason"]
    vram_safe = routing["vram_safe"]
    context_choice = choose_context_size(
        prompt=request.prompt,
        selected_model=selected_model,
        metrics=before_metrics
    )
    context_size = context_choice["context_size"]
    context_reason = context_choice["reason"]
    estimated_cost = 1.0 if selected_model == "qwen2.5-coder:3b" else 3.0

    start_time = time.time()

    draft_result = generate_response(
        prompt=request.prompt,
        model_name=selected_model,
        context_size=context_size
    )

    confidence_result = evaluate_response_confidence(
        prompt=request.prompt,
        response=draft_result["response"],
        predicted_class=predicted_class
    )

    escalation = should_escalate(
        confidence_result=confidence_result,
        predicted_class=predicted_class,
        selected_model=selected_model
    )

    final_response = draft_result["response"]
    final_model = selected_model
    escalated = False
    escalation_reason = escalation["reason"]
    final_context_reason = context_reason

    if escalation["escalate"] and escalation["target_model"]:
        escalated = True
        final_model = escalation["target_model"]
        final_context = choose_context_size(
            prompt=request.prompt,
            selected_model=final_model,
            metrics=before_metrics
        )
        final_context_size = final_context["context_size"]
        final_context_reason = final_context["reason"]
        escalation_reason = escalation["reason"]
        final_result = generate_response(
            prompt=request.prompt,
            model_name=final_model,
            context_size=final_context_size
        )
        final_response = final_result["response"]
        context_size = final_context_size
        context_reason = final_context_reason
        estimated_cost += 3.0 if final_model == "qwen2.5-coder:7b" else 1.0

    dequeue()

    position_after = queue_size()

    latency = round(
        time.time() - start_time,
        3
    )

    after_metrics = monitoring_service.get_metrics()

    runtime_workload_result = classify_runtime_workload(
        latency_seconds=latency,
        response_length=len(final_response),
        gpu_usage=after_metrics["gpu"]["usage_percent"],
        vram_usage=after_metrics["gpu"]["memory_used_mb"],
        ram_usage=after_metrics["memory"]["usage_percent"],
        final_model=final_model
    )

    actual_workload_class = runtime_workload_result["class"]
    actual_workload_score = runtime_workload_result["score"]

    prediction_correct = (
        predicted_class == actual_workload_class
    )

    decision = make_final_decision(
        predicted_class=predicted_class,
        predicted_score=predicted_score,
        context_size=context_size,
        before_metrics=before_metrics,
        selected_model=selected_model
    )

    confidence_score = confidence_result["confidence"]
    confidence_class = confidence_result["quality_class"]
    confidence_reasons = confidence_result["reasons"]

    db = SessionLocal()

    try:

        execution = LLMExecution(
            prompt=request.prompt,
            model_name=final_model,
            selected_model=selected_model,
            final_model=final_model,
            routing_reason=routing_reason,
            context_size=context_size,
            context_reason=context_reason,
            confidence_score=confidence_score,
            confidence_class=confidence_class,
            escalated=int(escalated),
            escalation_reason=escalation_reason if escalated else None,
            vram_safe=int(vram_safe),

            prompt_length=len(request.prompt),
            response_length=len(final_response),

            predicted_class=predicted_class,
            predicted_score=predicted_score,
            prediction_confidence=prediction_confidence,
            prediction_intent=prediction_intent,
            expected_response_size=expected_response_size,
            complexity_score=complexity_score,
            estimated_cost=estimated_cost,
            prediction_correct=int(prediction_correct),

            workload_class=actual_workload_class,
            workload_score=actual_workload_score,

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

        "response": final_response,
        "model_used": final_model,
        "selected_model": selected_model,
        "final_model": final_model,
        "escalated": escalated,
        "escalation_reason": escalation_reason if escalated else "",
        "confidence": confidence_score,
        "confidence_class": confidence_class,
        "confidence_reasons": confidence_reasons,
        "context_size": context_size,
        "context_reason": context_reason,
        "routing_reason": routing_reason,
        "vram_safe": vram_safe,

        "latency_seconds": latency,

        "predicted_class": predicted_class,
        "predicted_score": predicted_score,
        "prediction_confidence": prediction_confidence,
        "prediction_intent": prediction_intent,
        "expected_response_size": expected_response_size,
        "complexity_score": complexity_score,
        "estimated_cost": estimated_cost,
        "prediction_correct": prediction_correct,

        "actual_workload_class": actual_workload_class,
        "actual_workload_score": actual_workload_score,
        "workload_class": actual_workload_class,
        "workload_score": actual_workload_score,

        "scheduler_decision": decision["decision"],
        "decision_reason": decision["reason"],
        "scheduler_reason": decision["reason"],
        "risk_level": decision["risk_level"],

        "queue_position_before": position_before,
        "queue_size_after": position_after
    }
