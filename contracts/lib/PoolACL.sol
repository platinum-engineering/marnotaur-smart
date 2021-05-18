// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.6.10;
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";

contract PoolACL is Ownable{

    mapping(address => bool) private _poolServices;

    modifier onlyPoolService() {
        require(_poolServices[msg.sender], "Allowed for pool services only");
        _;
    }

    function addToPoolServicesList(address poolService) external onlyOwner{
        _poolServices[poolService] = true;
    }
}
