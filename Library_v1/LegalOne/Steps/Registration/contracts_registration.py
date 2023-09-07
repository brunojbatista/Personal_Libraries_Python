from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Excel.RowExcel import RowExcel
from Library_v1.LegalOne.Actions.ContractActions import ContractActions
from Library_v1.Driver.ChromeDriver import ChromeDriver
from Library_v1.LegalOne.Rules.ContractRules import ContractRules
from Library_v1.LegalOne.xpath import get_xpath
import re
from Utils.string import (slug_name, )

from Library_v1.LegalOne.Fields.Actions.DropdownSimpleSelectionField import DropdownSimpleSelectionField
from Library_v1.LegalOne.Fields.Actions.DropdownMultiLevelSelectionField import DropdownMultiLevelSelectionField
from Library_v1.LegalOne.Fields.Actions.InsertInputField import InsertInputField
from Library_v1.LegalOne.Fields.Actions.SelectInputField import SelectInputField

def contract_registration(driver: DriverInterface, row: RowExcel) -> str:
    actions = ContractActions(driver)
    rules = ContractRules(row)

    actions.navigate_new_contract()

    DropdownMultiLevelSelectionField(driver, get_xpath("contrato", "escritorio_responsavel")).set_value(rules.get_value("escritorio_responsavel"))

    DropdownSimpleSelectionField(driver, get_xpath("contrato", "modalidade")).set_value(rules.get_value("modalidade"))
    
    InsertInputField(driver, get_xpath("contrato", "pasta")).set_value(rules.get_value("pasta"))

    InsertInputField(driver, get_xpath("contrato", "numero_contrato")).set_value(rules.get_value("numero_contrato"))

    DropdownSimpleSelectionField(driver, get_xpath("contrato", "situacao")).set_value(rules.get_value("situacao"))

    SelectInputField(driver, get_xpath("contrato", "prioridade")).set_value(rules.get_value("prioridade"))

    vendedor_values = DropdownSimpleSelectionField(driver, get_xpath("contrato", "vendedor")).set_value(rules.get_value("vendedor"))
    # print(f"vendedor_values: {vendedor_values}")

    comprador_values = DropdownSimpleSelectionField(driver, get_xpath("contrato", "comprador")).set_value(rules.get_value("comprador"))
    # print(f"comprador_values: {comprador_values}")

    DropdownSimpleSelectionField(driver, get_xpath("contrato", "responsavel")).set_value(rules.get_value("responsavel"))

    # -----------------------------------------------
    # Seleção do cliente
    client_option = rules.check_customer(rules.get_value("cliente"), vendedor_values, comprador_values)
    if client_option < 0: actions.click_element_by_js(get_xpath("contrato", "cliente_vendedor"))
    else: actions.click_element_by_js(get_xpath("contrato", "cliente_comprador"))

    actions.click_button_save_close()

    # -----------------------------------------------
    # Buscar o ID do contrato cadastrado
    contrato_link_el = actions.get_element(get_xpath("contrato", "edit_link"), time=10)
    contract_id = re.sub(r".*\/", "", actions.get_attr(contrato_link_el, "href"))
    print(f"contract_id: {contract_id}")
    

    return contract_id;

