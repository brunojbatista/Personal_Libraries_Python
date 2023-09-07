from Library_v1.Excel.RowExcel import RowExcel
from Library_v1.LegalOne.Rules.Rules import Rules
from Utils.string import (
    slug_name,
    create_regex_latin_str,
)
import re

class ProgressRules(Rules):
    def __init__(self, row: RowExcel) -> None:
        super().__init__(row)
        self.apply_rules()

    def apply_rules(self, ):
        # ---------------------------------------------------
        # Situação
        self.apply_rule("Situação")

        # ---------------------------------------------------
        # Descrição andamento
        self.apply_rule("Descrição andamento")

        # ---------------------------------------------------
        # Modalidade
        self.apply_rule("Responsável")

        print(f"self.formatted: {self.formatted}")

        return self;