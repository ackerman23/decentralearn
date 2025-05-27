// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FLContract {
    address public owner;
    mapping(address => bool) public registeredClients;
    mapping(address => string) public clientModelHashes;
    address[] public clientList;
    
    event ClientRegistered(address indexed client);
    event ModelSubmitted(address indexed client, string modelHash);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyRegisteredClient() {
        require(registeredClients[msg.sender], "Client not registered");
        _;
    }
    
    function registerClient(address client) public onlyOwner returns (bool) {
        require(!registeredClients[client], "Client already registered");
        registeredClients[client] = true;
        clientList.push(client);
        emit ClientRegistered(client);
        return true;
    }
    
    function submitModel(string memory modelHash) public onlyRegisteredClient returns (bool) {
        clientModelHashes[msg.sender] = modelHash;
        emit ModelSubmitted(msg.sender, modelHash);
        return true;
    }
    
    function getModelHash(address client) public view returns (string memory) {
        return clientModelHashes[client];
    }
    
    function getRegisteredClients() public view returns (address[] memory) {
        return clientList;
    }
    
    function verifyModel(address client, string memory modelHash) public view returns (bool) {
        return keccak256(bytes(clientModelHashes[client])) == keccak256(bytes(modelHash));
    }
} 