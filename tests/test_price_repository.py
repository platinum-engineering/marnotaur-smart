import pytest
from brownie import reverts
from fixtures.constants import *


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_transfer_ownership(accounts, contract_pricerepository):
    new_account = accounts.add()
    contract_pricerepository.transferOwnership(new_account)
    assert contract_pricerepository.owner() == new_account
    with reverts("Ownable: caller is not the owner"):
        contract_pricerepository.transferOwnership(accounts[0])


def test_renounce_ownership(contract_pricerepository):
    contract_pricerepository.renounceOwnership()
    assert contract_pricerepository.owner() == '0x0000000000000000000000000000000000000000'


def test_get_price(contract_poolservice, contract_aggregatorv3, contract_pricerepository):
    contract_pricerepository.addToPoolServicesList(contract_poolservice)
    contract_pricerepository.addPriceFeed(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
        contract_aggregatorv3,
        {'from': contract_poolservice}
    )
    assert contract_pricerepository.getLastPrice(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
    ) == 1
