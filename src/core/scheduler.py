"""
Task scheduler module
"""

import time
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional
from threading import Thread, Event, Lock

from ..utils.logger import get_logger


class ScheduledTask:
    """Scheduled task representation"""

    def __init__(
        self,
        name: str,
        func: Callable,
        interval: Optional[int] = None,
        at_time: Optional[str] = None,
        args: tuple = (),
        kwargs: dict = None
    ):
        """Initialize scheduled task

        Args:
            name: Task name
            func: Function to execute
            interval: Interval in seconds (for periodic tasks)
            at_time: Time to run (HH:MM format, for daily tasks)
            args: Function positional arguments
            kwargs: Function keyword arguments
        """
        self.name = name
        self.func = func
        self.interval = interval
        self.at_time = at_time
        self.args = args
        self.kwargs = kwargs or {}
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.enabled = True

        self._calculate_next_run()

    def _calculate_next_run(self):
        """Calculate next run time"""
        now = datetime.now()

        if self.interval:
            if self.last_run:
                self.next_run = self.last_run + timedelta(seconds=self.interval)
            else:
                self.next_run = now
        elif self.at_time:
            hour, minute = map(int, self.at_time.split(':'))
            self.next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if self.next_run <= now:
                self.next_run += timedelta(days=1)

    def should_run(self) -> bool:
        """Check if task should run now

        Returns:
            True if task should run
        """
        if not self.enabled or not self.next_run:
            return False
        return datetime.now() >= self.next_run

    def run(self):
        """Execute task"""
        self.func(*self.args, **self.kwargs)
        self.last_run = datetime.now()
        self._calculate_next_run()


class Scheduler:
    """Task scheduler for running periodic and scheduled tasks"""

    def __init__(self):
        """Initialize scheduler"""
        self.tasks: Dict[str, ScheduledTask] = {}
        self._running = False
        self._thread: Optional[Thread] = None
        self._stop_event = Event()
        self._lock = Lock()
        self.logger = get_logger()

    def add_task(
        self,
        name: str,
        func: Callable,
        interval: Optional[int] = None,
        at_time: Optional[str] = None,
        args: tuple = (),
        kwargs: dict = None
    ) -> None:
        """Add scheduled task

        Args:
            name: Task name
            func: Function to execute
            interval: Interval in seconds (for periodic tasks)
            at_time: Time to run (HH:MM format, for daily tasks)
            args: Function positional arguments
            kwargs: Function keyword arguments
        """
        with self._lock:
            task = ScheduledTask(name, func, interval, at_time, args, kwargs)
            self.tasks[name] = task
            self.logger.info(f"Added scheduled task: {name}")

    def remove_task(self, name: str) -> bool:
        """Remove scheduled task

        Args:
            name: Task name

        Returns:
            True if task was removed
        """
        with self._lock:
            if name in self.tasks:
                del self.tasks[name]
                self.logger.info(f"Removed scheduled task: {name}")
                return True
            return False

    def enable_task(self, name: str) -> bool:
        """Enable scheduled task

        Args:
            name: Task name

        Returns:
            True if task was enabled
        """
        with self._lock:
            if name in self.tasks:
                self.tasks[name].enabled = True
                self.logger.info(f"Enabled task: {name}")
                return True
            return False

    def disable_task(self, name: str) -> bool:
        """Disable scheduled task

        Args:
            name: Task name

        Returns:
            True if task was disabled
        """
        with self._lock:
            if name in self.tasks:
                self.tasks[name].enabled = False
                self.logger.info(f"Disabled task: {name}")
                return True
            return False

    def start(self):
        """Start scheduler"""
        if self._running:
            self.logger.warning("Scheduler already running")
            return

        self._running = True
        self._stop_event.clear()
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop scheduler"""
        if not self._running:
            return

        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        self.logger.info("Scheduler stopped")

    def _run_loop(self):
        """Main scheduler loop"""
        while self._running and not self._stop_event.is_set():
            with self._lock:
                tasks = list(self.tasks.values())

            for task in tasks:
                if task.should_run():
                    try:
                        self.logger.debug(f"Running scheduled task: {task.name}")
                        task.run()
                    except Exception as e:
                        self.logger.error(f"Error running task {task.name}: {e}")

            # Sleep briefly to avoid high CPU usage
            time.sleep(1)

    def get_tasks(self) -> Dict[str, Dict]:
        """Get information about all tasks

        Returns:
            Dictionary of task information
        """
        with self._lock:
            return {
                name: {
                    'enabled': task.enabled,
                    'interval': task.interval,
                    'at_time': task.at_time,
                    'last_run': task.last_run,
                    'next_run': task.next_run
                }
                for name, task in self.tasks.items()
            }


# Global scheduler instance
_default_scheduler: Optional[Scheduler] = None
_scheduler_lock = Lock()


def get_scheduler() -> Scheduler:
    """Get or create default scheduler (thread-safe)

    Returns:
        Scheduler instance
    """
    global _default_scheduler
    if _default_scheduler is None:
        with _scheduler_lock:
            # Double-check locking pattern
            if _default_scheduler is None:
                _default_scheduler = Scheduler()
    return _default_scheduler
