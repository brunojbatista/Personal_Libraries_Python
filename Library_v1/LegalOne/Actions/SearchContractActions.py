from Library_v1.LegalOne.Actions.LegalOneActions import LegalOneActions
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.xpath import get_xpath
import re

from Library_v1.LegalOne.Fields.Actions.DropdownMultipleSelectionField import DropdownMultipleSelectionField
from Library_v1.LegalOne.Fields.Actions.DropdownSimpleSelectionField import DropdownSimpleSelectionField

class SearchContractActions(LegalOneActions):
    def __init__(self, driver: DriverInterface = None) -> None:
        super().__init__(driver)

    def navegate_search_page(self, ):
        if not self.in_url("/contratos/contratocliente/search"):
            self.navigate_page('search')
        return self;

    def navigate_search_advanced(self, ):
        self.navegate_search_page()
        button_filter = self.get_element(get_xpath("busca_avancada", "filtro_avancado"))
        if not self.has_class(button_filter, "active"):
            self.click_element_with_loading(
                get_xpath("busca_avancada", "filtro_avancado"),
                get_xpath("busca_avancada", "filtro_carregamento"),
            )
        return self;

    def search_advanced_contract(self, folder: str, contract: str):
        try:
            DropdownMultipleSelectionField(self.get_driver(), get_xpath("busca_avancada", "lookup_pasta")).set_value(folder)
            self.click_element(get_xpath("busca_avancada", "botao_pesquisar"))
        except ValueError:
            self.clear_element(get_xpath("busca_avancada", "input_numero_contrato"))
            self.write_element(get_xpath("busca_avancada", "input_numero_contrato"), contract)
        self.click_element(get_xpath("busca_avancada", "botao_pesquisar"))
        return self;
    
    def enter_contract(self, folder: str):
        rows_el = self.get_elements(get_xpath("busca_avancada", "tabela_pesquisa"), time=10)
        has_found = False
        for index, row_el in enumerate(rows_el):
            data_folder_el = self.set_ref(row_el).get_element("./td[3]")
            folder_txt = self.get_text(data_folder_el)
            if folder_txt == folder:
                self.click_element_by_js(f"({get_xpath('busca_avancada', 'tabela_pesquisa')}[{index+1}])/td[3]")
                has_found = True;
        if not has_found: raise ValueError(f"Não foi encontrado o contrato na busca com a pasta '{folder}'")
        return self;

    def navigate_search_simple(self, ):
        self.navegate_search_page()
        button_filter = self.get_element(get_xpath("busca_simples", "filtro_simples"))
        if not self.has_class(button_filter, "active"):
            self.click_element_with_loading(
                get_xpath("busca_simples", "filtro_simples"),
                get_xpath("busca_simples", "filtro_carregamento"),
            )
        return self;

    def search_simple_by_situation(self, *situations):
        DropdownMultipleSelectionField(self.get_driver(), get_xpath("busca_simples", "lookup_situacao")).set_value(*situations)
        self.click_element(get_xpath("busca_simples", "botao_pesquisar"))
        return self;

    def get_contracts(self, ):
        contracts = []
        rows_el = self.get_elements(get_xpath("busca_simples", "tabela_pesquisa"), time=10)
        for row_el in rows_el:
            folder_el       = self.set_ref(row_el).get_element("./td[3]")
            link_el         = self.set_ref(folder_el).get_element("./a")
            situation_el    = self.set_ref(row_el).get_element("./td[6]/a")
            contracted_person_el    = self.set_ref(row_el).get_element("./td[7]/a")
            contractor_person_el    = self.set_ref(row_el).get_element("./td[8]/a")
            responsible_person_el   = self.set_ref(row_el).get_element("./td[9]/a")

            folder_txt      = self.get_text(folder_el)
            situation_txt   = self.get_text(situation_el)
            url_txt         = self.get_attr(link_el, 'href')
            contracted_person_txt   = self.get_text(contracted_person_el)
            contractor_person_txt   = self.get_text(contractor_person_el)
            responsible_person_txt  = self.get_text(responsible_person_el)

            contracts.append({
                "pasta": folder_txt,
                "situacao": situation_txt,
                "contratado": contracted_person_txt,
                "contratante": contractor_person_txt,
                "responsavel": responsible_person_txt,
                "url": re.sub(r"\?.+", "", url_txt),
            })
            
        return contracts;