from datetime import datetime
import psutil
from pynvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetTemperature,
    nvmlDeviceGetPowerUsage,
    NVML_TEMPERATURE_GPU,
)


def get_system_metrics():
    metrics = {
        "timestamp": datetime.now().isoformat()
    }

    # =====================
    # CPU Metrics
    # =====================
    metrics["cpu"] = {
        "usage_percent": psutil.cpu_percent(interval=None),
        "cores": psutil.cpu_count(logical=True),
    }

    # =====================
    # Memory Metrics
    # =====================
    memory = psutil.virtual_memory()

    metrics["memory"] = {
        "total_gb": round(memory.total / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "usage_percent": memory.percent,
    }

    # =====================
    # GPU Metrics
    # =====================
    try:
        nvmlInit()

        handle = nvmlDeviceGetHandleByIndex(0)

        gpu_util = nvmlDeviceGetUtilizationRates(handle)
        gpu_memory = nvmlDeviceGetMemoryInfo(handle)

        metrics["gpu"] = {
            "usage_percent": gpu_util.gpu,
            "memory_used_mb": round(gpu_memory.used / (1024**2), 2),
            "memory_total_mb": round(gpu_memory.total / (1024**2), 2),
            "memory_free_mb": round(gpu_memory.free / (1024**2), 2),
            "temperature_c": nvmlDeviceGetTemperature(
                handle,
                NVML_TEMPERATURE_GPU,
            ),
            "power_watts": round(
                nvmlDeviceGetPowerUsage(handle) / 1000,
                2,
            ),
        }

        nvmlShutdown()

    except Exception as e:
        metrics["gpu"] = {
            "error": str(e)
        }

    return metrics