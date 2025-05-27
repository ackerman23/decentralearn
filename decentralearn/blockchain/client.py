"""
Blockchain client for DecentraLearn - Because who doesn't love a good blockchain?

This module is where the magic happens - connecting our fancy ML models to the blockchain.
Think of it as the bridge between your AI dreams and the immutable ledger of truth.
"""
import logging
from typing import Optional, List, Dict, Any
from web3 import Web3
from eth_account import Account
from eth_typing import Address
from decentralearn.config.blockchain_config import BlockchainConfig, default_config
from decentralearn.contracts import FLContract, ModelRegistry
from decentralearn.models.base import BaseModel
import hashlib

logger = logging.getLogger(__name__)

class BlockchainClient:
    """The cool kid that knows how to talk to the blockchain
    
    This class is like your blockchain BFF - it handles all the messy details of
    talking to Ethereum while you focus on building awesome ML models.
    """
    
    def __init__(self, config: Optional[BlockchainConfig] = None):
        """Initialize the blockchain client
        
        Args:
            config: Because sometimes you want to customize things. We won't judge.
        """
        self.config = config or default_config
        self.w3 = Web3(Web3.HTTPProvider(self.config.rpc_url))
        
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node - Did you remember to feed the blockchain?")
        
        # Enable account creation - because who doesn't love creating new accounts?
        Account.enable_unaudited_hdwallet_features()
        
        self.accounts = []
        self.client_addresses = {}
        self.current_model: Optional[BaseModel] = None
        
        # Create server account - the boss of all accounts
        self.server_account = Account.create()
        self.accounts.append(self.server_account)
        
        logger.info("BlockchainClient initialized with server account: %s", 
                   self.server_account.address)
        
        # Initialize contracts if addresses are provided
        # Because sometimes you want to be fancy and use smart contracts
        self.fl_contract = None
        self.model_registry = None
        
        if self.config.fl_contract_address:
            self.fl_contract = FLContract(self.w3, self.config.fl_contract_address)
        
        if self.config.model_registry_address:
            self.model_registry = ModelRegistry(self.w3, self.config.model_registry_address)
    
    def create_account(self) -> Address:
        """Create a new Ethereum account
        
        Returns:
            Address: Your shiny new blockchain address. Use it wisely.
        """
        account = Account.create()
        self.accounts.append(account)
        return account.address
    
    def register_client(self) -> str:
        """Register a new client and return client ID
        
        Returns:
            str: Your VIP pass to the DecentraLearn party
        """
        client_id = str(len(self.client_addresses) + 1)
        if len(self.accounts) <= len(self.client_addresses) + 1:
            self.create_account()
        
        client_address = self.accounts[len(self.client_addresses) + 1].address
        self.client_addresses[client_id] = client_address
        
        if self.fl_contract:
            self.fl_contract.register_client(client_address)
        
        return client_id
    
    def get_client_address(self, client_id: str) -> Optional[Address]:
        """Get client's Ethereum address
        
        Args:
            client_id: The ID of the client you're stalking
        
        Returns:
            Optional[Address]: The address if found, None if they're hiding
        """
        return self.client_addresses.get(client_id)
    
    def upload_model(self, model: BaseModel) -> bool:
        """Upload model to blockchain
        
        Args:
            model: Your precious ML model that you want to immortalize on the blockchain
        
        Returns:
            bool: True if successful, False if the blockchain gods are angry
        """
        if not self.fl_contract:
            raise RuntimeError("FL contract not initialized - Did you forget to feed the blockchain?")
        
        model_json = model.to_json()
        model_hash = hashlib.sha256(model_json.encode()).hexdigest()
        self.current_model = model
        
        # Submit model hash to contract - because we love hashes
        success = self.fl_contract.submit_model(self.server_account.address, model_hash)
        
        # Register model in registry if available
        if success and self.model_registry:
            metadata = model.get_metadata()
            self.model_registry.register_model(
                model_id=metadata.get('id', 'default'),
                model_metadata=metadata
            )
        
        logger.info("Model uploaded successfully - Your model is now blockchain-famous!")
        return success
    
    def download_model(self) -> Optional[BaseModel]:
        """Download model from blockchain
        
        Returns:
            Optional[BaseModel]: The model if it exists, None if it's playing hard to get
        """
        if not self.current_model:
            raise RuntimeError("No model available - Did you forget to upload one?")
        
        return self.current_model
    
    def verify_model(self, client_address: Address, model: BaseModel) -> bool:
        """Verify model on blockchain
        
        Args:
            client_address: The address claiming to own the model
            model: The model to verify
        
        Returns:
            bool: True if the model is legit, False if it's an imposter
        """
        if not self.fl_contract:
            raise RuntimeError("FL contract not initialized - The blockchain is confused")
        
        model_json = model.to_json()
        model_hash = hashlib.sha256(model_json.encode()).hexdigest()
        
        return self.fl_contract.verify_model(
            client_address,
            model_hash
        )
    
    def get_registered_clients(self) -> List[Address]:
        """Get list of registered clients
        
        Returns:
            List[Address]: All the cool kids in the DecentraLearn club
        """
        if not self.fl_contract:
            raise RuntimeError("FL contract not initialized - The blockchain is lonely")
        
        return self.fl_contract.get_registered_clients()
    
    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        """Get model metadata from registry
        
        Args:
            model_id: The ID of the model you're curious about
        
        Returns:
            Dict[str, Any]: All the juicy details about the model
        """
        if not self.model_registry:
            raise RuntimeError("Model registry not initialized - The blockchain forgot where it put things")
        
        return self.model_registry.get_model_metadata(model_id) 