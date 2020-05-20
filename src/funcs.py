import os

def get_from_txt(file='frases.txt'):    
    """
        Função que obtém frases de um arquivo .txt. Essa obtenção se dá orientada ao caractere de quebra de linha \\n. A função também realiza tratamento de espaços em branco a cada frase obtida e, se houver no arquivo apenas espaços em branco, o retorno será uma lista vazia.

        Keyword Arguments:
            file {str} -- nome do arquivo que contém as frases. 
            (default: {'frases.txt'})

        Returns:
            list -- lista contendo as frases obtidas do arquivo."""
    while True:
        if os.path.isfile(file) and str(file).endswith('.txt'):            
            with open(file, 'r') as f:                
                phrases = [line.strip() for line in f.read().split('\n') if line.strip() != '']        
                return phrases  
        else:
            print(f'\n\n"{file}" não é um arquivo ou um path de arquivo válido.')
            file = input('\nInsira um arquivo existente no mesmo path da VENV ou insira um path de arquivo válido: ')


"""def anki_bot(autoCards):
    if type(autoCards) != AutoCards:
        return
        
    url = "https://ankiweb.net/account/login"
    browser = Firefox()
    browser.get(url)
    sleep(3)

    browser.find_element_by_css_selector('input[id="email"]').send_keys(autoCards.email)
    sleep(2)

    browser.find_element_by_css_selector('input[type="password"]').send_keys(input('senha: '))
    browser.find_element_by_css_selector('input[type="submit"]').click()
    sleep(4)
    #TODO: VALIDAR PELA URL A SEGUIR PARA VERIFICAR SE A SENHA FORNECIDA FOI VALIDA

    #clicar na ancora que adiciona os cards
    browser.find_elements_by_css_selector('a[class="nav-link"]')[1].click()

    sleep(4)

    for card in autoCards.cards:
        browser.find_element_by_id('f0').send_keys(card.front)
        sleep(1)
        browser.find_element_by_id('f1').send_keys(card.back)
        sleep(1)
        browser.find_element_by_css_selector('button[class$="primary"]').click()
        
        sleep(1)    """
