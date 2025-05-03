'''
JSON format utilities for model state dict serialization
'''
import torch
import json
import base64
import numpy as np
from typing import Dict, Any

def tensor_to_base64(tensor: torch.Tensor) -> str:
    """Convert a PyTorch tensor to a base64 string"""
    numpy_array = tensor.cpu().numpy()
    bytes_array = numpy_array.tobytes()
    base64_str = base64.b64encode(bytes_array).decode('utf-8')
    return base64_str

def base64_to_tensor(base64_str: str, dtype: torch.dtype, shape: tuple) -> torch.Tensor:
    """Convert a base64 string back to a PyTorch tensor"""
    bytes_array = base64.b64decode(base64_str.encode('utf-8'))
    numpy_array = np.frombuffer(bytes_array, dtype=np.float32).reshape(shape)
    tensor = torch.from_numpy(numpy_array).to(dtype=dtype)
    return tensor

def model2json(state_dict: Dict[str, torch.Tensor]) -> str:
    """Convert a model state dict to a JSON string"""
    json_dict = {}
    for key, tensor in state_dict.items():
        json_dict[key] = {
            'data': tensor_to_base64(tensor),
            'dtype': str(tensor.dtype),
            'shape': list(tensor.shape)
        }
    return json.dumps(json_dict)

def json2model(json_str: str) -> Dict[str, torch.Tensor]:
    """Convert a JSON string back to a model state dict"""
    json_dict = json.loads(json_str)
    state_dict = {}
    for key, tensor_data in json_dict.items():
        dtype = getattr(torch, tensor_data['dtype'].split('.')[-1])
        shape = tuple(tensor_data['shape'])
        tensor = base64_to_tensor(tensor_data['data'], dtype, shape)
        state_dict[key] = tensor
    return state_dict 