# Contributing Guide

This guide provides comprehensive information for contributing to DecentraLearn.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Process](#development-process)
3. [Code Style](#code-style)
4. [Documentation](#documentation)
5. [Pull Requests](#pull-requests)
6. [Review Process](#review-process)
7. [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Development environment setup
- Understanding of federated learning
- Basic knowledge of blockchain

### First Steps

1. **Fork the Repository**:
   - Go to [DecentraLearn GitHub](https://github.com/yourusername/DecentraLearn)
   - Click "Fork" button
   - Clone your fork locally

2. **Set Up Development Environment**:
   ```bash
   # Clone your fork
   git clone https://github.com/yourusername/decentralearn.git
   cd DecentraLearn

   # Add upstream remote
   git remote add upstream https://github.com/original-repo/decentralearn.git

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

### 1. Code Changes

1. **Follow Code Style**:
   - Use black for formatting
   - Follow PEP 8 guidelines
   - Use type hints
   - Write docstrings

2. **Write Tests**:
   - Add unit tests
   - Include integration tests
   - Maintain test coverage
   - Test edge cases

3. **Update Documentation**:
   - Update docstrings
   - Add examples
   - Update README if needed
   - Document breaking changes

### 2. Commit Changes

1. **Commit Message Format**:
   ```
   <type>(<scope>): <description>

   [optional body]

   [optional footer]
   ```

   Types:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation
   - style: Code style
   - refactor: Code refactoring
   - test: Testing
   - chore: Maintenance

2. **Example**:
   ```
   feat(dataset): add CIFAR100 support

   - Add CIFAR100 dataset loader
   - Update dataset factory
   - Add tests for CIFAR100

   Closes #123
   ```

### 3. Keep Branch Updated

```bash
# Fetch upstream changes
git fetch upstream

# Rebase your branch
git rebase upstream/main

# Resolve conflicts if any
git add .
git rebase --continue
```

## Code Style

### Python Code

1. **Formatting**:
   - Use black for formatting
   - Line length: 88 characters
   - Use 4 spaces for indentation
   - No trailing whitespace

2. **Imports**:
   ```python
   # Standard library
   import os
   import sys

   # Third-party
   import torch
   import numpy as np

   # Local
   from decentralearn.dataset import DatasetFactory
   ```

3. **Type Hints**:
   ```python
   def process_data(data: torch.Tensor, 
                   batch_size: int = 32) -> List[torch.Tensor]:
       """Process data in batches."""
       pass
   ```

4. **Docstrings**:
   ```python
   def split_dataset(dataset: Dataset, 
                    num_clients: int) -> List[Dataset]:
       """Split dataset among clients.
       
       Args:
           dataset: Dataset to split
           num_clients: Number of clients
           
       Returns:
           List of datasets for each client
       """
       pass
   ```

### Solidity Code

1. **Formatting**:
   - Use prettier-solidity
   - Follow Solidity style guide
   - Use 4 spaces for indentation

2. **Documentation**:
   ```solidity
   /// @title ModelRegistry
   /// @notice Registry for federated learning models
   contract ModelRegistry {
       /// @notice Submit a new model
       /// @param modelHash Hash of the model
       function submitModel(bytes32 modelHash) external {
           // ...
       }
   }
   ```

## Documentation

### Code Documentation

1. **Docstrings**:
   - Use Google style
   - Include type hints
   - Document exceptions
   - Provide examples

2. **Examples**:
   ```python
   def example_function():
       """Example function with usage.
       
       Examples:
           >>> result = example_function()
           >>> print(result)
           'Hello, World!'
       """
       return "Hello, World!"
   ```

### Project Documentation

1. **README Updates**:
   - Update features
   - Add examples
   - Update requirements
   - Document changes

2. **API Documentation**:
   - Document new endpoints
   - Update examples
   - Add type information
   - Include error cases

## Pull Requests

### Creating PR

1. **Title Format**:
   ```
   <type>(<scope>): <description>
   ```

2. **Description Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Changes
   - List of changes
   - Bullet points
   - Key modifications

   ## Testing
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Documentation

   ## Related Issues
   Closes #123
   ```

### PR Guidelines

1. **Requirements**:
   - All tests pass
   - Code coverage maintained
   - Documentation updated
   - No merge conflicts

2. **Review Process**:
   - Address comments
   - Update documentation
   - Fix issues
   - Rebase if needed

## Review Process

### Reviewer Guidelines

1. **Code Review**:
   - Check code style
   - Verify tests
   - Review documentation
   - Test functionality

2. **Feedback**:
   - Be constructive
   - Provide examples
   - Suggest improvements
   - Consider edge cases

### Author Guidelines

1. **Responding to Reviews**:
   - Address all comments
   - Explain decisions
   - Provide updates
   - Request clarification

2. **Updates**:
   - Push changes
   - Update documentation
   - Fix issues
   - Rebase if needed

## Release Process

### Versioning

1. **Semantic Versioning**:
   - MAJOR.MINOR.PATCH
   - MAJOR: Breaking changes
   - MINOR: New features
   - PATCH: Bug fixes

2. **Changelog**:
   - Document changes
   - Group by type
   - Include PR numbers
   - Update version

### Release Steps

1. **Preparation**:
   ```bash
   # Update version
   # Update changelog
   # Run tests
   # Build documentation
   ```

2. **Release**:
   ```bash
   # Create tag
   git tag v1.0.0
   git push origin v1.0.0

   # Create release
   # Upload package
   # Announce release
   ```

## Additional Resources

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html) 