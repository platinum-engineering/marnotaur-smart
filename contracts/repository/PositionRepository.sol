// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../lib/PoolACL.sol";

/**
 * @title Leverage Repository
 * @author Platinum Forked
 * @notice Stores Leve
 * @dev Do not use in mainnet.
 */
contract PositionRepository is Ownable, PoolACL {
    using SafeMath for uint256;

    struct Position {
        uint256 mainTokenAmount;
        uint256 leveragedTokenAmount;
        mapping(address => bool) tokensListMap;
        // Tokens which trader has
        // ToDo: move to ERC20 tokens
        mapping(address => uint256) tokensBalances;
        // cumulative index at open
        uint256 cumulativeIndexAtOpen;
        // Active is true if leverage is opened
        bool active;
        // Exists is true if leverage was created sometime
        bool exists;
        address[] tokensList;
    }

    mapping(address => address[]) private _traders;
    mapping(address => mapping(address => Position)) private _positions;

    modifier activePositionOnly(address trader) {
        require(
            _positions[msg.sender][trader].active,
            "Position doesn't not exists"
        );
        _;
    }

   modifier activePoolPositionOnly(address pool, address trader) {
        require(
            _positions[pool][trader].active,
            "Position doesn't not exists"
        );
        _;
    }

    function hasOpenPosition(address pool, address trader)
        external
        view
        returns (bool)
    {
        return _positions[pool][trader].active;
    }

    // Returns quantity of leverages holders
    function tradersCount(address pool) external view returns (uint256) {
        return _traders[pool].length;
    }

    // Returns trader address by id
    function getTraderById(address pool, uint256 id)
        external
        view
        returns (address)
    {
        return _traders[pool][id];
    }

    function getPositionDetails(address pool, address trader)
        external
        view
        returns (
            uint256 amount,
            uint256 leveragedAmount,
            uint256 cumulativeIndex
        )
    {
        Position memory position = _positions[pool][trader];
        amount = position.mainTokenAmount;
        leveragedAmount = position.leveragedTokenAmount;
        cumulativeIndex = position.cumulativeIndexAtOpen;
    }

    // @dev Opens leverage for trader
    function openPosition(
        address trader,
        address mainAsset,
        uint256 mainTokenAmount,
        uint256 leveragedTokenAmount,
        uint256 cumulativeIndex
    ) external onlyPoolService {
        address pool = msg.sender;
        // Check that trader doesn't have open leverages
        require(!_positions[pool][trader].active, "Position is already opened");

        // Add trader to list if he creates leverage first time
        if (!_positions[pool][trader].exists) {
            _traders[pool].push(trader);
        } else {}

        address[] memory emptyArray;
        // Create leverage
        _positions[pool][trader] = Position({
            mainTokenAmount: mainTokenAmount,
            leveragedTokenAmount: leveragedTokenAmount,
            cumulativeIndexAtOpen: cumulativeIndex,
            tokensList: emptyArray,
            active: true,
            exists: true
        });

        _updateLeverageToken(pool, trader, mainAsset, leveragedTokenAmount);
    }

    function closePosition(address trader)
        external
        onlyPoolService
        activePositionOnly(trader)
    {
        address pool = msg.sender;
        for (uint256 i = 0; i < getTokenListCount(pool, trader); i++) {
            (address token, ) = getTokenById(pool, trader, i);
            delete _positions[pool][trader].tokensListMap[token];
            delete _positions[pool][trader].tokensBalances[token];
        }
        _positions[pool][trader].active = false;
    }

    function swapAssets(
        address trader,
        address tokenIn,
        uint256 amountIn,
        address tokenOut,
        uint256 amountOut
    ) external onlyPoolService activePositionOnly(trader) {
        address pool = msg.sender;
        require(
            _positions[pool][trader].tokensBalances[tokenIn] >= amountIn,
            "Insufficient funds"
        );

        _updateLeverageToken(
            pool,
            trader,
            tokenIn,
            _positions[pool][trader].tokensBalances[tokenIn].sub(amountIn)
        );
        _updateLeverageToken(
            pool,
            trader,
            tokenOut,
            _positions[pool][trader].tokensBalances[tokenOut].add(amountOut)
        );
    }

    function getTokenListCount(address pool, address trader)
        public
        view
        activePoolPositionOnly(pool, trader)
        returns (uint256)
    {
        return _positions[pool][trader].tokensList.length;
    }

    function getTokenById(
        address pool,
        address trader,
        uint256 id
    ) public view activePoolPositionOnly(pool, trader) returns (address, uint256) {
        address tokenAddr = _positions[pool][trader].tokensList[id];
        uint256 amount = _positions[pool][trader].tokensBalances[tokenAddr];
        return (tokenAddr, amount);
    }

    // @dev updates leverage token balances
    function _updateLeverageToken(
        address pool,
        address trader,
        address token,
        uint256 amount
    ) internal activePoolPositionOnly(pool, trader) {
        if (!_positions[pool][trader].tokensListMap[token]) {
            _positions[pool][trader].tokensListMap[token] = true;
            _positions[pool][trader].tokensList.push(token);
        }

        _positions[pool][trader].tokensBalances[token] = amount;
    }
}
