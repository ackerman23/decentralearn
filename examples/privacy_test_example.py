"""
Example script demonstrating privacy mechanism testing in DecentraLearn
"""
import numpy as np
from decentralearn.privacy.dp import DifferentialPrivacy

def main():
    # Create sample medical data updates (simulated)
    medical_updates = [
        {
            'patient_age': np.array([0.1, 0.2, 0.3]),
            'blood_pressure': np.array([0.4, 0.5]),
            'heart_rate': np.array([0.6])
        },
        {
            'patient_age': np.array([0.15, 0.25, 0.35]),
            'blood_pressure': np.array([0.45, 0.55]),
            'heart_rate': np.array([0.65])
        }
    ]

    # Initialize differential privacy with strong privacy guarantees
    dp = DifferentialPrivacy(epsilon=0.1, delta=1e-6)

    # Test 1: Protect Updates
    print("Testing protect_updates...")
    protected = dp.protect_updates(medical_updates, sensitivity=1.0)
    
    # Verify noise was added
    original = medical_updates[0]['patient_age']
    noised = protected[0]['patient_age']
    diff = np.linalg.norm(original - noised)
    print(f"Noise magnitude: {diff:.6f}")
    assert diff > 0, "No noise was added!"

    # Test 2: Clip Gradients
    print("\nTesting gradient clipping...")
    clip_norm = 0.5
    clipped = dp.clip_gradients(medical_updates, clip_norm)
    
    # Verify clipping worked
    for update in clipped:
        for key, param in update.items():
            norm = np.linalg.norm(param)
            print(f"Clipped norm for {key}: {norm:.6f}")
            assert norm <= clip_norm + 1e-6, f"Clipping failed for {key}!"

    # Test 3: Calculate Sensitivity
    print("\nTesting sensitivity calculation...")
    sensitivity = dp.calculate_sensitivity(medical_updates)
    print(f"Calculated sensitivity: {sensitivity:.6f}")

    print("\nAll privacy tests passed!")

if __name__ == "__main__":
    main() 