# GRUB - A Powerful Utility Application

GRUB is a comprehensive Python utility application featuring data processing, caching, logging, event systems, task scheduling, and more.

## Features

- **Core Application Framework** - Modular architecture with configurable components
- **Configuration Management** - JSON-based configuration system
- **Database Support** - SQLite database with ORM-like interface
- **Data Processing** - Parallel batch processing, filtering, transformation, and aggregation
- **Event System** - Publish-subscribe pattern for event-driven architecture
- **Task Scheduler** - Periodic and time-based task scheduling
- **Logging System** - Flexible logging with file and console output
- **Caching** - In-memory cache with TTL support
- **File Operations** - Comprehensive file and directory management
- **Data Validation** - Email, URL, phone, and custom validation rules
- **HTTP API Client** - RESTful API client with authentication
- **CLI Interface** - Command-line interface for all operations
- **Comprehensive Testing** - Unit tests for core functionality

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd grub

# Install dependencies (if any)
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from src.core.app import GrubApp
from src.core.config import Config

config = Config()
app = GrubApp(config.get_all())
app.run()
```

### CLI Commands

```bash
# Start the application
python -m src.cli.commands start --workers 4

# Check status
python -m src.cli.commands status

# Manage configuration
python -m src.cli.commands config show
python -m src.cli.commands config get app_name
python -m src.cli.commands config set debug true
```

## Project Structure

```
grub/
├── src/
│   ├── core/           # Core application modules
│   │   ├── app.py      # Main application
│   │   ├── config.py   # Configuration management
│   │   ├── database.py # Database operations
│   │   ├── processor.py # Data processing
│   │   ├── events.py   # Event system
│   │   └── scheduler.py # Task scheduler
│   ├── utils/          # Utility modules
│   │   ├── logger.py   # Logging system
│   │   ├── cache.py    # Caching system
│   │   ├── helpers.py  # Helper functions
│   │   ├── file_ops.py # File operations
│   │   ├── validator.py # Data validation
│   │   └── api_client.py # HTTP client
│   ├── cli/            # Command-line interface
│   └── tests/          # Test suite
├── config/             # Configuration files
├── docs/               # Documentation
├── examples/           # Usage examples
└── README.md
```

## Core Modules

### Configuration

```python
from src.core.config import Config

config = Config('config/default.json')
value = config.get('app_name')
config.set('debug', True)
```

### Database

```python
from src.core.database import Database

db = Database('data.db')
db.create_table('users', {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})
db.insert('users', {'name': 'John'})
users = db.fetch_all('SELECT * FROM users')
```

### Event System

```python
from src.core.events import get_event_emitter

emitter = get_event_emitter()
emitter.on('event_name', callback_function)
emitter.emit('event_name', data)
```

### Task Scheduler

```python
from src.core.scheduler import get_scheduler

scheduler = get_scheduler()
scheduler.add_task('cleanup', cleanup_func, interval=3600)
scheduler.start()
```

## Documentation

- [Usage Guide](docs/USAGE.md) - Comprehensive usage instructions
- [API Reference](docs/API.md) - Complete API documentation
- [Examples](examples/) - Code examples for each module

## Testing

Run all tests:

```bash
python -m unittest discover src/tests
```

Run specific test:

```bash
python -m unittest src.tests.test_config
python -m unittest src.tests.test_helpers
```

## Examples

See the `examples/` directory for detailed examples:

- `basic_usage.py` - Basic application usage
- `database_example.py` - Database operations
- `event_example.py` - Event system usage
- `scheduler_example.py` - Task scheduling

## Requirements

- Python 3.7+
- No external dependencies required (uses standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for use under your preferred license.

## Support

For questions and issues, please refer to the documentation or open an issue on the repository.
