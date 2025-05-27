"""
Base model class for DecentraLearn
This module provides the foundation for all machine learning models in the DecentraLearn ecosystem.
Because let's face it, every ML model needs a good foundation to stand on.
"""
from typing import Dict, Any
import torch
from decentralearn.utils import jsonFormat

class BaseModel:
    """The granddaddy of all models in DecentraLearn
    
    This class is like the Swiss Army knife of model management - it does everything
    except make coffee (though we're working on that feature).
    
    Features:
    - State dictionary management (because models need their state)
    - JSON serialization/deserialization (for when models need to travel)
    - Metadata handling (because models have feelings too)
    - Model verification (to catch those pesky imposters)
    """
    
    def __init__(self):
        """Initialize a new model
        
        Warning: This model is born innocent and pure. What you do with it is your responsibility.
        """
        self.state_dict = {}
        self.metadata = {}
    
    def set_state_dict(self, state_dict: Dict[str, torch.Tensor]):
        """Set the model's state dictionary
        
        Args:
            state_dict: The new state dictionary. Make it good, the model deserves it.
        """
        self.state_dict = state_dict
    
    def get_state_dict(self) -> Dict[str, torch.Tensor]:
        """Get the model's state dictionary
        
        Returns:
            Dict[str, torch.Tensor]: The model's current state. Handle with care.
        """
        return self.state_dict
    
    def set_metadata(self, metadata: Dict[str, Any]):
        """Set model metadata
        
        Args:
            metadata: The model's new identity. Make it interesting.
        """
        self.metadata = metadata
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get model metadata
        
        Returns:
            Dict[str, Any]: Everything you ever wanted to know about the model
            (but were afraid to ask)
        """
        return self.metadata
    
    def to_json(self) -> str:
        """Convert model state to JSON format
        
        Returns:
            str: The model's life story in JSON format. Perfect for blockchain.
        """
        data = {
            'state_dict': jsonFormat.model2json(self.state_dict),
            'metadata': self.metadata
        }
        return jsonFormat.dict2json(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """Create model from JSON format
        
        Args:
            json_str: The model's life story in JSON format
        
        Returns:
            BaseModel: A brand new model, resurrected from JSON
        """
        data = jsonFormat.json2dict(json_str)
        model = cls()
        model.state_dict = jsonFormat.json2model(data['state_dict'])
        model.metadata = data['metadata']
        return model
    
    def verify_state_dict(self, other_state_dict: Dict[str, torch.Tensor]) -> bool:
        """Verify if two state dictionaries have matching keys and shapes
        
        Args:
            other_state_dict: The state dictionary to compare against
        
        Returns:
            bool: True if they're twins, False if they're just distant cousins
        """
        if set(self.state_dict.keys()) != set(other_state_dict.keys()):
            return False
        
        for key in self.state_dict:
            if self.state_dict[key].shape != other_state_dict[key].shape:
                return False
        
        return True 