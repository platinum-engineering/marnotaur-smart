import pytest


def test_allow_token_for_trading(contract_vaultservice, contract_gtoken, contract_pricerepository, contract_poolservice):
    contract_vaultservice.transferOwnership(contract_poolservice)
    contract_pricerepository.addToPoolServicesList(contract_poolservice)
    contract_poolservice.allowTokenForTrading(contract_gtoken, contract_poolservice)
    find_token = False
    for i in range(contract_poolservice.allowedTokenCount()):
        if contract_poolservice.allowedTokenById(i) == contract_gtoken:
            find_token = True
    assert find_token
