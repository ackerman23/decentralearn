"""
Balance Aggregation Strategy
A dynamic aggregation strategy that filters models based on their distance from the global model.
It's like having a bouncer at the door checking IDs!
"""
from typing import List, Dict, Optional
import numpy as np
import torch
from .aggFac import AggregationStrategy

class Balance(AggregationStrategy):
    """The quality control expert of federated learning
    
    Balance aggregation filters out models that are too far from the global model,
    using a dynamic threshold that adapts over time. It's particularly useful when
    you want to maintain model quality while allowing for some variation.
    """
    
    def __init__(self, gamma: float = 1.0, kappa: float = 1.0):
        """Initialize Balance with distance threshold parameters
        
        Args:
            gamma: Base threshold multiplier for model distance
            kappa: Decay rate for the threshold over time
        """
        self.gamma = gamma
        self.kappa = kappa
        self.saved_model = None
    
    def aggregate(self, models: List[Dict[str, torch.Tensor]], 
                 weights: Optional[List[float]] = None,
                 t: Optional[int] = None) -> Dict[str, torch.Tensor]:
        """Aggregate models using distance-based filtering
        
        Args:
            models: List of model state dictionaries to aggregate
            weights: Optional list of weights for each model
            t: Current round number for dynamic threshold adjustment
            
        Returns:
            The filtered and averaged model state dictionary
            
        Raises:
            ValueError: If no models are provided or if saved_model is not set
        """
        if not models:
            raise ValueError("No models to aggregate - the party's empty!")
        
        if self.saved_model is None:
            raise ValueError("Saved model not set - please set it before aggregation")
        
        # Calculate global model norm
        global_norm = np.linalg.norm(np.array(list(self.saved_model.values())))
        
        # Calculate dynamic threshold
        lambda_t = 1 / (1 + t) if t is not None else 1
        distance_threshold = self.gamma * np.exp(-self.kappa * lambda_t) * global_norm
        
        # Filter models based on distance
        filtered_models = []
        for model in models:
            # Calculate distance from global model
            distance = np.linalg.norm(np.array(list(model.values())) - 
                                    np.array(list(self.saved_model.values())))
            
            if distance < distance_threshold:
                filtered_models.append(model)
            else:
                print(f"Model rejected: distance {distance:.4f} >= threshold {distance_threshold:.4f}")
        
        # If no models passed the filter, return the saved model
        if not filtered_models:
            print("No models were accepted for aggregation. Using saved model.")
            return self.saved_model
        
        # Average the filtered models
        aggregated_model = {}
        for key in filtered_models[0].keys():
            values = [model[key] for model in filtered_models]
            aggregated_model[key] = np.mean(values, axis=0)
            
            # Convert back to torch tensor if needed
            if isinstance(values[0], torch.Tensor):
                aggregated_model[key] = torch.from_numpy(aggregated_model[key])
        
        return aggregated_model
    
    def set_saved_model(self, model: Dict[str, torch.Tensor]) -> None:
        """Set the saved model for distance comparison
        
        Args:
            model: The model state dictionary to save
        """
        self.saved_model = model
