from brownie import PoolService, VaultService, interface, accounts

VAULT = "0xA2f8727e09438A553c356b4bD5816265eae0D580"
POOL = "0x1C7040B1688c0FACf013734c515E48BF7715a87F"

DAI_ADDRESS = "0xc7AD46e0b8a400Bb3C915120d284AafbA8fc4735"
DAI_AMOUNT = 1e18

LINK_ADDRESS = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
UNISWAP_PAIR_LINK_ADDRESS = "0xd8bD0a1cB028a31AA859A21A3758685a95dE4623"


def main():
    account = accounts.load('deployment_rinkeby_account')

    vault = VaultService.at(VAULT)
    pool = PoolService.at(POOL)
    underlyingtoken = interface.IERC20(DAI_ADDRESS)

    underlyingtoken.approve(vault, DAI_AMOUNT, {'from': account})
    vault.addLiquidity(DAI_AMOUNT, {'from': account})
    vault.removeLiquidity(DAI_AMOUNT, {'from': account})

    underlyingtoken.approve(vault, DAI_AMOUNT, {'from': account})
    vault.addLiquidity(DAI_AMOUNT, {'from': account})
    underlyingtoken.approve(vault, DAI_AMOUNT/5, {'from': account})
    pool.openPosition(DAI_AMOUNT/5, {'from': account})
    pool.closePosition({'from': account})
    vault.removeLiquidity(DAI_AMOUNT, {'from': account})

    pool.allowTokenForTrading(LINK_ADDRESS, UNISWAP_PAIR_LINK_ADDRESS, {'from': account})

