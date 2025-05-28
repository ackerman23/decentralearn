"""
Smart contract interfaces for DecentraLearn
This module provides interfaces for interacting with DecentraLearn's smart contracts,
including the FL contract and Model Registry.
"""
from .fl_contract import FLContract
from .model_registry import ModelRegistry

__all__ = ['FLContract', 'ModelRegistry'] 