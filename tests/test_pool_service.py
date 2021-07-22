import pytest
import datetime
from brownie import reverts
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


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_transfer_ownership(accounts, contract_poolservice):
    new_account = accounts.add()
    contract_poolservice.transferOwnership(new_account)
    assert contract_poolservice.owner() == new_account
    with reverts("Ownable: caller is not the owner"):
        contract_poolservice.transferOwnership(accounts[0])


def test_renounce_ownership(contract_poolservice):
    contract_poolservice.renounceOwnership()
    assert contract_poolservice.owner() == '0x0000000000000000000000000000000000000000'


def test_get_vault_service(contract_vaultservice, contract_poolservice):
    assert contract_poolservice.getVaultService() == contract_vaultservice.address


def test_get_risk_level(contract_poolservice):
    assert contract_poolservice.getRiskLevel()


def test_allow_token_for_trading(contract_vaultservice, contract_gtoken, contract_pricerepository, contract_poolservice):
    _prepare_allow_token_for_trading(contract_vaultservice, contract_pricerepository, contract_poolservice)
    _allow_token_for_trading(contract_gtoken, contract_poolservice)
    find_token = False
    for i in range(contract_poolservice.allowedTokenCount()):
        if contract_poolservice.allowedTokenById(i) == contract_gtoken:
            find_token = True
    assert find_token


def test_open_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice):
    amount = 1e18
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    position_amount, position_leverage_amount, _ = contract_positionrepository.getPositionDetails(contract_poolservice, accounts[0])
    assert (contract_poolservice.hasOpenPosition()) & \
           (position_amount == amount) & \
           (position_leverage_amount == amount*4) & \
           (contract_vaultservice.getTotalLiquidity() == amount * 10) & \
           (contract_vaultservice.getAvailableLiquidity() == amount * 10 - amount * 4)


def test_close_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice):
    amount = 1e18
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    vaultservice_underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(contract_vaultservice)
    underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(accounts[0])
    position_amount, position_leverage_amount, _ = contract_positionrepository.getPositionDetails(contract_poolservice, accounts[0])
    vaultservice_total_liquidity_prev = contract_vaultservice.getTotalLiquidity()
    vaultservice_available_liquidity_prev = contract_vaultservice.getAvailableLiquidity()
    _close_position(contract_poolservice)
    calcAmountInterested = contract_poolservice.calcAmountInterested(accounts[0])
    vaultservice_underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(contract_vaultservice)
    underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(accounts[0])
    vaultservice_total_liquidity_curr = contract_vaultservice.getTotalLiquidity()
    vaultservice_available_liquidity_curr = contract_vaultservice.getAvailableLiquidity()
    assert (not contract_poolservice.hasOpenPosition()) & \
           (vaultservice_total_liquidity_prev <= vaultservice_total_liquidity_curr + calcAmountInterested + position_amount) & \
           (vaultservice_available_liquidity_curr <= vaultservice_available_liquidity_prev + calcAmountInterested + position_leverage_amount - position_amount) & \
           (underlyingtoken_balance_curr <= underlyingtoken_balance_prev + position_amount) & \
           (vaultservice_underlyingtoken_balance_prev <= vaultservice_underlyingtoken_balance_curr + position_amount)


def test_liquidate_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_positionrepository, contract_poolservice):
    amount = 1e18
    new_account = accounts.add()
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)
    vaultservice_underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(contract_vaultservice)
    underlyingtoken_balance_prev = contract_underlyingtoken.balanceOf(accounts[0])
    underlyingtoken_new_account_balance_prev = contract_underlyingtoken.balanceOf(new_account)
    position_amount, position_leverage_amount, _ = contract_positionrepository.getPositionDetails(contract_poolservice, accounts[0])
    liquidation_amount = position_leverage_amount * 10 / 100
    vaultservice_total_liquidity_prev = contract_vaultservice.getTotalLiquidity()
    vaultservice_available_liquidity_prev = contract_vaultservice.getAvailableLiquidity()
    with reverts("Allowed for who can liquidate position only"):
        contract_poolservice.liquidatePosition(accounts[0], {'from': new_account})
    contract_poolservice.setLiquidatorStatus(new_account, True)
    contract_poolservice.setLiquidatorStatus(new_account, False)
    with reverts("Allowed for who can liquidate position only"):
        contract_poolservice.liquidatePosition(accounts[0], {'from': new_account})
    contract_poolservice.setLiquidatorStatus(new_account, True)
    contract_poolservice.liquidatePosition(accounts[0], {'from': new_account})
    calcAmountInterested = contract_poolservice.calcAmountInterested(accounts[0])
    vaultservice_underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(contract_vaultservice)
    underlyingtoken_balance_curr = contract_underlyingtoken.balanceOf(accounts[0])
    underlyingtoken_new_account_balance_curr = contract_underlyingtoken.balanceOf(new_account)
    vaultservice_total_liquidity_curr = contract_vaultservice.getTotalLiquidity()
    vaultservice_available_liquidity_curr = contract_vaultservice.getAvailableLiquidity()
    assert (not contract_poolservice.hasOpenPosition()) & \
           (vaultservice_total_liquidity_prev <= vaultservice_total_liquidity_curr + calcAmountInterested + position_amount) & \
           (vaultservice_available_liquidity_curr <= vaultservice_available_liquidity_prev + calcAmountInterested + position_leverage_amount - position_amount) & \
           (underlyingtoken_balance_curr <= underlyingtoken_balance_prev + position_amount - liquidation_amount) & \
           (vaultservice_underlyingtoken_balance_prev <= vaultservice_underlyingtoken_balance_curr + position_amount) & \
           (underlyingtoken_new_account_balance_curr == underlyingtoken_new_account_balance_prev + liquidation_amount)


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
