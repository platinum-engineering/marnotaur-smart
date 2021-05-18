// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "../../interfaces/AggregatorV3Interface.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../repository/AddressRepository.sol";
import "./IPriceRepository.sol";
import "../lib/PoolACL.sol";
import "../lib/console.sol";

/**
 * @title Price Repository
 * @author Platinum Forked
 * @notice Stores Prices from Chainlink and cache them
 * @dev Do not use in mainnet.
 */
contract PriceRepository is Ownable, IPriceRepository, PoolACL {
    using SafeMath for uint256;

    mapping(address => mapping(address => AggregatorV3Interface)) _oracles;

    // And new source of prices for tokens
    function addPriceFeed(address token1,
        address token2,
        address priceFeedContract) external override onlyPoolService {
        _oracles[token1][token2] = AggregatorV3Interface(priceFeedContract);
    }

    function getLastPrice(address token1, address token2) external view override returns (uint256) {

        if (token1 == token2) return 1;

        require(address(_oracles[token1][token2]) != address(0), "Oracle doesn't exists");

        (
        uint80 roundID,
        int price,
        uint startedAt,
        uint timeStamp,
        uint80 answeredInRound
        ) = _oracles[token1][token2].latestRoundData();


        return uint256(price);


    }

}
