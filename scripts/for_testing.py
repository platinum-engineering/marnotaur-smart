import sys
sys.path.insert(0, "./scripts")
from brownie import PoolService, VaultService, interface, accounts
import datetime
from constants import UNISWAP_ROUTER, TOKENS, CHAINLINKS, SETS


def swap_token(account, pool, underlyingtoken, uniswap_router, token, amount):
    deadline = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    ratioOut, ratioIn = uniswap_router.getAmountsIn(1, [underlyingtoken.address, TOKENS[token]])
    pool.swapTokensForExactTokens(
        amount/ratioOut, amount/ratioIn, [underlyingtoken.address, TOKENS[token]], deadline, {'from': account}
    )


def filling_gvp(account, vault_addr, pool_addr, token, tokens, amount):
    vault = VaultService.at(vault_addr)
    pool = PoolService.at(pool_addr)
    underlyingtoken = interface.IERC20(TOKENS[token])
    uniswap_router = interface.IUniswapV2Router02(UNISWAP_ROUTER)

    underlyingtoken.approve(vault, amount, {'from': account})
    vault.addLiquidity(amount, {'from': account})
    underlyingtoken.approve(vault, amount/5, {'from': account})
    pool.openPosition(amount/5, {'from': account})
    for item in tokens:
        pool.allowTokenForTrading(TOKENS[item], CHAINLINKS[item], {'from': account})
        swap_token(account, pool, underlyingtoken, uniswap_router, item, amount / (5 * len(tokens)))
    pool.closePosition({'from': account})
    vault.removeLiquidity(amount, {'from': account})

    underlyingtoken.approve(vault, amount, {'from': account})
    vault.addLiquidity(amount, {'from': account})
    underlyingtoken.approve(vault, amount/5, {'from': account})
    pool.openPosition(amount/5, {'from': account})
    for item in tokens:
        swap_token(account, pool, underlyingtoken, uniswap_router, item, amount / (5 * len(tokens)))


def main():
    account = accounts.load('deployment_account')
    amount = 1e17
    for item in SETS:
        filling_gvp(account, item['VAULT'], item['POOL'], item['TOKEN'], item['TOKENS'], amount)
