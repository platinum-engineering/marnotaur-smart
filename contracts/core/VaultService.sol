// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../repository/AddressRepository.sol";
import "../uniswap/IUniswapV2Router02.sol";
import "../token/DieselToken.sol";
import "../lib/PriceModel.sol";
import "../lib/console.sol";

/**
 * @title Vault Service
 * @author Platinum Forked
 * @notice This vault service manages liquidity for the pool
 * @dev Do not use in mainnet.
 */
contract VaultService is PriceModel, Ownable {
    using SafeMath for uint256;


    uint256 constant MAX_INT =
        0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;

    // Liquidity parameters
    uint256 private _totalLiquidity;
    uint256 private _availableLiquidity;

    /// @dev Token address for vault asset
    address private _underlyingTokenAddress;

    // Repositories
    AddressRepository private _addressRepository;
    DieselToken private _dieselToken;

    // Swap operators
    IUniswapV2Router02 private _uniswapRouter;

    // Liquidity pool
    event AddLiquidity(address indexed sender, uint256 amount);
    event RemoveLiquidity(address indexed sender, uint256 amount);

    constructor(address addressRepository,
        address underlyingTokenAddress,
        address gToken) public {
        _addressRepository = AddressRepository(addressRepository);
        _dieselToken = DieselToken(gToken);
        _underlyingTokenAddress = underlyingTokenAddress;
        _uniswapRouter = IUniswapV2Router02(
            _addressRepository.getUniswapRouter()
        );

        approveOnUniswap(_underlyingTokenAddress);
        _updateCumulativeIndex(S_1);
    }

    function approveOnUniswap(address token) public onlyOwner {
        ERC20(token).approve(address(_uniswapRouter), MAX_INT);
    }

    // Add liquidity to vault
    function addLiquidity(uint256 amount) external {
        ERC20(_underlyingTokenAddress).transferFrom(
            msg.sender,
            address(this),
            amount
        );
        _dieselToken.mint(msg.sender, amount);
        _totalLiquidity = _totalLiquidity.add(amount);
        _availableLiquidity = _availableLiquidity.add(amount);
        _updateCumIndexByLiquidity(_totalLiquidity, _availableLiquidity);
        emit AddLiquidity(msg.sender, amount);
    }

    function removeLiquidity(uint256 amount) external {
        ERC20(_underlyingTokenAddress).transfer(msg.sender, amount);
        _dieselToken.burn(msg.sender, amount);
        _totalLiquidity = _totalLiquidity.sub(amount);
        _availableLiquidity = _availableLiquidity.sub(amount);
        _updateCumIndexByLiquidity(_totalLiquidity, _availableLiquidity);
        emit RemoveLiquidity(msg.sender, amount);
    }

    function updateLeverageOpen(
        address holder,
        uint256 amount,
        uint256 leveragedAmount
    ) external {
        require(leveragedAmount < _availableLiquidity, "Not enough liquidity");
        ERC20(_underlyingTokenAddress).transferFrom(holder, address(this), amount);
        _availableLiquidity = _availableLiquidity.add(amount).sub(
            leveragedAmount
        );
        _totalLiquidity = _totalLiquidity.add(amount);
        _updateCumIndexByLiquidity(_totalLiquidity, _availableLiquidity);
    }

    function updateOnLeverageClose(
        address holder,
        uint256 amountToReturn,
        uint256 backToVault,
        uint256 liquidatorPremium,
        address liquidatorAddress
    ) external {
        ERC20(_underlyingTokenAddress).transfer(
            holder,
            amountToReturn
        );
        _totalLiquidity = _totalLiquidity.sub(amountToReturn);

        // Pay liquidator premium;
        if (liquidatorPremium > 0 && liquidatorAddress != address(0)) {
            ERC20(_underlyingTokenAddress).transfer(
                liquidatorAddress,
                liquidatorPremium
            );
            _totalLiquidity = _totalLiquidity.sub(liquidatorPremium);
        }

        // Update available liquidity
        _availableLiquidity = _availableLiquidity.add(backToVault);
        _updateCumIndexByLiquidity(_totalLiquidity, _availableLiquidity);
    }

    function getBalance(address token) external view returns (uint256) {
        return ERC20(token).balanceOf(address(this));
    }

    /// SWAP PART

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        uint256 deadline
    ) external onlyOwner {
        _uniswapRouter.swapTokensForExactTokens(
            amountOut,
            amountInMax,
            path,
            address(this),
            deadline
        );
    }

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        uint256 deadline
    ) external onlyOwner {
        _uniswapRouter.swapExactTokensForTokens(
            amountIn,
            amountOutMin,
            path,
            address(this),
            deadline
        );
    }

    function getTotalLiquidity() external view returns (uint256) {
        return _totalLiquidity;
    }

    function getAvailableLiquidity() external view returns (uint256) {
        return _availableLiquidity;
    }

    function calcBorrowRate_S1() public view returns (uint256) {
        return _calcBorrowRate_S1(_totalLiquidity, _availableLiquidity);
    }

    function getUnderlyingToken() external view returns (address) {
        return _underlyingTokenAddress;
    }

    function getDieselToken() external view returns (address) {
        return address(_dieselToken);
    }

}
