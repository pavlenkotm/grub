# GRUB API Reference

## Core Modules

### GrubApp

Main application class.

#### Methods

- `__init__(config=None)` - Initialize application
- `start()` - Start the application
- `stop()` - Stop the application
- `run()` - Main run loop

### Config

Configuration management.

#### Methods

- `__init__(config_file=None)` - Initialize with optional config file
- `get(key, default=None)` - Get configuration value
- `set(key, value)` - Set configuration value
- `load_from_file(filepath)` - Load configuration from JSON file
- `save_to_file(filepath)` - Save configuration to JSON file
- `get_all()` - Get all configuration values

### Database

SQLite database manager.

#### Methods

- `__init__(db_path=":memory:")` - Initialize database connection
- `connect()` - Establish connection
- `disconnect()` - Close connection
- `execute(query, params=None)` - Execute SQL query
- `fetch_one(query, params=None)` - Fetch single row
- `fetch_all(query, params=None)` - Fetch all rows
- `create_table(table_name, columns)` - Create table
- `insert(table_name, data)` - Insert row
- `update(table_name, data, where, where_params)` - Update rows
- `delete(table_name, where, where_params)` - Delete rows

### DataProcessor

Data processing with parallel execution.

#### Methods

- `__init__(max_workers=4)` - Initialize with worker count
- `process_batch(items, process_func)` - Process items in parallel
- `filter_data(data, conditions)` - Filter data by conditions
- `transform_data(data, transformations)` - Transform data fields
- `aggregate_data(data, group_by, aggregations)` - Aggregate data
- `export_to_json(data, filepath)` - Export to JSON file
- `import_from_json(filepath)` - Import from JSON file

### EventEmitter

Event system for pub-sub pattern.

#### Methods

- `on(event, callback)` - Register listener
- `off(event, callback)` - Unregister listener
- `emit(event, *args, **kwargs)` - Emit event
- `once(event, callback)` - Register one-time listener
- `remove_all_listeners(event=None)` - Remove all listeners
- `listener_count(event)` - Get listener count
- `event_names()` - Get list of event names

### Scheduler

Task scheduler for periodic and scheduled tasks.

#### Methods

- `add_task(name, func, interval=None, at_time=None, args=(), kwargs=None)` - Add task
- `remove_task(name)` - Remove task
- `enable_task(name)` - Enable task
- `disable_task(name)` - Disable task
- `start()` - Start scheduler
- `stop()` - Stop scheduler
- `get_tasks()` - Get task information

## Utility Modules

### Logger

Logging system with file and console output.

#### Methods

- `__init__(name="GRUB", level="INFO", log_file=None)` - Initialize logger
- `debug(message)` - Log debug message
- `info(message)` - Log info message
- `warning(message)` - Log warning message
- `error(message)` - Log error message
- `critical(message)` - Log critical message
- `exception(message)` - Log exception with traceback

#### Functions

- `get_logger(name="GRUB", level="INFO", log_file=None)` - Get logger instance

### Cache

In-memory cache with TTL support.

#### Methods

- `__init__(default_ttl=300)` - Initialize with default TTL
- `get(key)` - Get cached value
- `set(key, value, ttl=None)` - Set cached value
- `delete(key)` - Delete cached value
- `clear()` - Clear all cache
- `cleanup_expired()` - Remove expired entries
- `size()` - Get cache size
- `keys()` - Get all keys
- `has(key)` - Check if key exists

#### Functions

- `get_cache(default_ttl=300)` - Get cache instance

### FileOperations

File operation utilities.

#### Methods

- `read_file(filepath, encoding='utf-8')` - Read file
- `write_file(filepath, content, encoding='utf-8')` - Write file
- `read_json(filepath)` - Read JSON file
- `write_json(filepath, data, indent=2)` - Write JSON file
- `copy_file(src, dst)` - Copy file
- `move_file(src, dst)` - Move file
- `delete_file(filepath)` - Delete file
- `file_exists(filepath)` - Check if file exists
- `dir_exists(dirpath)` - Check if directory exists
- `create_directory(dirpath)` - Create directory
- `list_files(directory, pattern=None)` - List files
- `get_file_size(filepath)` - Get file size
- `get_file_extension(filepath)` - Get file extension

### Validator

Data validation utilities.

#### Methods

- `is_email(value)` - Validate email
- `is_url(value)` - Validate URL
- `is_phone(value)` - Validate phone number
- `is_alphanumeric(value)` - Check if alphanumeric
- `is_numeric(value)` - Check if numeric
- `is_in_range(value, min_val, max_val)` - Check range
- `min_length(value, length)` - Check minimum length
- `max_length(value, length)` - Check maximum length
- `is_required(value)` - Check if required
- `matches_pattern(value, pattern)` - Check regex pattern
- `is_in_list(value, allowed_values)` - Check if in list
- `validate_dict(data, rules)` - Validate dictionary

### APIClient

HTTP API client with built-in retries and a circuit breaker.

#### Methods

- `__init__(base_url, timeout=30, headers=None, max_retries=2, backoff_factor=0.5, jitter=0.1, circuit_breaker_threshold=5, circuit_breaker_reset=30)` - Initialize client with resilience controls
- `get(endpoint, headers=None)` - Make GET request
- `post(endpoint, data=None, headers=None)` - Make POST request
- `put(endpoint, data=None, headers=None)` - Make PUT request
- `delete(endpoint, headers=None)` - Make DELETE request
- `set_auth_token(token, token_type="Bearer")` - Set auth token
- `get_resilience_state()` - Inspect retry/circuit-breaker state for observability

### Helper Functions

Utility helper functions.

#### Functions

- `get_timestamp()` - Get current timestamp
- `calculate_hash(data, algorithm="sha256")` - Calculate hash
- `retry(max_attempts=3, delay=1.0)` - Retry decorator
- `chunk_list(items, chunk_size)` - Split list into chunks
- `sanitize_filename(filename)` - Sanitize filename
- `format_size(size_bytes)` - Format byte size

## CLI Interface

### Commands

- `start [--workers N] [--config FILE] [--debug] [--log-file FILE]` - Start application
- `status` - Show application status
- `config show` - Show all configuration
- `config get KEY` - Get configuration value
- `config set KEY VALUE` - Set configuration value

### Options

- `-v, --version` - Show version
- `-c, --config FILE` - Configuration file path
- `-d, --debug` - Enable debug mode
- `-l, --log-file FILE` - Log file path

## Examples

See the `examples/` directory for code examples demonstrating each module's usage.
