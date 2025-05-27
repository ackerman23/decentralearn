"""
Smart contract interfaces for DecentraLearn
This module provides the core smart contract interfaces used in DecentraLearn,
including the FL contract for federated learning operations and the Model Registry
for model management and verification.
"""
from web3 import Web3
from eth_typing import Address
from typing import Dict, List, Tuple, Any
import json
import os

class FLContract:
    def __init__(self, w3: Web3, contract_address: Address):
        self.w3 = w3
        self.contract_address = contract_address
        
        # Load contract ABI
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abi_path = os.path.join(current_dir, 'FLContract.json')
        with open(abi_path) as f:
            contract_abi = json.load(f)['abi']
        
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    def register_client(self, client_address: Address) -> bool:
        """Register a new client in the federated learning system"""
        tx_hash = self.contract.functions.registerClient(client_address).transact()
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    
    def submit_model(self, client_address: Address, model_hash: str) -> bool:
        """Submit a model update from a client"""
        tx_hash = self.contract.functions.submitModel(model_hash).transact({'from': client_address})
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    
    def get_model_hash(self, client_address: Address) -> str:
        """Get the latest model hash submitted by a client"""
        return self.contract.functions.getModelHash(client_address).call()
    
    def get_registered_clients(self) -> List[Address]:
        """Get list of all registered clients"""
        return self.contract.functions.getRegisteredClients().call()
    
    def verify_model(self, client_address: Address, model_hash: str) -> bool:
        """Verify if a model hash matches the one stored on-chain"""
        return self.contract.functions.verifyModel(client_address, model_hash).call()

class ModelRegistry:
    def __init__(self, w3: Web3, contract_address: Address):
        self.w3 = w3
        self.contract_address = contract_address
        
        # Load contract ABI
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abi_path = os.path.join(current_dir, 'ModelRegistry.json')
        with open(abi_path) as f:
            contract_abi = json.load(f)['abi']
        
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    def register_model(self, model_id: str, model_metadata: Dict[str, Any]) -> bool:
        """Register a new model in the registry"""
        tx_hash = self.contract.functions.registerModel(
            model_id,
            model_metadata['name'],
            model_metadata['description'],
            model_metadata['version'],
            model_metadata['tags']
        ).transact()
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    
    def update_model(self, model_id: str, model_metadata: Dict[str, Any]) -> bool:
        """Update an existing model in the registry"""
        tx_hash = self.contract.functions.updateModel(
            model_id,
            model_metadata['name'],
            model_metadata['description'],
            model_metadata['version'],
            model_metadata['tags']
        ).transact()
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    
    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        """Get metadata for a registered model"""
        result = self.contract.functions.getModelMetadata(model_id).call()
        return {
            'name': result[0],
            'description': result[1],
            'version': result[2],
            'owner': result[3],
            'timestamp': result[4],
            'tags': result[5]
        }
    
    def verify_model_ownership(self, model_id: str, owner_address: Address) -> bool:
        """Verify if an address owns a registered model"""
        return self.contract.functions.verifyModelOwnership(model_id, owner_address).call()
    
    def get_owner_models(self, owner_address: Address) -> List[str]:
        """Get list of models owned by an address"""
        return self.contract.functions.getOwnerModels(owner_address).call() 