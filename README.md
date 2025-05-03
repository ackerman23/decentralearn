# VeryFL: Federated Learning with Blockchain Integration

VeryFL is a federated learning framework that integrates with blockchain technology to provide secure and transparent model updates. The framework uses smart contracts to manage client registration, model updates, and model ownership verification.

## Features

- Federated learning with blockchain-based model update verification
- Smart contract-based client registration and management
- Model registry for tracking model ownership and metadata
- Secure model state dict serialization and deserialization
- Integration with local Ethereum node (e.g., Ganache)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/veryfl.git
cd veryfl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start a local Ethereum node (e.g., Ganache) on port 8545.

## Usage

### Blockchain Integration

1. Initialize the Web3 connection:
```python
from web3 import Web3
from chainfl import chain_proxy

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum node")
```

2. Register a new client:
```python
client_id = chain_proxy.client_regist()
print(f"Registered client with ID: {client_id}")
```

3. Upload model parameters:
```python
model_params = {
    'state_dict': model.state_dict(),
    'epoch': current_epoch,
    'accuracy': validation_accuracy
}
chain_proxy.upload_model(model_params)
```

4. Download model parameters:
```python
downloaded_params = chain_proxy.download_model()
model.load_state_dict(downloaded_params['state_dict'])
```

### Smart Contracts

1. Deploy the FLContract:
```python
from chainfl.contracts import FLContract

# Deploy contract
contract = w3.eth.contract(abi=fl_contract_abi, bytecode=fl_contract_bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
fl_contract = FLContract(w3, tx_receipt.contractAddress)
```

2. Register a client:
```python
client_address = w3.eth.accounts[1]
success = fl_contract.register_client(client_address)
if success:
    print(f"Successfully registered client: {client_address}")
```

3. Submit a model update:
```python
model_hash = "QmHash123..."  # IPFS hash or other identifier
success = fl_contract.submit_model(client_address, model_hash)
if success:
    print("Successfully submitted model update")
```

4. Verify model ownership:
```python
is_valid = fl_contract.verify_model(client_address, model_hash)
print(f"Model verification result: {is_valid}")
```

### Model Registry

1. Deploy the ModelRegistry contract:
```python
from chainfl.contracts import ModelRegistry

# Deploy contract
contract = w3.eth.contract(abi=registry_abi, bytecode=registry_bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
registry = ModelRegistry(w3, tx_receipt.contractAddress)
```

2. Register a model:
```python
model_metadata = {
    'name': 'MyModel',
    'description': 'A federated learning model',
    'version': '1.0.0',
    'tags': ['federated', 'classification']
}
success = registry.register_model('model123', model_metadata)
if success:
    print("Successfully registered model")
```

3. Get model metadata:
```python
metadata = registry.get_model_metadata('model123')
print(f"Model metadata: {metadata}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.