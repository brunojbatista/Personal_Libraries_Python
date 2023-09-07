from Library_v1.LegalOne.Fields.Field import Field

class SelectField(Field):
    def __init__(self, input_xpath: str) -> None:
        super().__init__(input_xpath, None)