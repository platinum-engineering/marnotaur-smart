import sys
sys.path.insert(0, "./scripts")
from brownie import accounts
from helpers import get_repository, generate_gvp
from constants import TOKENS, UNISWAP_ROUTER


def main():
    account = accounts.load('deployment_rinkeby_account')

    positionRepository, poolRepository, priceRepository, addressRepository = get_repository(
        account, UNISWAP_ROUTER
    )

    resume = f"""
    ********************************************************
    Report
    ********************************************************
    positionRepository: {positionRepository}
    poolRepository: {poolRepository}
    priceRepository: {priceRepository}
    addressRepository: {addressRepository}
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
