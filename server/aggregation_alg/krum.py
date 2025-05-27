"""
Krum Aggregation Strategy
A Byzantine-robust aggregation strategy that selects the model closest to its neighbors.
It's like choosing the most trustworthy friend in a group!
"""
from typing import List, Dict, Optional
import numpy as np
import torch
from .aggFac import AggregationStrategy

class Krum(AggregationStrategy):
    """The security guard of federated learning
    
    Krum is designed to be robust against Byzantine attacks by selecting the model
    that is closest to its neighbors. It's particularly useful when you suspect
    some clients might be malicious or compromised.
    """
    
    def __init__(self, f: Optional[int] = None):
        """Initialize Krum with optional Byzantine tolerance
        
        Args:
            f: Maximum number of Byzantine clients to tolerate. If None, defaults to n//4
               where n is the number of clients.
        """
        self.f = f
    
    def aggregate(self, models: List[Dict[str, torch.Tensor]], 
                 weights: Optional[List[float]] = None) -> Dict[str, torch.Tensor]:
        """Aggregate models using Krum's Byzantine-robust algorithm
        
        Args:
            models: List of model state dictionaries to aggregate
            weights: Not used in Krum (weights are determined by distances)
            
        Returns:
            The selected model state dictionary that is most robust against attacks
            
        Raises:
            ValueError: If no models are provided
        """
        if not models:
            raise ValueError("No models to aggregate - the party's empty!")
        
        # Convert models to numpy arrays for efficient computation
        model_arrays = [np.array(list(model.values())) for model in models]
        n = len(model_arrays)
        
        # Set Byzantine tolerance if not provided
        if self.f is None:
            self.f = n // 4  # Default to tolerating up to 25% Byzantine clients
            
        # Calculate pairwise distances between all models
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                distances[i,j] = np.linalg.norm(model_arrays[i] - model_arrays[j])
                distances[j,i] = distances[i,j]
        
        # Calculate scores for each model
        scores = []
        for i in range(n):
            # Sort distances and take sum of n-f-2 smallest distances
            dists = np.sort(distances[i])
            scores.append(np.sum(dists[1:n-self.f-1]))  # Skip self (distance=0)
        
        # Select the model with the smallest score
        selected_idx = np.argmin(scores)
        return models[selected_idx]
