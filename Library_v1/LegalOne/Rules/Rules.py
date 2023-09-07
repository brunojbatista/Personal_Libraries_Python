from Library_v1.Excel.RowExcel import RowExcel
from Utils.string import (
    slug_name,
    create_regex_latin_str,
)
import re

class Rules():
    def __init__(self, row: RowExcel) -> None:
        self.row = row
        self.formatted = {}
        self.rules = {}

    def generate_slug(self, name) -> str:
        slug = slug_name(name)
        # print(f"slug: {slug}")
        return slug;

    def generate_regex(self, name) -> str:
        regex = create_regex_latin_str(name)
        # print(f"regex: {regex}")
        return regex;

    def apply_rule(self, field: str, adjustment_function = lambda x: x, *additional_fields):
        if len(additional_fields) <= 0:
            self.formatted[self.generate_slug(field)] = adjustment_function(
                self.row.regex(self.generate_regex(field)).get()
            )
        else:
            values_fields = []
            for additional_field in additional_fields:
                values_fields.append(self.row.regex(self.generate_regex(additional_field)).get())
            self.formatted[self.generate_slug(field)] = adjustment_function(
                self.row.regex(self.generate_regex(field)).get(),
                *values_fields
            )

    def apply_rules(self, ):
        raise NotImplementedError("É preciso implementar a aplicação de regras de negócio dos campos")

    def get_value(self, field: str):
        field_slug = self.generate_slug(field)
        if field_slug not in self.formatted: raise ValueError(f"O campo '{field}' não existe")
        return self.formatted[field_slug]