"""
Main application module
"""

class GrubApp:
    """Main application class for GRUB"""

    def __init__(self, config=None):
        """Initialize the GRUB application

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.is_running = False

    def start(self):
        """Start the application"""
        self.is_running = True
        print("GRUB Application started successfully!")

    def stop(self):
        """Stop the application"""
        self.is_running = False
        print("GRUB Application stopped.")

    def run(self):
        """Main run loop"""
        self.start()
        try:
            self._main_loop()
        finally:
            self.stop()

    def _main_loop(self):
        """Main application loop"""
        print("Running main application loop...")


if __name__ == "__main__":
    app = GrubApp()
    app.run()
