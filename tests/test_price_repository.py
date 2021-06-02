import pytest
from fixtures.constants import *


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
