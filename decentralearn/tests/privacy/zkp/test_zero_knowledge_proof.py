"""
Tests for the ZeroKnowledgeProof class
"""
import pytest
import torch
import numpy as np
from decentralearn.privacy.zkp.zero_knowledge_proof import ZeroKnowledgeProof

@pytest.fixture
def zkp():
    """Create a ZeroKnowledgeProof instance for testing"""
    return ZeroKnowledgeProof(protocol="zk-snark")

@pytest.fixture
def sample_model():
    """Create a sample model for testing"""
    return {
        'weight1': torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
        'weight2': torch.tensor([5.0, 6.0])
    }

def test_generate_verify_proof(zkp, sample_model):
    """Test proof generation and verification"""
    # Generate proof
    statement = "model has positive weights"
    proof = zkp.generate_proof(sample_model, statement)
    
    # Check proof structure
    assert isinstance(proof, dict)
    assert 'protocol' in proof
    assert 'statement' in proof
    assert 'model_hash' in proof
    assert 'proof' in proof
    
    # Check protocol
    assert proof['protocol'] == "zk-snark"
    assert proof['statement'] == statement
    
    # Verify proof
    assert zkp.verify_proof(proof, statement)

def test_hash_model(zkp, sample_model):
    """Test model hashing"""
    # Generate hash
    model_hash = zkp._hash_model(sample_model)
    
    # Check hash
    assert isinstance(model_hash, str)
    assert len(model_hash) == 64  # SHA-256 hash length
    
    # Hash should be deterministic
    assert model_hash == zkp._hash_model(sample_model)
    
    # Hash should change with model
    modified_model = {
        'weight1': torch.tensor([[1.1, 2.0], [3.0, 4.0]]),
        'weight2': torch.tensor([5.0, 6.0])
    }
    assert model_hash != zkp._hash_model(modified_model)

def test_different_protocols(sample_model):
    """Test different proof protocols"""
    protocols = ["zk-snark", "zk-stark", "bulletproofs"]
    statement = "model has positive weights"
    
    for protocol in protocols:
        zkp = ZeroKnowledgeProof(protocol=protocol)
        proof = zkp.generate_proof(sample_model, statement)
        
        # Check protocol-specific proof
        assert proof['protocol'] == protocol
        assert proof['proof']['type'] == protocol.split('-')[-1].lower()
        
        # Verify proof
        assert zkp.verify_proof(proof, statement)

def test_protocol_mismatch(zkp, sample_model):
    """Test handling of protocol mismatches"""
    statement = "model has positive weights"
    proof = zkp.generate_proof(sample_model, statement)
    
    # Modify proof protocol
    modified_proof = proof.copy()
    modified_proof['protocol'] = "zk-stark"
    
    # Verification should fail
    with pytest.raises(ValueError):
        zkp.verify_proof(modified_proof, statement)

def test_statement_mismatch(zkp, sample_model):
    """Test handling of statement mismatches"""
    original_statement = "model has positive weights"
    proof = zkp.generate_proof(sample_model, original_statement)
    
    # Try to verify with different statement
    different_statement = "model has negative weights"
    with pytest.raises(ValueError):
        zkp.verify_proof(proof, different_statement)

def test_invalid_protocol():
    """Test handling of invalid protocols"""
    with pytest.raises(ValueError):
        ZeroKnowledgeProof(protocol="invalid-protocol") 