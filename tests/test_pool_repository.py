import pytest
from brownie import reverts

POOL_ADDRESS = "0x0000000000000000000000000000000000000001"


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_transfer_ownership(accounts, contract_poolrepository):
    new_account = accounts.add()
    contract_poolrepository.transferOwnership(new_account)
    assert contract_poolrepository.owner() == new_account
    with reverts("Ownable: caller is not the owner"):
        contract_poolrepository.transferOwnership(accounts[0])


def test_renounce_ownership(contract_poolrepository):
    contract_poolrepository.renounceOwnership()
    assert contract_poolrepository.owner() == '0x0000000000000000000000000000000000000000'


def test_add_pool(contract_poolrepository):
    contract_poolrepository.addPool(POOL_ADDRESS)
    addr, status = contract_poolrepository.getPoolById(0)
    assert (contract_poolrepository.getPoolsCount() == 1) & (addr == POOL_ADDRESS) & (status == 0)


def test_set_status(contract_poolrepository):
    contract_poolrepository.addPool(POOL_ADDRESS)
    contract_poolrepository.setStatusPool(0, 1)
    addr, status = contract_poolrepository.getPoolById(0)
    assert (addr == POOL_ADDRESS) & (status == 1)
