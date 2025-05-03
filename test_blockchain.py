import torch
from web3 import Web3
from chainfl import chain_proxy
from chainfl.contracts import FLContract, ModelRegistry

def test_blockchain_integration():
    print("Testing VeryFL blockchain integration...")
    
    # 1. Test Web3 connection
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    assert w3.is_connected(), "Failed to connect to Ethereum node"
    print("✓ Connected to Ethereum node")
    
    # 2. Test client registration
    client_id = chain_proxy.client_regist()
    print(f"✓ Registered client with ID: {client_id}")
    
    # 3. Test model upload/download
    # Create a simple model state dict
    model_state = {
        'layer1.weight': torch.randn(10, 5),
        'layer1.bias': torch.randn(10),
        'layer2.weight': torch.randn(5, 10),
        'layer2.bias': torch.randn(5)
    }
    
    model_params = {
        'state_dict': model_state,
        'epoch': 1,
        'accuracy': 0.85
    }
    
    # Upload model
    chain_proxy.upload_model(model_params)
    print("✓ Uploaded model parameters")
    
    # Download model
    downloaded_params = chain_proxy.download_model()
    print("✓ Downloaded model parameters")
    
    # Verify state dict keys match
    assert set(downloaded_params['state_dict'].keys()) == set(model_state.keys()), "Model state dict keys don't match"
    print("✓ Model state dict verified")
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_blockchain_integration() 