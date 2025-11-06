"""
Event system example
"""

from src.core.events import get_event_emitter
from src.utils.logger import get_logger


def main():
    """Demonstrate event system"""

    logger = get_logger(level='INFO')
    logger.info("Event system example started")

    # Get event emitter
    emitter = get_event_emitter()

    # Define event handlers
    def on_user_login(username):
        logger.info(f"User logged in: {username}")

    def on_user_logout(username):
        logger.info(f"User logged out: {username}")

    def on_data_received(data):
        logger.info(f"Data received: {data}")

    # Register event listeners
    emitter.on('user_login', on_user_login)
    emitter.on('user_logout', on_user_logout)
    emitter.on('data_received', on_data_received)

    # One-time listener
    def on_system_start():
        logger.info("System started - this will only fire once")

    emitter.once('system_start', on_system_start)

    # Emit events
    emitter.emit('system_start')
    emitter.emit('system_start')  # This won't trigger the listener
    emitter.emit('user_login', 'john_doe')
    emitter.emit('data_received', {'value': 42, 'timestamp': '2025-01-01'})
    emitter.emit('user_logout', 'john_doe')

    # Check listener counts
    logger.info(f"Login listeners: {emitter.listener_count('user_login')}")
    logger.info(f"All events: {emitter.event_names()}")

    logger.info("Event system example completed")


if __name__ == "__main__":
    main()
