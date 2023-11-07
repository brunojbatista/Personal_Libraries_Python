from Library_v1.Driver.DriverActions import DriverActions
from Library_v1.Driver.DriverInterface import DriverInterface

from Library_v1.LegalOne.xpath import get_xpath
from Library_v1.LegalOne.url import get_url
import re

from Library_v1.LegalOne.XPath.XPath import XPath

from Library_v1.LegalOne.Fields.Actions.DropdownMultiLevelSelectionField import DropdownMultiLevelSelectionField
from Library_v1.LegalOne.Fields.Actions.DropdownMultipleSelectionField import DropdownMultipleSelectionField
from Library_v1.LegalOne.Fields.Actions.DropdownSimpleSelectionField import DropdownSimpleSelectionField

class LegalOneActions(DriverActions):
    def __init__(self, driver: DriverInterface = None) -> None:
        super().__init__(driver)
        self.xpath = XPath()
        self.navigate_page("login")
        
    def navigate_page(self, screen):
        return self.navigate_url(get_url(screen))
    
    def login(self, login: str, password: str):
        self.xpath.screen('login')
        self.clear_element(self.xpath.get("usuario"))
        self.clear_element(self.xpath.get("senha"))
        self.write_element(self.xpath.get("usuario"), login)
        self.write_element(self.xpath.get("senha"), password)
        self.click_element(self.xpath.get("entrar"))
        
    def click_element_with_loading(self, element_xpath, loading_xpath, time: int = 60):
        self.click_element(element_xpath, time)
        self.disappear_element(loading_xpath, time)

    def dropdown_multi_level_selection_field(self, element_xpath, *options):
        DropdownMultiLevelSelectionField(self.get_driver(), element_xpath).set_value(*options)

    def dropdown_multiple_selection_field(self, element_xpath, *options):
        DropdownMultipleSelectionField(self.get_driver(), element_xpath).set_value(*options)

    def dropdown_simple_selection_field(self, element_xpath, *options):
        DropdownSimpleSelectionField(self.get_driver(), element_xpath).set_value(*options)


