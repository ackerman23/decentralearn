"""
Homomorphic Encryption for DecentraLearn
This module implements homomorphic encryption for secure model aggregation.
"""
from typing import Dict, List, Union, Any
import torch
import numpy as np
from phe import paillier  # Python Homomorphic Encryption library
import base64
import json

class HomomorphicEncryption:
    """Homomorphic encryption for secure model aggregation
    
    This class implements homomorphic encryption to enable secure aggregation
    of model updates without revealing individual client contributions.
    """
    
    def __init__(self, key_size: int = 2048, scheme: str = "paillier"):
        """Initialize homomorphic encryption settings
        
        Args:
            key_size: Size of encryption key in bits
            scheme: Encryption scheme to use (paillier, bfv, ckks)
        """
        self.key_size = key_size
        self.scheme = scheme
        
        # Initialize encryption keys
        if scheme == "paillier":
            self.public_key, self.private_key = paillier.generate_paillier_keypair(
                n_length=key_size
            )
        else:
            raise ValueError(f"Unsupported encryption scheme: {scheme}")
    
    def _encrypt_value(self, value: float) -> paillier.EncryptedNumber:
        """Encrypt a single value using Paillier encryption"""
        if self.scheme == "paillier":
            return self.public_key.encrypt(float(value))
        raise ValueError(f"Unsupported encryption scheme: {self.scheme}")
    
    def _decrypt_value(self, encrypted_value: paillier.EncryptedNumber) -> float:
        """Decrypt a single value using Paillier encryption"""
        if self.scheme == "paillier":
            return self.private_key.decrypt(encrypted_value)
        raise ValueError(f"Unsupported encryption scheme: {self.scheme}")
    
    def _encrypt_tensor(self, tensor: torch.Tensor) -> Dict[str, Any]:
        """Encrypt a tensor"""
        # Convert to numpy for encryption
        np_array = tensor.detach().cpu().numpy()
        encrypted = np.empty(np_array.shape, dtype=object)
        for idx in np.ndindex(np_array.shape):
            encrypted[idx] = self._encrypt_value(np_array[idx])
        return {
            'shape': tensor.shape,
            'encrypted': encrypted
        }
    
    def _decrypt_tensor(self, encrypted_data: Dict[str, Any]) -> torch.Tensor:
        """Decrypt a tensor"""
        encrypted = encrypted_data['encrypted']
        decrypted = np.empty(encrypted.shape, dtype=np.float32)
        for idx in np.ndindex(encrypted.shape):
            decrypted[idx] = self._decrypt_value(encrypted[idx])
        # Convert back to torch tensor
        return torch.tensor(decrypted, dtype=torch.float32)
    
    def encrypt_model(self, model: Dict[str, Union[torch.Tensor, np.ndarray]]) -> Dict[str, Dict[str, Any]]:
        """Encrypt a model's parameters"""
        encrypted_model = {}
        for key, param in model.items():
            if isinstance(param, torch.Tensor):
                tensor = param
            else:
                tensor = torch.tensor(param, dtype=torch.float32)
            
            encrypted_model[key] = self._encrypt_tensor(tensor)
        return encrypted_model
    
    def decrypt_model(self, encrypted_model: Dict[str, Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """Decrypt a model's parameters"""
        decrypted_model = {}
        for key, encrypted_data in encrypted_model.items():
            decrypted_model[key] = self._decrypt_tensor(encrypted_data)
        return decrypted_model
    
    def add_encrypted_models(self, model1: Dict[str, Dict[str, Any]], 
                           model2: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Add two encrypted models"""
        if set(model1.keys()) != set(model2.keys()):
            raise ValueError("Models must have the same keys")
        
        result = {}
        for key in model1.keys():
            if model1[key]['shape'] != model2[key]['shape']:
                raise ValueError(f"Shape mismatch for key {key}")
            
            # Add encrypted values
            encrypted1 = model1[key]['encrypted']
            encrypted2 = model2[key]['encrypted']
            added = np.empty(encrypted1.shape, dtype=object)
            
            for idx in np.ndindex(encrypted1.shape):
                added[idx] = encrypted1[idx] + encrypted2[idx]
            
            result[key] = {
                'shape': model1[key]['shape'],
                'encrypted': added
            }
        return result
    
    def aggregate_encrypted_models(self, models: List[Dict[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
        """Aggregate multiple encrypted models"""
        if not models:
            return {}
        
        # Start with the first model
        result = models[0].copy()
        
        # Add remaining models
        for model in models[1:]:
            result = self.add_encrypted_models(result, model)
        
        return result
    
    def _serialize_encrypted_data(self, data: Dict[str, Any]) -> bytes:
        """Serialize encrypted data to bytes"""
        # Convert bytes to base64 strings for JSON serialization
        encrypted_b64 = np.vectorize(lambda x: base64.b64encode(x).decode())(data['encrypted'])
        
        serialized = {
            'shape': list(data['shape']),
            'encrypted': encrypted_b64.tolist()
        }
        return json.dumps(serialized).encode()
    
    def _deserialize_encrypted_data(self, data_bytes: bytes) -> Dict[str, Any]:
        """Deserialize encrypted data from bytes"""
        data = json.loads(data_bytes.decode())
        # Convert base64 strings back to bytes
        encrypted = np.array(data['encrypted'])
        encrypted_bytes = np.vectorize(lambda x: base64.b64decode(x.encode()))(encrypted)
        return {
            'shape': tuple(data['shape']),
            'encrypted': encrypted_bytes
        } 