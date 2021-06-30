import pytest

POOL_ADDRESS = "0x0000000000000000000000000000000000000001"


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_add_pool(contract_poolrepository):
    contract_poolrepository.addPool(POOL_ADDRESS)
    addr, status = contract_poolrepository.getPoolById(0)
    assert (contract_poolrepository.getPoolsCount() == 1) & (addr == POOL_ADDRESS) & (status == 0)


def test_set_status(contract_poolrepository):
    contract_poolrepository.addPool(POOL_ADDRESS)
    contract_poolrepository.setStatusPool(0, 1)
    addr, status = contract_poolrepository.getPoolById(0)
    assert (addr == POOL_ADDRESS) & (status == 1)
