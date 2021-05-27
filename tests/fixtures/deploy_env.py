import pytest
from fixtures.constants import *


@pytest.fixture(scope="module")
def contract_pricerepository(accounts, PriceRepository, AggregatorV3Mock):
    contract = accounts[0].deploy(PriceRepository)
    contract_aggregatorv3_mock = accounts[0].deploy(AggregatorV3Mock)
    contract.addToPoolServicesList(accounts[0])
    contract.addPriceFeed(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
        contract_aggregatorv3_mock
    )
    yield contract
