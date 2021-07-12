import sys
sys.path.insert(0, "./scripts")
from brownie import accounts
from helpers import get_repository_with_addresses, generate_gvp

POSITION_REPOSITORY = "0x89267e15b0faECD6B6d28a20148ed662D481B269"
POOL_REPOSITORY = "0x7E2c9c5E3Dc138b9B2e8C14E1d5bEFCb72aeBa73"
PRICE_REPOSITORY = "0x35E9e4D9B79edF67dfC4A6C2cF1f491157647F18"
ADDRESS_REPOSITORY = "0xbC58035c8bC416c7a446335367Fb2f540Efd7E7e"
DAI_ADDRESS = "0xc7AD46e0b8a400Bb3C915120d284AafbA8fc4735"
USDC_ADDRESS = "0x4DBCdF9B62e891a7cec5A2568C3F4FAF9E8Abe2b"
LINK_ADDRESS = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
UNISWAP_PAIR_DAI = "0x2bA49Aaa16E6afD2a993473cfB70Fa8559B523cF"
UNISWAP_PAIR_USDC = "0xa24de01df22b63d23Ebc1882a5E3d4ec0d907bFB"
UNISWAP_PAIR_LINK = "0xd8bD0a1cB028a31AA859A21A3758685a95dE4623"


def main():
    account = accounts.load('deployment_rinkeby_account')

    positionRepository, poolRepository, priceRepository, addressRepository = get_repository_with_addresses(
        POSITION_REPOSITORY, POOL_REPOSITORY, PRICE_REPOSITORY, ADDRESS_REPOSITORY
    )

    for i in range(poolRepository.getPoolsCount()):
        poolRepository.setStatusPool(i, 2, {'from': account})

    gToken4DAI, vault4DAI, pool4DAI = generate_gvp(
        account, DAI_ADDRESS, UNISWAP_PAIR_DAI, positionRepository, poolRepository, priceRepository, addressRepository
    )
    gToken4USDC, vault4USDC, pool4USDC = generate_gvp(
        account, USDC_ADDRESS, UNISWAP_PAIR_USDC, positionRepository, poolRepository, priceRepository, addressRepository
    )
    gToken4LINK, vault4LINK, pool4LINK = generate_gvp(
        account, LINK_ADDRESS, UNISWAP_PAIR_LINK, positionRepository, poolRepository, priceRepository, addressRepository
    )

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
