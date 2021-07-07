// SPDX-License-Identifier: MIT
// Gearbox forked by Platinum . Uncollateralized protocol for margin trading
pragma solidity ^0.6.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "./console.sol";

/**
 * @title Pricing Model
 * @author Mikhail Lazarev
 * @notice This vault contract accepts liquidity
 * @dev Do not use in mainnet.
 */
contract PriceModel {
    using SafeMath for uint256;

    uint256 constant U_OPTIMAL = 80;
    uint256 constant R_BASE = 0;
    uint256 constant R_SLOPE1 = 4;
    uint256 constant R_SLOPE2 = 75;
    uint256 constant S_1 = 1e18;

    function getInterestParameters()
    external
    pure
    returns (
        uint256,
        uint256,
        uint256,
        uint256
    )
    {
        return (U_OPTIMAL, R_BASE, R_SLOPE1, R_SLOPE2);
    }

    uint256 private _cumulativeIndex;
    uint256 private _currentBorrowRate;
    uint256 private _cumulativeIndexLastUpdate;
    uint256 internal constant SECONDS_PER_YEAR = 365 days;

    /// NEEDS PARAMS
    function _calcBorrowRate_S1(uint256 totalLiquidity, uint256 availableLiquidity) internal view returns (uint256) {
        uint256 U_OPTIMAL_S1 = U_OPTIMAL.mul(S_1);
        uint256 R_BASE_S1 = R_BASE.mul(S_1);
        uint256 R_SLOPE1_S1 = R_SLOPE1.mul(S_1);

        if (totalLiquidity == 0) {
            return 0;
        }

        uint256 utilisationRate_s1 =
        totalLiquidity.sub(availableLiquidity).mul(S_1).mul(100).div(totalLiquidity);
        if (utilisationRate_s1 < U_OPTIMAL_S1) {
            return
            utilisationRate_s1.mul(R_SLOPE1).div(U_OPTIMAL).add(R_BASE_S1);
        }

        return
        utilisationRate_s1
        .sub(U_OPTIMAL_S1)
        .mul(R_SLOPE2)
        .div(100 - U_OPTIMAL)
        .add(R_BASE_S1)
        .add(R_SLOPE1_S1);
    }

    function calcLinearCumulative_S1() public view returns (uint256) {
        //solium-disable-next-line
        uint256 timeDifference =
        block.timestamp.sub(uint256(_cumulativeIndexLastUpdate));

        return calcLinearIndex(timeDifference);
    }

    function calcLinearIndex(uint256 timeDifference)
    public
    view
    returns (uint256)
    {
        uint256 linearAccumulated_S1 =
        _currentBorrowRate.mul(timeDifference).div(SECONDS_PER_YEAR).add(
            S_1
        );

        return _cumulativeIndex.mul(linearAccumulated_S1).div(S_1);
    }

    function getCumulativeIndex() external view returns (uint256) {
        return _cumulativeIndex;
    }

    /// NEEDS PARAMS
    function _updateCumIndexByLiquidity(uint256 totalLiquidity, uint256 availableLiquidity) internal {
        uint256 newCIndex = calcLinearCumulative_S1();

        // Update cumulativeIndex
        _updateCumulativeIndex(newCIndex);

        // update borrow rate
        _currentBorrowRate = _calcBorrowRate_S1(totalLiquidity, availableLiquidity);
    }

    function _updateCumulativeIndex(uint256 value) internal {
        _cumulativeIndex = value;
        _cumulativeIndexLastUpdate = block.timestamp;
    }
}
