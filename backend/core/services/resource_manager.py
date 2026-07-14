import os
import psutil
import gc
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """Monitors local node hardware utilizing psutil and simulated GPU tracking."""
    
    @staticmethod
    def get_system_metrics() -> Dict[str, float]:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        
        metrics = {
            "cpu_usage_percent": cpu_percent,
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "ram_used_gb": round(ram.used / (1024**3), 2),
            "ram_usage_percent": ram.percent,
            "gpu_usage_percent": 0.0,  # Simulated (pynvml required for physical)
            "vram_usage_percent": 0.0
        }
        return metrics

    @staticmethod
    def assert_memory_safe(required_gb: float = 0.5) -> bool:
        """
        Prevents Out-Of-Memory (OOM) crashes by asserting available RAM.
        If less than required_gb is available, returns False.
        """
        ram = psutil.virtual_memory()
        available_gb = ram.available / (1024**3)
        if available_gb < required_gb:
            logger.warning(f"Memory unsafe! Only {available_gb:.2f}GB available, {required_gb}GB required.")
            return False
        return True

class MemoryManager:
    """Manages active memory garbage collection to prevent pipeline leaks."""
    
    @staticmethod
    def release_memory():
        """Aggressively forces Python's garbage collector to flush unreferenced dataframes."""
        collected = gc.collect()
        logger.debug(f"MemoryManager flushed {collected} unreferenced objects.")
        
    @staticmethod
    def batch_generator(df, batch_size: int = 50000):
        """
        Automatically slices massive Pandas DataFrames into memory-safe generator chunks.
        """
        for i in range(0, len(df), batch_size):
            yield df.iloc[i:i + batch_size]

class CacheManager:
    """Caches reusable computations to bypass redundant calculations."""
    
    _cache = {}
    
    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._cache.get(key)
        
    @classmethod
    def set(cls, key: str, value: Any, max_keys: int = 50):
        if len(cls._cache) >= max_keys:
            # Simple FIFO eviction
            oldest_key = next(iter(cls._cache))
            del cls._cache[oldest_key]
        cls._cache[key] = value
        
    @classmethod
    def clear(cls):
        cls._cache.clear()
        
# Singletons for easy importing
resource_monitor = ResourceMonitor()
memory_manager = MemoryManager()
cache_manager = CacheManager()
