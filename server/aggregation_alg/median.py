"""
Median Aggregation Strategy
A robust aggregation strategy that uses the median of model parameters.
It's like finding the middle ground in a group discussion!
"""
from typing import List, Dict, Optional
import numpy as np
import torch
from .aggFac import AggregationStrategy

class Median(AggregationStrategy):
    """The peacemaker of federated learning
    
    Median aggregation is robust against outliers and Byzantine attacks by
    selecting the middle value of all parameters. It's particularly useful
    when you want to be resistant to extreme values but still want to consider
    all inputs.
    """
    
    def aggregate(self, models: List[Dict[str, torch.Tensor]], 
                 weights: Optional[List[float]] = None) -> Dict[str, torch.Tensor]:
        """Aggregate models using median-based robust aggregation
        
        Args:
            models: List of model state dictionaries to aggregate
            weights: Not used in Median (all models are treated equally)
            
        Returns:
            The median model state dictionary
            
        Raises:
            ValueError: If no models are provided
        """
        if not models:
            raise ValueError("No models to aggregate - the party's empty!")
        
        # Initialize aggregated model
        aggregated_model = {}
        
        # For each parameter in the model
        for key in models[0].keys():
            # Get all values for this parameter across clients
            values = [model[key] for model in models]
            
            # Convert to numpy array for efficient median computation
            values_array = np.array(values)
            
            # Compute median along the client axis
            median_value = np.median(values_array, axis=0)
            
            # Convert back to torch tensor if needed
            if isinstance(values[0], torch.Tensor):
                median_value = torch.from_numpy(median_value)
            
            aggregated_model[key] = median_value
        
        return aggregated_model
