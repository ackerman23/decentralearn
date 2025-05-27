import pytest
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei, decode_hex
from web3 import Web3, EthereumTesterProvider
from eth.constants import GENESIS_DIFFICULTY

@pytest.fixture
def eth_tester():
    """Create EthereumTester instance with custom settings"""
    # Create backend with custom configuration
    genesis_params = {
        'base_fee_per_gas': 875000000,  # Base fee of 0.875 gwei
        'gas_limit': 15_000_000,  # Increased to accommodate contract deployments
        'difficulty': 1,  # Set to 1 for easy mining
        'timestamp': 0,  # Set to 0 for deterministic behavior
    }

    # Set initial balance for test accounts
    test_accounts = [
        '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf',
        '0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF',
        '0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69',
        '0x1efF47bc3a10a45D4B230B5d10E37751FE6AA718',
        '0xe1AB8145F7E55DC933d51a18c793F901A3A0b276'
    ]
    
    # Initialize genesis state with test accounts
    genesis_state = {
        decode_hex(account): {
            'balance': to_wei(1000000, 'ether'),
            'code': b'',
            'nonce': 0,
            'storage': {}
        }
        for account in test_accounts
    }

    backend = PyEVMBackend(
        genesis_parameters=genesis_params,
        genesis_state=genesis_state
    )

    # Create tester with custom backend
    return EthereumTester(backend=backend)

@pytest.fixture
def w3(eth_tester):
    """Create Web3 instance connected to EthereumTester"""
    provider = EthereumTesterProvider(eth_tester)
    w3 = Web3(provider)
    
    # Set high default gas limit and zero gas price
    w3.eth.default_gas = 8_000_000
    w3.eth.gas_price = 0
    
    # Set default account
    w3.eth.default_account = w3.eth.accounts[0]
    
    return w3

@pytest.fixture
def accounts(w3):
    """Get test accounts"""
    return w3.eth.accounts 