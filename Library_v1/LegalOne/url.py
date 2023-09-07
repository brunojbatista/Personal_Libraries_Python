URLS = {
    "login": "https://regispontesadvogados.novajus.com.br",
    "main_base": "https://regispontesadvogados.novajus.com.br",
    "search": "https://regispontesadvogados.novajus.com.br/contratos/contratocliente/search",
    "new_contract": "https://regispontesadvogados.novajus.com.br/contratos/contratocliente/create",
}

def get_url(screen):
    url_text = None;
    if screen not in URLS: raise ValueError("A url não encontrada")
    url_text = URLS[screen]
    return url_text