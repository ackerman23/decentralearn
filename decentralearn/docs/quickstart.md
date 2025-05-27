# DecentraLearn Quick Start Guide

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- Ganache CLI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/decentralearn.git
cd decentralearn
```

2. Install Node.js dependencies:
```bash
cd contracts
npm install
```

3. Install Python dependencies:
```bash
cd ..
pip install -r requirements.txt
```

## Development Setup

1. Start Ganache:
```bash
ganache --deterministic
```

2. Compile the smart contract:
```bash
cd contracts
npm run compile
```

3. Run tests:
```bash
cd ..
python -m pytest tests/contracts/test_decentralearn.py -v
```

## Contract Interaction

### 1. Staking ETH

```python
from web3 import Web3

# Connect to local blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load contract
with open('contracts/build/DecentraLearn.json') as f:
    contract_json = json.load(f)

contract = w3.eth.contract(
    address='YOUR_CONTRACT_ADDRESS',
    abi=contract_json['abi']
)

# Stake 1 ETH
amount = Web3.to_wei(1, 'ether')
tx_hash = contract.functions.stake().transact({
    'from': w3.eth.accounts[0],
    'value': amount
})
```

### 2. Adding Rewards

```python
# Add 0.1 ETH as rewards
reward_amount = Web3.to_wei(0.1, 'ether')
tx_hash = contract.functions.addRewards().transact({
    'from': w3.eth.accounts[0],  # Must be contract owner
    'value': reward_amount
})
```

### 3. Claiming Rewards

```python
# Claim rewards
tx_hash = contract.functions.claimRewards().transact({
    'from': w3.eth.accounts[0]
})
```

### 4. Withdrawing Stake

```python
# Withdraw entire stake
tx_hash = contract.functions.withdraw().transact({
    'from': w3.eth.accounts[0]
})
```

## Common Operations

### Check User's Stake

```python
stake = contract.functions.getUserStake(user_address).call()
print(f"Stake: {Web3.from_wei(stake, 'ether')} ETH")
```

### Check User's Rewards

```python
rewards = contract.functions.getUserRewards(user_address).call()
print(f"Rewards: {Web3.from_wei(rewards, 'ether')} ETH")
```

### Monitor Events

```python
# Get stake events
stake_filter = contract.events.Staked.create_filter(fromBlock=0)
stake_events = stake_filter.get_all_entries()

# Get reward claim events
claim_filter = contract.events.RewardsClaimed.create_filter(fromBlock=0)
claim_events = claim_filter.get_all_entries()
```

## Troubleshooting

1. **Ganache Connection Issues**
   - Ensure Ganache is running on port 8545
   - Check if another process is using the port
   - Try restarting Ganache

2. **Compilation Errors**
   - Verify Node.js dependencies are installed
   - Check Solidity version compatibility
   - Ensure OpenZeppelin contracts are available

3. **Test Failures**
   - Check Ganache is running with `--deterministic` flag
   - Verify account balances are sufficient
   - Check for proper gas estimation

## Best Practices

1. **Local Development**
   - Always use a local blockchain for testing
   - Keep test accounts funded
   - Monitor gas usage

2. **Contract Interaction**
   - Always check transaction receipts
   - Handle errors gracefully
   - Monitor events for state changes

3. **Security**
   - Never expose private keys
   - Validate all inputs
   - Test edge cases thoroughly 