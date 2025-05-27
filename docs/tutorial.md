# DecentraLearn Tutorial

This tutorial will guide you through setting up and running the DecentraLearn framework step by step.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Setting Up the Development Environment](#setting-up-the-development-environment)
4. [Running the Local Blockchain](#running-the-local-blockchain)
5. [Basic Usage Example](#basic-usage-example)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have the following installed:

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Node.js 16+ and npm**
   ```bash
   node --version
   npm --version
   ```

3. **Git**
   ```bash
   git --version
   ```

4. **PyTorch 2.7.0+ and torchvision 0.22.0+**
   ```bash
   python -c "import torch; print(torch.__version__)"
   python -c "import torchvision; print(torchvision.__version__)"
   ```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/decentralearn.git
   cd decentralearn
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   pip install torch torchvision

   # Install Ganache (local Ethereum network)
   npm install -g ganache
   ```

## Setting Up the Development Environment

1. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```bash
   # Blockchain Configuration
   RPC_URL=http://127.0.0.1:8545
   CHAIN_ID=1337
   GAS_LIMIT=3000000
   GAS_PRICE=20000000000

   # Project Configuration
   LOG_LEVEL=INFO
   DATA_DIR=./data
   ```

2. **Create Required Directories**
   ```bash
   mkdir -p data/models
   mkdir -p data/datasets
   mkdir -p logs
   ```

## Running the Local Blockchain

1. **Start Ganache**
   ```bash
   ganache --port 8545 --miner.blockTime 0
   ```
   Keep this terminal window open.

2. **Verify Ganache is Running**
   Open a new terminal and run:
   ```bash
   curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' http://127.0.0.1:8545
   ```
   You should see a response with the current block number.

## Basic Usage Example

1. **Initialize the Project**
   Create a new Python script `main.py`:
   ```python
   from decentralearn.blockchain.client import BlockchainClient
   from decentralearn.config.blockchain_config import BlockchainConfig
   from decentralearn.models.base import BaseModel
   from decentralearn.dataset import DatasetFactory
   import torch

   # Configure blockchain client
   config = BlockchainConfig(
       rpc_url="http://127.0.0.1:8545",
       chain_id=1337
   )
   client = BlockchainClient(config)

   # Register as a participant
   client_id = client.register_client()
   print(f"Registered with ID: {client_id}")
   ```

2. **Run the Script**
   ```bash
   python main.py
   ```

## Advanced Usage

### 1. Training with MNIST Dataset

Create a new script `train_mnist.py`:
```python
import torch
import torch.nn as nn
from decentralearn.dataset import DatasetFactory, DatasetSpliter
from decentralearn.models.base import BaseModel
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.config.blockchain_config import BlockchainConfig

# Initialize components
config = BlockchainConfig(
    rpc_url="http://127.0.0.1:8545",
    chain_id=1337
)
client = BlockchainClient(config)
factory = DatasetFactory()
splitter = DatasetSpliter()

# Get dataset
train_dataset = factory.get_dataset('FashionMNIST', train=True)

# Define model
class MNISTModel(nn.Module):
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

# Initialize model and optimizer
model = MNISTModel()
optimizer = torch.optim.Adam(model.parameters())

# Split dataset among clients
client_list = {
    'client1': 'addr1',
    'client2': 'addr2',
    'client3': 'addr3'
}
dataloaders = splitter.random_split(train_dataset, client_list, batch_size=64)

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

        # Upload to blockchain after each epoch
        decentralearn_model = BaseModel()
        decentralearn_model.set_state_dict(model.state_dict())
        decentralearn_model.set_metadata({
            'id': f'mnist_model_epoch_{epoch}',
            'name': 'MNIST CNN',
            'version': '1.0.0',
            'accuracy': 0.85
        })
        
        success = client.upload_model(decentralearn_model)
        print(f"Client {client_id} - Epoch {epoch} model upload: {'Success' if success else 'Failed'}")
```

### 2. Using Custom Datasets

Create a new script `custom_dataset.py`:
```python
from torch.utils.data import Dataset
from decentralearn.dataset import DatasetFactory

# Create custom dataset
class MyDataset(Dataset):
    def __init__(self, train=True):
        self.data = torch.randn(1000, 3, 32, 32)
        self.targets = torch.randint(0, 10, (1000,))
        self.train = train
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

# Create dataset loader function
def get_my_dataset(train=True, **kwargs):
    return MyDataset(train=train)

# Register with factory
factory = DatasetFactory()
factory.add_custom_dataset('MyDataset', get_my_dataset)

# Use your dataset
my_dataset = factory.get_dataset('MyDataset', train=True)
```

## Troubleshooting

### Common Issues and Solutions

1. **Ganache Connection Issues**
   - Ensure Ganache is running on port 8545
   - Check if the RPC URL is correct
   - Verify network connectivity

2. **Python Package Installation Issues**
   - Ensure virtual environment is activated
   - Try upgrading pip: `pip install --upgrade pip`
   - Check Python version compatibility

3. **Dataset Loading Issues**
   - Verify dataset files are in the correct location
   - Check file permissions
   - Ensure sufficient disk space

4. **Model Upload Issues**
   - Check gas settings in blockchain config
   - Verify account has sufficient funds
   - Ensure model serialization is working correctly

### Getting Help

1. **Check Logs**
   ```bash
   cat logs/decentralearn.log
   ```

2. **Enable Debug Mode**
   Set `LOG_LEVEL=DEBUG` in `.env` file

3. **Contact Support**
   - Open an issue on GitHub
   - Join the community Discord
   - Email support@decentralearn.org

## Next Steps

1. **Explore Advanced Features**
   - Non-IID data splitting
   - Custom model architectures
   - Advanced privacy features

2. **Contribute to the Project**
   - Fork the repository
   - Create a feature branch
   - Submit a pull request

3. **Join the Community**
   - Participate in discussions
   - Share your use cases
   - Help improve documentation 