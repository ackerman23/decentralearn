# DecentraLearn Technical Documentation

## Table of Contents
1. [Overview](#overview)
2. [Smart Contract Architecture](#smart-contract-architecture)
3. [Contract Features](#contract-features)
4. [Development Environment](#development-environment)
5. [Testing Infrastructure](#testing-infrastructure)
6. [Contract Deployment](#contract-deployment)
7. [Security Considerations](#security-considerations)

## Overview

DecentraLearn is a decentralized learning platform that implements a staking and rewards mechanism using smart contracts. The system allows users to stake tokens, earn rewards based on their stake proportion, and withdraw their stakes and rewards securely.

## Smart Contract Architecture

### Core Contract: DecentraLearn.sol

The main contract inherits from two OpenZeppelin contracts:
- `ReentrancyGuard`: Prevents reentrant calls to critical functions
- `Ownable`: Provides basic access control mechanism

### State Variables
```solidity
uint256 public totalStaked;        // Total amount staked by all users
uint256 public totalRewards;       // Total available rewards
mapping(address => uint256) public stakes;           // User stakes
mapping(address => uint256) public stakeTimestamps;  // Stake timestamps
mapping(address => uint256) public rewards;          // User rewards
```

### Events
```solidity
event Staked(address indexed user, uint256 amount);
event Withdrawn(address indexed user, uint256 amount);
event RewardsAdded(uint256 amount);
event RewardsClaimed(address indexed user, uint256 amount);
```

## Contract Features

### 1. Staking Mechanism
```solidity
function stake() external payable nonReentrant
```
- Allows users to stake ETH
- Updates user's stake and total staked amount
- Records stake timestamp
- Emits `Staked` event
- Protected against reentrancy attacks

### 2. Withdrawal System
```solidity
function withdraw() external nonReentrant
```
- Allows users to withdraw their entire stake
- Resets user's stake and timestamp
- Updates total staked amount
- Protected against reentrancy attacks
- Includes transfer success verification

### 3. Rewards Distribution
```solidity
function addRewards() external payable onlyOwner
```
- Allows contract owner to add rewards
- Updates total rewards pool
- Emits `RewardsAdded` event

```solidity
function claimRewards() external nonReentrant
```
- Calculates rewards based on stake proportion
- Updates user's rewards and total rewards
- Includes transfer success verification
- Protected against reentrancy attacks

### 4. View Functions
```solidity
function getUserRewards(address user) external view returns (uint256)
function getUserStake(address user) external view returns (uint256)
```
- Provide read-only access to user data
- Gas-efficient state queries

## Development Environment

### Dependencies
1. Node.js packages (package.json):
```json
{
  "dependencies": {
    "@openzeppelin/contracts": "^4.9.0"
  },
  "devDependencies": {
    "solc": "^0.8.20"
  }
}
```

2. Python packages (requirements.txt):
```
web3==6.11.1
eth-account==0.9.0
pytest==7.4.3
```

### Compilation Infrastructure

The contract compilation is handled by `compile.js`:
- Uses solc compiler version 0.8.20
- Handles OpenZeppelin imports
- Includes optimization settings
- Outputs ABI and bytecode
- Creates build directory for compiled artifacts

## Testing Infrastructure

### Test Environment
- Uses Ganache for local blockchain simulation
- Pytest for test organization and execution
- Web3.py for blockchain interaction

### Test Fixtures
```python
@pytest.fixture
def w3():
    return Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

@pytest.fixture
def accounts(w3):
    return w3.eth.accounts

@pytest.fixture
def contract(w3, accounts, contract_path):
    # Contract deployment logic
```

### Test Cases

1. Initial State Test
```python
def test_initial_state(contract, accounts):
    assert contract.functions.owner().call() == accounts[0]
    assert contract.functions.totalStaked().call() == 0
    assert contract.functions.totalRewards().call() == 0
```
- Verifies correct contract initialization
- Checks owner assignment
- Validates initial state variables

2. Staking Test
```python
def test_stake(contract, accounts, w3):
    amount = Web3.to_wei(1, 'ether')
    # Staking logic and assertions
```
- Tests stake functionality
- Verifies state updates
- Checks event emission

3. Withdrawal Test
```python
def test_withdraw(contract, accounts, w3):
    # Withdrawal logic and assertions
```
- Tests withdrawal mechanism
- Verifies state resets
- Checks balance updates

4. Rewards Test
```python
def test_claim_rewards(contract, accounts, w3):
    # Rewards distribution logic and assertions
```
- Tests reward distribution
- Verifies balance changes
- Accounts for gas costs
- Checks reward state updates

## Security Considerations

1. Reentrancy Protection
- All state-changing functions are protected with `nonReentrant` modifier
- State changes occur before external calls

2. Access Control
- Owner-only functions protected by `onlyOwner` modifier
- Clear separation of privileges

3. Safe Math
- Uses Solidity 0.8.20's built-in overflow protection
- Proper division ordering in reward calculations

4. Transfer Safety
- All ETH transfers use low-level call
- Success checks on all transfers
- Proper error handling

5. Gas Optimization
- Efficient state variable usage
- View functions for read-only operations
- Optimized compilation settings

## Contract Deployment

### Prerequisites
1. Install dependencies:
```bash
cd contracts && npm install
cd .. && pip install -r requirements.txt
```

2. Compile contract:
```bash
cd contracts && npm run compile
```

3. Run tests:
```bash
python -m pytest tests/contracts/test_decentralearn.py -v
```

### Deployment Process
1. Ensure Ganache is running:
```bash
ganache --deterministic
```

2. Deploy contract using deployment script
3. Verify contract on block explorer
4. Set up initial parameters

## Error Handling

The contract includes comprehensive error handling:
- Require statements with clear error messages
- Event emission for tracking
- Transfer success verification
- Gas limit considerations

## Future Improvements

1. Time-based Rewards
- Implement time-weighted rewards
- Add vesting periods

2. Multiple Token Support
- Add ERC20 token support
- Implement multi-token staking

3. Governance Features
- Add DAO functionality
- Implement proposal system

4. Enhanced Security
- Add emergency pause
- Implement upgrade proxy
- Add rate limiting 