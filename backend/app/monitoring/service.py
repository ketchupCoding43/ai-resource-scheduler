import threading
import time
from datetime import datetime

from app.monitoring.collector import get_system_metrics

from app.database.database import SessionLocal
from app.database.models import SystemMetrics


class MonitoringService:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def save_metrics(self, metrics):
        db = SessionLocal()

        try:
            record = SystemMetrics(
                timestamp=datetime.fromisoformat(
                    metrics["timestamp"]
                ),

                cpu_usage=metrics["cpu"]["usage_percent"],

                ram_usage=metrics["memory"]["usage_percent"],
                ram_available_gb=metrics["memory"]["available_gb"],

                gpu_usage=metrics["gpu"]["usage_percent"],

                vram_used_mb=metrics["gpu"]["memory_used_mb"],
                vram_free_mb=metrics["gpu"]["memory_free_mb"],

                temperature_c=metrics["gpu"]["temperature_c"],

                power_watts=metrics["gpu"]["power_watts"]
            )

            db.add(record)
            db.commit()

        except Exception as e:
            print(f"Database error: {e}")

        finally:
            db.close()

    def _monitor_loop(self):
        while self.running:
            try:
                latest_metrics = get_system_metrics()

                with self.lock:
                    self.metrics = latest_metrics

                self.save_metrics(latest_metrics)

            except Exception as e:
                print(f"Monitoring error: {e}")

            time.sleep(1)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )

        self.thread.start()

        print("Monitoring service started")

    def stop(self):
        self.running = False

    def get_metrics(self):
        with self.lock:
            return self.metrics.copy()


monitoring_service = MonitoringService()