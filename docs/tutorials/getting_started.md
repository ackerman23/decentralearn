# Getting Started with DecentraLearn

This tutorial will guide you through setting up DecentraLearn and running your first federated learning experiment.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Node.js 16+ and npm
- Git
- PyTorch 2.7.0+
- torchvision 0.22.0+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/decentralearn.git
cd DecentraLearn
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install torch torchvision
```

4. Install and start Ganache (local Ethereum network):
```bash
npm install -g ganache
ganache --port 8545 --miner.blockTime 0
```

## Basic Setup

1. Initialize the blockchain client:
```python
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.config.blockchain_config import BlockchainConfig

# Configure blockchain client
config = BlockchainConfig(
    rpc_url="http://127.0.0.1:8545",
    chain_id=1337
)
client = BlockchainClient(config)
```

2. Register as a participant:
```python
client_id = client.register_client()
print(f"Registered with ID: {client_id}")
```

## Your First Federated Learning Experiment

Let's create a simple federated learning experiment using FashionMNIST.

1. Set up the dataset:
```python
from decentralearn.dataset import DatasetFactory, DatasetSpliter

# Initialize dataset components
factory = DatasetFactory()
splitter = DatasetSpliter()

# Get FashionMNIST dataset
dataset = factory.get_dataset('FashionMNIST', train=True)

# Create client list
client_list = {
    'client1': 'addr1',
    'client2': 'addr2',
    'client3': 'addr3'
}

# Split dataset among clients
dataloaders = splitter.random_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32
)
```

2. Define the model:
```python
import torch
import torch.nn as nn

class FashionMNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = nn.functional.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = nn.functional.relu(x)
        x = self.fc2(x)
        return nn.functional.log_softmax(x, dim=1)
```

3. Train and upload the model:
```python
from decentralearn.models.base import BaseModel

# Initialize model and optimizer
model = FashionMNISTModel()
optimizer = torch.optim.Adam(model.parameters())

# Training loop
for epoch in range(2):
    model.train()
    for client_id, dataloader in dataloaders.items():
        for batch_idx, (data, target) in enumerate(dataloader):
            optimizer.zero_grad()
            output = model(data)
            loss = nn.functional.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            
            if batch_idx % 100 == 0:
                print(f'Client {client_id} - Epoch: {epoch} [{batch_idx * len(data)}/{len(dataloader.dataset)}]')

        # Upload model after each epoch
        DecentraLearn_model = BaseModel()
        DecentraLearn_model.set_state_dict(model.state_dict())
        DecentraLearn_model.set_metadata({
            'id': f'fashion_mnist_epoch_{epoch}',
            'name': 'FashionMNIST CNN',
            'version': '1.0.0',
            'accuracy': 0.85  # Add your actual accuracy
        })
        
        success = client.upload_model(DecentraLearn_model)
        print(f"Client {client_id} - Epoch {epoch} model upload: {'Success' if success else 'Failed'}")
```

## Next Steps

1. **Custom Datasets**: Learn how to create and use custom datasets
   - [Custom Dataset Tutorial](custom_dataset.md)

2. **Non-IID Data**: Explore non-IID data distribution
   - [Non-IID Distribution Tutorial](non_iid_distribution.md)

3. **Advanced Features**: Learn about advanced features
   - [Advanced Features Tutorial](advanced_features.md)

## Troubleshooting

Common issues and solutions:

1. **Ganache Connection Issues**:
   - Ensure Ganache is running on port 8545
   - Check if the RPC URL is correct
   - Verify network ID matches chain_id

2. **Dataset Loading Issues**:
   - Check if dataset files are downloaded
   - Verify dataset paths are correct
   - Ensure proper permissions

3. **Model Upload Issues**:
   - Check gas settings
   - Verify client registration
   - Ensure model serialization works

## Additional Resources

- [API Reference](../api/README.md)
- [Architecture Overview](../architecture/overview.md)
- [Examples](../examples/README.md) 