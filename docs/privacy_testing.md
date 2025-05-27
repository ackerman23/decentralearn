# Testing Privacy Mechanisms in DecentraLearn

This guide explains how to test the privacy mechanisms in DecentraLearn, including differential privacy, with real-world examples and explanations.

## Running Privacy Tests

### Basic Test Commands

To run all privacy-related tests:
```bash
python -m pytest decentralearn/tests/privacy/
```

To run specific privacy mechanism tests:
```bash
# Test differential privacy
python -m pytest decentralearn/tests/privacy/dp/test_differential_privacy.py -v

# Test homomorphic encryption (when implemented)
python -m pytest decentralearn/tests/privacy/he/test_homomorphic_encryption.py -v

# Test zero-knowledge proofs (when implemented)
python -m pytest decentralearn/tests/privacy/zkp/test_zero_knowledge_proofs.py -v
```

## Current Test Results

As of the latest implementation, all differential privacy tests are passing:

```
test_protect_updates PASSED             [ 25%]
test_clip_gradients PASSED              [ 50%]
test_calculate_sensitivity PASSED       [ 75%]
test_empty_updates PASSED               [100%]
```

## Real-World Example: Medical Data Analysis

Let's consider a real-world example of how our privacy mechanisms protect sensitive data in a medical research scenario.

### Scenario
A group of hospitals wants to collaborate on developing a machine learning model to predict patient readmission risk. However, they cannot share raw patient data due to privacy regulations (HIPAA).

### Example Implementation

```python
from decentralearn.privacy.dp import DifferentialPrivacy

# Initialize privacy mechanism
dp = DifferentialPrivacy(epsilon=0.1, delta=1e-6)  # Strong privacy guarantees

# Example hospital data (simplified for illustration)
hospital_updates = [
    {
        'age_weights': np.array([0.1, 0.2, 0.3]),  # Age feature weights
        'diagnosis_weights': np.array([0.4, 0.5])   # Diagnosis feature weights
    },
    {
        'age_weights': np.array([0.15, 0.25, 0.35]),
        'diagnosis_weights': np.array([0.45, 0.55])
    }
]

# Apply differential privacy
protected_updates = dp.protect_updates(hospital_updates, sensitivity=1.0)
```

### Privacy Guarantees

1. **Noise Addition**: The `protect_updates` method adds calibrated Laplace noise to the model updates:
   - With ε=0.1, an attacker cannot determine with high confidence whether any specific patient's data was included
   - Example: If a weight was originally 0.1, it might become 0.103 or 0.097

2. **Gradient Clipping**: The `clip_gradients` method ensures bounded sensitivity:
   ```python
   clipped_updates = dp.clip_gradients(hospital_updates, clip_norm=0.5)
   ```
   - Prevents any single update from having too much influence
   - Example: If a rare medical condition would cause a large gradient of 2.0, it's clipped to 0.5

3. **Sensitivity Analysis**: The `calculate_sensitivity` method measures the maximum possible impact of any single patient:
   ```python
   sensitivity = dp.calculate_sensitivity(hospital_updates)
   ```
   - Helps calibrate noise addition
   - Example: If sensitivity=0.8, we know no single patient can influence the model by more than this amount

## Testing Your Own Data

To test privacy mechanisms with your own data:

1. **Prepare Updates**:
```python
your_updates = [
    {
        'layer1.weights': np.array(...),
        'layer1.bias': np.array(...)
    },
    # More updates...
]
```

2. **Apply Privacy**:
```python
dp = DifferentialPrivacy(epsilon=1.0)  # Adjust epsilon based on privacy needs
protected = dp.protect_updates(your_updates)
```

3. **Verify Privacy**:
```python
# Check if updates are sufficiently different
import numpy as np
original = your_updates[0]['layer1.weights']
protected = protected_updates[0]['layer1.weights']
difference = np.linalg.norm(original - protected)
assert difference > 0  # Should have some noise added
```

## Privacy Budget Guidelines

| Use Case | Recommended ε | Privacy Level |
|----------|---------------|---------------|
| Medical  | 0.1 - 0.5    | Very Strong   |
| Financial| 0.5 - 1.0    | Strong        |
| General  | 1.0 - 2.0    | Moderate      |

## Current Limitations and Future Work

1. **Current Implementation**:
   - Successfully implements Laplace mechanism
   - Provides gradient clipping
   - Calculates sensitivity

2. **Planned Improvements**:
   - Gaussian mechanism implementation
   - Moments accountant for tighter privacy bounds
   - Advanced composition theorems
   - Integration with federated averaging

## Troubleshooting Common Issues

1. **High Noise Levels**:
   - If model accuracy is too low, try increasing epsilon
   - Use gradient clipping to reduce required noise

2. **Performance Issues**:
   - For large models, use batched noise addition
   - Consider using the parallel implementation for large datasets

3. **Privacy Budget Exhaustion**:
   - Monitor cumulative privacy loss
   - Implement privacy budget management 