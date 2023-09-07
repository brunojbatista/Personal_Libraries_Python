from Library_v1.LegalOne.Fields.Field import Field
import re

class DropdownField(Field):
    def __init__(self, dropdown_xpath: str) -> None:
        xpath = dropdown_xpath
        if re.search(r"^\/\/", dropdown_xpath): xpath = re.sub(r"^\/\/", "/", dropdown_xpath)
        error_xpath = f"//div[.{xpath}]//div[contains(@class, 'error-validation-message')]/span"
        super().__init__(dropdown_xpath, error_xpath)