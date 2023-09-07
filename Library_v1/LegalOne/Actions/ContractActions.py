from Library_v1.LegalOne.Actions.LegalOneActions import LegalOneActions
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.url import get_url
from Library_v1.LegalOne.xpath import get_xpath
import re

class ContractActions(LegalOneActions):
    def __init__(self, driver: DriverInterface = None) -> None:
        super().__init__(driver)

    def navigate_new_contract(self, ):
        if not self.in_url("/contratos/contratocliente/create"):
            self.navigate_page('new_contract')
        return self;

    def navigate_contract_progress(self, contract_id: str):
        regex = f"\/contratos\/contratocliente\/.*?\/{contract_id}"
        if not self.check_url(regex):
            self.navigate_url(f"{get_url('main_base')}/contratos/contratocliente/DetailsAndamentos/{contract_id}")

    def navigate_contract_ged(self, contract_id: str):
        regex = f"\/ged\/gedarquivos\/details\/{contract_id}"
        if not self.check_url(regex):
            self.navigate_url(f"{get_url('main_base')}/GED/GEDArquivos/details/{contract_id}")

    def navigate_new_contract_progress(self, contract_id: str):
        regex = f"\/contratos\/contratoclienteandamentos\/create\?.*?parentId\={contract_id}"
        if not self.check_url(regex):
            self.navigate_url(f"{get_url('main_base')}/contratos/contratoclienteandamentos/create?parentId={contract_id}")
    
    def click_button_save_close(self, ):
        self.click_element("//button[text()='Salvar e fechar']")

    def click_button_save_new(self, ):
        self.click_element("//button[text()='Salvar e novo']")

    def click_button_cancel(self, ):
        self.click_element("//div[contains(@class, 'footer-buttons')]/a[contains(text(), 'Cancelar')]")

    def click_tab(self, tab_name: str):
        if tab_name != 'Dados principais':
            tab_xpath = f"//ul[contains(@class, 'tab-navigation')]/li/a[contains(text(), '{tab_name}')]"
            self.click_element(tab_xpath)
            self.disappear_element("//div[@id='tab-container' and contains(@class, 'widget-loading')]")
        else:
            url = self.get_url()
            match = re.search(r"(\d+)$", url)
            id = match.group(1)
            url = f"https://regispontesadvogados.novajus.com.br/contratos/contratocliente/details/{id}"
            self.navigate_url(url)

    def read_table_elements(self, ) -> list:
        return self.get_elements(get_xpath("contrato", "lista_tabela"))

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

            ged_info.append({
                "date": date_txt,
                "name": name_txt,
                "name_link": name_link,
                "type": type_txt,
                "download_link": download_txt,
            })
        return ged_info
