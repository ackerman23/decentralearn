"""
Tests for the DifferentialPrivacy class
"""
import pytest
import numpy as np
from decentralearn.privacy.dp.differential_privacy import DifferentialPrivacy

@pytest.fixture
def dp():
    """Create a DifferentialPrivacy instance for testing"""
    return DifferentialPrivacy(epsilon=1.0, delta=1e-5)

@pytest.fixture
def sample_updates():
    """Create sample model updates for testing"""
    return [
        {
            'weight1': np.array([[0.1, 0.2], [0.3, 0.4]], dtype=np.float64),
            'weight2': np.array([0.5, 0.6], dtype=np.float64)
        },
        {
            'weight1': np.array([[0.2, 0.3], [0.4, 0.5]], dtype=np.float64),
            'weight2': np.array([0.6, 0.7], dtype=np.float64)
        }
    ]

def test_protect_updates(dp, sample_updates):
    """Test update protection with differential privacy"""
    protected_updates = dp.protect_updates(sample_updates, sensitivity=1.0)
    
    # Check that updates are modified
    assert len(protected_updates) == len(sample_updates)
    for orig, prot in zip(sample_updates, protected_updates):
        for key in orig.keys():
            assert not np.array_equal(orig[key], prot[key])
            # Check that noise is added
            assert np.any(orig[key] != prot[key])

def test_clip_gradients(dp, sample_updates):
    """Test gradient clipping"""
    clip_norm = 0.5
    clipped_updates = dp.clip_gradients(sample_updates, clip_norm)
    
    # Check that updates are clipped
    assert len(clipped_updates) == len(sample_updates)
    for update in clipped_updates:
        for key in update.keys():
            norm = np.linalg.norm(update[key])
            assert norm <= clip_norm + 1e-6  # Add small epsilon for floating point comparison

def test_calculate_sensitivity(dp, sample_updates):
    """Test sensitivity calculation"""
    sensitivity = dp.calculate_sensitivity(sample_updates)
    
    # Check that sensitivity is calculated correctly
    assert isinstance(sensitivity, float)
    assert sensitivity >= 0.0
    
    # For our test data, we can calculate the expected sensitivity
    max_diff = 0.0
    for i in range(len(sample_updates)):
        for j in range(i + 1, len(sample_updates)):
            diff = 0.0
            for key in sample_updates[i].keys():
                param_diff = sample_updates[i][key] - sample_updates[j][key]
                diff += np.linalg.norm(param_diff) ** 2
            diff = np.sqrt(diff)
            max_diff = max(max_diff, diff)
    
    assert abs(sensitivity - max_diff) < 1e-6  # Should match our manual calculation

def test_empty_updates(dp):
    """Test handling of empty updates"""
    empty_updates = []
    protected_updates = dp.protect_updates(empty_updates, sensitivity=1.0)
    assert len(protected_updates) == 0
    
    clipped_updates = dp.clip_gradients(empty_updates, clip_norm=0.5)
    assert len(clipped_updates) == 0
    
    sensitivity = dp.calculate_sensitivity(empty_updates)
    assert sensitivity == 0.0 