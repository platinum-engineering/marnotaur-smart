// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../repository/AddressRepository.sol";
import "./IPriceRepository.sol";
import "../lib/PoolACL.sol";
import "../lib/console.sol";

/**
 * @title Price Repository
 * @author PLatinum Forked
 * @notice Stores Prices from Chainlink and cache them
 * @dev Do not use in mainnet.
 */
contract PriceRepositoryMock is Ownable, IPriceRepository, PoolACL {
    using SafeMath for uint256;

    mapping(address => mapping(address => bool)) _oracles;

    function addPriceFeed(address token1,
        address token2,
        address priceFeedContract) external override onlyPoolService {
        _oracles[token1][token2] = true;
    }

    function getLastPrice(address token1, address token2) external  view override returns (uint256) {

        if (token1 == token2) return 1;

        require(_oracles[token1][token2], "Oracle doesn't exists");

        return 1000;

    }

}
