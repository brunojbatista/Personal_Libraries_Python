from Library_v1.Driver.DriverInterface import DriverInterface


# from Library_v1.LegalOne.Actions.LegalOneActions import LegalOneActions
# from Library_v1.LegalOne.Actions.ContractActions import ContractActions

from Library_v1.Excel.StructExcel import StructExcel
from Library_v1.Excel.RowExcel import RowExcel


from Library_v1.LegalOne.Steps.login import login
from Library_v1.LegalOne.Steps.Registration.contracts_registration import (contract_registration, )
from Library_v1.LegalOne.Steps.Registration.contracts_progress import (contract_progress, )

def cycle_contracts_registration(driver: DriverInterface, filepath_excel: str):
    login(driver)
    excel = StructExcel()
    excel.read_excel(filepath_excel)
    excel.set_compare_column(lambda col_target, col_ref: col_target == col_ref)
    excel.foreach_row(lambda row: cycle_contract_registration(driver, row))
    return True

def cycle_contract_registration(driver: DriverInterface, row: RowExcel):
    # actions = ContractActions(driver)

    contract_id = contract_registration(driver, row)

    contract_progress(driver, row, contract_id)

    # Adicionar a geração da minuta


    # actions.sleep(3600)

    return True