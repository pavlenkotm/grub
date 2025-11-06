"""
Event system for publish-subscribe pattern
"""

from typing import Any, Callable, Dict, List
from threading import Lock

from ..utils.logger import get_logger


class EventEmitter:
    """Event emitter for publish-subscribe pattern"""

    def __init__(self):
        """Initialize event emitter"""
        self._listeners: Dict[str, List[Callable]] = {}
        self._lock = Lock()
        self.logger = get_logger()

    def on(self, event: str, callback: Callable) -> None:
        """Register event listener

        Args:
            event: Event name
            callback: Callback function
        """
        with self._lock:
            if event not in self._listeners:
                self._listeners[event] = []
            self._listeners[event].append(callback)
            self.logger.debug(f"Registered listener for event: {event}")

    def off(self, event: str, callback: Callable) -> bool:
        """Unregister event listener

        Args:
            event: Event name
            callback: Callback function

        Returns:
            True if listener was removed
        """
        with self._lock:
            if event in self._listeners and callback in self._listeners[event]:
                self._listeners[event].remove(callback)
                self.logger.debug(f"Unregistered listener for event: {event}")
                return True
            return False

    def emit(self, event: str, *args, **kwargs) -> int:
        """Emit event to all listeners

        Args:
            event: Event name
            *args: Positional arguments for callbacks
            **kwargs: Keyword arguments for callbacks

        Returns:
            Number of listeners called
        """
        with self._lock:
            listeners = self._listeners.get(event, []).copy()

        if not listeners:
            self.logger.debug(f"No listeners for event: {event}")
            return 0

        self.logger.debug(f"Emitting event: {event} to {len(listeners)} listeners")

        count = 0
        for callback in listeners:
            try:
                callback(*args, **kwargs)
                count += 1
            except Exception as e:
                self.logger.error(f"Error in event listener for {event}: {e}")

        return count

    def once(self, event: str, callback: Callable) -> None:
        """Register one-time event listener

        Args:
            event: Event name
            callback: Callback function
        """
        def wrapper(*args, **kwargs):
            self.off(event, wrapper)
            callback(*args, **kwargs)

        self.on(event, wrapper)

    def remove_all_listeners(self, event: str = None) -> None:
        """Remove all listeners for event or all events

        Args:
            event: Optional event name (removes all if not specified)
        """
        with self._lock:
            if event:
                if event in self._listeners:
                    del self._listeners[event]
                    self.logger.info(f"Removed all listeners for event: {event}")
            else:
                self._listeners.clear()
                self.logger.info("Removed all event listeners")

    def listener_count(self, event: str) -> int:
        """Get number of listeners for event

        Args:
            event: Event name

        Returns:
            Number of listeners
        """
        with self._lock:
            return len(self._listeners.get(event, []))

    def event_names(self) -> List[str]:
        """Get list of event names with listeners

        Returns:
            List of event names
        """
        with self._lock:
            return list(self._listeners.keys())


# Global event emitter instance
_default_emitter: EventEmitter = None


def get_event_emitter() -> EventEmitter:
    """Get or create default event emitter

    Returns:
        EventEmitter instance
    """
    global _default_emitter
    if _default_emitter is None:
        _default_emitter = EventEmitter()
    return _default_emitter
