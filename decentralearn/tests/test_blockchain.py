"""
Tests for DecentraLearn blockchain integration
This module contains tests for blockchain-related functionality in DecentraLearn.
"""
import unittest
import torch
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.models.base import BaseModel
from decentralearn.config.blockchain_config import BlockchainConfig

class TestBlockchainIntegration(unittest.TestCase):
    """Test cases for blockchain integration"""
    
    def setUp(self):
        """Set up test environment"""
        print("\nSetting up blockchain test environment...")
        self.config = BlockchainConfig()
        print("Initialized blockchain config")
        
        self.client = BlockchainClient(self.config)
        print("Blockchain client initialized")
        
        # Create a test model
        print("Creating test model...")
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
    
    def test_client_registration(self):
        """Test client registration"""
        print("\nTesting client registration...")
        client_id = self.client.register_client()
        print(f"Registered client with ID: {client_id}")
        self.assertIsNotNone(client_id)
        self.assertTrue(isinstance(client_id, str))
        
        client_address = self.client.get_client_address(client_id)
        print(f"Client address: {client_address}")
        self.assertIsNotNone(client_address)
        print("Client registration test completed successfully")
    
    def test_model_operations(self):
        """Test model operations without blockchain"""
        print("\nTesting model operations...")
        # Test JSON serialization
        print("Testing model JSON serialization...")
        model_json = self.model.to_json()
        print(f"Model serialized to JSON (length: {len(model_json)} chars)")
        self.assertIsNotNone(model_json)
        self.assertTrue(isinstance(model_json, str))
        
        # Test model reconstruction
        print("Testing model reconstruction from JSON...")
        reconstructed_model = BaseModel.from_json(model_json)
        print("Model reconstructed successfully")
        self.assertIsNotNone(reconstructed_model)
        
        # Verify state dict compatibility
        print("Verifying state dictionary compatibility...")
        original_state = self.model.get_state_dict()
        reconstructed_state = reconstructed_model.get_state_dict()
        self.assertTrue(
            self.model.verify_state_dict(reconstructed_state)
        )
        print("State dictionary verification successful")
        
        # Verify metadata
        print("Verifying metadata...")
        original_metadata = self.model.get_metadata()
        reconstructed_metadata = reconstructed_model.get_metadata()
        print(f"Original metadata: {original_metadata}")
        print(f"Reconstructed metadata: {reconstructed_metadata}")
        self.assertEqual(original_metadata, reconstructed_metadata)
        print("Metadata verification successful")
        print("Model operations test completed successfully")

def run_tests():
    """Run all tests"""
    print("\n=== Starting Blockchain Unit Tests ===")
    unittest.main(argv=[''], verbosity=2, exit=False)
    print("\n=== Blockchain Unit Tests Completed ===")

if __name__ == "__main__":
    run_tests() 