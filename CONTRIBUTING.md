# Contributing to GRUB

Thank you for your interest in contributing to GRUB! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions with other contributors.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/grub.git
   cd grub
   ```
3. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Install Development Dependencies

```bash
pip install -r requirements.txt
```

For development tools (optional):
```bash
pip install pytest black flake8 mypy
```

## Making Changes

### Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Documentation

- Update documentation for any changed functionality
- Add docstrings following Google style format:
  ```python
  def function(arg1: str, arg2: int) -> bool:
      """Brief description of function

      Args:
          arg1: Description of arg1
          arg2: Description of arg2

      Returns:
          Description of return value
      """
  ```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting:
  ```bash
  python -m unittest discover src/tests
  ```
- Aim for high test coverage

### Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed after blank line
- Reference issues when applicable

Example:
```
Add cache invalidation feature

Implement cache invalidation by key pattern to allow
selective clearing of cached data. Addresses issue #123.
```

## Submitting Changes

1. Ensure all tests pass
2. Update documentation if needed
3. Commit your changes:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a Pull Request

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Changes are focused and coherent

### PR Description

Include in your PR description:

1. **Summary**: Brief description of changes
2. **Motivation**: Why are these changes needed?
3. **Changes**: List of specific changes made
4. **Testing**: How were changes tested?
5. **Screenshots**: If UI changes (if applicable)

Example:
```markdown
## Summary
Add support for custom cache TTL per key

## Motivation
Users need ability to set different TTL values for different cache keys

## Changes
- Modified Cache.set() to accept optional TTL parameter
- Updated tests to cover new functionality
- Added documentation for new parameter

## Testing
- Added unit tests for custom TTL
- Verified backward compatibility with existing code
```

## Types of Contributions

### Bug Fixes

- Create an issue describing the bug
- Reference the issue in your PR
- Include test that reproduces the bug

### New Features

- Discuss feature in an issue first
- Ensure feature aligns with project goals
- Include comprehensive tests
- Update documentation

### Documentation

- Fix typos, clarify explanations
- Add examples
- Improve API documentation

### Tests

- Add missing test coverage
- Improve existing tests
- Add integration tests

## Project Structure

```
grub/
├── src/
│   ├── core/           # Core application modules
│   ├── utils/          # Utility modules
│   ├── cli/            # Command-line interface
│   └── tests/          # Test suite
├── config/             # Configuration files
├── docs/               # Documentation
├── examples/           # Usage examples
└── README.md
```

## Running Tests

### All Tests
```bash
python -m unittest discover src/tests
```

### Specific Test File
```bash
python -m unittest src.tests.test_config
```

### With Coverage (if installed)
```bash
coverage run -m unittest discover src/tests
coverage report
```

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Getting Help

- Check existing documentation
- Search existing issues
- Create a new issue for questions
- Join community discussions

## Recognition

Contributors will be recognized in:
- Release notes
- Contributors list
- Project documentation

Thank you for contributing to GRUB!
