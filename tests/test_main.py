import pytest
from fixtures.constants import *


def test_get_price(contract_pricerepository):
    assert contract_pricerepository.getLastPrice(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
    ) == 1
