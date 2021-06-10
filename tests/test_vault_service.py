import pytest
from brownie import Wei, reverts


def _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    contract_gtoken.transferOwnership(contract_vaultservice)
    contract_underlyingtoken.mint(accounts[0], amount)
    contract_underlyingtoken.approve(contract_vaultservice, amount)


def _add_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    balance_gtoken_prev = contract_gtoken.balanceOf(accounts[0])
    balance_underlyingtoken_prev = contract_underlyingtoken.balanceOf(accounts[0])
    contract_vaultservice.addLiquidity(amount)
    balance_gtoken_curr = contract_gtoken.balanceOf(accounts[0])
    balance_underlyingtoken_curr = contract_underlyingtoken.balanceOf(accounts[0])
    return balance_gtoken_prev, balance_underlyingtoken_prev, balance_gtoken_curr, balance_underlyingtoken_curr


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_add_liquidity(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    amount = 1e18
    _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    balance_gtoken_prev, balance_underlyingtoken_prev, balance_gtoken_curr, balance_underlyingtoken_curr = \
        _add_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    assert balance_gtoken_prev + amount == balance_gtoken_curr & \
           balance_underlyingtoken_prev == balance_underlyingtoken_curr + amount

def test_add_liquidity_MAX(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    amount = 100e18
    _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    with reverts("NOT MORE in TESTS"):
        contract_vaultservice.addLiquidity(amount)
    

def test_remove_liquidity(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    amount = 1e18
    _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    _add_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    balance_gtoken_prev = contract_gtoken.balanceOf(accounts[0])
    balance_underlyingtoken_prev = contract_underlyingtoken.balanceOf(accounts[0])
    contract_vaultservice.removeLiquidity(amount)
    balance_gtoken_curr = contract_gtoken.balanceOf(accounts[0])
    balance_underlyingtoken_curr = contract_underlyingtoken.balanceOf(accounts[0])
    assert balance_gtoken_prev == balance_gtoken_curr + amount & \
           balance_underlyingtoken_prev + amount == balance_underlyingtoken_curr
