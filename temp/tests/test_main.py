import pytest


ADDRESS_ORACLE = "0xd8bD0a1cB028a31AA859A21A3758685a95dE4623"
ADDRESS_LINK_TOKEN = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
ADDRESS_USDT_TOKEN = "0xfb1d709cb959ac0ea14cad0927eabc7832e65058"

@pytest.fixture(scope="module")
def contractPR(accounts, PriceRepository):
    contract = accounts[0].deploy(PriceRepository)
    contract.addToPoolServicesList(accounts[0])
    contract.addPriceFeed(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
        ADDRESS_ORACLE
    )
    yield contract

def test_getPrice(contractPR):
    assert contractPR.getLastPrice(
        ADDRESS_LINK_TOKEN,
        ADDRESS_USDT_TOKEN,
    ) != 0
