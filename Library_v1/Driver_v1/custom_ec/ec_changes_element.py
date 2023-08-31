import time;
import re;

from selenium.webdriver.common.by import By

class ec_changes_element(object):

    def __init__(self, xpath, element):
        # print(f"ref element: {element}")
        self.xpath = xpath
        self.element = element
        self.ref_id = element.id

    def __call__(self, driver):
        # print(f"******************** ec_changes_element")
        element = driver.find_element(By.XPATH, self.xpath);
        # print(f"element: {element}")
        current_id = element.id;
        if current_id != self.ref_id:
            return element;
        else:
            return False;
