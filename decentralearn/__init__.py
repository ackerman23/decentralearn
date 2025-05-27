"""
DecentraLearn Smart Contracts Module
This is the main package for DecentraLearn, a decentralized federated learning platform.
It provides tools and interfaces for secure, transparent, and efficient federated learning
with blockchain integration.
"""

from .contracts import FLContract, ModelRegistry
from .blockchain.client import BlockchainClient
from .models.base import BaseModel
from .config.blockchain_config import BlockchainConfig

__all__ = [
    'FLContract',
    'ModelRegistry',
    'BlockchainClient',
    'BaseModel',
    'BlockchainConfig'
]
