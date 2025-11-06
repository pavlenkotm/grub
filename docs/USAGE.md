# GRUB Usage Guide

## Overview

GRUB is a powerful utility application with various modules for data processing, caching, logging, and more.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd grub

# Install dependencies (if any)
pip install -r requirements.txt
```

## Quick Start

### Running the Application

```bash
python -m src.cli.commands start
```

### CLI Commands

#### Start Command

Start the GRUB application with specified workers:

```bash
python -m src.cli.commands start --workers 8
```

#### Status Command

Check application status:

```bash
python -m src.cli.commands status
```

#### Config Commands

Show all configuration:

```bash
python -m src.cli.commands config show
```

Get specific configuration value:

```bash
python -m src.cli.commands config get app_name
```

Set configuration value:

```bash
python -m src.cli.commands config set debug true
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
db.connect()

# Create table
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT',
    'email': 'TEXT'
})

# Insert data
db.insert('users', {'name': 'John', 'email': 'john@example.com'})

# Query data
users = db.fetch_all('SELECT * FROM users')
```

### Data Processing

```python
from src.core.processor import DataProcessor

processor = DataProcessor(max_workers=4)

# Process batch
results = processor.process_batch(items, process_func)

# Filter data
filtered = processor.filter_data(data, {'status': 'active'})

# Transform data
transformed = processor.transform_data(data, {'price': lambda x: x * 1.1})
```

### Event System

```python
from src.core.events import get_event_emitter

emitter = get_event_emitter()

# Register listener
def on_data_received(data):
    print(f"Received: {data}")

emitter.on('data_received', on_data_received)

# Emit event
emitter.emit('data_received', {'value': 42})
```

### Scheduler

```python
from src.core.scheduler import get_scheduler

scheduler = get_scheduler()

# Add periodic task
scheduler.add_task('cleanup', cleanup_func, interval=3600)

# Add daily task
scheduler.add_task('report', generate_report, at_time='09:00')

# Start scheduler
scheduler.start()
```

## Utility Modules

### Logging

```python
from src.utils.logger import get_logger

logger = get_logger(level='DEBUG', log_file='app.log')
logger.info('Application started')
logger.error('An error occurred')
```

### Caching

```python
from src.utils.cache import get_cache

cache = get_cache(default_ttl=300)

# Set value
cache.set('key', 'value', ttl=600)

# Get value
value = cache.get('key')

# Clear cache
cache.clear()
```

### File Operations

```python
from src.utils.file_ops import FileOperations

file_ops = FileOperations()

# Read/write files
content = file_ops.read_file('data.txt')
file_ops.write_file('output.txt', content)

# JSON operations
data = file_ops.read_json('config.json')
file_ops.write_json('output.json', data)
```

### Validation

```python
from src.utils.validator import Validator

validator = Validator()

# Validate email
is_valid = validator.is_email('test@example.com')

# Validate dictionary
rules = {
    'email': [{'type': 'required'}, {'type': 'email'}],
    'age': [{'type': 'range', 'min': 0, 'max': 150}]
}
errors = validator.validate_dict(data, rules)
```

### API Client

```python
from src.utils.api_client import APIClient

client = APIClient('https://api.example.com')
client.set_auth_token('your-token')

# Make requests
data = client.get('/users')
result = client.post('/users', {'name': 'John'})
```

## Advanced Usage

### Custom Configuration

Create a custom configuration file:

```json
{
  "app_name": "MyApp",
  "debug": true,
  "log_level": "DEBUG",
  "max_workers": 8,
  "custom_setting": "value"
}
```

Load it:

```python
config = Config('my_config.json')
```

### Combining Modules

```python
from src.core.app import GrubApp
from src.core.config import Config
from src.utils.logger import get_logger

# Set up
config = Config('config/default.json')
logger = get_logger(level=config.get('log_level'))

# Run app
app = GrubApp(config.get_all())
app.run()
```

## Testing

Run tests:

```bash
python -m unittest discover src/tests
```

Run specific test:

```bash
python -m unittest src.tests.test_config
```

## Troubleshooting

### Debug Mode

Enable debug mode for verbose logging:

```bash
python -m src.cli.commands start --debug
```

### Log Files

Check log files for errors:

```bash
tail -f logs/app.log
```

## Support

For issues and questions, please refer to the project documentation or open an issue on the repository.
