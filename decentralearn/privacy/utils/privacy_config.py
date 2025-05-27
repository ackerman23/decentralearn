"""
Privacy Configuration for DecentraLearn
This module provides configuration settings for privacy mechanisms.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class PrivacyConfig:
    """Configuration settings for privacy mechanisms
    
    This class holds all configuration parameters for the privacy mechanisms
    used in the system, including differential privacy, homomorphic encryption,
    and zero-knowledge proofs.
    """
    # Differential Privacy settings
    dp_epsilon: float = 1.0  # Privacy budget
    dp_delta: float = 1e-5   # Failure probability
    
    # Homomorphic Encryption settings
    he_key_size: int = 2048  # Key size in bits
    he_scheme: str = "paillier"  # Encryption scheme
    
    # Zero-Knowledge Proof settings
    zkp_protocol: str = "zk-snark"  # Proof protocol
    
    # Optional settings
    dp_clip_norm: Optional[float] = None  # Gradient clipping norm
    he_parallel: bool = True  # Use parallel encryption
    zkp_curve: Optional[str] = None  # Elliptic curve for ZKP
    
    def validate(self) -> bool:
        """Validate the configuration settings
        
        Returns:
            True if settings are valid, False otherwise
        """
        # Validate DP settings
        if self.dp_epsilon <= 0 or self.dp_delta <= 0:
            return False
        
        # Validate HE settings
        if self.he_key_size not in [1024, 2048, 4096]:
            return False
        if self.he_scheme not in ["paillier", "bfv", "ckks"]:
            return False
        
        # Validate ZKP settings
        if self.zkp_protocol not in ["zk-snark", "zk-stark", "bulletproofs"]:
            return False
        
        return True 