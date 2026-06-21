from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SystemMetrics(Base):
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime)

    cpu_usage = Column(Float)

    ram_usage = Column(Float)
    ram_available_gb = Column(Float)

    gpu_usage = Column(Float)

    vram_used_mb = Column(Float)
    vram_free_mb = Column(Float)

    temperature_c = Column(Float)

    power_watts = Column(Float)