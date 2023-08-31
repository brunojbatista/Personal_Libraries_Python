import time;
import re;

from selenium.webdriver.common.by import By

class ec_match_text_i(object):

    def __init__(self, xpath: str, regex: str):
        self.xpath = xpath
        self.regex = regex

    def __call__(self, driver):
        text = driver.find_element(By.XPATH, self.xpath).text
        return re.search(self.regex, str(text), flags=re.I) != None;
