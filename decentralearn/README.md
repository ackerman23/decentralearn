# DecentraLearn

DecentraLearn is a decentralized learning platform that incentivizes content creation and learning through a staking and rewards system.

## Project Structure

```
decentralearn/
├── contracts/              # Smart contracts
│   ├── DecentraLearn.sol  # Main contract
│   ├── compile.js         # Compilation script
│   └── package.json       # Node.js dependencies
├── tests/                 # Test files
│   └── contracts/         # Smart contract tests
└── requirements.txt       # Python dependencies
```

## Smart Contract Features

- Staking system for content creators
- Reward distribution mechanism
- Withdrawal functionality
- Owner controls for reward management

## Setup and Installation

1. Install Node.js dependencies:
```bash
cd contracts
npm install
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Compile the smart contract:
```bash
cd contracts
npm run compile
```

4. Run the tests:
```bash
cd tests
pytest contracts/
```

## Testing

The project includes comprehensive tests for the smart contract functionality:
- Initial state verification
- Staking operations
- Withdrawal process
- Reward distribution

## License

MIT 