from brownie import PoolService, VaultService, DieselToken, PositionRepository, PoolRepository, PriceRepository, AddressRepository, UniswapRouterMock


def generate_gvp(account, token_address, positionRepository, poolRepository, priceRepository, addressRepository, internal=False):
    if internal:
        gtoken = DieselToken.deploy('Test', 'TST', {'from': account})
        vault = VaultService.deploy(addressRepository, token_address, gtoken, {'from': account})
        pool = PoolService.deploy(addressRepository, vault, True, {'from': account})
    else:
        gtoken = DieselToken.deploy('Test', 'TST', {'from': account}, publish_source=True)
        vault = VaultService.deploy(addressRepository, token_address, gtoken, {'from': account}, publish_source=True)
        pool = PoolService.deploy(addressRepository, vault, True, {'from': account}, publish_source=True)

    vault.transferOwnership(pool, {'from': account})
    gtoken.transferOwnership(vault, {'from': account})

    positionRepository.addToPoolServicesList(pool, {'from': account})
    priceRepository.addToPoolServicesList(pool, {'from': account})
    poolRepository.addPool(pool, {'from': account})

    return gtoken, vault, pool


def get_repository(account, uniswap_address="", internal=False):
    if internal:
        positionRepository = PositionRepository.deploy({'from': account})
        poolRepository = PoolRepository.deploy({'from': account})
        priceRepository = PriceRepository.deploy({'from': account})
        addressRepository = AddressRepository.deploy({'from': account})
    else:
        positionRepository = PositionRepository.deploy({'from': account}, publish_source=True)
        poolRepository = PoolRepository.deploy({'from': account}, publish_source=True)
        priceRepository = PriceRepository.deploy({'from': account}, publish_source=True)
        addressRepository = AddressRepository.deploy({'from': account}, publish_source=True)

    if uniswap_address == "":
        uniswapRouter = UniswapRouterMock.deploy({'from': account})
        uniswap_address = uniswapRouter.address

    addressRepository.setPositionRepository(positionRepository)
    addressRepository.setPoolRepository(poolRepository)
    addressRepository.setPriceRepository(priceRepository)
    addressRepository.setUniswapRouter(uniswap_address)

    return positionRepository, poolRepository, priceRepository, addressRepository


def get_repository_with_addresses(position_addr, pool_addr, price_addr, address_addr):
    positionRepository = PositionRepository.at(position_addr)
    poolRepository = PoolRepository.at(pool_addr)
    priceRepository = PriceRepository.at(price_addr)
    addressRepository = AddressRepository.at(address_addr)

    return positionRepository, poolRepository, priceRepository, addressRepository
