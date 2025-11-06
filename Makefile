.PHONY: help install test lint format clean run examples docs

help:
	@echo "GRUB Development Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help      - Show this help message"
	@echo "  install   - Install the package in development mode"
	@echo "  test      - Run all tests"
	@echo "  lint      - Run code linting"
	@echo "  format    - Format code with black"
	@echo "  clean     - Remove build artifacts and cache files"
	@echo "  run       - Run the application"
	@echo "  examples  - Run example scripts"
	@echo "  docs      - Build documentation"

install:
	@echo "Installing GRUB in development mode..."
	pip install -e .
	@echo "Installation complete!"

install-dev:
	@echo "Installing development dependencies..."
	pip install -e .[dev]
	@echo "Development dependencies installed!"

test:
	@echo "Running tests..."
	python -m unittest discover src/tests -v

test-coverage:
	@echo "Running tests with coverage..."
	coverage run -m unittest discover src/tests
	coverage report
	coverage html
	@echo "Coverage report generated in htmlcov/"

lint:
	@echo "Running linters..."
	flake8 src/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	@echo "Formatting code with black..."
	black src/ examples/ --line-length=100

format-check:
	@echo "Checking code format..."
	black src/ examples/ --check --line-length=100

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

run:
	@echo "Starting GRUB application..."
	python -m src.cli.commands start

run-debug:
	@echo "Starting GRUB application in debug mode..."
	python -m src.cli.commands start --debug

status:
	@echo "Checking GRUB status..."
	python -m src.cli.commands status

examples:
	@echo "Running basic usage example..."
	python examples/basic_usage.py
	@echo ""
	@echo "Running database example..."
	python examples/database_example.py
	@echo ""
	@echo "Running event example..."
	python examples/event_example.py

docs:
	@echo "Documentation available in:"
	@echo "  - docs/USAGE.md"
	@echo "  - docs/API.md"
	@echo "  - README.md"
	@echo "  - CONTRIBUTING.md"

build:
	@echo "Building distribution packages..."
	python setup.py sdist bdist_wheel
	@echo "Build complete! Check dist/ directory"

check: format-check lint test
	@echo "All checks passed!"

all: clean install test
	@echo "Complete setup and test finished!"
