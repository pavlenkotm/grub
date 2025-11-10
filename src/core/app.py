"""
Main application module
"""

import time
import signal
import sys
from typing import Optional, Dict, Any

from .config import Config
from .database import Database
from .scheduler import get_scheduler
from .events import get_event_emitter
from ..utils.logger import get_logger
from ..utils.cache import get_cache


class GrubApp:
    """Main application class for GRUB"""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None):
        """Initialize the GRUB application

        Args:
            config_path: Path to configuration file
            config_dict: Optional configuration dictionary
        """
        self.is_running = False
        self._shutdown_requested = False

        # Initialize logger first
        self.logger = get_logger(level="INFO")
        self.logger.info("Initializing GRUB Application...")

        # Initialize configuration
        try:
            self.config = Config()
            if config_path:
                self.config.load_from_file(config_path)
            elif config_dict:
                for key, value in config_dict.items():
                    self.config.set(key, value)
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise

        # Initialize database
        try:
            db_path = self.config.get("database.path", ":memory:")
            self.database = Database(db_path)
            self.database.connect()
            self.logger.info(f"Database initialized: {db_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise

        # Initialize cache
        try:
            cache_ttl = self.config.get("cache.default_ttl", 300)
            self.cache = get_cache(default_ttl=cache_ttl)
            self.logger.info(f"Cache initialized (TTL: {cache_ttl}s)")
        except Exception as e:
            self.logger.error(f"Failed to initialize cache: {e}")
            raise

        # Initialize event emitter
        try:
            self.events = get_event_emitter()
            self._setup_event_handlers()
            self.logger.info("Event system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize event system: {e}")
            raise

        # Initialize scheduler
        try:
            self.scheduler = get_scheduler()
            self._setup_scheduled_tasks()
            self.logger.info("Scheduler initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize scheduler: {e}")
            raise

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.logger.info("GRUB Application initialized successfully")

    def _setup_event_handlers(self):
        """Setup default event handlers"""
        self.events.on("app.start", lambda: self.logger.info("Application start event triggered"))
        self.events.on("app.stop", lambda: self.logger.info("Application stop event triggered"))
        self.events.on("app.error", lambda error: self.logger.error(f"Application error: {error}"))

    def _setup_scheduled_tasks(self):
        """Setup default scheduled tasks"""
        # Schedule cache cleanup every 5 minutes
        self.scheduler.add_task(
            "cache_cleanup",
            self.cache.cleanup_expired,
            interval=300
        )
        self.logger.info("Scheduled task: cache_cleanup (every 5 minutes)")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self._shutdown_requested = True

    def start(self):
        """Start the application"""
        if self.is_running:
            self.logger.warning("Application is already running")
            return

        self.logger.info("Starting GRUB Application...")
        self.is_running = True
        self._shutdown_requested = False

        # Start scheduler
        self.scheduler.start()

        # Emit start event
        self.events.emit("app.start")

        self.logger.info("GRUB Application started successfully!")

    def stop(self):
        """Stop the application"""
        if not self.is_running:
            self.logger.warning("Application is not running")
            return

        self.logger.info("Stopping GRUB Application...")
        self.is_running = False

        # Emit stop event
        self.events.emit("app.stop")

        # Stop scheduler
        try:
            self.scheduler.stop()
            self.logger.info("Scheduler stopped")
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {e}")

        # Disconnect database
        try:
            self.database.disconnect()
            self.logger.info("Database disconnected")
        except Exception as e:
            self.logger.error(f"Error disconnecting database: {e}")

        # Clear cache
        try:
            self.cache.clear()
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")

        self.logger.info("GRUB Application stopped")

    def run(self, duration: Optional[int] = None):
        """Main run loop

        Args:
            duration: Optional duration in seconds (runs indefinitely if None)
        """
        self.start()
        try:
            self._main_loop(duration)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
            self.events.emit("app.error", str(e))
            raise
        finally:
            self.stop()

    def _main_loop(self, duration: Optional[int] = None):
        """Main application loop

        Args:
            duration: Optional duration in seconds
        """
        self.logger.info("Running main application loop...")
        start_time = time.time()

        while self.is_running and not self._shutdown_requested:
            # Check duration limit
            if duration and (time.time() - start_time) >= duration:
                self.logger.info(f"Duration limit reached ({duration}s)")
                break

            # Perform health checks
            self._health_check()

            # Sleep briefly to avoid high CPU usage
            time.sleep(1)

        self.logger.info("Main loop exited")

    def _health_check(self):
        """Perform health checks on all components"""
        # This runs every loop iteration but should be lightweight
        # For now, just verify components are accessible
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get application status

        Returns:
            Dictionary containing status information
        """
        return {
            "running": self.is_running,
            "database_connected": self.database.connection is not None,
            "scheduler_running": self.scheduler.running,
            "cache_size": self.cache.size(),
            "event_listeners": len(self.events.event_names()),
            "scheduled_tasks": len(self.scheduler.get_tasks())
        }


if __name__ == "__main__":
    app = GrubApp()
    app.run()
