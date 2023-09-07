from Library_v1.Excel.RowExcel import RowExcel
from Library_v1.LegalOne.Rules.Rules import Rules
from Utils.string import (
    slug_name,
    create_regex_latin_str,
    search_into_str_i,
)
import re

class ContractRules(Rules):
    def __init__(self, row: RowExcel) -> None:
        super().__init__(row)
        self.apply_rules()

    def apply_rules(self, ):
        # ---------------------------------------------------
        # Escritório responsável
        self.apply_rule("Escritório responsável")

        # ---------------------------------------------------
        # Pasta
        self.apply_rule("Pasta")

        # ---------------------------------------------------
        # Situação
        self.apply_rule("Situação")

        # ---------------------------------------------------
        # Número do Contrato
        self.apply_rule("Número do Contrato")

        # ---------------------------------------------------
        # Modalidade
        self.apply_rule("Modalidade")

        # ---------------------------------------------------
        # Prioridade
        self.apply_rule("Prioridade")

        # ---------------------------------------------------
        # Vendedor
        self.apply_rule("Vendedor")

        # ---------------------------------------------------
        # Comprador
        self.apply_rule("Comprador")

        # ---------------------------------------------------
        # Responsável
        self.apply_rule("Responsável")

        # ---------------------------------------------------
        # Cliente
        self.apply_rule("Cliente")

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        # ---------------------------------------------------
        # 

        print(f"self.formatted: {self.formatted}")

        return self;

    def check_customer(self, cliente: str, vendedores: list, compradores: list):
        for vendedor in vendedores:
            if search_into_str_i(cliente, vendedor) >= 0:
                return -1;
        for comprador in compradores:
            if search_into_str_i(cliente, comprador) >= 0:
                return 1;
        raise ValueError("Não foi possível determinar o cliente")