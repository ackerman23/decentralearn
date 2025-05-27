"""
Tests for the IncentivePool smart contract
"""
import pytest
import json
from eth_utils import to_wei

# Transaction parameters
TX_PARAMS = {
    'gas': 6000000,  # Reasonable gas limit for contract deployment
    'gasPrice': 875000000  # 0.875 gwei to match base fee
}

@pytest.fixture
def reward_token(w3, accounts):
    """Deploy a test ERC20 token"""
    # Deploy TestToken contract
    with open('decentralearn/contracts/artifacts/TestToken.json') as f:
        contract_json = json.load(f)
    
    # Ensure bytecode has 0x prefix
    bytecode = contract_json['bytecode']
    if not bytecode.startswith('0x'):
        bytecode = '0x' + bytecode
    
    print("Deploying TestToken contract...")
    contract = w3.eth.contract(
        abi=contract_json['abi'],
        bytecode=bytecode
    )
    
    # Deploy contract
    tx_hash = contract.constructor(
        'Test Token',
        'TEST',
        to_wei(1000000, 'ether')
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"TestToken deployed at {tx_receipt.contractAddress}")
    print(f"Transaction status: {tx_receipt.status}")
    print(f"Gas used: {tx_receipt.gasUsed}")
    
    token = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_json['abi']
    )
    
    # Verify deployment
    name = token.functions.name().call()
    symbol = token.functions.symbol().call()
    total_supply = token.functions.totalSupply().call()
    print(f"Token name: {name}")
    print(f"Token symbol: {symbol}")
    print(f"Total supply: {total_supply}")
    
    return token

@pytest.fixture
def incentive_pool(w3, accounts, reward_token):
    """Deploy the IncentivePool contract"""
    # Deploy IncentivePool contract
    with open('decentralearn/contracts/artifacts/IncentivePool.json') as f:
        contract_json = json.load(f)
    
    # Ensure bytecode has 0x prefix
    bytecode = contract_json['bytecode']
    if not bytecode.startswith('0x'):
        bytecode = '0x' + bytecode
    
    print("Deploying IncentivePool contract...")
    contract = w3.eth.contract(
        abi=contract_json['abi'],
        bytecode=bytecode
    )
    
    # Deploy contract
    tx_hash = contract.constructor(
        reward_token.address
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"IncentivePool deployed at {tx_receipt.contractAddress}")
    print(f"Transaction status: {tx_receipt.status}")
    print(f"Gas used: {tx_receipt.gasUsed}")
    
    pool = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_json['abi']
    )
    
    # Fund the pool with rewards
    print("Funding pool with rewards...")
    tx_hash = reward_token.functions.transfer(
        pool.address,
        to_wei(100000, 'ether')
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Funding transaction status: {tx_receipt.status}")
    print(f"Gas used: {tx_receipt.gasUsed}")
    
    # Verify funding
    pool_balance = reward_token.functions.balanceOf(pool.address).call()
    print(f"Pool balance: {pool_balance}")
    
    return pool

def test_record_contribution(w3, accounts, incentive_pool):
    """Test recording a contribution"""
    # Record contribution
    print("Recording contribution...")
    tx = incentive_pool.functions.recordContribution(
        accounts[1],
        80  # Score out of 100
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    
    # Wait for transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx)
    print(f"Transaction status: {tx_receipt.status}")
    print(f"Gas used: {tx_receipt.gasUsed}")
    
    # Verify contribution was recorded
    score, claimed = incentive_pool.functions.getContribution(1, accounts[1]).call()
    assert score == 80
    assert not claimed
    
    # Verify round info
    total_reward, total_score, finalized = incentive_pool.functions.getRoundInfo(1).call()
    assert total_score == 80
    assert not finalized

def test_finalize_round(w3, accounts, incentive_pool):
    """Test finalizing a round"""
    # Record contribution
    tx1 = incentive_pool.functions.recordContribution(
        accounts[1],
        80
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx1)
    
    # Finalize round
    reward = to_wei(1000, 'ether')
    tx2 = incentive_pool.functions.finalizeRound(reward).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx2)
    
    # Verify round was finalized
    total_reward, total_score, finalized = incentive_pool.functions.getRoundInfo(1).call()
    assert total_reward == reward
    assert total_score == 80
    assert finalized
    
    # Verify current round increased
    current_round = incentive_pool.functions.currentRound().call()
    assert current_round == 2

def test_claim_reward(w3, accounts, incentive_pool, reward_token):
    """Test claiming rewards"""
    # Record contribution and finalize round
    tx1 = incentive_pool.functions.recordContribution(
        accounts[1],
        80
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx1)
    
    reward = to_wei(1000, 'ether')
    tx2 = incentive_pool.functions.finalizeRound(reward).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx2)
    
    # Get initial balance
    initial_balance = reward_token.functions.balanceOf(accounts[1]).call()
    
    # Claim reward
    tx3 = incentive_pool.functions.claimReward(1).transact({
        'from': accounts[1],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx3)
    
    # Verify reward was claimed
    final_balance = reward_token.functions.balanceOf(accounts[1]).call()
    assert final_balance == initial_balance + reward  # Full reward since only participant
    
    # Verify contribution marked as claimed
    score, claimed = incentive_pool.functions.getContribution(1, accounts[1]).call()
    assert claimed

def test_multiple_participants(w3, accounts, incentive_pool, reward_token):
    """Test reward distribution with multiple participants"""
    # Record contributions
    tx1 = incentive_pool.functions.recordContribution(
        accounts[1],
        80  # 80% of reward
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx1)
    
    tx2 = incentive_pool.functions.recordContribution(
        accounts[2],
        20  # 20% of reward
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx2)
    
    # Finalize round
    reward = to_wei(1000, 'ether')
    tx3 = incentive_pool.functions.finalizeRound(reward).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx3)
    
    # Get initial balances
    balance1 = reward_token.functions.balanceOf(accounts[1]).call()
    balance2 = reward_token.functions.balanceOf(accounts[2]).call()
    
    # Claim rewards
    tx4 = incentive_pool.functions.claimReward(1).transact({
        'from': accounts[1],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx4)
    
    tx5 = incentive_pool.functions.claimReward(1).transact({
        'from': accounts[2],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx5)
    
    # Verify rewards were distributed proportionally
    final_balance1 = reward_token.functions.balanceOf(accounts[1]).call()
    final_balance2 = reward_token.functions.balanceOf(accounts[2]).call()
    
    assert final_balance1 == balance1 + (reward * 80 // 100)  # 80% of reward
    assert final_balance2 == balance2 + (reward * 20 // 100)  # 20% of reward

def test_invalid_operations(w3, accounts, incentive_pool):
    """Test invalid operations are rejected"""
    # Try to record invalid score
    with pytest.raises(Exception):
        incentive_pool.functions.recordContribution(
            accounts[1],
            101  # Score > 100
        ).transact({
            'from': accounts[0],
            **TX_PARAMS
        })
    
    # Try to finalize round without contributions
    with pytest.raises(Exception):
        incentive_pool.functions.finalizeRound(
            to_wei(1000, 'ether')
        ).transact({
            'from': accounts[0],
            **TX_PARAMS
        })
    
    # Record a contribution
    tx1 = incentive_pool.functions.recordContribution(
        accounts[1],
        80
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx1)
    
    # Try to record duplicate contribution
    with pytest.raises(Exception):
        incentive_pool.functions.recordContribution(
            accounts[1],
            90
        ).transact({
            'from': accounts[0],
            **TX_PARAMS
        })
    
    # Finalize round
    tx2 = incentive_pool.functions.finalizeRound(
        to_wei(1000, 'ether')
    ).transact({
        'from': accounts[0],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx2)
    
    # Try to finalize again
    with pytest.raises(Exception):
        incentive_pool.functions.finalizeRound(
            to_wei(1000, 'ether')
        ).transact({
            'from': accounts[0],
            **TX_PARAMS
        })
    
    # Claim reward
    tx3 = incentive_pool.functions.claimReward(1).transact({
        'from': accounts[1],
        **TX_PARAMS
    })
    w3.eth.wait_for_transaction_receipt(tx3)
    
    # Try to claim again
    with pytest.raises(Exception):
        incentive_pool.functions.claimReward(1).transact({
            'from': accounts[1],
            **TX_PARAMS
        }) 