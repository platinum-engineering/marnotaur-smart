import pytest
from fixtures.constants import *


@pytest.fixture(scope="module")
def contract_aggregatorv3(accounts, AggregatorV3Mock):
    contract = accounts[0].deploy(AggregatorV3Mock)
    yield contract


@pytest.fixture(scope="module")
def contract_poolrepository(accounts, PoolRepository):
    contract = accounts[0].deploy(PoolRepository)
    yield contract


@pytest.fixture(scope="module")
def contract_positionrepository(accounts, PositionRepository):
    contract = accounts[0].deploy(PositionRepository)
    yield contract


@pytest.fixture(scope="module")
def contract_pricerepository(accounts, PriceRepository):
    contract = accounts[0].deploy(PriceRepository)
    yield contract


@pytest.fixture(scope="module")
def contract_uniswaprouter(accounts, UniswapRouterMock):
    contract = accounts[0].deploy(UniswapRouterMock)
    yield contract


@pytest.fixture(scope="module")
def contract_addressrepository(accounts, AddressRepository):
    contract = accounts[0].deploy(AddressRepository)
    yield contract


@pytest.fixture(scope="module")
def contract_gtoken(accounts, DieselToken):
    contract = accounts[0].deploy(DieselToken, "Token TEST", "TEST")
    yield contract


@pytest.fixture(scope="module")
def contract_underlyingtoken(accounts, DieselToken):
    contract = accounts[0].deploy(DieselToken, "UnderlyingToken TEST", "UTEST")
    yield contract


@pytest.fixture(scope="module")
def contract_vaultservice(accounts, contract_uniswaprouter, contract_addressrepository, contract_underlyingtoken, contract_gtoken, VaultService):
    contract_addressrepository.setUniswapRouter(contract_uniswaprouter)
    contract = accounts[0].deploy(VaultService, contract_addressrepository, contract_underlyingtoken, contract_gtoken)
    yield contract


@pytest.fixture(scope="module")
def contract_poolservice(accounts, contract_positionrepository, contract_pricerepository, contract_uniswaprouter, contract_addressrepository, contract_vaultservice, PoolService):
    contract_addressrepository.setPositionRepository(contract_positionrepository)
    contract_addressrepository.setPriceRepository(contract_pricerepository)
    contract_addressrepository.setUniswapRouter(contract_uniswaprouter)
    contract = accounts[0].deploy(PoolService, contract_addressrepository, contract_vaultservice, True)
    yield contract
