from brownie import PoolService, VaultService, interface, accounts

VAULT = "0x89692DF0404B43ee37241ba9F3b91C9308657508"
POOL = "0x5D31Ac01c4B3fF5cA37969CE20D48955316c047b"
DAI_ADDRESS = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"
DAI_AMOUNT = 1e18

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
