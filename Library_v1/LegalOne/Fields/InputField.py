from Library_v1.LegalOne.Fields.Field import Field
import re

class InputField(Field):
    def __init__(self, input_xpath: str) -> None:
        xpath = input_xpath
        if re.search(r"^\/\/", input_xpath): xpath = re.sub(r"^\/\/", "/", input_xpath)
        error_xpath = f"//div[.{xpath}]//div[contains(@class, 'error-validation-message')]/span"
        super().__init__(input_xpath, error_xpath)