from Library_v1.LegalOne.Fields.DropdownField import DropdownField
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions
import re

class DropdownMultipleSelectionField(DropdownField):
    def __init__(self, driver: DriverInterface, dropdown_xpath: str) -> None:
        self.driver = driver
        self.action = DriverActions(self.driver)
        super().__init__(dropdown_xpath)

    def set_value(self, *values):
        # print(f"values: {values}")
        if len(values) <= 0: raise ValueError("É preciso de ao menos uma entrada para o dropdown")
        # ---------------------------------------------------------
        # Definiçao dos xpaths
        input_xpath = f"{self.get_xpath()}//input[@type='text']"
        lookup_show_xpath = f"{self.get_xpath()}//div[contains(@class, 'lookup-show')]"
        lookup_dropdown_xpath = "//div[contains(@class, 'lookup-dropdown')][last()]"
        lookup_loading_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'lookup-loading')]"
        items_xpath = f"{self.get_xpath()}//input[@type='hidden' and @data-val-id and @data-val-type='text']"
        options_xpath = f"({lookup_dropdown_xpath})//table//tr/td[2]"
        empty_box_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'empty-box')]"
        selected_items = []

        # ----------------------------------------------------------
        # Buscar os campos que já foram adicionados e o que faltam
        try:
            selected_inputs = [(self.action.get_attr(el, 'value'), self.action.get_attr(el, 'data-val-id')) for el in self.action.get_elements(items_xpath, time=0)]
        except Exception:
            selected_inputs = []
        remove_entries  = [i for i in selected_inputs if i[0] not in values]
        only_values = []
        if len(selected_inputs) > 0: only_values = [x for x in selected_inputs[0]]
        missing_entries = [i for i in values if i not in only_values]

        # print(f"missing_entries: {missing_entries}")
        # print(f"remove_entries: {remove_entries}")
        # print(f"selected_inputs: {selected_inputs}")
       
        self.action.press_enter(input_xpath)
        self.action.disappear_element(lookup_loading_xpath)

        # -------------------------------------------
        # Remover os que estão selecionados
        for _, data_id in remove_entries:
            exclude_xpath = f"({lookup_dropdown_xpath})//div[@class='lookup-selection-inner-wrapper']/div[@data-val-id='{data_id}']/div[contains(@class, 'exclude-button')]"
            self.action.click_element_by_js(exclude_xpath)

        # -------------------------------------------
        # Selecionar as entradas que estão faltando
        for missing_entry in missing_entries:
            self.action.clear_element(input_xpath)
            self.action.write_element(input_xpath, missing_entry)
            self.action.press_enter(input_xpath)
            self.action.disappear_element(lookup_loading_xpath)
            if self.action.has_element(empty_box_xpath, time=0): raise ValueError(f"Não foi encontrado a busca de '{missing_entry}'")
            has_found = False
            for index, option_el in enumerate(self.action.get_elements(options_xpath, time=0)):
                option_text = self.action.get_text(option_el)
                if option_text == missing_entry:
                    row_el = f"({lookup_dropdown_xpath})//table//tr[{index+1}]"
                    self.action.click_element_by_js(row_el)
                    has_found = True
            if not has_found: 
                self.action.click_element(lookup_show_xpath)
                raise ValueError(f"Não foi encontrado a busca de '{missing_entry}'")
        try:
            selected_items = [self.action.get_attr(el, 'value') for el in self.action.get_elements(items_xpath, time=0)]
        except Exception:
            selected_items = []
        if re.search(r"display\s*\:\s*block", self.action.get_attr(lookup_dropdown_xpath, 'style'), flags=re.I):
            self.action.click_element(lookup_show_xpath)
        return selected_items;