// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "../../interfaces/AggregatorV3Interface.sol";

contract AggregatorV3Mock is AggregatorV3Interface {

  function decimals() external view override returns (uint8) {
      return 0;
  }

  function description() external view override returns (string memory) {
      return '';
  }

  function version() external view override returns (uint256) {
      return 0;
  }

  function getRoundData(uint80 _roundId) external view override returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
  ) {
      return (0, 1, 0, 0, 0);
  }

  function latestRoundData() external view override returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
  ) {
      return (0, 1, 0, 0, 0);
  }
}
