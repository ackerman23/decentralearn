# API Reference

This section provides detailed documentation for DecentraLearn's API components.

## Core Components

- [Blockchain Client](blockchain_client.md)
  - Client registration
  - Model management
  - Transaction handling
  - Contract interaction

- [Model Management](model_management.md)
  - Model serialization
  - State management
  - Version control
  - Verification

- [Dataset Management](dataset_management.md)
  - Dataset loading
  - Data splitting
  - Privacy handling
  - Custom datasets

- [Configuration](configuration.md)
  - Blockchain settings
  - Privacy parameters
  - Model configuration
  - Network settings

## Usage Examples

### Basic Setup

```python
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.config.blockchain_config import BlockchainConfig

config = BlockchainConfig(
    rpc_url="http://localhost:8545",
    chain_id=1337
)
client = BlockchainClient(config)
```

### Model Management

```python
from decentralearn.models.base import BaseModel
from decentralearn.privacy import DifferentialPrivacy

model = BaseModel()
dp = DifferentialPrivacy(epsilon=0.1)
```

### Dataset Handling

```python
from decentralearn.datasets import DatasetFactory
from decentralearn.datasets import DatasetSpliter

factory = DatasetFactory()
spliter = DatasetSpliter()
```

## Best Practices

1. Always initialize blockchain connection first
2. Use appropriate privacy mechanisms
3. Follow configuration guidelines
4. Implement proper error handling
5. Monitor privacy budgets

## See Also

- [Architecture Overview](../architecture/overview.md)
- [Tutorials](../tutorials/README.md)
- [Examples](../examples/README.md) 