// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./Security.sol";

contract DecentraLearn is ReentrancyGuard, Ownable {
    // State variables
    uint256 public totalStaked;
    uint256 public totalRewards;
    mapping(address => uint256) public stakes;
    mapping(address => uint256) public stakeTimestamps;
    mapping(address => uint256) public rewards;

    // Events
    event Staked(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardsAdded(uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);

    constructor() Ownable() {}

    // Stake tokens
    function stake() external payable nonReentrant {
        require(msg.value > 0, "Amount must be greater than 0");
        
        if (stakes[msg.sender] > 0) {
            // If user already has a stake, add to it
            stakes[msg.sender] += msg.value;
        } else {
            // New stake
            stakes[msg.sender] = msg.value;
            stakeTimestamps[msg.sender] = block.timestamp;
        }
        
        totalStaked += msg.value;
        emit Staked(msg.sender, msg.value);
    }

    // Withdraw staked tokens
    function withdraw() external nonReentrant {
        uint256 amount = stakes[msg.sender];
        require(amount > 0, "No stake to withdraw");
        
        // Reset stake
        stakes[msg.sender] = 0;
        stakeTimestamps[msg.sender] = 0;
        totalStaked -= amount;
        
        // Transfer tokens
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit Withdrawn(msg.sender, amount);
    }

    // Add rewards (only owner)
    function addRewards() external payable onlyOwner {
        require(msg.value > 0, "Amount must be greater than 0");
        totalRewards += msg.value;
        emit RewardsAdded(msg.value);
    }

    // Claim rewards
    function claimRewards() external nonReentrant {
        require(stakes[msg.sender] > 0, "No active stake");
        require(totalRewards > 0, "No rewards available");
        
        // Calculate reward based on stake proportion
        uint256 reward = (stakes[msg.sender] * totalRewards) / totalStaked;
        require(reward > 0, "No rewards to claim");
        
        // Update state
        rewards[msg.sender] += reward;
        totalRewards -= reward;
        
        // Transfer rewards
        (bool success, ) = msg.sender.call{value: reward}("");
        require(success, "Transfer failed");
        
        emit RewardsClaimed(msg.sender, reward);
    }

    // Get user's total rewards
    function getUserRewards(address user) external view returns (uint256) {
        return rewards[user];
    }

    // Get user's stake
    function getUserStake(address user) external view returns (uint256) {
        return stakes[user];
    }
} 