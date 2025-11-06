"""
Scheduler example
"""

import time
from src.core.scheduler import get_scheduler
from src.utils.logger import get_logger


def main():
    """Demonstrate task scheduler"""

    logger = get_logger(level='INFO')
    logger.info("Scheduler example started")

    # Get scheduler
    scheduler = get_scheduler()

    # Define tasks
    def periodic_task():
        logger.info("Periodic task executed")

    def cleanup_task():
        logger.info("Cleanup task executed")

    # Add tasks
    scheduler.add_task('periodic', periodic_task, interval=5)  # Every 5 seconds
    scheduler.add_task('cleanup', cleanup_task, interval=10)   # Every 10 seconds

    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started")

    # Let it run for 30 seconds
    try:
        logger.info("Running for 30 seconds... (Ctrl+C to stop)")
        time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")

    # Stop scheduler
    scheduler.stop()
    logger.info("Scheduler stopped")

    # Show task information
    tasks = scheduler.get_tasks()
    for name, info in tasks.items():
        logger.info(f"Task {name}: {info}")

    logger.info("Scheduler example completed")


if __name__ == "__main__":
    main()
