"""
Aggregation Factory for DecentraLearn
This module provides a factory pattern for creating different federated learning
aggregation strategies. Because one size doesn't fit all in the world of FL!
"""
from typing import Dict, List, Optional, Type
import torch
from .fedavg import FedAvg
from .krum import Krum
from .median import Median
from .balance import Balance

class AggregationFactory:
    """The master of ceremonies for all aggregation strategies
    
    This class is like a fancy restaurant menu - it offers different flavors of
    aggregation strategies to suit your federated learning needs.
    """
    
    # Registry of available aggregation strategies
    _strategies: Dict[str, Type] = {
        'fedavg': FedAvg,
        'krum': Krum,
        'median': Median,
        'balance': Balance
    }
    
    @classmethod
    def create(cls, strategy_name: str, **kwargs) -> 'AggregationStrategy':
        """Create an aggregation strategy
        
        Args:
            strategy_name: The name of the strategy you want to use
            **kwargs: Additional arguments for the strategy
            
        Returns:
            An instance of the requested aggregation strategy
            
        Raises:
            ValueError: If the strategy doesn't exist
        """
        if strategy_name not in cls._strategies:
            raise ValueError(f"Unknown aggregation strategy: {strategy_name}. "
                           f"Available strategies: {list(cls._strategies.keys())}")
        
        return cls._strategies[strategy_name](**kwargs)
    
    @classmethod
    def list_strategies(cls) -> List[str]:
        """Get a list of available aggregation strategies
        
        Returns:
            List of strategy names that are ready to party
        """
        return list(cls._strategies.keys())
    
    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type) -> None:
        """Register a new aggregation strategy
        
        Args:
            name: The name of the strategy
            strategy_class: The class implementing the strategy
            
        Raises:
            ValueError: If the name is already taken
        """
        if name in cls._strategies:
            raise ValueError(f"Strategy name '{name}' is already taken. "
                           "Choose a different name or remove the existing one first.")
        
        cls._strategies[name] = strategy_class

class AggregationStrategy:
    """Base class for all aggregation strategies
    
    This is the parent class that all aggregation strategies must inherit from.
    Think of it as the rulebook for how to combine models in a federated setting.
    """
    
    def aggregate(self, models: List[Dict[str, torch.Tensor]], 
                 weights: Optional[List[float]] = None) -> Dict[str, torch.Tensor]:
        """Aggregate multiple models into one
        
        Args:
            models: List of model state dictionaries to aggregate
            weights: Optional list of weights for each model
            
        Returns:
            The aggregated model state dictionary
        """
        raise NotImplementedError("Subclasses must implement this method")
