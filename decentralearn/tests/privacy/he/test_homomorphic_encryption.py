"""
Tests for homomorphic encryption functionality
"""
import pytest
import torch
import numpy as np
from decentralearn.privacy.he.homomorphic_encryption import HomomorphicEncryption

@pytest.fixture
def he():
    """Create a HomomorphicEncryption instance for testing"""
    return HomomorphicEncryption()

@pytest.fixture
def sample_model():
    """Create a sample model for testing"""
    return {
        'weight1': torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32),
        'weight2': torch.tensor([5.0, 6.0], dtype=torch.float32)
    }

def test_encrypt_decrypt_model(he, sample_model):
    """Test model encryption and decryption"""
    # Encrypt model
    encrypted_model = he.encrypt_model(sample_model)
    
    # Check encryption
    assert isinstance(encrypted_model, dict)
    assert all(isinstance(v, dict) for v in encrypted_model.values())
    assert all('shape' in v and 'encrypted' in v for v in encrypted_model.values())
    
    # Decrypt model
    decrypted_model = he.decrypt_model(encrypted_model)
    
    # Check decryption
    assert isinstance(decrypted_model, dict)
    for key in sample_model.keys():
        assert isinstance(decrypted_model[key], torch.Tensor)
        assert decrypted_model[key].dtype == torch.float32
        assert torch.allclose(decrypted_model[key], sample_model[key], rtol=1e-5, atol=1e-5)

def test_aggregate_encrypted_models(he, sample_model):
    """Test encrypted model aggregation"""
    # Create multiple encrypted models
    encrypted_models = [
        he.encrypt_model(sample_model),
        he.encrypt_model(sample_model),
        he.encrypt_model(sample_model)
    ]
    
    # Aggregate models
    aggregated = he.aggregate_encrypted_models(encrypted_models)
    
    # Check aggregation
    assert isinstance(aggregated, dict)
    assert all(isinstance(v, dict) for v in aggregated.values())
    assert all('shape' in v and 'encrypted' in v for v in aggregated.values())
    
    # Decrypt and verify
    decrypted = he.decrypt_model(aggregated)
    for key in sample_model.keys():
        assert isinstance(decrypted[key], torch.Tensor)
        assert decrypted[key].dtype == torch.float32
        expected = sample_model[key] * 3
        assert torch.allclose(decrypted[key], expected, rtol=1e-5, atol=1e-5)

def test_add_encrypted_models(he, sample_model):
    """Test addition of two encrypted models"""
    # Encrypt two models
    encrypted_model1 = he.encrypt_model(sample_model)
    encrypted_model2 = he.encrypt_model(sample_model)
    
    # Add models
    added = he.add_encrypted_models(encrypted_model1, encrypted_model2)
    
    # Check addition
    assert isinstance(added, dict)
    assert all(isinstance(v, dict) for v in added.values())
    assert all('shape' in v and 'encrypted' in v for v in added.values())
    
    # Decrypt and verify
    decrypted = he.decrypt_model(added)
    for key in sample_model.keys():
        assert isinstance(decrypted[key], torch.Tensor)
        assert decrypted[key].dtype == torch.float32
        expected = sample_model[key] * 2
        assert torch.allclose(decrypted[key], expected, rtol=1e-5, atol=1e-5)

def test_shape_mismatch(he, sample_model):
    """Test handling of shape mismatches"""
    # Create a model with different shape
    mismatched_model = {
        'weight1': torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=torch.float32),
        'weight2': torch.tensor([7.0, 8.0, 9.0], dtype=torch.float32)
    }
    
    encrypted_model1 = he.encrypt_model(sample_model)
    encrypted_model2 = he.encrypt_model(mismatched_model)
    
    # Adding models with different shapes should raise ValueError
    with pytest.raises(ValueError):
        he.add_encrypted_models(encrypted_model1, encrypted_model2)

def test_empty_aggregation(he):
    """Test aggregation of empty model list"""
    result = he.aggregate_encrypted_models([])
    assert isinstance(result, dict)
    assert len(result) == 0 