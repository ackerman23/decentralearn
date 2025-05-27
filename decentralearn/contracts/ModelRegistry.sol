// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelRegistry {
    struct ModelMetadata {
        string name;
        string description;
        string version;
        address owner;
        uint256 timestamp;
        string[] tags;
    }
    
    mapping(string => ModelMetadata) public models;
    mapping(address => string[]) public ownerModels;
    
    event ModelRegistered(string indexed modelId, address indexed owner);
    event ModelUpdated(string indexed modelId, address indexed owner);
    
    function registerModel(
        string memory modelId,
        string memory name,
        string memory description,
        string memory version,
        string[] memory tags
    ) public returns (bool) {
        require(bytes(models[modelId].name).length == 0, "Model ID already exists");
        
        ModelMetadata memory metadata = ModelMetadata({
            name: name,
            description: description,
            version: version,
            owner: msg.sender,
            timestamp: block.timestamp,
            tags: tags
        });
        
        models[modelId] = metadata;
        ownerModels[msg.sender].push(modelId);
        
        emit ModelRegistered(modelId, msg.sender);
        return true;
    }
    
    function updateModel(
        string memory modelId,
        string memory name,
        string memory description,
        string memory version,
        string[] memory tags
    ) public returns (bool) {
        require(models[modelId].owner == msg.sender, "Only model owner can update");
        
        ModelMetadata storage metadata = models[modelId];
        metadata.name = name;
        metadata.description = description;
        metadata.version = version;
        metadata.timestamp = block.timestamp;
        metadata.tags = tags;
        
        emit ModelUpdated(modelId, msg.sender);
        return true;
    }
    
    function getModelMetadata(string memory modelId) public view returns (
        string memory name,
        string memory description,
        string memory version,
        address owner,
        uint256 timestamp,
        string[] memory tags
    ) {
        ModelMetadata memory metadata = models[modelId];
        return (
            metadata.name,
            metadata.description,
            metadata.version,
            metadata.owner,
            metadata.timestamp,
            metadata.tags
        );
    }
    
    function verifyModelOwnership(string memory modelId, address owner) public view returns (bool) {
        return models[modelId].owner == owner;
    }
    
    function getOwnerModels(address owner) public view returns (string[] memory) {
        return ownerModels[owner];
    }
} 