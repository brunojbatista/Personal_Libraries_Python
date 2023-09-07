from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Excel.RowExcel import RowExcel
from Library_v1.LegalOne.Actions.ContractActions import ContractActions
from Library_v1.LegalOne.Rules.ProgressRules import ProgressRules
from Library_v1.LegalOne.xpath import get_xpath

from Library_v1.LegalOne.Fields.Actions.DropdownMultiLevelSelectionField import DropdownMultiLevelSelectionField
from Library_v1.LegalOne.Fields.Actions.DropdownSimpleSelectionField import DropdownSimpleSelectionField
from Library_v1.LegalOne.Fields.Actions.InsertInputField import InsertInputField

def contract_progress(driver: DriverInterface, row: RowExcel, contract_id: str):
    actions = ContractActions(driver)
    rules = ProgressRules(row)

    # -------------------------------------------------------
    # Verificar se está dentro do contrato com o id
    actions.navigate_new_contract_progress(contract_id)

    DropdownMultiLevelSelectionField(driver, get_xpath("andamento", "situacao")).set_value(rules.get_value("situacao"))

    DropdownSimpleSelectionField(driver, get_xpath("andamento", "responsavel")).set_value(rules.get_value("responsavel"))

    InsertInputField(driver, get_xpath("andamento", "descricao_andamento")).set_value(rules.get_value("descricao_andamento"))

    actions.click_button_save_close()
    
    return True;
