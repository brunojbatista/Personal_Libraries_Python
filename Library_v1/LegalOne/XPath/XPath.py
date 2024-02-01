from Library_v1.LegalOne.env import get_env

class XPath():
    def __init__(self) -> None:
        self.env = get_env("env");
        self.screen_name = None
        self.screen_names = []
        self.xpaths = {}
        self.init()
    
    def init(self, ):
        if self.env == 'prod':
            self.xpaths = {
                "login": {
                    "usuario":      "//input[@id='Username']",
                    "senha":        "//input[@id='Password']",
                    "entrar":       "//button[@id='SignIn']",
                },
                "search_contract": {
                    "filtro_simples": "//div[contains(@class, 'filter-options')]//small[contains(@onclick, 'openSimple')]",
                    "filtro_carregamento":  "//div[contains(@class, 'loading-box') and contains(@class, 'search-box-loading')]",
                    "lookup_situacao_simples": "//div[@id='lookup_situacao_simples']",
                    "filtro_avancado": "//div[contains(@class, 'filter-options')]//small[contains(@onclick, 'openAdvanced')]",
                    "botao_pesquisar": "//input[@value='Pesquisar']",
                    "tabela_resultados":  "//div[@class='search-list']//div[contains(@class, 'webgrid-wrapper')]//table/tbody/tr"
                },
                "contract": {
                    "tabela_resultados": "//div[contains(@class, 'webgrid-wrapper')]//table/tbody/tr",
                    "loading": "//div[@id='tab-container' and contains(@class, 'widget-loading')]",
                    "tabs_link": "//ul[contains(@class, 'tab-navigation')]/li/a",

                    "situacao_field": "//div[@id='LookupSituacao']",
                    "save_close_button": "//button[text()='Salvar e fechar']",
                    "save_new_button": "//button[text()='Salvar e novo']",
                    "cancel_button": "//div[contains(@class, 'footer-buttons')]/a[contains(text(), 'Cancelar')]",

                    "new_progress": "//div[@id='popovermenus']//a[text()='Novo andamento']",
                }
            }

    def screen(self, screen_name: str):
        if screen_name not in self.xpaths: raise ValueError(f"Não há a tela '{screen_name}'")
        self.screen_name = screen_name
        return self;

    def get(self, xpath_name: str):
        if self.screen_name is None: raise ValueError(f"Não foi definido a tela")
        screen_xpaths = self.xpaths[self.screen_name]
        if xpath_name not in screen_xpaths: raise ValueError(f"Não há o XPath '{xpath_name}' na tela '{self.screen_name}'")
        return screen_xpaths[xpath_name]
