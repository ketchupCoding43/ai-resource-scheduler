from app.database.database import SessionLocal
from app.database.llm_models import LLMExecution


def historical_accuracy():

    db = SessionLocal()

    try:

        records = db.query(
            LLMExecution
        ).all()

        if len(records) == 0:
            return 0

        correct = sum(
            row.prediction_correct
            for row in records
        )

        return round(
            correct / len(records),
            2
        )

    finally:
        db.close()