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

    enum Status {Active, Deprecated, Expired}
    struct Pool {
        address addr;
        Status status;
    }

    Pool[] private _pools;

    function getPoolsCount() public view returns (uint256) {
        return _pools.length;
    }

    function getPoolById(uint256 id) external view returns (address, Status) {
        return (_pools[id].addr, _pools[id].status);
    }

    function addPool(address newPoolAddress) external onlyOwner {
        _pools.push(Pool(newPoolAddress, Status.Active));
    }

    function setStatusPool(uint256 id, Status status) external onlyOwner {
        _pools[id].status = status;
    }
}
