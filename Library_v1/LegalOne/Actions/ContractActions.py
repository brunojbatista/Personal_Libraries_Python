from Library_v1.LegalOne.Actions.LegalOneActions import LegalOneActions
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.url import get_url
from Library_v1.LegalOne.xpath import get_xpath
import re

from Library_v1.LegalOne.XPath.XPath import XPath

class ContractActions(LegalOneActions):
    def __init__(self, driver: DriverInterface = None) -> None:
        super().__init__(driver)
        self.xpath = XPath()
        self.xpath.screen("contract")

    def navigate_url_contract(self, contract_id: str): # ok
        if not self.in_url(f"/contratos/contratocliente/details/{contract_id}"):
            self.navigate_url(f"{get_url('main_base')}/contratos/contratocliente/details/{contract_id}")
        return self;

    def navigate_contract_edit(self, contract_id: str): # ok
        if not self.in_url(f"/contratos/ContratoCliente/edit/{contract_id}"):
            self.navigate_url(f"{get_url('main_base')}/contratos/ContratoCliente/edit/{contract_id}")
        return self;

    # def navigate_new_contract(self, ):
    #     if not self.in_url("/contratos/contratocliente/create"):
    #         self.navigate_page('new_contract')
    #     return self;

    # def navigate_contract_progress(self, contract_id: str):
    #     regex = f"\/contratos\/contratocliente\/.*?\/{contract_id}"
    #     if not self.check_url(regex):
    #         self.navigate_url(f"{get_url('main_base')}/contratos/contratocliente/DetailsAndamentos/{contract_id}")

    # def navigate_contract_ged(self, contract_id: str):
    #     regex = f"\/contratos\/contratocliente\/detailsged\/{contract_id}"
    #     if not self.check_url(regex):
    #         url = f"{get_url('main_base')}/contratos/contratocliente/detailsged/{contract_id}"
    #         print(f"url_ged: {url}")
    #         # https://regispontesadvogados.novajus.com.br/GED/GEDArquivos/details/71921
    #         # https://regispontesadvogados.novajus.com.br/contratos/contratocliente/detailsged/71921
    #         self.navigate_url(url)

    # def navigate_new_contract_progress(self, contract_id: str):
    #     regex = f"\/contratos\/contratoclienteandamentos\/create\?.*?parentId\={contract_id}"
    #     if not self.check_url(regex):
    #         self.navigate_url(f"{get_url('main_base')}/contratos/contratoclienteandamentos/create?parentId={contract_id}")
    
    def click_button_save_close(self, ):
        self.click_element(self.xpath.get("save_close_button"))

    def click_button_save_new(self, ):
        self.click_element(self.xpath.get("save_new_button"))

    def click_button_cancel(self, ):
        self.click_element(self.xpath.get("cancel_button"))

    def click_tab(self, tab_name: str):
        elements = self.get_elements(self.xpath.get("tabs_link"))
        for el in elements:
            text = self.get_text(el)
            if text == tab_name and not self.has_class(el, 'you-are-here'):
                self.click_element(el)
                self.disappear_element(self.xpath.get("loading"))
        return self;

    def read_table_elements(self, ) -> list:
        return self.get_elements(self.xpath.get("tabela_resultados"))

    def read_table_ged(self, ):
        rows_el = self.read_table_elements()
        ged_info = []
        for row_el in rows_el:
            date_el = self.set_ref(row_el).get_element("./td[1]")
            name_el = self.set_ref(row_el).get_element("./td[2]//a")
            type_el = self.set_ref(row_el).get_element("./td[3]//img")
            download_el = self.set_ref(row_el).get_element("./td[4]//a")

            date_txt = self.get_text(date_el)
            name_txt = self.get_text(name_el)
            name_link = self.get_attr(name_el, "href")
            type_txt = self.get_attr(type_el, "title")
            download_txt = self.get_attr(download_el, "href")

            type_file = '';
            if self.set_ref(row_el).has_element("./td[5]/a", time=0):
                el = self.set_ref(row_el).get_element("./td[5]/a")
                type_file = self.get_text(el)

            ged_info.append({
                "date": date_txt,
                "name": name_txt,
                "name_link": name_link,
                "type": type_txt,
                "download_link": download_txt,
                "type_file": type_file,
            })
        return ged_info
    
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def set_field_situacao(self, value: str):
        self.dropdown_simple_selection_field(self.xpath.get("situacao_field"), value)
