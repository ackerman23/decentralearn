"""
Blockchain configuration settings for DecentraLearn
This module provides configuration settings for blockchain integration, including RPC endpoints,
contract addresses, and network parameters.

Because even blockchains need their settings just right - not too hot, not too cold.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class BlockchainConfig:
    """Blockchain configuration settings
    
    This class holds all the important numbers and addresses that make the blockchain
    tick. Think of it as the blockchain's personal assistant.
    """
    rpc_url: str = "http://127.0.0.1:8545"  # The blockchain's home address
    chain_id: int = 1337  # Because we're 1337 hackers
    gas_limit: int = 6721975  # The maximum amount of gas we're willing to burn
    gas_price: int = 20000000000  # 20 Gwei - because we're fancy like that
    
    # Contract addresses (to be set after deployment)
    # These are like the blockchain's phone numbers - don't lose them!
    fl_contract_address: Optional[str] = None
    model_registry_address: Optional[str] = None

# Default configuration - for when you just want things to work
default_config = BlockchainConfig() 