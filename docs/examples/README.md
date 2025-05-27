# Examples

This section provides practical examples of using DecentraLearn.

## Basic Examples

- [MNIST Classification](mnist_classification.md)
  - Model definition
  - Training process
  - Privacy integration
  - Blockchain verification

- [Custom Dataset](custom_dataset.md)
  - Dataset creation
  - Data loading
  - Privacy handling
  - Model training

- [Non-IID Distribution](non_iid_distribution.md)
  - Data distribution
  - Client assignment
  - Performance analysis
  - Privacy impact

## Advanced Examples

- Privacy Mechanisms
  - Differential Privacy
  - Homomorphic Encryption
  - Zero-Knowledge Proofs

- Blockchain Integration
  - Smart contracts
  - Model verification
  - Incentive mechanisms

- Security Features
  - Access control
  - Data protection
  - Audit logging

## Code Snippets

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

### Model Training

```python
from decentralearn.models.base import BaseModel
from decentralearn.privacy import DifferentialPrivacy

model = BaseModel()
dp = DifferentialPrivacy(epsilon=0.1)
# Train model with privacy
```

### Dataset Handling

```python
from decentralearn.datasets import DatasetFactory
from decentralearn.datasets import DatasetSpliter

factory = DatasetFactory()
spliter = DatasetSpliter()
```

## Best Practices

1. Study the examples thoroughly
2. Run the code yourself
3. Modify parameters
4. Test different scenarios
5. Monitor performance

## See Also

- [API Reference](../api/README.md)
- [Tutorials](../tutorials/README.md)
- [Development Guide](../development/README.md) 