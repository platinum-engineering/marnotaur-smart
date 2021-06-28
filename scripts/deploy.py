from brownie import PoolService, VaultService, DieselToken, PositionRepository, PoolRepository, PriceRepository, AddressRepository, accounts

UNISWAP_ROUTER = "0x7a250d5630b4cf539739df2c5dacb4c659f2488d"
DAI_ADDRESS = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"
USDC_ADDRESS = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b"
LINK_ADDRESS = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
UNISWAP_PAIR_DAI = "0x2bA49Aaa16E6afD2a993473cfB70Fa8559B523cF"
UNISWAP_PAIR_USDC = "0xa24de01df22b63d23Ebc1882a5E3d4ec0d907bFB"
UNISWAP_PAIR_LINK = "0xd8bD0a1cB028a31AA859A21A3758685a95dE4623"


def generate(token_address, uniswap_pair_address, account, positionRepository, poolRepository, priceRepository, addressRepository):
    gtoken = DieselToken.deploy('Test', 'TST', {'from': account}, publish_source=True)
    vault = VaultService.deploy(addressRepository, token_address, gtoken, {'from': account}, publish_source=True)
    pool = PoolService.deploy(addressRepository, vault, True, {'from': account}, publish_source=True)

    vault.transferOwnership(pool, {'from': account})
    gtoken.transferOwnership(vault, {'from': account})

    positionRepository.addToPoolServicesList(pool, {'from': account})
    priceRepository.addToPoolServicesList(pool, {'from': account})
    poolRepository.addPool(pool, {'from': account})
    pool.allowTokenForTrading(token_address, uniswap_pair_address, {'from': account})

    return gtoken, vault, pool


def main():
    account = accounts.load('deployment_rinkeby_account')

    positionRepository = PositionRepository.deploy({'from': account}, publish_source=True)
    poolRepository = PoolRepository.deploy({'from': account}, publish_source=True)
    priceRepository = PriceRepository.deploy({'from': account}, publish_source=True)

    addressRepository = AddressRepository.deploy({'from': account}, publish_source=True)
    addressRepository.setPositionRepository(positionRepository)
    addressRepository.setPoolRepository(poolRepository)
    addressRepository.setPriceRepository(priceRepository)
    addressRepository.setUniswapRouter(UNISWAP_ROUTER)

    gToken4DAI, vault4DAI, pool4DAI = generate(DAI_ADDRESS, UNISWAP_PAIR_DAI, account, positionRepository, poolRepository, priceRepository, addressRepository)
    gToken4USDC, vault4USDC, pool4USDC = generate(USDC_ADDRESS, UNISWAP_PAIR_USDC, account, positionRepository, poolRepository, priceRepository, addressRepository)
    gToken4LINK, vault4LINK, pool4LINK = generate(LINK_ADDRESS, UNISWAP_PAIR_LINK, account, positionRepository, poolRepository, priceRepository, addressRepository)

    print(f"""
    ********************************************************
    Report
    ********************************************************
    addressRepository: {addressRepository}
    poolRepository: {poolRepository}
    positionRepository: {positionRepository}
    priceRepository: {priceRepository}

    gToken4DAI: {gToken4DAI}
    vault4DAI: {vault4DAI}
    pool4DAI: {pool4DAI}

    gToken4USDC: {gToken4USDC}
    vault4USDC: {vault4USDC}
    pool4USDC: {pool4USDC}

    gToken4LINK: {gToken4LINK}
    vault4LINK: {vault4LINK}
    pool4LINK: {pool4LINK}
    ********************************************************
    """)
