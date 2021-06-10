from brownie import PoolService, VaultService, DieselToken, PositionRepository, PoolRepository, PriceRepository, accounts

ADDRESS_REPOSITORY_ADDRESS = "0x0Cc7e060944b9867eF0fE55881B0e048968C07eD"
POSITION_REPOSITORY_ADDRESS = "0x43445AA0e398C59B739420e392B630220fF627BD"
POOL_REPOSITORY_ADDRESS = "0x30028f85Da90855fB0F00117715815bf51D42519"
PRICE_REPOSITORY_ADDRESS = "0x43D151471169d3905dB57f8f1B8f8C0A757653e8"
DAI_ADDRESS = "0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa"
USDC_ADDRESS = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b"
LINK_ADDRESS = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
UNISWAP_PAIR_DAU = "0x2bA49Aaa16E6afD2a993473cfB70Fa8559B523cF"
UNISWAP_PAIR_USDC = "0xa24de01df22b63d23Ebc1882a5E3d4ec0d907bFB"
UNISWAP_PAIR_LINK = "0xd8bD0a1cB028a31AA859A21A3758685a95dE4623"

def generate(token_address, uniswap_pair_address, account, positionRepository, poolRepository, priceRepository):
    gtoken = DieselToken.deploy('Test', 'TST', {'from': account})
    vault = VaultService.deploy(ADDRESS_REPOSITORY_ADDRESS, token_address, gtoken, {'from': account})
    pool = PoolService.deploy(ADDRESS_REPOSITORY_ADDRESS, vault, True, {'from': account})

    vault.transferOwnership(pool, {'from': account})
    positionRepository.addToPoolServicesList(pool, {'from': account})
    priceRepository.addToPoolServicesList(pool, {'from': account})
    poolRepository.addPool(pool, {'from': account})
    pool.allowTokenForTrading(token_address, uniswap_pair_address, {'from': account})

    return gtoken, vault, pool

def main():
    account = accounts.load('deployment_rinkeby_account')
    positionRepository = PositionRepository.at(POSITION_REPOSITORY_ADDRESS)
    poolRepository = PoolRepository.at(POOL_REPOSITORY_ADDRESS)
    priceRepository = PriceRepository.at(PRICE_REPOSITORY_ADDRESS)

    gToken4DAI, vault4DAI, pool4DAI = generate(DAI_ADDRESS, UNISWAP_PAIR_DAU, account, positionRepository, poolRepository, priceRepository)
    gToken4USDC, vault4USDC, pool4USDC = generate(USDC_ADDRESS, UNISWAP_PAIR_USDC, account, positionRepository, poolRepository, priceRepository)
    gToken4LINK, vault4LINK, pool4LINK = generate(LINK_ADDRESS, UNISWAP_PAIR_LINK, account, positionRepository, poolRepository, priceRepository)

    print(f"""
    ********************************************************
    Report
    ********************************************************
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
