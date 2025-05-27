"""
Privacy Manager for DecentraLearn
This module provides comprehensive privacy protection mechanisms for federated learning,
including differential privacy, homomorphic encryption, and zero-knowledge proofs.
"""
from typing import Dict, List, Optional, Union, Any
import torch
import numpy as np
import json
from .dp.differential_privacy import DifferentialPrivacy
from .he.homomorphic_encryption import HomomorphicEncryption
from .zkp.zero_knowledge_proof import ZeroKnowledgeProof
from .utils.privacy_config import PrivacyConfig

class PrivacyManager:
    """The guardian of privacy in federated learning
    
    This class manages all privacy-preserving mechanisms in the system,
    including differential privacy, homomorphic encryption, and zero-knowledge proofs.
    It ensures that sensitive data and model updates remain private while still
    allowing effective federated learning.
    """
    
    def __init__(self, config: Optional[PrivacyConfig] = None):
        """Initialize the privacy manager with configuration
        
        Args:
            config: Privacy configuration object. If None, uses default settings.
        """
        self.config = config or PrivacyConfig()
        
        # Initialize privacy mechanisms
        self.dp = DifferentialPrivacy(
            epsilon=self.config.dp_epsilon,
            delta=self.config.dp_delta
        )
        
        self.he = HomomorphicEncryption(
            key_size=self.config.he_key_size,
            scheme=self.config.he_scheme
        )
        
        self.zkp = ZeroKnowledgeProof(
            protocol=self.config.zkp_protocol
        )
    
    def apply_differential_privacy(
        self, 
        model_updates: List[Dict[str, torch.Tensor]],
        sensitivity: float = 1.0
    ) -> List[Dict[str, torch.Tensor]]:
        """Apply differential privacy to model updates
        
        Args:
            model_updates: List of model state dictionaries to protect
            sensitivity: The sensitivity of the model updates
            
        Returns:
            List of differentially private model updates
        """
        # Convert PyTorch tensors to NumPy arrays
        numpy_updates = [
            {k: v.detach().cpu().numpy() for k, v in update.items()}
            for update in model_updates
        ]
        
        # Apply DP
        protected_numpy = self.dp.protect_updates(numpy_updates, sensitivity)
        
        # Convert back to PyTorch tensors with correct dtype
        return [
            {k: torch.from_numpy(v).to(dtype=torch.float32) for k, v in update.items()}
            for update in protected_numpy
        ]
    
    def encrypt_model(
        self, 
        model: Dict[str, torch.Tensor]
    ) -> Dict[str, Dict[str, Any]]:
        """Encrypt a model using homomorphic encryption
        
        Args:
            model: Model state dictionary to encrypt
            
        Returns:
            Encrypted model state dictionary
        """
        return self.he.encrypt_model(model)
    
    def decrypt_model(
        self, 
        encrypted_model: Dict[str, Dict[str, Any]]
    ) -> Dict[str, torch.Tensor]:
        """Decrypt a homomorphically encrypted model
        
        Args:
            encrypted_model: Encrypted model state dictionary
            
        Returns:
            Decrypted model state dictionary
        """
        return self.he.decrypt_model(encrypted_model)
    
    def generate_proof(
        self,
        model: Dict[str, torch.Tensor],
        statement: str
    ) -> Dict[str, Union[str, bytes]]:
        """Generate a zero-knowledge proof for a model
        
        Args:
            model: Model state dictionary to prove properties about
            statement: The statement to prove about the model
            
        Returns:
            Dictionary containing the proof
        """
        # Convert tensors to numpy arrays
        numpy_model = {k: v.detach().cpu().numpy() for k, v in model.items()}
        return self.zkp.generate_proof(numpy_model, statement)
    
    def verify_proof(
        self,
        proof: Dict[str, Union[str, bytes]],
        statement: str
    ) -> bool:
        """Verify a zero-knowledge proof
        
        Args:
            proof: The proof to verify
            statement: The statement being proved
            
        Returns:
            True if the proof is valid, False otherwise
        """
        return self.zkp.verify_proof(proof, statement)
    
    def aggregate_encrypted_models(
        self,
        encrypted_models: List[Dict[str, Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Any]]:
        """Aggregate homomorphically encrypted models
        
        Args:
            encrypted_models: List of encrypted model state dictionaries
            
        Returns:
            Aggregated encrypted model state dictionary
        """
        return self.he.aggregate_encrypted_models(encrypted_models) 