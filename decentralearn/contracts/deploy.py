"""
Smart contract deployment utilities
"""
import json
import os
from typing import Any, Dict, Optional
from web3 import Web3
from web3.contract import Contract

def load_contract_data(contract_name: str) -> Dict[str, Any]:
    """Load contract data from build artifacts
    
    Args:
        contract_name: Name of the contract
        
    Returns:
        Contract data including ABI and bytecode
    """
    # Get contract artifact path
    artifact_path = os.path.join(
        os.path.dirname(__file__),
        'artifacts',
        f'{contract_name}.json'
    )
    print(f"Loading contract data from {artifact_path}")
    
    # Load contract data
    with open(artifact_path) as f:
        contract_data = json.load(f)
    
    # Ensure bytecode has 0x prefix
    if not contract_data['bytecode'].startswith('0x'):
        contract_data['bytecode'] = '0x' + contract_data['bytecode']
    
    print(f"Contract {contract_name} bytecode length: {len(contract_data['bytecode'])}")
    print(f"Contract {contract_name} ABI length: {len(contract_data['abi'])}")
    
    return contract_data

def deploy_contract(
    web3: Web3,
    contract_file: str,
    contract_name: str,
    deployer: str,
    args: Optional[list] = None
) -> Contract:
    """Deploy a smart contract
    
    Args:
        web3: Web3 instance
        contract_file: Solidity contract file name (without .sol extension)
        contract_name: Name of the contract to deploy
        deployer: Address deploying the contract
        args: Constructor arguments
        
    Returns:
        Deployed contract instance
    """
    print(f"\nDeploying {contract_name} contract...")
    print(f"Deployer address: {deployer}")
    print(f"Constructor args: {args}")
    
    # Load contract data
    contract_data = load_contract_data(contract_name)
    
    # Create contract object
    contract = web3.eth.contract(
        abi=contract_data['abi'],
        bytecode=contract_data['bytecode']
    )
    
    # Deploy contract
    if args is None:
        args = []
    
    # Get nonce
    nonce = web3.eth.get_transaction_count(deployer)
    print(f"Nonce: {nonce}")
    
    # Get gas price
    gas_price = web3.eth.gas_price
    print(f"Gas price: {gas_price}")
    
    # Get block gas limit
    block = web3.eth.get_block('latest')
    block_gas_limit = block['gasLimit']
    print(f"Block gas limit: {block_gas_limit}")
    
    # Estimate gas with a buffer
    try:
        estimated_gas = contract.constructor(*args).estimate_gas({'from': deployer})
        print(f"Estimated gas: {estimated_gas}")
        gas_limit = min(block_gas_limit, estimated_gas * 2)  # Double the estimate but don't exceed block limit
    except Exception as e:
        print(f"Gas estimation failed: {e}")
        gas_limit = 12000000  # Use a higher fixed gas limit as fallback
    
    print(f"Using gas limit: {gas_limit}")
    
    # Build transaction
    transaction = contract.constructor(*args).build_transaction({
        'from': deployer,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    
    print(f"Transaction: {transaction}")
    
    # Send transaction
    tx_hash = web3.eth.send_transaction(transaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    
    # Wait for transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")
    
    # Verify contract was deployed
    if tx_receipt.contractAddress is None:
        raise Exception(f"Contract {contract_name} deployment failed")
    
    print(f"Contract deployed at: {tx_receipt.contractAddress}")
    
    # Verify contract code was deployed
    code = web3.eth.get_code(tx_receipt.contractAddress)
    print(f"Contract code length: {len(code)}")
    
    if code == '0x' or code == b'0x' or code == b'':
        raise Exception(f"Contract {contract_name} has no code at {tx_receipt.contractAddress}")
    
    # Create contract instance
    contract_instance = web3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_data['abi']
    )
    
    return contract_instance 