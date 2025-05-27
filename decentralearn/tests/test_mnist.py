"""
Test DecentraLearn with MNIST dataset
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from web3 import Web3
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.models.base import BaseModel
from decentralearn.config.blockchain_config import BlockchainConfig

class MockFLContract:
    """Mock FL contract for testing"""
    def __init__(self, w3, address):
        print("\nInitializing Mock FL Contract...")
        self.w3 = w3
        self.address = address
        self.models = {}
        print(f"Mock contract initialized at address: {address}")
    
    def register_client(self, client_address):
        print(f"Registering client with address: {client_address}")
        return True
    
    def upload_model(self, client_address, model_hash):
        print(f"Uploading model from client {client_address}")
        self.models[client_address] = model_hash
        return True
    
    def verify_model(self, client_address, model_hash):
        print(f"Verifying model for client {client_address}")
        return model_hash in self.models.values()

class MNISTModel(nn.Module):
    """Simple CNN for MNIST classification"""
    def __init__(self):
        print("\nInitializing MNIST CNN model...")
        super(MNISTModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        print("MNIST CNN model initialized successfully")

    def forward(self, x):
        x = self.conv1(x)
        x = nn.ReLU()(x)
        x = self.conv2(x)
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2)(x)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = nn.ReLU()(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return nn.LogSoftmax(dim=1)(x)

def train(model, train_loader, optimizer, epoch):
    """Train the model for one epoch"""
    print(f"\nStarting training epoch {epoch}...")
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = nn.NLLLoss()(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} '
                  f'({100. * batch_idx / len(train_loader):.0f}%)]\tLoss: {loss.item():.6f}')
    print(f"Completed training epoch {epoch}")

def test(model, test_loader):
    """Test the model"""
    print("\nStarting model testing...")
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            test_loss += nn.NLLLoss()(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100. * correct / len(test_loader.dataset)
    print(f'\nTest set: Average loss: {test_loss:.4f}, '
          f'Accuracy: {correct}/{len(test_loader.dataset)} ({accuracy:.0f}%)\n')
    return accuracy

def main():
    print("\n=== Starting MNIST Test Suite ===")
    
    # Initialize Web3 connection
    print("\nInitializing Web3 connection...")
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
        raise Exception("Failed to connect to Ethereum node")
    print("Successfully connected to Ethereum node")
    
    # Deploy mock contract
    print("\nDeploying mock contract...")
    mock_contract = MockFLContract(w3, w3.eth.accounts[0])
    
    # Initialize blockchain client with mock contract
    print("\nInitializing blockchain client...")
    config = BlockchainConfig(
        rpc_url="http://127.0.0.1:8545",
        chain_id=1337,
        fl_contract_address=mock_contract.address
    )
    client = BlockchainClient(config)
    client.fl_contract = mock_contract  # Inject mock contract
    print("Blockchain client initialized successfully")
    
    # Register client
    print("\nRegistering client...")
    client_id = client.register_client()
    print(f"Registered client with ID: {client_id}")
    
    # Load MNIST dataset
    print("\nLoading MNIST dataset...")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Download training data
    print("Downloading training data...")
    train_dataset = datasets.MNIST('../data', train=True, download=True,
                                 transform=transform)
    print(f"Downloaded {len(train_dataset)} training samples")
    
    # Split into training and validation
    print("\nSplitting dataset...")
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = random_split(train_dataset, [train_size, val_size])
    print(f"Split into {train_size} training and {val_size} validation samples")
    
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    
    # Create and train model
    print("\nCreating and training model...")
    model = MNISTModel()
    optimizer = optim.Adam(model.parameters())
    
    # Train for 2 epochs
    for epoch in range(1, 3):
        train(model, train_loader, optimizer, epoch)
        accuracy = test(model, val_loader)
        
        # Create DecentraLearn model and set state
        print(f"\nCreating DecentraLearn model for epoch {epoch}...")
        DecentraLearn_model = BaseModel()
        DecentraLearn_model.set_state_dict(model.state_dict())
        DecentraLearn_model.set_metadata({
            'id': f'mnist_model_epoch_{epoch}',
            'name': 'MNIST CNN',
            'version': '1.0.0',
            'accuracy': accuracy
        })
        print(f"Model metadata: {DecentraLearn_model.get_metadata()}")
        
        # Upload model to blockchain
        print(f"\nUploading model for epoch {epoch}...")
        success = client.upload_model(DecentraLearn_model)
        if success:
            print(f"Successfully uploaded model for epoch {epoch}")
            
            # Verify model on blockchain
            print("Verifying model on blockchain...")
            is_verified = client.verify_model(client.server_account.address, DecentraLearn_model.to_json())
            print(f"Model verification result: {is_verified}")
        else:
            print(f"Failed to upload model for epoch {epoch}")
    
    print("\n=== MNIST Test Suite Completed ===")

if __name__ == "__main__":
    main() 