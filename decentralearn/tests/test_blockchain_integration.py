"""
Integration tests for DecentraLearn blockchain functionality
This module contains comprehensive tests for blockchain integration features,
including smart contract interactions, model verification, and client management.
"""
import unittest
import torch
from web3 import Web3
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.models.base import BaseModel
from decentralearn.config.blockchain_config import BlockchainConfig

class TestBlockchainIntegration(unittest.TestCase):
    """Integration test cases for blockchain functionality"""
    
    def setUp(self):
        """Set up test environment"""
        print("\nSetting up test environment...")
        # Configure blockchain client with Ganache settings
        self.config = BlockchainConfig(
            rpc_url="http://127.0.0.1:8545",
            chain_id=1337,
            gas_limit=6721975,
            gas_price=20000000000  # 20 Gwei
        )
        print(f"Initialized blockchain config with RPC URL: {self.config.rpc_url}")
        
        self.client = BlockchainClient(self.config)
        print("Blockchain client initialized")
        
        # Create test model
        self.model = BaseModel()
        self.model.set_state_dict({
            'layer1.weight': torch.randn(10, 5),
            'layer1.bias': torch.randn(10),
            'layer2.weight': torch.randn(5, 10),
            'layer2.bias': torch.randn(5)
        })
        self.model.set_metadata({
            'id': 'test_model',
            'name': 'Test Model',
            'version': '1.0.0',
            'accuracy': 0.85
        })
        print("Test model created with metadata:", self.model.get_metadata())
    
    def test_web3_connection(self):
        """Test Web3 connection to Ganache"""
        print("\nTesting Web3 connection...")
        w3 = Web3(Web3.HTTPProvider(self.config.rpc_url))
        self.assertTrue(w3.is_connected())
        print("Successfully connected to Web3")
        
        # Check if we can get accounts
        accounts = w3.eth.accounts
        print(f"Found {len(accounts)} accounts")
        self.assertGreater(len(accounts), 0)
        
        # Check chain ID
        chain_id = w3.eth.chain_id
        print(f"Chain ID: {chain_id}")
        self.assertEqual(chain_id, self.config.chain_id)
        print("Chain ID verification successful")
    
    def test_account_creation(self):
        """Test account creation and management"""
        print("\nTesting account creation...")
        # Create new account
        address = self.client.create_account()
        print(f"Created new account with address: {address}")
        self.assertIsNotNone(address)
        self.assertTrue(Web3.is_address(address))
        
        # Check if account is stored in client
        client_addresses = [acc.address for acc in self.client.accounts]
        print(f"Current client accounts: {client_addresses}")
        self.assertIn(address, client_addresses)
        print("Account creation test completed successfully")
    
    def test_multiple_clients(self):
        """Test multiple client registrations"""
        print("\nTesting multiple client registrations...")
        # Register multiple clients
        client_ids = []
        for i in range(3):
            print(f"Registering client {i+1}...")
            client_id = self.client.register_client()
            client_ids.append(client_id)
            print(f"Registered client with ID: {client_id}")
        
        # Verify each client has unique ID and address
        addresses = set()
        for client_id in client_ids:
            address = self.client.get_client_address(client_id)
            print(f"Client {client_id} has address: {address}")
            self.assertIsNotNone(address)
            self.assertNotIn(address, addresses)
            addresses.add(address)
        print("Multiple client registration test completed successfully")
    
    def test_server_account(self):
        """Test server account initialization"""
        print("\nTesting server account initialization...")
        # Verify server account exists
        print(f"Server account address: {self.client.server_account.address}")
        self.assertIsNotNone(self.client.server_account)
        self.assertTrue(Web3.is_address(self.client.server_account.address))
        
        # Verify it's the first account
        print(f"First account in client: {self.client.accounts[0].address}")
        self.assertEqual(self.client.accounts[0], self.client.server_account)
        print("Server account test completed successfully")

def run_tests():
    """Run all blockchain integration tests"""
    print("\n=== Starting Blockchain Integration Tests ===")
    unittest.main(argv=[''], verbosity=2, exit=False)
    print("\n=== Blockchain Integration Tests Completed ===")

if __name__ == "__main__":
    run_tests() 