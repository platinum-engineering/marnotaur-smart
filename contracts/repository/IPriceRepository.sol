// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

/**
 * @title Price Repository interface
 * @author Platinum Forked
 * @notice Interface for price repository
 * @dev Do not use in mainnet.
 */
interface IPriceRepository {

    function addPriceFeed(address token1,
        address token2,
        address priceFeedContract) external;

    function getLastPrice(address token1, address token2) external view returns (uint256);

}
