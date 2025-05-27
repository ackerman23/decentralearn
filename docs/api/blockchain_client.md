# Blockchain Client API

The `BlockchainClient` class provides the interface for interacting with the blockchain network.

## Overview

```python
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.config.blockchain_config import BlockchainConfig

config = BlockchainConfig(
    rpc_url="http://localhost:8545",
    chain_id=1337
)
client = BlockchainClient(config)
```

## Class: BlockchainClient

### Constructor

```python
def __init__(self, config: BlockchainConfig)
```

Parameters:
- `config`: BlockchainConfig object containing connection settings

### Methods

#### Client Management

```python
def register_client(self) -> str:
    """Register a new client and return client ID"""
```

```python
def get_client_address(self, client_id: str) -> str:
    """Get blockchain address for client"""
```

```python
def create_account(self) -> str:
    """Create new blockchain account"""
```

#### Model Management

```python
def upload_model(self, model: BaseModel) -> bool:
    """Upload model to blockchain"""
```

```python
def verify_model(self, address: str, model_json: str) -> bool:
    """Verify model on blockchain"""
```

```python
def get_model(self, model_id: str) -> BaseModel:
    """Retrieve model from blockchain"""
```

#### Transaction Management

```python
def send_transaction(self, to: str, value: int) -> str:
    """Send blockchain transaction"""
```

```python
def get_transaction_receipt(self, tx_hash: str) -> dict:
    """Get transaction receipt"""
```

#### Contract Interaction

```python
def deploy_contract(self, contract_name: str) -> str:
    """Deploy smart contract"""
```

```python
def call_contract(self, contract_address: str, 
                 function_name: str, *args) -> Any:
    """Call smart contract function"""
```

### Properties

```python
@property
def accounts(self) -> List[Account]:
    """List of available accounts"""
```

```python
@property
def server_account(self) -> Account:
    """Server account for transactions"""
```

## Configuration

### BlockchainConfig

```python
class BlockchainConfig:
    def __init__(self,
                 rpc_url: str = "http://localhost:8545",
                 chain_id: int = 1337,
                 gas_limit: int = 6721975,
                 gas_price: int = 20000000000):
```

Parameters:
- `rpc_url`: Blockchain node RPC URL
- `chain_id`: Network chain ID
- `gas_limit`: Transaction gas limit
- `gas_price`: Gas price in wei

## Examples

### Basic Usage

```python
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.config.blockchain_config import BlockchainConfig

# Initialize client
config = BlockchainConfig(
    rpc_url="http://localhost:8545",
    chain_id=1337
)
client = BlockchainClient(config)

# Register client
client_id = client.register_client()

# Create account
address = client.create_account()

# Upload model
success = client.upload_model(model)
```

### Contract Interaction

```python
# Deploy contract
contract_address = client.deploy_contract("FederatedLearning")

# Call contract function
result = client.call_contract(
    contract_address,
    "registerModel",
    model_hash
)
```

### Transaction Management

```python
# Send transaction
tx_hash = client.send_transaction(
    to=recipient_address,
    value=web3.toWei(1, 'ether')
)

# Get receipt
receipt = client.get_transaction_receipt(tx_hash)
```

## Error Handling

The client implements comprehensive error handling:

```python
try:
    client.upload_model(model)
except BlockchainConnectionError:
    # Handle connection error
except TransactionError:
    # Handle transaction error
except ContractError:
    # Handle contract error
```

## Best Practices

1. Connection Management
   ```python
   # Always check connection
   if not client.is_connected():
       client.reconnect()
   ```

2. Gas Management
   ```python
   # Set appropriate gas limits
   config = BlockchainConfig(
       gas_limit=8000000,
       gas_price=20000000000
   )
   ```

3. Account Security
   ```python
   # Use secure account management
   client.use_encrypted_keystore(
       path="keystore",
       password=secure_password
   )
   ```

## See Also

- [Model Management](model_management.md)
- [Configuration](configuration.md)
- [Smart Contracts](../architecture/smart_contracts.md) 