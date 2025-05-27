# Smart Contracts Architecture

This document provides a comprehensive overview of DecentraLearn's smart contracts architecture.

## Table of Contents

1. [Contract Overview](#contract-overview)
2. [Core Contracts](#core-contracts)
3. [Contract Interactions](#contract-interactions)
4. [Security Features](#security-features)
5. [Gas Optimization](#gas-optimization)

## Contract Overview

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  ModelRegistry   |<--->|  GradientPool    |<--->|  IncentivePool   |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
         ^                      ^                      ^
         |                      |                      |
         v                      v                      v
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  AccessControl   |     |  DataRegistry    |     |  Verification    |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

## Core Contracts

### 1. ModelRegistry

```solidity
/// @title ModelRegistry
/// @notice Registry for federated learning models
contract ModelRegistry {
    /// @notice Submit a new model
    /// @param modelHash Hash of the model
    /// @param metadata Model metadata
    function submitModel(bytes32 modelHash, bytes memory metadata) external;

    /// @notice Get model information
    /// @param modelHash Hash of the model
    function getModel(bytes32 modelHash) external view returns (ModelInfo memory);

    /// @notice Update model status
    /// @param modelHash Hash of the model
    /// @param status New status
    function updateStatus(bytes32 modelHash, Status status) external;
}
```

### 2. GradientPool

```solidity
/// @title GradientPool
/// @notice Pool for gradient aggregation
contract GradientPool {
    /// @notice Submit gradients
    /// @param modelHash Hash of the model
    /// @param gradients Gradient values
    function submitGradients(bytes32 modelHash, int[] memory gradients) external;

    /// @notice Aggregate gradients
    /// @param modelHash Hash of the model
    function aggregateGradients(bytes32 modelHash) external;

    /// @notice Get aggregated gradients
    /// @param modelHash Hash of the model
    function getAggregatedGradients(bytes32 modelHash) external view returns (int[] memory);
}
```

### 3. IncentivePool

```solidity
/// @title IncentivePool
/// @notice Pool for incentive distribution
contract IncentivePool {
    /// @notice Deposit rewards
    /// @param amount Amount to deposit
    function deposit(uint256 amount) external payable;

    /// @notice Distribute rewards
    /// @param modelHash Hash of the model
    /// @param participants List of participants
    function distributeRewards(bytes32 modelHash, address[] memory participants) external;

    /// @notice Claim rewards
    /// @param modelHash Hash of the model
    function claimRewards(bytes32 modelHash) external;
}
```

## Contract Interactions

### 1. Model Submission Flow

```
1. Client submits model
   ModelRegistry.submitModel()
   ↓
2. Verify model
   Verification.verifyModel()
   ↓
3. Update access control
   AccessControl.grantAccess()
   ↓
4. Initialize gradient pool
   GradientPool.initialize()
```

### 2. Gradient Aggregation Flow

```
1. Submit gradients
   GradientPool.submitGradients()
   ↓
2. Aggregate gradients
   GradientPool.aggregateGradients()
   ↓
3. Update model
   ModelRegistry.updateModel()
   ↓
4. Distribute rewards
   IncentivePool.distributeRewards()
```

### 3. Access Control Flow

```
1. Request access
   AccessControl.requestAccess()
   ↓
2. Verify identity
   Verification.verifyIdentity()
   ↓
3. Grant access
   AccessControl.grantAccess()
   ↓
4. Update registry
   ModelRegistry.updateAccess()
```

## Security Features

### 1. Access Control

```solidity
/// @title AccessControl
/// @notice Access control for contracts
contract AccessControl {
    /// @notice Check if address has role
    /// @param account Address to check
    /// @param role Role to check
    function hasRole(address account, bytes32 role) public view returns (bool);

    /// @notice Grant role to address
    /// @param account Address to grant role
    /// @param role Role to grant
    function grantRole(address account, bytes32 role) external;

    /// @notice Revoke role from address
    /// @param account Address to revoke role
    /// @param role Role to revoke
    function revokeRole(address account, bytes32 role) external;
}
```

### 2. Verification

```solidity
/// @title Verification
/// @notice Verification system for models and identities
contract Verification {
    /// @notice Verify model
    /// @param modelHash Hash of the model
    /// @param proof Proof of verification
    function verifyModel(bytes32 modelHash, bytes memory proof) external;

    /// @notice Verify identity
    /// @param identity Identity to verify
    /// @param proof Proof of identity
    function verifyIdentity(address identity, bytes memory proof) external;

    /// @notice Check verification status
    /// @param target Target to check
    function isVerified(bytes32 target) external view returns (bool);
}
```

### 3. Data Protection

```solidity
/// @title DataRegistry
/// @notice Registry for data management
contract DataRegistry {
    /// @notice Register dataset
    /// @param datasetHash Hash of the dataset
    /// @param metadata Dataset metadata
    function registerDataset(bytes32 datasetHash, bytes memory metadata) external;

    /// @notice Get dataset info
    /// @param datasetHash Hash of the dataset
    function getDataset(bytes32 datasetHash) external view returns (DatasetInfo memory);

    /// @notice Update access permissions
    /// @param datasetHash Hash of the dataset
    /// @param permissions New permissions
    function updatePermissions(bytes32 datasetHash, bytes memory permissions) external;
}
```

## Gas Optimization

### 1. Storage Optimization

```solidity
// Use packed storage
struct ModelInfo {
    address owner;
    uint32 timestamp;
    uint16 version;
    uint8 status;
    bytes32 hash;
}

// Use memory for temporary data
function processGradients(int[] memory gradients) internal {
    uint sum;
    for (uint i = 0; i < gradients.length; i++) {
        sum += uint(gradients[i]);
    }
}
```

### 2. Batch Processing

```solidity
// Process multiple items in one transaction
function batchSubmitGradients(
    bytes32[] memory modelHashes,
    int[][] memory gradients
) external {
    require(modelHashes.length == gradients.length, "Length mismatch");
    
    for (uint i = 0; i < modelHashes.length; i++) {
        submitGradients(modelHashes[i], gradients[i]);
    }
}
```

### 3. Event Usage

```solidity
// Emit events for off-chain processing
event ModelSubmitted(
    bytes32 indexed modelHash,
    address indexed submitter,
    uint256 timestamp
);

event GradientsAggregated(
    bytes32 indexed modelHash,
    uint256 timestamp,
    uint256 participantCount
);
```

## Additional Resources

- [Solidity Documentation](https://docs.soliditylang.org/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Ethereum Gas Optimization](https://ethereum.org/en/developers/docs/gas/)
- [Smart Contract Security](https://consensys.github.io/smart-contract-best-practices/) 