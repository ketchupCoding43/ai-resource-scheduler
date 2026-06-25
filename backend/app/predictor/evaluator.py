from app.database.database import SessionLocal
from app.database.llm_models import LLMExecution
from app.predictor.predictor_v2 import predict_workload_v2


def evaluate_predictor():
    db = SessionLocal()

    try:
        records = db.query(LLMExecution).all()
        total_samples = len(records)

        if total_samples == 0:
            return {
                "accuracy": 0,
                "precision": 0,
                "recall": 0,
                "total_samples": 0,
                "confusion_matrix": {
                    "LIGHT": {"LIGHT": 0, "MEDIUM": 0, "HEAVY": 0},
                    "MEDIUM": {"LIGHT": 0, "MEDIUM": 0, "HEAVY": 0},
                    "HEAVY": {"LIGHT": 0, "MEDIUM": 0, "HEAVY": 0},
                },
            }

        labels = ["LIGHT", "MEDIUM", "HEAVY"]
        confusion_matrix = {
            actual: {predicted: 0 for predicted in labels}
            for actual in labels
        }

        correct = 0
        predicted_positive = {label: 0 for label in labels}
        true_positive = {label: 0 for label in labels}
        actual_positive = {label: 0 for label in labels}

        for row in records:
            actual = row.workload_class or "LIGHT"
            predicted = predict_workload_v2(row.prompt or "")["class"]

            if actual in labels and predicted in labels:
                confusion_matrix[actual][predicted] += 1
                predicted_positive[predicted] += 1
                actual_positive[actual] += 1

                if actual == predicted:
                    correct += 1
                    true_positive[actual] += 1

        precision_values = []
        recall_values = []

        for label in labels:
            precision_denominator = predicted_positive[label]
            recall_denominator = actual_positive[label]

            precision_values.append(
                true_positive[label] / precision_denominator
                if precision_denominator
                else 0
            )
            recall_values.append(
                true_positive[label] / recall_denominator
                if recall_denominator
                else 0
            )

        return {
            "accuracy": round((correct / total_samples) * 100, 2),
            "precision": round(sum(precision_values) / len(labels) * 100, 2),
            "recall": round(sum(recall_values) / len(labels) * 100, 2),
            "total_samples": total_samples,
            "confusion_matrix": confusion_matrix,
        }

    finally:
        db.close()
