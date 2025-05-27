// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IERC20.sol";

contract IncentivePool {
    IERC20 public rewardToken;
    address public owner;
    
    struct Round {
        uint256 totalReward;
        uint256 totalScore;
        bool finalized;
    }
    
    mapping(uint256 => Round) public rounds;
    mapping(uint256 => mapping(address => uint256)) public scores;
    mapping(uint256 => mapping(address => bool)) public claimed;
    uint256 public currentRound;
    
    event ContributionRecorded(uint256 indexed round, address indexed participant, uint256 score);
    event RoundFinalized(uint256 indexed round, uint256 totalReward);
    event RewardClaimed(uint256 indexed round, address indexed participant, uint256 amount);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor(address _rewardToken) {
        rewardToken = IERC20(_rewardToken);
        owner = msg.sender;
        currentRound = 1;
    }
    
    function recordContribution(address participant, uint256 score) external onlyOwner {
        require(score <= 100, "Score must be <= 100");
        require(!rounds[currentRound].finalized, "Round finalized");
        require(scores[currentRound][participant] == 0, "Already contributed");
        
        scores[currentRound][participant] = score;
        rounds[currentRound].totalScore += score;
        
        emit ContributionRecorded(currentRound, participant, score);
    }
    
    function finalizeRound(uint256 reward) external onlyOwner {
        require(!rounds[currentRound].finalized, "Round finalized");
        require(rounds[currentRound].totalScore > 0, "No contributions");
        
        rounds[currentRound].totalReward = reward;
        rounds[currentRound].finalized = true;
        
        emit RoundFinalized(currentRound, reward);
        currentRound++;
    }
    
    function claimReward(uint256 round) external {
        require(round < currentRound, "Invalid round");
        require(rounds[round].finalized, "Round not finalized");
        require(!claimed[round][msg.sender], "Already claimed");
        require(scores[round][msg.sender] > 0, "No contribution");
        
        uint256 reward = (scores[round][msg.sender] * rounds[round].totalReward) / rounds[round].totalScore;
        require(reward > 0, "No reward");
        
        claimed[round][msg.sender] = true;
        require(rewardToken.transfer(msg.sender, reward), "Transfer failed");
        
        emit RewardClaimed(round, msg.sender, reward);
    }
    
    function getRoundInfo(uint256 round) external view returns (uint256 totalReward, uint256 totalScore, bool finalized) {
        Round storage r = rounds[round];
        return (r.totalReward, r.totalScore, r.finalized);
    }
    
    function getContribution(uint256 round, address participant) external view returns (uint256 score, bool isClaimed) {
        return (scores[round][participant], claimed[round][participant]);
    }
} 