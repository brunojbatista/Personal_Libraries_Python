# from DriverInterface import DriverInterface
from Library_v1.Driver.DriverInterface import DriverInterface
# from Library_v1.Driver.DriverInterface import DriverInterface

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder


from Library_v1.Driver.custom_ec.ec_changes_text import ec_changes_text
from Library_v1.Driver.custom_ec.ec_changes_url import ec_changes_url
from Library_v1.Driver.custom_ec.ec_has_attribute import ec_has_attribute
from Library_v1.Driver.custom_ec.ec_no_attribute import ec_no_attribute
from Library_v1.Driver.custom_ec.ec_changes_element import ec_changes_element
from Library_v1.Driver.custom_ec.ec_has_element import ec_has_element
from Library_v1.Driver.custom_ec.ec_has_no_element import ec_has_no_element
from Library_v1.Driver.custom_ec.ec_disappear_element import ec_disappear_element
from Library_v1.Driver.custom_ec.ec_match_text_i import ec_match_text_i
from Library_v1.Driver.custom_ec.ec_remove_text_by_backspace import ec_remove_text_by_backspace

from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
    presence_of_element_located,
    invisibility_of_element_located,
    presence_of_all_elements_located,
    visibility_of_all_elements_located,
) 

from selenium.common.exceptions import (
    ElementNotVisibleException, 
    ElementNotSelectableException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

from Library_v1.Utils.file import (
    download,
    delete_folder,
)

from Library_v1.Utils.string import (
    clear_accents,
)

import re;
from time import sleep;

# import requests;
# FILE_SAVER_MIN_JS_URL = "https://raw.githubusercontent.com/eligrey/FileSaver.js/master/dist/FileSaver.min.js"

# import os
# import sys
# import re;
# import urllib.request;

# def get_script_path():
#     return os.path.dirname(os.path.realpath(sys.argv[0]))

# def get_custom_path(relative_path: str):
#     folders = re.split(r"[\/\\]", re.sub(r"(^\s*\\+|^\s*\/+)", '', relative_path))
#     return re.sub(r"(\\+\s*$|\/+\s*$)", '', os.path.join(get_script_path(), *folders))]

from Library_v1.Directory.Directory import Directory

class DriverActions():

    def __init__(self, driver: DriverInterface = None) -> None:
        self.driver : DriverInterface = None;
        self.set_driver(driver);
        self.ref : str|WebElement = None;
    
    def get_driver(self, ) -> DriverInterface:
        return self.driver
    
    def get_download_path(self, ) -> str:
        return self.driver.get_download_path()

    def get_download_relativepath(self, ) -> str:
        return self.driver.get_download_relativepath()

    def sleep(self, time: float, offset_max: float = 0):
        timing = self.generate_random(time, offset_max)
        print(f"sleep: {timing} seconds")
        sleep(timing)

    def generate_random(self, value: float, offset_max: float = 0):
        from random import seed
        from random import random
        import time as t1
        seed(t1.time())
        new_value = value + offset_max*random()
        return new_value;

    def set_ref(self, ref : str|WebElement):
        # self.ref = ref;
        if isinstance(ref, str): ref = self.get_element(ref)
        self.ref = ref;
        return self;

    def clear_ref(self, ):
        return self.set_ref(None);
    
    def get_ref(self, ):
        ref = self.ref
        self.clear_ref();
        return ref;

    def set_driver(self, driver: DriverInterface):
        self.driver = None;
        if driver != None: self.driver = driver;
        return self;

    def open_driver(self, reopen: bool = False):
        if not(self.driver): raise ValueError("O driver não foi iniciado")
        if reopen: self.driver.open();
        elif not self.driver.is_open(): self.driver.open();
        return self;

    def lock(self, timeout : int = 30):
        self.driver.lock(timeout);

    def unlock(self, ):
        self.driver.unlock();

    def navigate_url(self, url: str):
        self.open_driver();
        self.driver.get_url(url)
        return self;

    def check_url(self, regex_match: str) -> bool:
        self.open_driver();
        return re.search(regex_match, self.get_url(), flags=re.I) != None;

    def in_url(self, search_url: str) -> bool:
        self.open_driver();
        cleared_search_url = re.sub(r'(\/\s*$)', '', search_url, flags=re.I)
        status = cleared_search_url in self.get_url();
        # print(f"in_url - cleared_search_url: {cleared_search_url} / url: {self.get_url()} / status: {status}")
        return status;

    def get_url(self, ):
        self.open_driver();
        return re.sub(r'(\/\s*$)', '', self.driver.get_current_url(), flags=re.I);

    def check_title(self, regex_match: str) -> bool:
        self.open_driver();
        return re.search(regex_match, clear_accents(self.driver.get_title()), flags=re.I) != None;

    def get_current_tab(self, ) -> str:
        self.open_driver();
        return self.driver.get_current_window()

    def get_tabs(self, ) -> list:
        self.open_driver();
        return self.driver.get_windows();

    def switch_tab(self, handle: str = None):
        if handle is None: return;
        self.open_driver();
        current_tab = self.get_current_tab()
        # if current_tab == handle: return;
        return self.driver.switch_window(handle)

    def new_tab(self, ):
        self.open_driver();
        return self.driver.new_window();

    def refresh(self, ):
        self.open_driver();
        return self.driver.refresh();

    def set_maximize(self, ):
        self.driver.set_maximize();
    
    def save_screenshot(self, name: str) -> str:
        return self.driver.save_screenshot(name)
    
    # ==========================================================================================
    # Funções que usam Expected Condition

    def get_element(self, xpath: str, type: str = 'presence', time: int = 60):
        self.open_driver();
        if time <= 0: time = 0.5;
        ec_function = None;
        locator = (By.XPATH, xpath)
        if type == 'presence' or type == 'pre':
            ec_function = presence_of_element_located(locator)
        elif type == 'visibility' or type == 'vis':
            ec_function = visibility_of_element_located(locator)
        elif type == 'invisibility' or type == 'invis':
            ec_function = invisibility_of_element_located(locator)
        else:
            raise ValueError("A busca do tipo do elemento não é conhecida");
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_function);
        except TimeoutException:
            raise ValueError(f"Elemento não encontrado")

    def get_elements(self, xpath: str, type: str = 'presence', time: int = 60):
        self.open_driver();
        if time <= 0: time = 0.5;
        ec_function = None;
        locator = (By.XPATH, xpath)
        if type == 'presence' or type == 'pre':
            ec_function = presence_of_all_elements_located(locator)
        elif type == 'visibility' or type == 'vis':
            ec_function = visibility_of_all_elements_located(locator)
        else:
            raise ValueError("A busca do tipo dos elementos não é conhecida");
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_function);
        except TimeoutException:
            raise ValueError(f"Elementos não encontrados")

    def has_element(self, xpath: str, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_has_element(xpath));
        except TimeoutException:
            return False;

    def disappear_element(self, xpath: str, time: int = 60) -> bool:
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_disappear_element(xpath));
        except TimeoutException:
            return False;

    def has_no_element(self, xpath: str, time: int = 60) -> bool:
        return self.disappear_element(xpath, time)
    
    def match_text_i(self, xpath: str, regex: str, time: int = 60):
        self.open_driver();
        if time <= 0: time = 0.5;
        try:
            return self.driver.set_wait(time, ref=self.get_ref()).set_condition(ec_match_text_i(xpath, regex));
        except TimeoutException:
            raise ValueError(f"O conteudo do elemento não foi encontrado")

    def promise(self, success_xpath: str, fail_xpath: str, time: int = 30) -> bool:
        status = False;
        step_time = 0.5;
        total_time = time
        ref = self.get_ref();
        while total_time > 0:
            if self.set_ref(ref).has_element(success_xpath, time=step_time):
                status = True;
                break;
            else:
                if self.set_ref(ref).has_element(fail_xpath, time=step_time):
                    status = False;
                    break;
                else:
                    total_time -= (2*step_time)
        if total_time <= 0: raise TimeoutError("Não foi possível resolver a promessa")
        return status;

    # ==========================================================================================
    # Funções que  usam funções de elementos

    def parse_element(self, xpath_or_webelement: str|WebElement, time: int = 60) -> WebElement:
        self.open_driver();
        el = xpath_or_webelement
        if isinstance(el, str): el = self.get_element(xpath_or_webelement, 'presence', time);
        return el;

    def clear_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        self.parse_element(xpath_or_webelement, time).clear();
        return True

    def write_element(self, xpath_or_webelement: str|WebElement, text: str, time: int = 60):
        self.parse_element(xpath_or_webelement, time).send_keys(text)
        return True

    def click_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        last_ref = self.get_ref();
        try:
            self.set_ref(last_ref).parse_element(xpath_or_webelement, time).click();
        except ElementClickInterceptedException:
            self.set_ref(last_ref).click_element_by_js(xpath_or_webelement, time)
        return True;

    def click_element_by_js(self, xpath_or_webelement: str|WebElement, time: int = 60):
        return self.driver.execute_script("arguments[0].click();", self.parse_element(xpath_or_webelement, time));

    def remove_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        return self.driver.execute_script("arguments[0].remove();", self.parse_element(xpath_or_webelement, time));

    def press_tab(self, xpath_or_webelement: str|WebElement, time: int = 60):
        self.parse_element(xpath_or_webelement, time).send_keys(Keys.TAB)
        return True;

    def press_enter(self, xpath_or_webelement: str|WebElement, time: int = 60):
        self.parse_element(xpath_or_webelement, time).send_keys(Keys.ENTER)
        return True;

    def press_backspace(self, xpath_or_webelement: str|WebElement, time: int = 60):
        self.parse_element(xpath_or_webelement, time).send_keys(Keys.BACKSPACE)
        return True;

    def has_stateless(self, xpath: str):
        try:
            el = self.parse_element(xpath)
            return False;
        except StaleElementReferenceException:
            return True;

    def clear_field_backspace(self, xpath_or_webelement: str|WebElement, time: int = 60):
        el = self.parse_element(xpath_or_webelement, time)
        total_caracters = len(el.get_attribute("value"))
        while total_caracters > 0:
            self.press_backspace(el);
            value = el.get_attribute("value")
            if re.search(r"^\s*$", str(value)) != None:
                return True;
            total_caracters -= 1;
            if total_caracters <= 0: raise ValueError("Não foi possível limpar o texto")

    def scroll_down(self, ):
        import time;
        self.open_driver();
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height >= last_height:
                break
            last_height = new_height
        return True;
        
    def download(self, url: str, filename: str, relative_path: str = ''):
        # print("------------------------------------------------------------------")
        # print(">> Download:")
        # print(f"url: {url} / filename: {filename} / relative_path: {relative_path}")
        return download(url, filename, relative_path)
        
    def drag_element(self, xpath_or_webelement: str|WebElement, pos_x: int, pos_y: int, time: int = 60):
        self.open_driver();
        el = self.parse_element(xpath_or_webelement, time)
        action = ActionChains(self.driver.get())
        return action.move_to_element_with_offset(el, pos_x, pos_y).click().perform()

    def get_text(self, xpath_or_webelement: str|WebElement, time: int = 60):
        return self.parse_element(xpath_or_webelement, time).text;

    def get_attr(self, xpath_or_webelement: str|WebElement, attr_name: str, time: int = 60):
        return self.parse_element(xpath_or_webelement, time).get_attribute(attr_name);

    def has_class(self, xpath_or_webelement: str|WebElement, name: str, time: int = 60) -> bool:
        return name in self.get_attr(xpath_or_webelement, 'class', time)
    
    # ==========================================================================================
    def force_click_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        attempts = 20
        has_finished = False
        while True:
            if attempts <= 0: break;
            try:
                self.sleep(0.5)
                self.click_element(xpath_or_webelement, time)
                has_finished = True;
                break;
            except ElementNotInteractableException:
                attempts -= 1;
                
        if not has_finished: raise ValueError("A tentativa de forçar o clique não funcionou")

    def force_write_element(self, xpath_or_webelement: str|WebElement, time: int = 60):
        attempts = 60
        has_finished = False
        while True:
            if attempts <= 0: break;
            try:
                self.sleep(1)
                self.write_element(xpath_or_webelement, time)
                has_finished = True;
                break;
            except ElementNotInteractableException:
                attempts -= 1;
                
        if not has_finished: raise ValueError("A tentativa de escrever não funcionou")
    
    # ==========================================================================================
    # Comportamentos como humano
    def digit_like_human(self, text: str):
        letters = re.split('', text)
        letters = [x for x in re.split('', text) if x != '']
        if len(letters) <= 0: return;
        action = ActionChains(self.driver.get())
        for letter in letters:
            action = action.pause(self.generate_random(0.05, 0.05)).send_keys(letter)
        action.perform();

    # def clear_like_human(self, ):

    # Movendo um elemento para dentro do outro
    def drag_and_drop_element(self, drag_el: WebElement, drop_el: WebElement):
        ActionChains(self.driver.get()).drag_and_drop(drag_el, drop_el).perform()
        return self;

    def scroll_to_element(self, target_el: WebElement):
        ActionChains(self.driver.get()).scroll_to_element(target_el).perform()
