# Development Setup Guide

This guide provides detailed instructions for setting up the DecentraLearn development environment.

## Prerequisites

### System Requirements

1. **Operating System**
   - Linux (recommended)
   - macOS
   - Windows (with WSL2)

2. **Software**
   - Python 3.8 or higher
   - Git
   - Virtual environment tool (venv or conda)
   - Ethereum node (Ganache or local node)
   - Docker (optional)

3. **Hardware**
   - 8GB RAM minimum
   - 20GB free disk space
   - GPU (optional, for model training)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/decentralearn.git
cd decentralearn
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Using conda
conda create -n decentralearn python=3.8
conda activate decentralearn
```

### 3. Install Dependencies

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install testing dependencies
pip install -e ".[test]"

# Install documentation dependencies
pip install -e ".[docs]"
```

### 4. Configure Development Tools

1. **Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

2. **IDE Configuration**
   - VS Code: Install Python extension
   - PyCharm: Configure Python interpreter
   - Set up linting and formatting

### 5. Setup Blockchain Environment

1. **Local Development**
   ```bash
   # Start Ganache
   ganache-cli

   # Deploy contracts
   python scripts/deploy_contracts.py
   ```

2. **Test Network**
   ```bash
   # Configure test network
   export WEB3_PROVIDER_URI="https://ropsten.infura.io/v3/YOUR-PROJECT-ID"
   ```

## Development Tools

### Code Quality Tools

1. **Black (Code Formatter)**
   ```bash
   # Format code
   black decentralearn tests

   # Check formatting
   black --check decentralearn tests
   ```

2. **Pylint (Linter)**
   ```bash
   # Run linter
   pylint decentralearn tests

   # Generate report
   pylint --output-format=html decentralearn > pylint.html
   ```

3. **Mypy (Type Checker)**
   ```bash
   # Check types
   mypy decentralearn tests

   # Generate report
   mypy --html-report mypy-report decentralearn
   ```

### Documentation Tools

1. **Sphinx**
   ```bash
   # Build documentation
   cd docs
   make html

   # Serve documentation
   python -m http.server -d _build/html
   ```

2. **Docstring Checker**
   ```bash
   # Check docstrings
   pydocstyle decentralearn tests
   ```

### Testing Tools

1. **pytest**
   ```bash
   # Run tests
   pytest

   # Run with coverage
   pytest --cov=decentralearn

   # Run specific tests
   pytest tests/blockchain/test_client.py
   ```

2. **tox**
   ```bash
   # Run all environments
   tox

   # Run specific environment
   tox -e py38
   ```

## Project Structure

```
decentralearn/
├── decentralearn/           # Main package
│   ├── blockchain/         # Blockchain integration
│   ├── models/            # Machine learning models
│   ├── privacy/           # Privacy mechanisms
│   └── utils/             # Utility functions
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/              # Example scripts
└── scripts/               # Development scripts
```

## Common Development Tasks

### Creating New Features

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement Changes**
   ```python
   # Add new functionality
   def new_feature():
       pass
   ```

3. **Add Tests**
   ```python
   def test_new_feature():
       assert new_feature() == expected_result
   ```

4. **Update Documentation**
   ```markdown
   # New Feature
   Description of new feature...
   ```

### Updating Documentation

1. **Update Docstrings**
   ```python
   def function():
       """Updated documentation."""
       pass
   ```

2. **Update Markdown Files**
   ```bash
   # Build documentation
   cd docs
   make html
   ```

### Running Tests

1. **Unit Tests**
   ```bash
   pytest tests/unit/
   ```

2. **Integration Tests**
   ```bash
   pytest tests/integration/
   ```

3. **All Tests**
   ```bash
   pytest
   ```

## Troubleshooting

### Common Issues

1. **Dependency Conflicts**
   ```bash
   # Create fresh environment
   rm -rf venv
   python -m venv venv
   pip install -e ".[dev]"
   ```

2. **Blockchain Connection**
   ```bash
   # Check connection
   python scripts/check_connection.py

   # Reset blockchain
   python scripts/reset_blockchain.py
   ```

3. **Test Failures**
   ```bash
   # Run specific test
   pytest -v tests/specific_test.py

   # Debug test
   pytest --pdb tests/specific_test.py
   ```

### Debugging

1. **Python Debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

2. **Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## Best Practices

1. **Environment Management**
   - Use virtual environments
   - Pin dependency versions
   - Document environment setup
   - Keep environment clean

2. **Version Control**
   - Follow git workflow
   - Write meaningful commits
   - Use feature branches
   - Review changes

3. **Testing**
   - Write comprehensive tests
   - Maintain test coverage
   - Test edge cases
   - Document test requirements

4. **Documentation**
   - Keep docs up to date
   - Write clear docstrings
   - Include examples
   - Document changes

## See Also

- [Code Style Guide](code_style.md)
- [Testing Guide](testing.md)
- [Development Guide](../development/README.md)
- [API Documentation](../api/README.md) 