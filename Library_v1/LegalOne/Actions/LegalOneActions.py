from Library_v1.Driver.DriverActions import DriverActions
from Library_v1.Driver.DriverInterface import DriverInterface

from Library_v1.LegalOne.xpath import get_xpath
from Library_v1.LegalOne.url import get_url
import re

class LegalOneActions(DriverActions):
    def __init__(self, driver: DriverInterface = None) -> None:
        super().__init__(driver)
        
    def navigate_page(self, screen):
        return self.navigate_url(get_url(screen))
    
    def login(self, office: str, login: str, password: str):
        self.navigate_page("login")
        self.clear_element(get_xpath("login", "usuario"))
        self.clear_element(get_xpath("login", "senha"))
        self.write_element(get_xpath("login", "usuario"), login)
        self.write_element(get_xpath("login", "senha"), password)
        self.click_element(get_xpath("login", "entrar"))
        
    def click_element_with_loading(self, element_xpath, loading_xpath, time: int = 60):
        self.click_element(element_xpath, time)
        self.disappear_element(loading_xpath, time)


