# DecentraLearn Tutorial

This tutorial will guide you through installing and using DecentraLearn, a decentralized federated learning framework with privacy guarantees.

## Installation

You can install DecentraLearn using pip:

```bash
pip install decentralearn
```

For development or additional features, you can install with extras:

```bash
# For testing
pip install decentralearn[test]

# For development
pip install decentralearn[dev]

# For documentation
pip install decentralearn[docs]
```

### Note on Dependencies

If you encounter any dependency issues, particularly with `eth-tester`, you can resolve them by installing the beta version:

```bash
# Install eth-tester beta version first
pip install eth-tester==0.13.0b1

# Then install decentralearn
pip install decentralearn
```

Alternatively, you can install all dependencies manually:

```bash
pip install torch>=2.0.0 numpy>=1.21.0 scipy>=1.7.0 opacus>=1.1.0 phe>=1.5.0 web3>=6.0.0 eth-tester==0.13.0b1 eth-utils>=2.1.0
pip install decentralearn
```

## Basic Usage

### 1. Simple Federated Learning Setup

Here's a basic example of setting up a federated learning task:

```python
from decentralearn import FederatedLearning
from decentralearn.config import DataFlowConfig, PrivacyConfig, NetworkConfig

# Initialize configuration
config = DataFlowConfig(
    privacy=PrivacyConfig(epsilon=0.1),
    network=NetworkConfig(timeout=30)
)

# Create federated learning instance
fl = FederatedLearning(config)

# Add clients
fl.add_client("client1", dataset_path="path/to/dataset1")
fl.add_client("client2", dataset_path="path/to/dataset2")

# Start training
fl.train(epochs=10)
```

### 2. Privacy-Preserving Training

Example of setting up training with differential privacy:

```python
from decentralearn import FederatedLearning
from decentralearn.privacy import DifferentialPrivacy

# Initialize privacy mechanism
dp = DifferentialPrivacy(
    noise_multiplier=0.1,
    max_grad_norm=1.0
)

# Create federated learning with privacy
fl = FederatedLearning(
    privacy_mechanism=dp,
    privacy_budget=0.5
)

# Train with privacy guarantees
fl.train(epochs=5)
```

### 3. Blockchain Integration

Example of using DecentraLearn with blockchain:

```python
from decentralearn import FederatedLearning
from decentralearn.blockchain import BlockchainManager

# Initialize blockchain manager
blockchain = BlockchainManager(
    contract_address="0x...",
    network="ethereum"
)

# Create federated learning with blockchain
fl = FederatedLearning(
    blockchain_manager=blockchain,
    reward_token="DLT"
)

# Train and earn rewards
fl.train(epochs=3)
```

### 4. Custom Model Training

Example of using a custom model:

```python
import torch
import torch.nn as nn
from decentralearn import FederatedLearning

# Define custom model
class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(10, 20)
        self.layer2 = nn.Linear(20, 2)
    
    def forward(self, x):
        x = torch.relu(self.layer1(x))
        return self.layer2(x)

# Initialize federated learning with custom model
fl = FederatedLearning(
    model_class=CustomModel,
    model_params={}
)

# Train custom model
fl.train(epochs=5)
```

### 5. Advanced Privacy Features

Example of combining multiple privacy mechanisms:

```python
from decentralearn import FederatedLearning
from decentralearn.privacy import (
    DifferentialPrivacy,
    HomomorphicEncryption,
    ZeroKnowledgeProof
)

# Initialize privacy mechanisms
dp = DifferentialPrivacy(noise_multiplier=0.1)
he = HomomorphicEncryption(key_size=2048)
zkp = ZeroKnowledgeProof()

# Create federated learning with multiple privacy layers
fl = FederatedLearning(
    privacy_mechanisms=[dp, he, zkp],
    privacy_budget=1.0
)

# Train with enhanced privacy
fl.train(epochs=3)
```

## Best Practices

1. **Privacy Budget Management**
   - Monitor your privacy budget during training
   - Adjust epsilon values based on your requirements
   - Use appropriate noise levels for your use case

2. **Data Distribution**
   - Ensure balanced data distribution among clients
   - Consider non-IID scenarios
   - Validate data quality before training

3. **Model Verification**
   - Verify model updates before aggregation
   - Check for malicious updates
   - Maintain model versioning

4. **Error Handling**
   - Implement proper error handling
   - Monitor training progress
   - Handle network failures gracefully

## Troubleshooting

Common issues and solutions:

1. **Installation Issues**
   ```bash
   # If you encounter dependency conflicts
   pip install --upgrade pip
   pip install decentralearn --no-deps
   pip install -r requirements.txt
   ```

2. **Privacy Budget Errors**
   - Increase privacy budget
   - Reduce number of training rounds
   - Adjust noise parameters

3. **Blockchain Connection Issues**
   - Check network connectivity
   - Verify contract address
   - Ensure sufficient gas fees

## Additional Resources

- [Documentation](https://decentralearn.readthedocs.io/)
- [API Reference](https://decentralearn.readthedocs.io/api.html)
- [GitHub Repository](https://github.com/decentralearn/decentralearn)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details. 