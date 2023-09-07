from Library_v1.LegalOne.Fields.DropdownField import DropdownField
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions
import re
from Utils.string import (default_space, default_lower, clear_accents, search_into_str_i, )

class DropdownMultiLevelSelectionField(DropdownField):
    def __init__(self, driver: DriverInterface, dropdown_xpath: str) -> None:
        self.driver = driver
        self.action = DriverActions(self.driver)
        super().__init__(dropdown_xpath)

    def set_value(self, *values):
        # print("====================================================================")
        input = default_space(values[0])
        # print(f"input: {input}")
        levels = [default_lower(clear_accents(x)) for x in re.split(r"\s*\/\s*", input)]
        # print(f"levels: {levels}")
        input_xpath = f"{self.get_xpath()}//input[@type='text']"
        lookup_show_xpath = f"{self.get_xpath()}//div[contains(@class, 'lookup-show')]"
        lookup_dropdown_xpath = "//div[contains(@class, 'lookup-dropdown')][last()]"
        lookup_loading_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'lookup-loading')]"
        rows_xpath = f"({lookup_dropdown_xpath})//table/tbody/tr"
        empty_box_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'empty-box')]"
        # print(f"input_xpath: {input_xpath}")
        # print(f"lookup_show_xpath: {lookup_show_xpath}")
        # print(f"lookup_dropdown_xpath: {lookup_dropdown_xpath}")
        # print(f"lookup_loading_xpath: {lookup_loading_xpath}")
        # print(f"rows_xpath: {rows_xpath}")
        # print(f"empty_box_xpath: {empty_box_xpath}")

        # --------------------------------------------------
        # Buscar o valor atual do campo
        current_input = self.action.get_attr(input_xpath, 'value')
        # print(f"current_input: {current_input}")
        if input == current_input: return [] # melhorar a verificação

        # --------------------------------------------------
        # Inserindo a opção
        self.action.press_enter(input_xpath)
        self.action.disappear_element(lookup_loading_xpath)
        self.action.clear_element(input_xpath)
        self.action.write_element(input_xpath, input)
        self.action.press_enter(input_xpath)
        self.action.disappear_element(lookup_loading_xpath)
        if self.action.has_element(empty_box_xpath, time=0): raise ValueError(f"Não foi encontrado a busca de '{input}'")
        
        # --------------------------------------------------
        # Ler as opções da busca
        options = []
        rows_el = self.action.get_elements(rows_xpath, time=0)
        last_elements = []
        for row_el in rows_el:
            content_row = self.action.get_text(row_el)
            # print(f"levels[-1]: {levels[-1]} / content_row: {content_row}")
            if search_into_str_i(levels[-1], content_row) >= 0:
                last_elements.append(row_el)
        # print(f"last_elements: {last_elements}")
        for el in last_elements:
            current_el = el
            option = []
            while True:
                content_row = default_space(self.action.get_text(current_el))
                id = self.action.get_attr(current_el, 'id')
                option.insert(0, (id, content_row))
                if not self.action.has_class(current_el, 'child-of'): break;
                match = re.search(r"child-of-(\d+)", self.action.get_attr(current_el, 'class'))
                father_id = match.group(1)
                row_xpath = f"{rows_xpath}[@id='{father_id}' and contains(@class, 'initialized')]"
                # print(f"row_xpath: {row_xpath}")
                current_el = self.action.get_element(row_xpath)
            options.append(option)
        # print(f"options: {options}")

        # --------------------------------------------------
        # Comprar as entradas para buscar a que bate
        match_options = []
        input_default = " / ".join(levels)
        # print(f"input_default: {input_default}")
        for option in options:
            current_default = " / ".join([default_lower(clear_accents(x[1])) for x in option])
            # print(f"current_default: {current_default}")
            if current_default == input_default:
                match_options.append(option)
        # print(f"match_options: {match_options}")
        
        if len(match_options) <= 0: raise ValueError(f"Não foi encontrado a busca de '{input}'")

        first_option = match_options[0]
        last_id = first_option[-1][0]
        # print(f"last_id: {last_id}")
        row_xpath = f"{rows_xpath}[@id='{last_id}' and contains(@class, 'initialized')]"
        # print(f"row_xpath: {row_xpath}")
        self.action.click_element(row_xpath)

        if re.search(r"display\s*\:\s*block", self.action.get_attr(lookup_dropdown_xpath, 'style'), flags=re.I):
            self.action.click_element(lookup_show_xpath)

