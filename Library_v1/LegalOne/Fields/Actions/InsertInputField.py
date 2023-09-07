from Library_v1.LegalOne.Fields.InputField import InputField
from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions
import re

class InsertInputField(InputField):
    def __init__(self, driver: DriverInterface, dropdown_xpath: str) -> None:
        self.driver = driver
        self.action = DriverActions(self.driver)
        super().__init__(dropdown_xpath)

    def set_value(self, *values):
        input = values[0]
        # --------------------------------------------------
        # Buscar o valor atual do campo
        current_input = self.action.get_attr(self.get_xpath(), 'value')
        if input == current_input: return

        # --------------------------------------------------
        # Inserindo a opção
        self.action.clear_element(self.get_xpath())
        self.action.write_element(self.get_xpath(), input)