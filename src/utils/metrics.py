"""
Metrics tracking and monitoring module
"""

import time
from collections import defaultdict
from typing import Dict, List, Optional
from threading import Lock
from datetime import datetime

from .logger import get_logger


class MetricsCollector:
    """Metrics collector for tracking application performance and usage"""

    def __init__(self):
        """Initialize metrics collector"""
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.timers: Dict[str, List[float]] = defaultdict(list)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = Lock()
        self.logger = get_logger()
        self.start_time = time.time()

    def increment(self, metric: str, value: int = 1) -> None:
        """Increment a counter metric

        Args:
            metric: Metric name
            value: Value to increment by
        """
        with self._lock:
            self.counters[metric] += value
            self.logger.debug(f"Incremented metric {metric} by {value}")

    def decrement(self, metric: str, value: int = 1) -> None:
        """Decrement a counter metric

        Args:
            metric: Metric name
            value: Value to decrement by
        """
        with self._lock:
            self.counters[metric] -= value
            self.logger.debug(f"Decremented metric {metric} by {value}")

    def set_gauge(self, metric: str, value: float) -> None:
        """Set a gauge metric

        Args:
            metric: Metric name
            value: Gauge value
        """
        with self._lock:
            self.gauges[metric] = value
            self.logger.debug(f"Set gauge {metric} to {value}")

    def record_timing(self, metric: str, duration: float) -> None:
        """Record a timing metric

        Args:
            metric: Metric name
            duration: Duration in seconds
        """
        with self._lock:
            self.timers[metric].append(duration)
            self.logger.debug(f"Recorded timing for {metric}: {duration:.4f}s")

    def record_value(self, metric: str, value: float) -> None:
        """Record a histogram value

        Args:
            metric: Metric name
            value: Value to record
        """
        with self._lock:
            self.histograms[metric].append(value)
            self.logger.debug(f"Recorded value for {metric}: {value}")

    def get_counter(self, metric: str) -> int:
        """Get counter value

        Args:
            metric: Metric name

        Returns:
            Counter value
        """
        with self._lock:
            return self.counters.get(metric, 0)

    def get_gauge(self, metric: str) -> Optional[float]:
        """Get gauge value

        Args:
            metric: Metric name

        Returns:
            Gauge value or None
        """
        with self._lock:
            return self.gauges.get(metric)

    def get_timing_stats(self, metric: str) -> Dict[str, float]:
        """Get timing statistics

        Args:
            metric: Metric name

        Returns:
            Dictionary of timing statistics
        """
        with self._lock:
            timings = self.timers.get(metric, [])
            if not timings:
                return {}

            return {
                'count': len(timings),
                'min': min(timings),
                'max': max(timings),
                'avg': sum(timings) / len(timings),
                'total': sum(timings)
            }

    def get_histogram_stats(self, metric: str) -> Dict[str, float]:
        """Get histogram statistics

        Args:
            metric: Metric name

        Returns:
            Dictionary of histogram statistics
        """
        with self._lock:
            values = self.histograms.get(metric, [])
            if not values:
                return {}

            sorted_values = sorted(values)
            count = len(sorted_values)

            return {
                'count': count,
                'min': sorted_values[0],
                'max': sorted_values[-1],
                'avg': sum(sorted_values) / count,
                'median': sorted_values[count // 2],
                'p95': sorted_values[int(count * 0.95)] if count > 0 else 0,
                'p99': sorted_values[int(count * 0.99)] if count > 0 else 0
            }

    def get_all_metrics(self) -> Dict:
        """Get all metrics

        Returns:
            Dictionary of all metrics
        """
        with self._lock:
            return {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'timers': {k: self.get_timing_stats(k) for k in self.timers},
                'histograms': {k: self.get_histogram_stats(k) for k in self.histograms},
                'uptime': time.time() - self.start_time
            }

    def reset_metric(self, metric: str) -> None:
        """Reset a specific metric

        Args:
            metric: Metric name
        """
        with self._lock:
            if metric in self.counters:
                self.counters[metric] = 0
            if metric in self.gauges:
                del self.gauges[metric]
            if metric in self.timers:
                self.timers[metric] = []
            if metric in self.histograms:
                self.histograms[metric] = []
            self.logger.info(f"Reset metric: {metric}")

    def reset_all(self) -> None:
        """Reset all metrics"""
        with self._lock:
            self.counters.clear()
            self.gauges.clear()
            self.timers.clear()
            self.histograms.clear()
            self.start_time = time.time()
            self.logger.info("Reset all metrics")

    def timer(self, metric: str):
        """Context manager for timing operations

        Args:
            metric: Metric name

        Example:
            with metrics.timer('operation'):
                # code to time
        """
        return TimerContext(self, metric)


class TimerContext:
    """Context manager for timing operations"""

    def __init__(self, collector: MetricsCollector, metric: str):
        """Initialize timer context

        Args:
            collector: Metrics collector
            metric: Metric name
        """
        self.collector = collector
        self.metric = metric
        self.start_time = None

    def __enter__(self):
        """Start timer"""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and record duration"""
        duration = time.time() - self.start_time
        self.collector.record_timing(self.metric, duration)


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics() -> MetricsCollector:
    """Get or create metrics collector

    Returns:
        MetricsCollector instance
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
