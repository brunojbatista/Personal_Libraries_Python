from Library_v1.LegalOne.Fields.DropdownField import DropdownField
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions
import re

class DropdownSimpleSelectionField(DropdownField):
    def __init__(self, driver: DriverInterface, dropdown_xpath: str) -> None:
        self.driver = driver
        self.action = DriverActions(self.driver)
        super().__init__(dropdown_xpath)

    def set_value(self, *values):
        input = values[0]
        input_xpath = f"{self.get_xpath()}//input[@type='text']"
        lookup_show_xpath = f"{self.get_xpath()}//div[contains(@class, 'lookup-show')]"
        lookup_dropdown_xpath = "//div[contains(@class, 'lookup-dropdown')][last()]"
        lookup_loading_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'lookup-loading')]"
        rows_xpath = f"({lookup_dropdown_xpath})//table/tbody/tr"
        empty_box_xpath = f"({lookup_dropdown_xpath})//div[contains(@class, 'empty-box')]"

        # --------------------------------------------------
        # Buscar o valor atual do campo
        current_input = self.action.get_attr(input_xpath, 'value')
        if input == current_input: return []

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
        # Buscando a opção
        has_found = False
        datas = []
        for index, row_el in enumerate(self.action.get_elements(rows_xpath, time=0)):
            datas = [self.action.get_text(el) for el in self.action.set_ref(row_el).get_elements("./td")]
            if input in datas:
                row_xpath = f"({lookup_dropdown_xpath})//table//tr[{index+1}]"
                self.action.click_element(row_xpath)
                has_found = True
        if not has_found: 
            raise ValueError(f"Não foi encontrado a busca de '{input}'")
        if re.search(r"display\s*\:\s*block", self.action.get_attr(lookup_dropdown_xpath, 'style'), flags=re.I):
            self.action.click_element(lookup_show_xpath)
        return datas;