from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import DateTime

from datetime import datetime

from app.database.models import Base


class LLMExecution(Base):
    __tablename__ = "llm_executions"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    prompt = Column(Text)
    
    workload_class = Column(Text)
 
    workload_score = Column(Float)

    prompt_length = Column(Integer)

    response_length = Column(Integer)

    latency_seconds = Column(Float)

    cpu_before = Column(Float)
    cpu_after = Column(Float)

    ram_before = Column(Float)
    ram_after = Column(Float)

    gpu_before = Column(Float)
    gpu_after = Column(Float)

    vram_before = Column(Float)
    vram_after = Column(Float)

    temperature_before = Column(Float)
    temperature_after = Column(Float)

    power_before = Column(Float)
    power_after = Column(Float)