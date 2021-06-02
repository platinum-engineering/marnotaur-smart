import pytest


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
