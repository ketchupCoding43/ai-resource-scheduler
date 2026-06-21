import threading
import time

from app.monitoring.collector import get_system_metrics


class MonitoringService:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def _monitor_loop(self):
        """
        Runs continuously in a background thread.
        Collects metrics every second.
        """

        while self.running:
            try:
                print("Collecting metrics...")

                latest_metrics = get_system_metrics()

                with self.lock:
                    self.metrics = latest_metrics

            except Exception as e:
                print(f"Monitoring error: {e}")

            time.sleep(1)

    def start(self):
        """
        Start monitoring thread.
        """

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
        """
        Stop monitoring thread.
        """

        self.running = False

    def get_metrics(self):
        """
        Return latest cached metrics.
        """

        with self.lock:
            return self.metrics.copy()


monitoring_service = MonitoringService()