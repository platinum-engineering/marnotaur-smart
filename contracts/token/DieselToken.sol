// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";

contract DieselToken is ERC20, Ownable {
    constructor(string memory name_, string memory symbol_) ERC20(name_, symbol_) public {

    }

    function mint(address to, uint256 amount ) external onlyOwner {
        _mint(to, amount);
    }

    function burn(address to, uint256 amount ) external onlyOwner {
        _burn(to, amount);
    }
}
