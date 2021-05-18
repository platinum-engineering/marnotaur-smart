// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../repository/AddressRepository.sol";
import "../lib/console.sol";

/**
 * @title Pool Repository
 * @author Platinum Forked
 * @notice Stores all available pools in one place
 * @dev Do not use in mainnet.
 */
contract PoolRepository is Ownable {
    using SafeMath for uint256;

    address[] private _pools;

    function getPoolsCount() public view returns (uint256) {
        return _pools.length;
    }

    function getPoolById(uint256 id) external view returns (address) {
        return _pools[id];
    }

    function addPool(address newPoolAddress) external onlyOwner {
        _pools.push(newPoolAddress);
    }



}
