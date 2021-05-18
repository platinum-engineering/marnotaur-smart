// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.6.10;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "../lib/AddressStorage.sol";

/**
 * @title AddressRepository
 * @notice Stores addresses of deployed contracts
 * @author Platinum Forked
 */
contract AddressRepository is Ownable, AddressStorage {
    // Repositories & services
    bytes32 private constant POOL_REPOSITORY = "POOL_REPOSITORY";
    bytes32 private constant POSITION_REPOSITORY = "POSITION_REPOSITORY";
    bytes32 private constant PRICE_REPOSITORY = "PRICE_REPOSITORY";

    // External swap services
    bytes32 private constant UNISWAP_ROUTER = "UNISWAP_ROUTER";

    /**
     * @dev returns the address of the LendingPool proxy
     * @return the lending pool proxy address
     **/

    function getPoolRepository() public view returns (address) {
        return getAddress(POOL_REPOSITORY);
    }

    function setPoolRepository(address _address) public onlyOwner {
        _setAddress(POOL_REPOSITORY, _address);
    }

    function getPositionRepository() public view returns (address) {
        return getAddress(POSITION_REPOSITORY);
    }

    function setPositionRepository(address _address) public onlyOwner {
        _setAddress(POSITION_REPOSITORY, _address);
    }

    function getPriceRepository() public view returns (address) {
        return getAddress(PRICE_REPOSITORY);
    }

    function setPriceRepository(address _address) public onlyOwner {
        _setAddress(PRICE_REPOSITORY, _address);
    }

    function getUniswapRouter() public view returns (address) {
        return getAddress(UNISWAP_ROUTER);
    }

    function setUniswapRouter(address _address) public onlyOwner {
        _setAddress(UNISWAP_ROUTER, _address);
    }




}
