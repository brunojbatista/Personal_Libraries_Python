XPATHS = {
    "login": {
        "usuario":      "//input[@id='Username']",
        "senha":        "//input[@id='Password']",
        "entrar":       "//button[@id='SignIn']",
    },
    "busca_avancada": {
        "filtro_avancado":      "//div[contains(@class, 'filter-options')]//small[contains(@onclick, 'openAdvanced')]",
        "filtro_carregamento":  "//div[contains(@class, 'loading-box') and contains(@class, 'search-box-loading')]",
        "input_numero_contrato": "//input[@id='NumeroContrato']",
        "lookup_pasta":         "//div[@id='lookupPasta']",
        "botao_pesquisar":      "//input[@value='Pesquisar']",
        "tabela_pesquisa":      "//div[@class='search-list']//div[contains(@class, 'webgrid-wrapper')]//table/tbody/tr",
    },
    "busca_simples": {
        "filtro_simples":       "//div[contains(@class, 'filter-options')]//small[contains(@onclick, 'openSimple')]",
        "filtro_carregamento":  "//div[contains(@class, 'loading-box') and contains(@class, 'search-box-loading')]",
        "lookup_situacao":      "//div[@id='lookup_situacao_simples']",
        "botao_pesquisar":      "//input[@value='Pesquisar']",
        "tabela_pesquisa":      "//div[@class='search-list']//div[contains(@class, 'webgrid-wrapper')]//table/tbody/tr",
    },
    "contrato": {
        "lista_tabela": "//table[contains(@class, 'webgrid')]/tbody/tr",
        "escritorio_responsavel": "//div[@id='LookupTreeEscritorio']",
        "modalidade": "//div[@id='LookupModalidadeContrato']",
        "pasta": "//input[@id='Pasta']",
        "numero_contrato": "//input[@id='NumeroContrato']",
        "situacao": "//div[@id='LookupSituacao']",
        "prioridade": "//select[@id='Prioridade']",
        "vendedor": "//div[starts-with(@id, 'Contratados') and contains(@id, 'LookupContato')]",
        "comprador": "//div[starts-with(@id, 'Contratante') and contains(@id, 'LookupContato')]",
        "responsavel": "//div[starts-with(@id, 'Responsaveis') and contains(@id, 'LookupUsuariosAtivos')]",
        "cliente_vendedor": "//label[text()='Cliente' and starts-with(@for, 'Contratados')]",
        "cliente_comprador": "//label[text()='Cliente' and starts-with(@for, 'Contratantes')]",
        "edit_link": "//a[contains(@href, '/contratos/contratoCliente/Details')]",
        "error_message": "//div[contains(@class, 'error-validation-message')]",
        "general_errors": "//div[contains(@class, 'validation-summary-errors')]/ul/li[not(contains(@style, 'display: none'))]",
    },
    "andamento": {
        "situacao": "//div[@id='tipo_andamento']",
        "responsavel": "//div[@id='quem_executou']",
        "descricao_andamento": "//textarea[@id='DescricaoText']",
    },
}

def get_xpath(screen, field):
    xpath_el = None;
    if screen not in XPATHS: raise ValueError("O xpath da tela não encontrada")
    screen_xpath = XPATHS[screen]
    if field not in screen_xpath: raise ValueError(f"O xpath do campo da tela '{screen}' não encontrada")
    xpath_el = screen_xpath[field]
    return xpath_el