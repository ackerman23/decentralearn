"""
Differential Privacy for DecentraLearn
This module implements differential privacy mechanisms for federated learning.
"""
from typing import Dict, List, Optional
import numpy as np
from scipy.stats import laplace

class DifferentialPrivacy:
    """Differential privacy protection for model updates
    
    This class implements differential privacy mechanisms to protect
    model updates in federated learning. It uses the Laplace mechanism
    to add calibrated noise to model parameters.
    """
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """Initialize differential privacy settings
        
        Args:
            epsilon: Privacy budget (smaller = more privacy)
            delta: Failure probability
        """
        self.epsilon = epsilon
        self.delta = delta
    
    def protect_updates(
        self,
        model_updates: List[Dict[str, np.ndarray]],
        sensitivity: float = 1.0
    ) -> List[Dict[str, np.ndarray]]:
        """Apply differential privacy to model updates
        
        Args:
            model_updates: List of model state dictionaries
            sensitivity: The sensitivity of the updates
            
        Returns:
            List of differentially private model updates
        """
        protected_updates = []
        
        for update in model_updates:
            protected_update = {}
            
            for key, param in update.items():
                # Add Laplace noise scaled by sensitivity/epsilon
                scale = sensitivity / self.epsilon
                noise = laplace.rvs(scale=scale, size=param.shape)
                protected_update[key] = param + noise
            
            protected_updates.append(protected_update)
        
        return protected_updates
    
    def clip_gradients(
        self,
        model_updates: List[Dict[str, np.ndarray]],
        clip_norm: float = 1.0
    ) -> List[Dict[str, np.ndarray]]:
        """Clip gradients to bound sensitivity
        
        Args:
            model_updates: List of model state dictionaries
            clip_norm: Maximum L2 norm for gradients
            
        Returns:
            List of clipped model updates
        """
        clipped_updates = []
        
        for update in model_updates:
            clipped_update = {}
            
            for key, param in update.items():
                # Calculate L2 norm
                norm = np.linalg.norm(param)
                
                # Clip if norm exceeds threshold
                if norm > clip_norm:
                    clipped_update[key] = param * (clip_norm / norm)
                else:
                    clipped_update[key] = param
            
            clipped_updates.append(clipped_update)
        
        return clipped_updates
    
    def calculate_sensitivity(
        self,
        model_updates: List[Dict[str, np.ndarray]]
    ) -> float:
        """Calculate sensitivity of model updates
        
        Args:
            model_updates: List of model state dictionaries
            
        Returns:
            Maximum L2 norm difference between any two updates
        """
        max_sensitivity = 0.0
        
        # Compare each pair of updates
        for i in range(len(model_updates)):
            for j in range(i + 1, len(model_updates)):
                diff = 0.0
                
                # Calculate L2 norm of difference for each parameter
                for key in model_updates[i].keys():
                    param_diff = model_updates[i][key] - model_updates[j][key]
                    diff += np.linalg.norm(param_diff) ** 2
                
                diff = np.sqrt(diff)
                max_sensitivity = max(max_sensitivity, diff)
        
        return max_sensitivity 