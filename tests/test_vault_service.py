import pytest
from brownie import reverts


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


def test_get_diesel_token(contract_vaultservice, contract_gtoken):
    assert contract_vaultservice.getDieselToken() == contract_gtoken.address


def test_get_underlying_token(contract_vaultservice, contract_underlyingtoken):
    assert contract_vaultservice.getUnderlyingToken() == contract_underlyingtoken.address


def test_transfer_ownership(accounts, contract_vaultservice):
    new_account = accounts.add()
    contract_vaultservice.transferOwnership(new_account)
    assert contract_vaultservice.owner() == new_account
    with reverts("Ownable: caller is not the owner"):
        contract_vaultservice.transferOwnership(accounts[0])


def test_renounce_ownership(contract_vaultservice):
    contract_vaultservice.renounceOwnership()
    assert contract_vaultservice.owner() == '0x0000000000000000000000000000000000000000'


def test_add_liquidity(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice):
    amount = 1e18
    _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    balance_gtoken_prev, balance_underlyingtoken_prev, balance_gtoken_curr, balance_underlyingtoken_curr = \
        _add_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    assert (balance_gtoken_prev + amount == balance_gtoken_curr) & \
           (balance_underlyingtoken_prev == balance_underlyingtoken_curr + amount) & \
           (contract_vaultservice.getTotalLiquidity() == amount) & \
           (contract_vaultservice.getAvailableLiquidity() == amount)


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
    assert (balance_gtoken_prev == balance_gtoken_curr + amount) & \
           (balance_underlyingtoken_prev + amount == balance_underlyingtoken_curr) & \
           (contract_vaultservice.getTotalLiquidity() == 0) & \
           (contract_vaultservice.getAvailableLiquidity() == 0)


def test_calc_borrow_rate_s1(accounts, contract_gtoken, contract_underlyingtoken, contract_positionrepository, contract_poolservice, contract_vaultservice):
    assert contract_vaultservice.calcBorrowRate_S1() == 0
    amount = 1e18
    _prepare_actions_liquidity(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    _add_liquidity(amount * 0.9, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice)
    assert contract_vaultservice.calcBorrowRate_S1() == 0
    contract_positionrepository.addToPoolServicesList(contract_poolservice)
    contract_poolservice.openPosition(amount * 0.1)
    assert contract_vaultservice.calcBorrowRate_S1() > 0
