"""
JSON serialization utilities for model state dictionaries
"""
import json
import torch
import numpy as np
from typing import Dict, Any

def model2json(state_dict: Dict[str, torch.Tensor]) -> str:
    """
    Convert a model's state dictionary to JSON format
    
    Args:
        state_dict: Model state dictionary
        
    Returns:
        JSON string representation of the state dictionary
    """
    # Convert tensors to numpy arrays and then to lists
    json_dict = {}
    for key, tensor in state_dict.items():
        # Convert tensor to numpy array and then to list
        json_dict[key] = tensor.detach().numpy().tolist()
    
    return json.dumps(json_dict)

def json2model(json_str: str) -> Dict[str, torch.Tensor]:
    """
    Convert JSON string to model state dictionary
    
    Args:
        json_str: JSON string representation of the state dictionary
        
    Returns:
        Model state dictionary with torch tensors
    """
    # Parse JSON string
    json_dict = json.loads(json_str)
    
    # Convert lists back to torch tensors
    state_dict = {}
    for key, value in json_dict.items():
        # Convert list to numpy array and then to torch tensor
        state_dict[key] = torch.tensor(np.array(value))
    
    return state_dict

def dict2json(data: Dict[str, Any]) -> str:
    """
    Convert dictionary to JSON string
    
    Args:
        data: Dictionary to convert
        
    Returns:
        JSON string representation of the dictionary
    """
    return json.dumps(data)

def json2dict(json_str: str) -> Dict[str, Any]:
    """
    Convert JSON string to dictionary
    
    Args:
        json_str: JSON string to convert
        
    Returns:
        Dictionary representation of the JSON string
    """
    return json.loads(json_str) 