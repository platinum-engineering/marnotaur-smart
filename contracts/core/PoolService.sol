// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "./VaultService.sol";
import "../repository/AddressRepository.sol";
import "../repository/PositionRepository.sol";
import "../repository/IPriceRepository.sol";
import "../uniswap/IUniswapV2Router02.sol";
import "../token/DieselToken.sol";

import "../lib/console.sol";

/**
 * @title Leverage
 * @author Platinum forked
 * @notice This contract manage leverage operations
 * @dev Leverage trading on UniSwap.
 */
contract PoolService is Ownable {
    //!!!!!!!! Check befor deploy !!!!!!!!
    // Not more then 100 units  of underline token(see decimals) 
    uint256 constant MAX_DEPOSIT = 100e18;

    using SafeMath for uint256;
    uint256 constant X_LEVERAGE = 4;
    uint256 constant S_1 = 1e18;
    uint256 constant LEVERAGE_CUT = 10;

    /// @dev Token address for vault asset
    address private _underlyingTokenAddress;

    mapping(address => bool) _allowedTokens;
    address[] _allowedTokensList;

    // Repositories
    AddressRepository private _addressRepository;
    PositionRepository private _PositionRepository;
    IPriceRepository private _priceRepository;

    // Tokens
    VaultService private _vaultService;
    DieselToken private _dieselToken;

    // Risk Level
    bool private _isHighRisk;

    // Leverage events
    event OpenLeverage(address indexed sender, uint256 amount);
    event CloseLeverage(address indexed sender);
    event LiquidateLeverage(address indexed sender, address indexed liquidator);

    constructor(address addressRepository, address vault, bool isHighRisk) public {
        // Repositories & services
        _addressRepository = AddressRepository(addressRepository);
        _PositionRepository = PositionRepository(
            _addressRepository.getPositionRepository()
        );
        _priceRepository = IPriceRepository(
            _addressRepository.getPriceRepository()
        );
        _vaultService = VaultService(vault);

        // Tokens init
        _dieselToken = DieselToken(_vaultService.getDieselToken());
        _underlyingTokenAddress = _vaultService.getUnderlyingToken();

        _allowedTokens[_underlyingTokenAddress] = true;
        _allowedTokensList.push(_underlyingTokenAddress);

        _isHighRisk = isHighRisk;
    }

    modifier allowedTokensOnly(address token) {
        require(_allowedTokens[token], "This token is not allowed");
        _;
    }

    function allowTokenForTrading(address token, address priceFeedContract) external onlyOwner {
        require(token != address(0), "0x0 address is not allowed");
        require(priceFeedContract != address(0), "0x0 pricefeed address is not allowed");
        _vaultService.approveOnUniswap(token);
        _priceRepository.addPriceFeed(token, _underlyingTokenAddress, priceFeedContract);
        _allowedTokens[token] = true;
        _allowedTokensList.push(token);
    }

    function allowedTokenCount() external view returns (uint256) {
        return _allowedTokensList.length;
    }

    function allowedTokenById(uint256 id) external view returns (address) {
        return _allowedTokensList[id];
    }

    function hasOpenPosition() external view returns(bool) {
        return _PositionRepository.hasOpenPosition(address(this), msg.sender);
    }


    function disallowTokenForTrading(address token) external onlyOwner {
        require(
            token != _underlyingTokenAddress,
            "You cant disallow base vault token"
        );
        _allowedTokens[token] = false;
    }

    // open Leverage for client
    function openPosition(uint256 amount) external {
        require(amount < MAX_DEPOSIT, "NOT MORE in TESTS");
        // move tokens to vault
        uint256 leveragedAmount = amount.mul(X_LEVERAGE);
        uint256 ci = _vaultService.calcLinearCumulative_S1();
        _vaultService.updateLeverageOpen(msg.sender, amount, leveragedAmount);
        _PositionRepository.openPosition(
            msg.sender,
            _underlyingTokenAddress,
            amount,
            leveragedAmount,
            ci
        );
        emit OpenLeverage(msg.sender, amount);
    }

    function closePosition() external {
        _closePosition(msg.sender, address(0));
        emit CloseLeverage(msg.sender);
    }

    // @dev liquidate leverage if it meets required conditions
    // and return premium for liquidator
    function liquidatePosition(address holder) external {
        _closePosition(holder, msg.sender);
        emit LiquidateLeverage(holder, msg.sender);
    }

    function _closePosition(address holder, address liquidator) internal {
        uint256 balanceBeforeSale =
            _vaultService.getBalance(_underlyingTokenAddress);

        console.log("CLOSE POSITION");
        console.log(balanceBeforeSale);

        uint256 underlyingAssetAmount = _saleAllTokensExceptVaultToken(holder);

        console.log(underlyingAssetAmount);

        (uint256 amount, uint256 leveragedAmount, ) =
            _PositionRepository.getPositionDetails(address(this), holder);

        console.log(amount);
        console.log(leveragedAmount);

        uint256 totalBalanceInVaultTokens =
            _vaultService.getBalance(_underlyingTokenAddress).add(underlyingAssetAmount).sub(balanceBeforeSale);

        console.log(totalBalanceInVaultTokens);
        uint256 amountInterested = calcAmountInterested(holder);

        console.log(amountInterested);

        // Amount which should be pushed back to pool
        uint256 backToVault = leveragedAmount.add(amountInterested).sub(amount);

        console.log(backToVault);
        uint256 amountToReturn = totalBalanceInVaultTokens.sub(backToVault);

        console.log(amountToReturn);

        uint256 liquidationPremium;
        if (liquidator == address(0)) {
            liquidationPremium = 0;
        } else {
            liquidationPremium = leveragedAmount.mul(LEVERAGE_CUT).div(100);
            if (liquidationPremium > amountToReturn) {
                liquidationPremium = amountToReturn;
            }
        }



        amountToReturn = amountToReturn.sub(liquidationPremium);

        console.log(amountToReturn);
        // Vault move tokens to holder

        _vaultService.updateOnLeverageClose(
            holder,
            amountToReturn,
            backToVault,
            liquidationPremium,
            liquidator
        );
        // Closing leverage in repository
        _PositionRepository.closePosition(holder);
    }

    function _saleAllTokensExceptVaultToken(address holder) internal returns (uint256) {
        uint256 tokensCount = _PositionRepository.getTokenListCount(address(this), holder);
        uint256 underlying = 0;
        for (uint256 i = 0; i < tokensCount; i++) {
            (address addr, uint256 amount) =
                _PositionRepository.getTokenById(address(this), holder, i);
            if (addr != _underlyingTokenAddress) {
                // Sell on vault
                address[] memory path = new address[](2);
                path[0] = addr;
                path[1] = _underlyingTokenAddress;

                uint256 deadline = block.timestamp + 1;
                _vaultService.swapExactTokensForTokens(
                    amount,
                    0,
                    path,
                    deadline
                );
            } else {
                underlying = amount;
            }
        }
        return underlying;
    }

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        uint256 deadline
    ) external {
        address tokenIn = path[0];
        require(_allowedTokens[tokenIn], "This token is not allowed");

        address tokenOut = path[path.length - 1];
        require(_allowedTokens[tokenOut], "This token is not allowed");

        // store balances before swap
        uint256 balanceInBefore = _vaultService.getBalance(tokenIn);
        uint256 balanceOutBefore = _vaultService.getBalance(tokenOut);

        // swapTokens
        _vaultService.swapTokensForExactTokens(
            amountOut,
            amountInMax,
            path,
            deadline
        );

        // compute changes in balances
        uint256 amountInSpent =
            balanceInBefore.sub(_vaultService.getBalance(tokenIn));
        uint256 amountOutGot =
            _vaultService.getBalance(tokenOut).sub(balanceOutBefore);

        // update stored balances with differences
        _PositionRepository.swapAssets(
            msg.sender,
            tokenIn,
            amountInSpent,
            tokenOut,
            amountOutGot
        );
    }

    function calcPositionBalance(address holder) public view returns (uint256) {
        uint256 total = 0;
        uint256 tokensCount = _PositionRepository.getTokenListCount(address(this), holder);
        for (uint256 i = 0; i < tokensCount; i++) {
            (address addr, uint256 amount) =
                _PositionRepository.getTokenById(address(this), holder, i);
            uint256 price =
                _priceRepository.getLastPrice(addr, _underlyingTokenAddress);
            uint256 tokenValueInVaultCurrency = price.mul(amount);

            total = total.add(tokenValueInVaultCurrency);
        }
        return total;
    }

    function calcAmountInterested(address holder)
        public
        view
        returns (uint256)
    {
        uint256 current_cumulative_index =
            _vaultService.calcLinearCumulative_S1();

        (uint256 amount, uint256 leveragedAmount, uint256 ciAtOpen) =
            _PositionRepository.getPositionDetails(address(this), holder);

        uint256 amountBorrowed = leveragedAmount - amount;
        return amountBorrowed.mul(current_cumulative_index).div(ciAtOpen).div(S_1);
    }

    function calcPositionCoverage_S1(address holder)
        public
        view
        returns (uint256)
    {
        (, uint256 leveragedAmount, ) =
            _PositionRepository.getPositionDetails(address(this), holder);

        uint256 amountInterested = calcAmountInterested(holder);
        uint256 balance = calcPositionBalance(holder);
        return balance.sub(amountInterested).mul(S_1).div(leveragedAmount);
    }

    function getVaultService() external view returns (address) {
        return address (_vaultService);
    }


    function getPositionDetails(address holder) external view returns (uint256, uint256) {
        (uint256 amount, uint256 leveragedAmount, ) =
        _PositionRepository.getPositionDetails(address(this), holder);
        return (amount, leveragedAmount);
    }


    function getPositionTokensCount(address trader) external view returns (uint256) {
        return  _PositionRepository.getTokenListCount(address(this), trader);
    }

    function getPositionTokensById(address trader, uint256 id) external view returns (address, uint256) {
        return  _PositionRepository.getTokenById(address(this), trader, id);
    }

    function getRiskLevel() external view returns (bool) {
        return _isHighRisk;
    }

}
