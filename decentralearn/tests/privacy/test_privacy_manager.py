"""
Tests for the PrivacyManager class
"""
import pytest
import torch
import numpy as np
from decentralearn.privacy.manager import PrivacyManager
from decentralearn.privacy.utils.privacy_config import PrivacyConfig

@pytest.fixture
def privacy_manager():
    """Create a PrivacyManager instance for testing"""
    config = PrivacyConfig(
        dp_epsilon=1.0,
        dp_delta=1e-5,
        he_key_size=2048,
        he_scheme="paillier",
        zkp_protocol="zk-snark"
    )
    return PrivacyManager(config)

@pytest.fixture
def sample_model():
    """Create a sample model for testing"""
    return {
        'weight1': torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32),
        'weight2': torch.tensor([5.0, 6.0], dtype=torch.float32)
    }

@pytest.fixture
def sample_model_updates():
    """Create sample model updates for testing"""
    return [
        {
            'weight1': torch.tensor([[0.1, 0.2], [0.3, 0.4]], dtype=torch.float32),
            'weight2': torch.tensor([0.5, 0.6], dtype=torch.float32)
        },
        {
            'weight1': torch.tensor([[0.2, 0.3], [0.4, 0.5]], dtype=torch.float32),
            'weight2': torch.tensor([0.6, 0.7], dtype=torch.float32)
        }
    ]

def test_apply_differential_privacy(privacy_manager, sample_model_updates):
    """Test differential privacy application"""
    protected_updates = privacy_manager.apply_differential_privacy(
        sample_model_updates,
        sensitivity=1.0
    )
    
    # Check that updates are modified
    assert len(protected_updates) == len(sample_model_updates)
    for orig, prot in zip(sample_model_updates, protected_updates):
        for key in orig.keys():
            assert not torch.allclose(orig[key], prot[key])

def test_encrypt_decrypt_model(privacy_manager, sample_model):
    """Test model encryption and decryption"""
    # Encrypt model
    encrypted_model = privacy_manager.encrypt_model(sample_model)
    
    # Check encryption
    assert isinstance(encrypted_model, dict)
    assert all(isinstance(v, dict) for v in encrypted_model.values())
    assert all('shape' in v and 'encrypted' in v for v in encrypted_model.values())
    
    # Decrypt model
    decrypted_model = privacy_manager.decrypt_model(encrypted_model)
    
    # Check decryption
    assert isinstance(decrypted_model, dict)
    for key in sample_model.keys():
        assert torch.allclose(sample_model[key], decrypted_model[key], rtol=1e-5, atol=1e-5)

def test_generate_verify_proof(privacy_manager, sample_model):
    """Test zero-knowledge proof generation and verification"""
    # Generate proof
    statement = "model has positive weights"
    proof = privacy_manager.generate_proof(sample_model, statement)
    
    # Check proof structure
    assert isinstance(proof, dict)
    assert 'protocol' in proof
    assert 'statement' in proof
    assert 'model_hash' in proof
    assert 'proof' in proof
    
    # Verify proof
    assert privacy_manager.verify_proof(proof, statement)

def test_aggregate_encrypted_models(privacy_manager, sample_model):
    """Test encrypted model aggregation"""
    # Encrypt two copies of the model
    encrypted_model1 = privacy_manager.encrypt_model(sample_model)
    encrypted_model2 = privacy_manager.encrypt_model(sample_model)
    
    # Aggregate models
    aggregated = privacy_manager.aggregate_encrypted_models([
        encrypted_model1,
        encrypted_model2
    ])
    
    # Check aggregation
    assert isinstance(aggregated, dict)
    assert all(isinstance(v, dict) for v in aggregated.values())
    assert all('shape' in v and 'encrypted' in v for v in aggregated.values())
    
    # Decrypt and verify
    decrypted = privacy_manager.decrypt_model(aggregated)
    for key in sample_model.keys():
        expected = sample_model[key] * 2
        assert torch.allclose(decrypted[key], expected, rtol=1e-5, atol=1e-5) 