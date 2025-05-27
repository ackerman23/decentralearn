# Code Style Guide

This guide outlines the coding standards and best practices for DecentraLearn development.

## Python Style Guide

### General Rules

1. **PEP 8 Compliance**
   - Follow PEP 8 style guide
   - Use 4 spaces for indentation
   - Maximum line length of 88 characters
   - Use double quotes for strings

2. **Naming Conventions**
   ```python
   # Classes: PascalCase
   class BlockchainClient:
       pass

   # Functions and variables: snake_case
   def register_client():
       client_address = "0x123..."

   # Constants: UPPER_CASE
   MAX_CLIENTS = 100
   ```

3. **Imports**
   ```python
   # Standard library imports
   import os
   import sys

   # Third-party imports
   import torch
   import web3

   # Local imports
   from decentralearn.blockchain import client
   from decentralearn.models import base
   ```

### Documentation

1. **Docstrings**
   ```python
   def register_client(client_id: str) -> str:
       """Register a new client on the blockchain.

       Args:
           client_id: Unique identifier for the client.

       Returns:
           str: Blockchain address of the registered client.

       Raises:
           BlockchainError: If registration fails.
       """
   ```

2. **Type Hints**
   ```python
   from typing import List, Dict, Optional

   def get_model(model_id: str) -> Optional[BaseModel]:
       """Get model from blockchain."""
   ```

3. **Comments**
   ```python
   # Use comments sparingly and only when necessary
   # Explain why, not what
   ```

### Code Organization

1. **Class Structure**
   ```python
   class BlockchainClient:
       """Client for blockchain interactions."""

       def __init__(self, config: BlockchainConfig):
           """Initialize client."""
           self.config = config
           self._setup()

       def _setup(self):
           """Setup internal state."""
           pass

       def public_method(self):
           """Public interface."""
           pass
   ```

2. **Function Design**
   ```python
   def process_data(
       data: List[float],
       threshold: float = 0.5,
       normalize: bool = True
   ) -> Dict[str, float]:
       """Process data with optional normalization."""
   ```

## Testing Style

1. **Test Naming**
   ```python
   def test_client_registration():
       """Test client registration process."""

   def test_model_verification_with_privacy():
       """Test model verification with privacy mechanisms."""
   ```

2. **Test Organization**
   ```python
   class TestBlockchainClient:
       """Test suite for blockchain client."""

       def setup_method(self):
           """Setup test environment."""
           self.client = BlockchainClient()

       def test_connection(self):
           """Test blockchain connection."""
   ```

## Error Handling

1. **Exception Handling**
   ```python
   try:
       client.upload_model(model)
   except BlockchainError as e:
       logger.error(f"Failed to upload model: {e}")
       raise
   ```

2. **Custom Exceptions**
   ```python
   class BlockchainError(Exception):
       """Base exception for blockchain operations."""

   class ConnectionError(BlockchainError):
       """Failed to connect to blockchain."""
   ```

## Security Guidelines

1. **Input Validation**
   ```python
   def validate_address(address: str) -> bool:
       """Validate blockchain address."""
       if not address.startswith("0x"):
           raise ValueError("Invalid address format")
   ```

2. **Secure Defaults**
   ```python
   class SecurityConfig:
       def __init__(self, encryption: str = "AES-256"):
           """Initialize with secure defaults."""
   ```

## Best Practices

1. **Code Quality**
   - Write clean, readable code
   - Use meaningful variable names
   - Keep functions focused
   - Document complex logic

2. **Performance**
   - Optimize critical paths
   - Use appropriate data structures
   - Minimize memory usage
   - Profile code regularly

3. **Maintainability**
   - Follow DRY principle
   - Write modular code
   - Use design patterns
   - Keep dependencies minimal

4. **Testing**
   - Write comprehensive tests
   - Test edge cases
   - Maintain test coverage
   - Use fixtures effectively

## Tools and Configuration

1. **Black Configuration**
   ```toml
   [tool.black]
   line-length = 88
   target-version = ['py38']
   include = '\.pyi?$'
   ```

2. **Pylint Configuration**
   ```ini
   [MASTER]
   disable = C0111
   max-line-length = 88

   [FORMAT]
   max-line-length = 88
   ```

3. **Mypy Configuration**
   ```ini
   [mypy]
   python_version = 3.8
   warn_return_any = True
   warn_unused_configs = True
   ```

## See Also

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Testing Guide](testing.md)
- [Development Setup](setup.md) 