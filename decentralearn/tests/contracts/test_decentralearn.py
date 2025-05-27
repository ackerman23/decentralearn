import pytest
from web3 import Web3
import json
import os

@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

@pytest.fixture
def accounts(w3):
    return w3.eth.accounts

@pytest.fixture
def contract_path():
    return os.path.join(os.path.dirname(__file__), '../../contracts/build/DecentraLearn.json')

@pytest.fixture
def contract(w3, accounts, contract_path):
    with open(contract_path) as f:
        contract_json = json.load(f)
    
    contract = w3.eth.contract(
        abi=contract_json['abi'],
        bytecode=contract_json['bytecode']
    )
    
    tx_hash = contract.constructor().transact({'from': accounts[0]})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_json['abi']
    )

def test_initial_state(contract, accounts):
    assert contract.functions.owner().call() == accounts[0]
    assert contract.functions.totalStaked().call() == 0
    assert contract.functions.totalRewards().call() == 0

def test_stake(contract, accounts, w3):
    amount = Web3.to_wei(1, 'ether')
    
    # Stake tokens
    tx_hash = contract.functions.stake().transact({
        'from': accounts[1],
        'value': amount
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Check staking state
    assert contract.functions.totalStaked().call() == amount
    assert contract.functions.stakes(accounts[1]).call() == amount
    assert contract.functions.stakeTimestamps(accounts[1]).call() > 0

def test_withdraw(contract, accounts, w3):
    amount = Web3.to_wei(1, 'ether')
    
    # Stake first
    tx_hash = contract.functions.stake().transact({
        'from': accounts[1],
        'value': amount
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Withdraw
    tx_hash = contract.functions.withdraw().transact({
        'from': accounts[1]
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Check withdrawal state
    assert contract.functions.totalStaked().call() == 0
    assert contract.functions.stakes(accounts[1]).call() == 0
    assert contract.functions.stakeTimestamps(accounts[1]).call() == 0

def test_claim_rewards(contract, accounts, w3):
    amount = Web3.to_wei(1, 'ether')
    
    # Stake first
    tx_hash = contract.functions.stake().transact({
        'from': accounts[1],
        'value': amount
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Add rewards
    reward_amount = Web3.to_wei(0.1, 'ether')
    tx_hash = contract.functions.addRewards().transact({
        'from': accounts[0],
        'value': reward_amount
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Get initial balance
    initial_balance = w3.eth.get_balance(accounts[1])
    
    # Claim rewards
    tx_hash = contract.functions.claimRewards().transact({
        'from': accounts[1]
    })
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Calculate gas cost
    gas_cost = receipt.gasUsed * w3.eth.gas_price
    
    # Check final balance increased by reward amount minus gas cost
    final_balance = w3.eth.get_balance(accounts[1])
    balance_change = final_balance - initial_balance
    expected_change = reward_amount - gas_cost
    
    # Allow for a small margin of error in gas calculation
    assert abs(balance_change - expected_change) < Web3.to_wei(0.001, 'ether')
    
    # Check rewards state
    assert contract.functions.totalRewards().call() == 0  # All rewards claimed
    assert contract.functions.rewards(accounts[1]).call() == reward_amount 