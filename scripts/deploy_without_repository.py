import sys
sys.path.insert(0, "./scripts")
from brownie import accounts
from helpers import get_repository_with_addresses, generate_gvp
from constants import TOKENS, POSITION_REPOSITORY, POOL_REPOSITORY, PRICE_REPOSITORY, ADDRESS_REPOSITORY


def main():
    account = accounts.load('deployment_account')

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
