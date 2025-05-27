# Core Components

This document describes the core components of the DecentraLearn framework.

## Overview

DecentraLearn consists of several key components that work together to enable decentralized federated learning:

1. Client Node
2. Blockchain Integration
3. Model Management
4. Dataset Management
5. Privacy Layer
6. Smart Contracts

## 1. Client Node

The client node is responsible for:

- Local model training
- Data preprocessing and management
- Communication with the blockchain
- Model state synchronization
- Privacy mechanism implementation

Key classes:
```python
from decentralearn.blockchain.client import BlockchainClient
from decentralearn.models.base import BaseModel
```

## 2. Blockchain Integration

The blockchain layer handles:

- Model verification
- Client registration
- Incentive distribution
- Smart contract interaction
- Transaction management

Key components:
- `BlockchainClient`: Manages blockchain interactions
- `BlockchainConfig`: Configuration for blockchain connection
- Smart contracts for model verification and incentives

## 3. Model Management

The model management system:

- Handles model serialization/deserialization
- Manages model versioning
- Implements model verification
- Coordinates model updates

Key features:
- JSON serialization for blockchain storage
- State dictionary management
- Model metadata handling
- Version control

## 4. Dataset Management

Dataset management includes:

- Dataset loading and preprocessing
- Data splitting (IID and non-IID)
- Privacy-preserving data handling
- Custom dataset support

Components:
- `DatasetFactory`: Creates and manages datasets
- `DatasetSpliter`: Handles data distribution
- Custom dataset implementations

## 5. Privacy Layer

Privacy mechanisms include:

- Differential Privacy
- Homomorphic Encryption
- Zero-Knowledge Proofs
- Secure Aggregation

Implementation:
```python
from decentralearn.privacy import (
    DifferentialPrivacy,
    HomomorphicEncryption,
    ZeroKnowledgeProof
)
```

## 6. Smart Contracts

Smart contracts manage:

- Model verification
- Client registration
- Incentive distribution
- Access control

Key contracts:
- `FederatedLearningContract`: Main FL coordination
- `ModelVerificationContract`: Model verification
- `IncentiveContract`: Reward distribution

## Component Interaction

The components interact in the following way:

1. Client Node initializes with blockchain connection
2. Dataset Management prepares local data
3. Model Management handles training and updates
4. Privacy Layer ensures secure operations
5. Smart Contracts verify and coordinate
6. Blockchain Integration manages transactions

## Configuration

Components can be configured through:

```python
from decentralearn.config import (
    BlockchainConfig,
    PrivacyConfig,
    ModelConfig,
    DatasetConfig
)
```

## Error Handling

Each component implements robust error handling:

- Network failures
- Invalid transactions
- Data corruption
- Privacy breaches
- Smart contract errors

## Extensibility

Components are designed for extensibility:

- Custom model implementations
- New privacy mechanisms
- Additional smart contracts
- Custom dataset types

## Best Practices

When working with components:

1. Always initialize blockchain connection first
2. Implement proper error handling
3. Use privacy mechanisms appropriately
4. Follow smart contract upgrade patterns
5. Maintain proper configuration

## See Also

- [Data Flow](data_flow.md)
- [Security Model](security.md)
- [API Reference](../api/README.md) 