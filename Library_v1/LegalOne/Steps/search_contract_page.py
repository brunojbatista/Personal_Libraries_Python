# from Library_v1.Driver.DriverActions import DriverActions
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.SearchContractActions import SearchContractActions

# def search_contract(driver: DriverInterface, pasta: str, numero_contrato: str = None):
#     if not numero_contrato: numero_contrato = pasta
#     actions = SearchContractActions(driver)
#     actions.navigate_search_advanced()
#     actions.search_advanced_contract(pasta, numero_contrato)
#     actions.enter_contract(pasta)

def get_contracts_by_situation(driver: DriverInterface, situation: str):
    actions = SearchContractActions(driver)
    actions.navigate_search_simple()
    actions.search_simple_by_situation(situation)
    # Lista os contratos encontrados
    contracts = actions.get_contracts()
    return contracts