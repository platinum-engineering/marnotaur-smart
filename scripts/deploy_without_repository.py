import sys
sys.path.insert(0, "./scripts")
from brownie import accounts
from helpers import get_repository_with_addresses, generate_gvp
from constants import TOKENS

POSITION_REPOSITORY = '0x89267e15b0faECD6B6d28a20148ed662D481B269'
POOL_REPOSITORY = '0x7E2c9c5E3Dc138b9B2e8C14E1d5bEFCb72aeBa73'
PRICE_REPOSITORY = '0x35E9e4D9B79edF67dfC4A6C2cF1f491157647F18'
ADDRESS_REPOSITORY = '0xbC58035c8bC416c7a446335367Fb2f540Efd7E7e'


def main():
    account = accounts.load('deployment_rinkeby_account')

    positionRepository, poolRepository, priceRepository, addressRepository = get_repository_with_addresses(
        POSITION_REPOSITORY, POOL_REPOSITORY, PRICE_REPOSITORY, ADDRESS_REPOSITORY
    )

    for i in range(poolRepository.getPoolsCount()):
        poolRepository.setStatusPool(i, 2, {'from': account})

    resume = f"""
    ********************************************************
    Report
    ********************************************************
    """

    for key in TOKENS.keys():
        gToken, vault, pool = generate_gvp(
            account, TOKENS[key], positionRepository, poolRepository, priceRepository, addressRepository
        )

        resume += f"""
        {key}
        gToken: {gToken}
        vault: {vault}
        pool: {pool}
        """

    resume += "********************************************************"

    print(resume)
