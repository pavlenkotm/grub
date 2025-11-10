"""
CLI command definitions
"""

import argparse
import sys
from typing import List, Optional

from ..core.app import GrubApp
from ..core.config import Config
from ..utils.logger import get_logger


class CommandLineInterface:
    """Command-line interface for GRUB application"""

    def __init__(self):
        """Initialize CLI"""
        self.parser = self._create_parser()
        self.logger = get_logger()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser

        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            prog="grub",
            description="GRUB - A powerful utility application",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument(
            "-v", "--version",
            action="version",
            version="%(prog)s 1.0.0"
        )

        parser.add_argument(
            "-c", "--config",
            type=str,
            help="Path to configuration file"
        )

        parser.add_argument(
            "-d", "--debug",
            action="store_true",
            help="Enable debug mode"
        )

        parser.add_argument(
            "-l", "--log-file",
            type=str,
            help="Path to log file"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Start command
        start_parser = subparsers.add_parser("start", help="Start the application")
        start_parser.add_argument(
            "-w", "--workers",
            type=int,
            default=4,
            help="Number of workers"
        )

        # Status command
        subparsers.add_parser("status", help="Show application status")

        # Config command
        config_parser = subparsers.add_parser("config", help="Manage configuration")
        config_parser.add_argument(
            "action",
            choices=["show", "set", "get"],
            help="Configuration action"
        )
        config_parser.add_argument(
            "key",
            nargs="?",
            help="Configuration key"
        )
        config_parser.add_argument(
            "value",
            nargs="?",
            help="Configuration value"
        )

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI with given arguments

        Args:
            args: Command-line arguments (uses sys.argv if None)

        Returns:
            Exit code
        """
        parsed_args = self.parser.parse_args(args)

        # Set up logging
        log_level = "DEBUG" if parsed_args.debug else "INFO"
        logger = get_logger(level=log_level, log_file=parsed_args.log_file)

        # Load configuration
        config = Config(parsed_args.config) if parsed_args.config else Config()

        if parsed_args.command == "start":
            return self._handle_start(config, parsed_args)
        elif parsed_args.command == "status":
            return self._handle_status()
        elif parsed_args.command == "config":
            return self._handle_config(config, parsed_args)
        else:
            self.parser.print_help()
            return 0

    def _handle_start(self, config: Config, args) -> int:
        """Handle start command"""
        try:
            self.logger.info(f"Starting application with {args.workers} workers")
            config.set("max_workers", args.workers)
            app = GrubApp(config_dict=config.get_all())
            app.run()
            return 0
        except Exception as e:
            self.logger.error(f"Failed to start application: {e}")
            return 1

    def _handle_status(self) -> int:
        """Handle status command"""
        try:
            # Create a temporary app instance to get status
            print("GRUB Application Status")
            print("=" * 40)
            print(f"Version: 1.0.0")
            print(f"Status: Ready to start")
            print("")
            print("To run the application, use: grub start")
            return 0
        except Exception as e:
            print(f"Error getting status: {e}")
            return 1

    def _handle_config(self, config: Config, args) -> int:
        """Handle config command"""
        try:
            if args.action == "show":
                print("Current configuration:")
                config_data = config.get_all()
                if not config_data:
                    print("  (empty)")
                else:
                    for key, value in config_data.items():
                        print(f"  {key}: {value}")
            elif args.action == "get":
                if not args.key:
                    print("Error: key required for 'get' action")
                    return 1
                # Validate key format
                if not args.key.replace('.', '').replace('_', '').isalnum():
                    print(f"Error: invalid key format '{args.key}'")
                    return 1
                value = config.get(args.key)
                if value is None:
                    print(f"Key '{args.key}' not found")
                    return 1
                print(f"{args.key}: {value}")
            elif args.action == "set":
                if not args.key or not args.value:
                    print("Error: key and value required for 'set' action")
                    return 1
                # Validate key format
                if not args.key.replace('.', '').replace('_', '').isalnum():
                    print(f"Error: invalid key format '{args.key}'")
                    return 1
                # Try to parse value as appropriate type
                try:
                    # Try to convert to int
                    if args.value.isdigit():
                        value = int(args.value)
                    # Try to convert to float
                    elif '.' in args.value and args.value.replace('.', '').replace('-', '').isdigit():
                        value = float(args.value)
                    # Check for boolean
                    elif args.value.lower() in ('true', 'false'):
                        value = args.value.lower() == 'true'
                    else:
                        value = args.value
                    config.set(args.key, value)
                    print(f"Set {args.key} = {value}")
                except ValueError:
                    config.set(args.key, args.value)
                    print(f"Set {args.key} = {args.value}")
            return 0
        except Exception as e:
            print(f"Error handling config command: {e}")
            return 1


def main():
    """Main entry point for CLI"""
    cli = CommandLineInterface()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
