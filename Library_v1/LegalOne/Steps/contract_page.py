# from Library_v1.Driver.DriverActions import DriverActions
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.ContractActions import ContractActions

from Library_v1.Utils.string import (
    clear_accents,
    create_regex_lowercase_str,
)

from Library_v1.Directory.Directory import Directory
import re;

def navigate_contract_page(driver: DriverInterface, contract_id: str):
    actions = ContractActions(driver)
    actions.navigate_url_contract(contract_id)

def download_geds(driver: DriverInterface, geds: list):
    dir = Directory('Downloads/')
    actions = ContractActions(driver)
    for ged in geds:
        link = ged['download_link']
        name = ged['name']
        actions.navigate_url(link)
        regex = create_regex_lowercase_str(name)
        print(f"regex file: {regex}")
        dir.wait_filename(lambda filename: re.search(regex, filename))
    return dir.find_files(r".*")

def get_geds_by_file_type(driver: DriverInterface, contract_id: str, *types):
    types = [clear_accents(x) for x in types]
    print(f"types: {types}")
    actions = ContractActions(driver)
    actions.navigate_url_contract(contract_id)
    actions.click_tab('GED')
    geds = actions.read_table_ged()
    # print(f"geds: {geds}")
    ged_filtered = [ x for x in geds if clear_accents(x["type_file"]) in types ]
    # print(f"ged_filtered: {ged_filtered}")
    return ged_filtered

def check_file_type(geds: list, *types):
    types = [clear_accents(x) for x in types]
    remain_types = types
    for ged in geds:
        type_file = clear_accents(ged['type_file'])
        if type_file in types:
            remain_types.remove(type_file)
    if len(remain_types) > 0: raise ValueError(f"Não foram encontrados o seguintes tipos(s) de arquivo(s) {', '.join(remain_types)}")
    return True;

def change_situation_contract(driver: DriverInterface, contract_id: str, situation: str):
    actions = ContractActions(driver)
    actions.navigate_url_contract(contract_id)
    actions.navigate_contract_edit(contract_id)
    actions.set_field_situacao(situation)
    actions.click_button_save_close()
    # actions.sleep(3600)

def add_progress_contract(driver: DriverInterface, contract_id: str, progress_list: list):
    actions = ContractActions(driver)
    actions.navigate_url_contract(contract_id)
    actions.click_tab('Andamentos')
    actions.click_new_progress()