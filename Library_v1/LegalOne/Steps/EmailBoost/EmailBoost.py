from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.ContractActions import ContractActions
from Library_v1.Directory import Directory
from datetime import datetime
import pandas as pd
import datetime as dt

BRAND_SLUGS = [
    'mpc',
    'vix',
    'tempo',
    'lux',
    'desttra',
    'wx',
    'bep',
    'flow',
    'genial',
    'hydro',
    'merito',
    'mercatto',
    'thera',
    'ecel',
    'bc',
    'migratio',
    'maxima',
    'infinity',
    'kroma',
    'petra',
    'trinity',
    'multti',
    'energisa',
    'czarnikow',
    'urca',
    'canadian',
    'olympe',
    'squadra',
    'trifase',
    'amaggi',
]

from Utils.string import (
    format_folder_windows,
    create_regex_latin_str,
)
from Utils.time import (
    format_date,
    get_date,
)

from Library_v1.Excel.StructExcel import StructExcel
from Library_v1.Excel.RowExcel import RowExcel

from Library_v1.LegalOne.ContractJson import ContractJson

class EmailBoost():
    def __init__(self, driver: DriverInterface, contract_folder: str, contract_id: str) -> None:
        self.driver = driver
        self.contract_folder = contract_folder
        self.contract_id = contract_id
        self.action = ContractActions(self.driver)
        self.base_relativepath = "IMPULSIONAMENTOS"
        self.dir = Directory()
        self.excel = None
        self.folder_SO = ""
        self.worksheet_name = ""
        self.json_name = ""
        self.json = None

        self.init_enviroment()
        self.init_worksheet()
        self.init_json()

    """
        01. Criar a pasta de acordo com o contrato de impulsionamento
    """

    def init_enviroment(self, ):
        print("==================================================================")
        print(">> init_enviroment")
        # ----------------------------------------------------
        # Deixar o nome da pasta padrão para SO não bugar
        self.folder_SO = format_folder_windows(self.contract_folder)
        self.worksheet_name = f"{self.folder_SO}.xlsx"
        self.json_name = f"{self.folder_SO}.json"
        print(f"self.folder_SO: {self.folder_SO}")
        print(f"self.worksheet_name: {self.worksheet_name}")
        print(f"self.json_name: {self.json_name}")

        # ----------------------------------------------------
        # Caminhos relativos das pastas e arquivos
        self.assets_relativepath = Directory.separator(f"{self.base_relativepath}/assets")
        self.assinaturas_relativepath = Directory.separator(f"{self.base_relativepath}/assinaturas")
        self.contracts_relativepath = Directory.separator(f"{self.base_relativepath}/Contratos")
        self.contract_relativepath = Directory.separator(f"{self.contracts_relativepath}/{self.folder_SO}")
        self.download_email_relativepath = Directory.separator(f"{self.contract_relativepath}/Downloads")
        self.email_relativepath = Directory.separator(f"{self.contract_relativepath}/Emails")
        self.worksheet_relativepath = Directory.separator(f"{self.contract_relativepath}/{self.worksheet_name}")
        self.json_relativepath = Directory.separator(f"{self.contract_relativepath}/{self.json_name}")

        print(f"self.assets_relativepath: {self.assets_relativepath}")
        print(f"self.assinaturas_relativepath: {self.assinaturas_relativepath}")
        print(f"self.contracts_relativepath: {self.contracts_relativepath}")
        print(f"self.contract_relativepath: {self.contract_relativepath}")
        print(f"self.download_email_relativepath: {self.download_email_relativepath}")
        print(f"self.email_relativepath: {self.email_relativepath}")
        print(f"self.worksheet_relativepath: {self.worksheet_relativepath}")
        print(f"self.json_relativepath: {self.json_relativepath}")

        # ----------------------------------------------------
        # Criação das pastas do contrato
        self.dir.create_dir(self.contract_relativepath)
        self.dir.create_dir(self.download_email_relativepath)
        self.dir.create_dir(self.email_relativepath)

        # ----------------------------------------------------
        # Pegando o caminho completo das pastas e arquivos
        self.assets_path = self.dir.find_dir(Directory.separator(f"{self.base_relativepath}/assets"))
        self.assinaturas_path = self.dir.find_dir(Directory.separator(f"{self.base_relativepath}/assinaturas"))
        self.contracts_path = self.dir.find_dir(Directory.separator(f"{self.base_relativepath}/Contratos"))

        self.contract_path = self.dir.find_dir(Directory.separator(f"{self.contracts_relativepath}/{self.folder_SO}"))
        self.download_email_path = self.dir.find_dir(Directory.separator(f"{self.contract_relativepath}/Downloads"))
        self.email_path = self.dir.find_dir(Directory.separator(f"{self.contract_relativepath}/Emails"))
        self.worksheet_path = Directory.separator(f"{self.contract_path}/{self.worksheet_name}")
        self.json_path = Directory.separator(f"{self.contract_path}/{self.json_name}")

        
        print("-------------------------------------------------------")
        print(f"self.assets_path: {self.assets_path}")
        print(f"self.assinaturas_path: {self.assinaturas_path}")
        print(f"self.contracts_path: {self.contracts_path}")
        print(f"self.contract_path: {self.contract_path}")
        print(f"self.download_email_path: {self.download_email_path}")
        print(f"self.email_path: {self.email_path}")
        print(f"self.worksheet_path: {self.worksheet_path}")
        print(f"self.json_path: {self.json_path}")
        
        return self;

    def init_worksheet(self, ):
        print("==================================================================")
        print(">> init_worksheet")

        # ----------------------------------------------------
        # Verificar a existência da planilha
        worksheet_path = self.dir.find_file(r"\.xlsx$", self.contract_relativepath)
        print(f"worksheet_path: {worksheet_path}")
        if worksheet_path is None: 
    
            # -----------------------------------------------
            # Navegar até o GED
            # self.action.navigate_contract_ged(self.contract_id)

            # -----------------------------------------------
            # Buscar todos os itens listados no GED

            # -----------------------------------------------
            # Buscar o link do GED do Excel

            # -----------------------------------------------
            # Clicar no link para baixar

            # -----------------------------------------------
            # Pegar o caminho da planilha
            worksheet_path = self.dir.find_file(r"\.xlsx$", self.contract_relativepath)

        self.excel = StructExcel()
        self.excel.read_excel(worksheet_path)
        self.excel.set_compare_column(lambda col_target, col_ref: col_target == col_ref)

        return self;

    def init_json(self, ):
        print("==================================================================")
        print(">> init_json")

        # ----------------------------------------------------
        # Verificar a existência do json
        self.json = ContractJson(self.json_path)

        if not self.json.has_init():
            self.row_position = 1;
            self.json.init({
                    "tipo": "impulsionamento",
                    "status": "EM_ESPERA",
                    "idContrato": self.contract_id,
                    "empresa": None,
                    "slug_empresa": None,
                    "andamento": None,
                }, 
                [ "montar_dados", "baixar_email", "montar_email" ], 
                self.excel.get_total_rows()
            )
            def read_row(row: RowExcel):
                print("--------------------------------------------------------------------")
                values = {
                    "pastaContrato"     : row.regex(create_regex_latin_str('Pasta')).get(),
                    "numeroContrato"    : row.regex(create_regex_latin_str('Número do contrato')).get(),
                    "contratante"       : row.regex(create_regex_latin_str('Contratante principal / Nome/razão social')).get(),
                    "contratado"        : row.regex(create_regex_latin_str('Contratado principal / Nome/razão social')).get(),
                    "inicioFornecimento": None,
                    "fimFornecimento"   : None,
                    "submercado"        : row.regex(create_regex_latin_str('Submercado')).get(),
                    "situacao"          : row.regex(create_regex_latin_str('Situação')).get(),
                    "tipoEnergia"       : row.regex(create_regex_latin_str('Tipo de Energia')).get(),
                    "volumeMWm"         : row.regex(create_regex_latin_str('Volume MWm')).get(),
                    "volumeMWh"         : row.regex(create_regex_latin_str('Volume MWh')).get(),

                    "pendencia"         : None,
                    "assunto"           : None,
                    "arquivo"           : None,
                    "url"               : None,
                    "prefix"            : None,
                    "idContrato"        : None,
                    "idGed"             : None,
                    "urlContrato"       : None,
                    "grupo"             : None,
                    "download_path"     : None,
                    "email_path"        : None,
                }

                self.json.set_row(self.row_position).set_data(**values)
                self.row_position += 1

            self.excel.foreach_row(read_row)

        return self;

    def execute(self, ):
        from Library_v1.LegalOne.Steps.EmailBoost.MountData import MountData

        # -----------------------------------------------------------
        # Executar o 'montar_dados'
        MountData(self.driver, self.json)

        # -----------------------------------------------------------
        # Executar o 'baixar_email'

        # -----------------------------------------------------------
        # Executar o 'montar_email'

        return self;


