// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SpatSubscription is Ownable {
    IERC20 public spatToken;
    // Set to 100,000 tokens (assuming 18 decimals)
    uint256 public monthlyRate = 100_000 * 10**18; 
    
    mapping(address => uint256) public subscriptionExpiry;

    event Subscribed(address indexed user, uint256 expiry);

    constructor(address _spatToken) Ownable(msg.sender) {
        spatToken = IERC20(_spatToken);
    }

    function subscribe(uint256 months) external {
        require(months > 0, "Minimum 1 month");
        uint256 totalCost = monthlyRate * months;
        
        require(spatToken.transferFrom(msg.sender, address(this), totalCost), "Transfer failed");

        uint256 currentExpiry = subscriptionExpiry[msg.sender];
        uint256 startTime = currentExpiry > block.timestamp ? currentExpiry : block.timestamp;
        
        subscriptionExpiry[msg.sender] = startTime + (months * 30 days);
        
        emit Subscribed(msg.sender, subscriptionExpiry[msg.sender]);
    }

    function isActive(address user) public view returns (bool) {
        return subscriptionExpiry[user] > block.timestamp;
    }

    function withdraw() external onlyOwner {
        uint256 balance = spatToken.balanceOf(address(this));
        spatToken.transfer(owner(), balance);
    }

    function setRate(uint256 _newRate) external onlyOwner {
        monthlyRate = _newRate;
    }
}
