"""
Basic usage example for GRUB application
"""

from src.core.app import GrubApp
from src.core.config import Config
from src.utils.logger import get_logger


def main():
    """Main function demonstrating basic usage"""

    # Set up logging
    logger = get_logger(level='INFO')
    logger.info("Starting GRUB basic usage example")

    # Load configuration
    config = Config()
    config.set('debug', True)
    config.set('max_workers', 4)

    # Create and run application
    app = GrubApp(config.get_all())
    app.run()

    logger.info("Example completed")


if __name__ == "__main__":
    main()
