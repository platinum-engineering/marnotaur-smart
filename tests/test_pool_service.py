import pytest
import datetime
from test_vault_service import _prepare_actions_liquidity, _add_liquidity


def _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice):
    contract_vaultservice.transferOwnership(contract_poolservice)
    contract_pricerepository.addToPoolServicesList(contract_poolservice)


def _prepare_open_position(contract_positionrepository, contract_poolservice):
    contract_positionrepository.addToPoolServicesList(contract_poolservice)


def _prepare_swap_tokens_for_exact_tokens(contract_positionrepository, contract_poolservice):
    contract_positionrepository.addToPoolServicesList(contract_poolservice)


def _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice):
    _prepare_actions_liquidity(amount * 5, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    _add_liquidity(amount * 4, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    contract_poolservice.openPosition(amount / 2)


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
    test_open_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice)
    contract_poolservice.closePosition()
    assert not contract_poolservice.hasOpenPosition()


def test_swap_tokens_for_exact_tokens(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_pricerepository, contract_positionrepository, contract_poolservice):
    amount = 1e18
    amountOut = 1e18
    amountInMax = 1e18
    deadline = (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    _prepare_swap_tokens_for_exact_tokens(contract_positionrepository, contract_poolservice)
    _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice)
    _allow_token_for_trading(contract_gtoken, contract_poolservice)
    contract_poolservice.swapTokensForExactTokens(amountOut, amountInMax, [contract_underlyingtoken, contract_gtoken], deadline)
    assert True
