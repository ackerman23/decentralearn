"""
Federated Averaging (FedAvg) Aggregation Strategy
The classic and most popular federated learning aggregation strategy.
It's like democracy for models - everyone gets an equal vote!
"""
from typing import List, Dict, Optional
import torch
from .aggFac import AggregationStrategy

class FedAvg(AggregationStrategy):
    """The OG of federated learning aggregation strategies
    
    This is the vanilla ice cream of aggregation strategies - simple, reliable,
    and loved by everyone. It averages model parameters with equal weights.
    """
    
    def aggregate(self, models: List[Dict[str, torch.Tensor]], 
                 weights: Optional[List[float]] = None) -> Dict[str, torch.Tensor]:
        """Aggregate models using FedAvg
        
        Args:
            models: List of model state dictionaries to aggregate
            weights: Optional list of weights for each model. If None, equal weights are used.
            
        Returns:
            The averaged model state dictionary
        """
        if not models:
            raise ValueError("No models to aggregate - the party's empty!")
        
        # Use equal weights if none provided
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        
        # Initialize aggregated model
        aggregated_model = {}
        
        # Average each parameter
        for key in models[0].keys():
            # Weighted sum of parameters
            weighted_sum = sum(w * model[key] for w, model in zip(weights, models))
            aggregated_model[key] = weighted_sum
        
        return aggregated_model


if __name__ == '__main__':
    client1_model = {'weight': 0.5, 'bias': 0.2}
    client2_model = {'weight': 0.3, 'bias': 0.1}
    client3_model = {'weight': 0.6, 'bias': 0.3}

    aggregator = FedAvg()
    aggregated_model = aggregator.aggregate([client1_model, client2_model, client3_model])

    print(aggregated_model)
