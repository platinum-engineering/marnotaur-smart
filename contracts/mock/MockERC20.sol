// SPDX-License-Identifier: MIT
// Gearbox. Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";

contract TokenMock is ERC20 {
    constructor(string memory name_,
        string memory symbol_) ERC20(name_, symbol_) public {
        _mint(msg.sender, 1000000000000000000000000000);

    }
}
