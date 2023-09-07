from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.SearchContractActions import SearchContractActions

def monitoring_contracts(driver: DriverInterface, *situacoes) -> list:
    actions = SearchContractActions(driver)
    contracts = []
    actions.navigate_search_simple()
    actions.search_simple_by_situation(*situacoes)
    contracts = actions.get_contracts()
    return contracts;