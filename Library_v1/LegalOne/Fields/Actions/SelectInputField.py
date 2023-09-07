from Library_v1.LegalOne.Fields.SelectField import SelectField
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions
import re

class SelectInputField(SelectField):
    def __init__(self, driver: DriverInterface, dropdown_xpath: str) -> None:
        self.driver = driver
        self.action = DriverActions(self.driver)
        super().__init__(dropdown_xpath)

    def set_value(self, *values):
        value = values[0]
        select_xpath = self.get_xpath()
        select_el = self.action.get_element(select_xpath)
        options_el = self.action.set_ref(select_el).get_elements("./option", time=0)
        has_found = False
        for option_el in options_el:
            option_txt = self.action.get_text(option_el)
            if option_txt == value:
                self.action.write_element(select_xpath, value)
                has_found = True
        if not has_found: 
            raise ValueError(f"Não foi encontrado a seleção de '{value}'")