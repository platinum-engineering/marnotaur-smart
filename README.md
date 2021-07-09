## X5 MarginSwap smart contracts
First cross-chain platform for Margin Trading with x5 leverage

### Testnet deployments
#### Rinkeby
`AddressRegistry`  
https://rinkeby.etherscan.io/address/0x0cc7e060944b9867ef0fe55881b0e048968c07ed#code  
`PoolRepository`  
https://rinkeby.etherscan.io/address/0x30028f85Da90855fB0F00117715815bf51D42519#code  
`PositionRepository`  
https://rinkeby.etherscan.io/address/0x43445AA0e398C59B739420e392B630220fF627BD#code  
`PriceRepository`  
https://rinkeby.etherscan.io/address/0x43D151471169d3905dB57f8f1B8f8C0A757653e8#code  

`GToken`  
Gtoken for dummy DAI vault:  
https://rinkeby.etherscan.io/address/0x7A54D9bEbeD62DcdDb429Abfac8d622c9F363FC0#code  

`VP (pool, Vault)`   
`VaultService` for dummy DAI:  
https://rinkeby.etherscan.io/address/0x13878C184C4c33a090b3159f7e6fB2E8DC73EF3b#code  
`PoolService`  
PoolService for dummy MAKER (MKR) trade  
https://rinkeby.etherscan.io/address/0x6daa061e6b8fd4de2c4e1467ca91ab7fefcd1ccf#code  


#### Testnet Binance smart chain
be soon

## Abstract
Here's a list of those that most inspired us:  
 - Bancor’s single-sided liquidity and second coin in a pool as a synthetix stablecoin
  https://blog.bancor.network/guide-single-sided-amm-staking-on-bancor-v2-1-93e6839959ba  
  https://www.gemini.com/cryptopedia/bancor-network-liquidity-provider-bnt-token  
  https://blog.bancor.network/proposing-bancor-v2-1-single-sided-amm-with-elastic-bnt-supply-bcac9fe655b
  https://github.com/bancorprotocol  

 - Stable Credit synthetic coins, liquidations in user's Vaults and leverage trading of Yearn Finance, developed by Andre Cronje
  https://andrecronje.medium.com/stable-credit-understanding-automated-positive-sum-liquidations-1083c73e4e00  
  https://andrecronje.medium.com/collateralized-stable-yield-credit-2ea65a50c7e5  
  https://github.com/yearn/yearn-docs/blob/master/yearn-ecosystem/r-and-d/stablecredit.md  

 - Synthetix farming originally created by Anton Bukov
  https://github.com/Synthetixio/synthetix-mintr  
  https://github.com/Synthetixio/staking  
  https://github.com/Synthetixio/synthetix/pull/523  
  https://synthetix.community/docs/staking-snx-overview   

 - Liquidity mining pool factory developed by SWAPR  
  https://swapr.eth.link/#/pools  
  https://github.com/psq/swapr  
  https://github.com/nicoelzer/dxstats  

 - Vaults and Collateralized Debt Position concepts created by Maker DAO 
  https://community-development.makerdao.com/en/learn/vaults/  
  https://github.com/makerdao/developerguides/blob/master/vault/vault-integration-guide/vault-integration-guide.md  
  https://github.com/makerdao/awesome-makerdao  
  https://github.com/makerdao/developerguides/blob/master/vault/cdp-manager-guide/cdp-manager-guide.md  

 - Features of the Gearbox protocol
  https://github.com/Gearbox-protocol/gearbox-protocol  

 - WowSwap’s concept
  https://github.com/wowswap-io  

 - Margin and interest accumulating tokens by bZxNetwork  
  https://github.com/bZxNetwork/contractsV2  
  https://bzx.network/itokens  

 - Mainframe\Hifi.Finance’s fixed-rate, fixed-term borrowing  
  https://github.com/hifi-finance  

 - Tokenized debts/DebtTokens of Aave  
  https://github.com/aave/protocol-v2/tree/master/contracts/protocol/lendingpool  

 - Liquidity staking developed by Sigmadex  
  https://sigmadex.org (https://sigmadex.org/)  
  https://blog.sigmadex.org/decision-making-and-game-theory/  
  https://blog.sigmadex.org/understanding-game-theory/  

 - Pools for Isolated Margin trading by Sushi Kashi  
  https://github.com/sushiswap/sushiswap/tree/master/contracts/bentobox  
  https://github.com/sushiswap/sushiswap/blob/master/contracts/SushiMakerKashi.sol  

 - Alpha Homorra’s leveraged farming  
  https://github.com/AlphaFinanceLab/alphahomora  

 - InstaDApp’s smart contracts  
  https://github.com/Instadapp/smart-contract  
  https://github.com/Instadapp/InstaContract  

 - Bonding Curves for defining the interest rate determined by the utilization ratio in lending pools  
  https://medium.com/linum-labs/intro-to-bonding-curves-and-shapes-bf326bc4e11a  
  https://medium.com/molecule-blog/token-bonding-curve-design-parameters-95d365cbec4f  
  https://medium.com/coinmonks/token-bonding-curves-explained-7a9332198e0e  
  https://defiprime.com/bonding-curve-explained  
  https://billyrennekamp.medium.com/re-fungible-token-rft-297003592769  
  https://github.com/ethereum/EIPs/issues/1634  

 - 0x’s open protocol for a decentralized exchange on the Ethereum blockchain by Will Warren and Amir Bandeali  
  https://github.com/0xProject/whitepaper