// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

import "../../interfaces/AggregatorV3Interface.sol";

/**
 * @title Mock Price Feed
 * @author MaxSiz
 * @notice Emulate Prices from Chainlink and cache them
 * @dev Do not use in mainnet.
 */
contract MockChainLinkPriceFeed is AggregatorV3Interface {

  struct FeedRecord {
    int256  price;
    uint256 startedAt;
    uint256 updatedAt;
    uint80 answeredInRound;
  }

  mapping(uint80 => FeedRecord) priceFeed;
  uint80 roundId;

  function decimals() external view override returns (uint8){
    return uint8(4); 
  }
  
  function description() external view override returns (string memory){
    return 'Mock FeedPrice';
  }
  
  function version() external view override returns (uint256){
    return uint256(0); 
  }

  function setPrice(int256 _price) external  returns (uint80 _roundId) {
    roundId++;
    priceFeed[roundId] = FeedRecord({
        price: _price,
        startedAt: block.timestamp,
        updatedAt: block.timestamp,
        answeredInRound: 0
        });

    return roundId;
  }

  // getRoundData and latestRoundData should both raise "No data present"
  // if they do not have data to report, instead of returning unset values
  // which could be misinterpreted as actual reported values.
  function getRoundData(uint80 _roundId)
    external
    view
    override
    returns (
      uint80 _rId,
      int256 _answer,
      uint256 _startedAt,
      uint256 _updatedAt,
      uint80 _answeredInRound
    ) {

    FeedRecord memory rec = priceFeed[_roundId];
    return (_roundId, rec.price, rec.startedAt, rec.updatedAt, rec.answeredInRound); 

  }


  function latestRoundData()
    external
    view
    override
    returns (
      uint80 _rId,
      int256 _answer,
      uint256 _startedAt,
      uint256 _updatedAt,
      uint80 _answeredInRound
    ) {
    
    FeedRecord memory rec = priceFeed[roundId];
    return (roundId, rec.price, rec.startedAt, rec.updatedAt, rec.answeredInRound);
  }

}
