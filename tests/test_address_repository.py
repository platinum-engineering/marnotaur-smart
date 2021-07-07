import pytest
from brownie import reverts
from brownie.convert.datatypes import HexString


def _convert_str2bytes(key):
    _str = str(HexString(key.encode(), "bytes32")).lstrip('0x')
    return '0x' + _str + ''.zfill(64 - len(_str))


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_transfer_ownership(accounts, contract_addressrepository):
    new_account = accounts.add()
    contract_addressrepository.transferOwnership(new_account)
    assert contract_addressrepository.owner() == new_account
    with reverts("Ownable: caller is not the owner"):
        contract_addressrepository.transferOwnership(accounts[0])


def test_renounce_ownership(contract_addressrepository):
    contract_addressrepository.renounceOwnership()
    assert contract_addressrepository.owner() == '0x0000000000000000000000000000000000000000'


def test_get_pool_repository(contract_poolrepository, contract_addressrepository):
    contract_addressrepository.setPoolRepository(contract_poolrepository)
    assert contract_addressrepository.getPoolRepository() == contract_poolrepository


def test_get_position_repository(contract_positionrepository, contract_addressrepository):
    contract_addressrepository.setPositionRepository(contract_positionrepository)
    assert contract_addressrepository.getPositionRepository() == contract_positionrepository


def test_get_price_repository(contract_pricerepository, contract_addressrepository):
    contract_addressrepository.setPriceRepository(contract_pricerepository)
    assert contract_addressrepository.getPriceRepository() == contract_pricerepository


def test_get_uniswap_router(contract_uniswaprouter, contract_addressrepository):
    contract_addressrepository.setUniswapRouter(contract_uniswaprouter)
    assert contract_addressrepository.getUniswapRouter() == contract_uniswaprouter


def test_get_address(contract_poolrepository, contract_positionrepository, contract_pricerepository, contract_uniswaprouter, contract_addressrepository):
    contract_addressrepository.setPoolRepository(contract_poolrepository)
    contract_addressrepository.setPositionRepository(contract_positionrepository)
    contract_addressrepository.setPriceRepository(contract_pricerepository)
    contract_addressrepository.setUniswapRouter(contract_uniswaprouter)
    assert (contract_addressrepository.getAddress(_convert_str2bytes("POOL_REPOSITORY")) == contract_poolrepository) & \
           (contract_addressrepository.getAddress(_convert_str2bytes("POSITION_REPOSITORY")) == contract_positionrepository) & \
           (contract_addressrepository.getAddress(_convert_str2bytes("PRICE_REPOSITORY")) == contract_pricerepository) & \
           (contract_addressrepository.getAddress(_convert_str2bytes("UNISWAP_ROUTER")) == contract_uniswaprouter)
