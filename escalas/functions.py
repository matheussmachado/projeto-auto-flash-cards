from time import sleep
from googletrans import Translator
import os

def translate_phrases(phrases_list):
    """Traduzir frases dispostas em uma lista

        Arguments:
            frases {lista} -- lista que contendo as frases que serão traduzidas. A lista do argumento desta função deverá tratar string de modo que uma string vazia não seja aceita na sua coleção. Por via das dúvidas, a própria função fará a verificação a fim de não rodar a tradução caso não haja o que traduzir.

        Returns:
            lista -- lista contendo as frases traduzidas
            None  -- None, caso o arg. passado não for uma lista ou for lista vazia.
    """
    #if type(frases) == list and len(frases) > 0:
    if type(phrases_list) == list:
        phrases_filter = [
            phrase.strip() for phrase in phrases_list if phrase.strip() != ''
            ]
        if len(phrases_filter) == 0:
            print('Não há o que traduzir. Por favor, insira uma palavra ou frase válida em inglês.')
            return None
        trans = Translator(
            service_urls=['translate.google.com.br'], timeout=200
            )
        translations = []
        for frase in phrases_filter:
            sleep(0.3)
            translations.append(trans.translate(frase, src='en', dest='pt').text)
        return translations
    else:
        print(f'"{phrases_list}" não é uma lista ou é uma uma lista vazia')
        return None

def get_from_file(file='frases.txt'):
    #TODO: TRATAR o possível erro abaixo e verificar se serve apenas passar o nome do arquivo
    while True:
        if os.path.isfile(file) and str(file).endswith('.txt'):
            #TESTAR COM OUTROS ARQUIVOS            
            with open(file, 'r', encoding='UTF8') as f:                
                phrases = [line.strip() for line in f.read().split('\n') if line.strip() != '']        
                return phrases  
        else:
            print(f'\n\n"{file}" não é um arquivo ou um path de arquivo válido.')
            file = input('\nInsira um arquivo existente no mesmo path da VENV ou insira um path de arquivo válido: ')


def send_to_file(phrases_list, trans_list):
        with open('traducoes.txt', 'w', encoding='UTF8') as file:            
            for phrases, translates in zip(phrases_list, trans_list):
                file.write(f'{phrases}\n{translates}\n\n')