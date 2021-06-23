import pytest
import datetime
from test_vault_service import _prepare_actions_liquidity, _add_liquidity


def _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice):
    contract_vaultservice.transferOwnership(contract_poolservice)
    contract_pricerepository.addToPoolServicesList(contract_poolservice)


def _prepare_open_position(contract_positionrepository, contract_poolservice):
    contract_positionrepository.addToPoolServicesList(contract_poolservice)


def _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice):
    _prepare_actions_liquidity(amount * 10, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    _add_liquidity(amount * 9, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    contract_poolservice.openPosition(amount)


def _close_position(contract_poolservice):
    contract_poolservice.closePosition()

def _allow_token_for_trading(contract_gtoken, contract_poolservice):
    contract_poolservice.allowTokenForTrading(contract_gtoken, contract_poolservice)


def test_allow_token_for_trading(contract_vaultservice, contract_gtoken, contract_pricerepository, contract_poolservice):
    _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice)
    _allow_token_for_trading(contract_gtoken, contract_poolservice)
    find_token = False
    for i in range(contract_poolservice.allowedTokenCount()):
        if contract_poolservice.allowedTokenById(i) == contract_gtoken:
            find_token = True
    assert find_token


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_open_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice):
    amount = 1e18
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    assert contract_poolservice.hasOpenPosition()


def test_close_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice):
    amount = 1e18
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    _close_position(contract_poolservice)
    assert not contract_poolservice.hasOpenPosition()


def test_swap_tokens_for_exact_tokens(accounts, contract_uniswaprouter, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_pricerepository, contract_positionrepository, contract_poolservice):
    amount = 1e17
    amountOut = 1e17
    amountInMax = 1e17
    deadline = (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice)
    _allow_token_for_trading(contract_gtoken, contract_poolservice)
    contract_gtoken.mint(contract_uniswaprouter, amountInMax, {'from': contract_vaultservice})
    vaultservice_gtoken_balance_prev = contract_gtoken.balanceOf(contract_vaultservice)
    vaultservice_underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(contract_vaultservice)
    uniswaprouter_gtoken_balance_prev = contract_gtoken.balanceOf(contract_uniswaprouter)
    uniswaprouter_underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(contract_uniswaprouter)
    contract_poolservice.swapTokensForExactTokens(amountOut, amountInMax, [contract_underlyingtoken, contract_gtoken], deadline)
    vaultservice_gtoken_balance_curr = contract_gtoken.balanceOf(contract_vaultservice)
    vaultservice_underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(contract_vaultservice)
    uniswaprouter_gtoken_balance_curr = contract_gtoken.balanceOf(contract_uniswaprouter)
    uniswaprouter_underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(contract_uniswaprouter)
    assert (vaultservice_gtoken_balance_prev + amountOut == vaultservice_gtoken_balance_curr) & \
           (vaultservice_underlyingtoken_balance_prev == vaultservice_underlyingtoken_balance_curr + amountInMax) & \
           (uniswaprouter_gtoken_balance_prev == uniswaprouter_gtoken_balance_curr + amountOut) & \
           (uniswaprouter_underlyingtoken_balance_prev + amountInMax == uniswaprouter_underlyingtoken_balance_curr)
