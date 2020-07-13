from time import sleep
from abc import ABC, abstractmethod
import shelve
from selenium.webdriver import Firefox
from .funcs import os, get_from_txt, get_imgs_name, remove_imgs_list



class FlashCard(object):
    """
        Classe que representa um objeto Flash Card, que são cartões utilizados em revisões espaçadas e que possuem o conteúdo estudado na parte da frente e sua "resposta na parte de trás."""
        
    def __init__(self, front, back):
        self.front = front
        self.back = back



class MyCard(FlashCard):
    
    _DEFAULT_BACK = '*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*'    

    def __init__(self, front, source):
        super().__init__(front, back=self._DEFAULT_BACK)
        self.source = source
        self.inserted = False



class AbstraticSource(ABC):    

    @abstractmethod
    def return_source(self):
        ...

    @abstractmethod
    def update_source(self):
        ...



class AbstraticCardWriter(ABC):    
    
    @abstractmethod
    def get_phrases(self):
        ...

    @abstractmethod
    def write(self):
        ...



class TextCardWriter(AbstraticCardWriter):
    
    def get_phrases(self, source):
        phrases = get_from_txt(source)
        return phrases


    def write(self, phrase, source):
        return MyCard(phrase, source)


class ImageCardWriter(AbstraticCardWriter):

    def get_phrases(self, source):
        return print('obtendo frases...')


    def write(self, phrase, source):
        return print('escrevendo card...')



class WriterAdmin(TextCardWriter, ImageCardWriter):
    #TODO: realizar uma lógica para decidir de qual super classe irá herdar os métodos de acordo com o card_type

    def __init__(self, card_type, source):
        self.card_type = card_type
        self.source = source
        if card_type == 'text':            
            TextCardWriter.write(self)
            TextCardWriter.get_phrases(self)
        elif card_type == 'image':
            ImageCardWriter.write(self)
            ImageCardWriter.get_phrases(self)
        else:
            raise NameError('card_type inválido! Deve ser "text" ou "image"')

'''class WriterAdmin:

    def __new__(cls, card_type, source):
        if card_type == 'text':            
            return TextCardWriter()
        else:
            raise NameError('card_type inválido! Deve ser "text" ou "image"')
'''

class TextSourceAdmin(AbstraticSource):

    def __init__(self, source):
        self.source = source
        
    
    def return_source(self):
        """
            Retorna o caminho do arquivo de texto"""
        return self.source


    def update_source(self):
        ...



class SourceAdmin(TextSourceAdmin):
    """
        Deve ter um card_type e um source

        - Retorna uma fonte de extração
        - Atualiza a fonte de extração
    """
    
    def __init__(self, card_type, source):
        if card_type == 'text':
            TextSourceAdmin.__init__(source)

'''class SourceAdmin:
    """
        Deve ter um card_type e um source

        - Retorna uma fonte de extração
        - Atualiza a fonte de extração
    """
    
    def __new__(cls, card_type, source):
        if card_type == 'text':
            return TextSourceAdmin(source)
'''


class DataBaseAdmin(AbstraticSource):
    ...



class ContextManager(WriterAdmin, SourceAdmin):

    #TODO: verificar se vai iniciar o determinado tip ode writer ao inciar com o card_type passado

    def __init__(self, card_type, source):
        self.card_type = card_type
        self.source = source
        self.cards = []
    
        
    def create_card(self):        
        card_src = self.return_source()
        src = self.source
        for phrase in self.get_phrases(card_src):        
        #for phrase in self.source:
            card = self.write(phrase, src)
            self.cards.append(card)


'''class ContextManager:

    def __init__(self, card_type, source):        
        self.card_type = card_type
        self.source = source
        self.cards = []
        self.writer = WriterAdmin(card_type, source)
        self.sourceAdmin = SourceAdmin(card_type, source)


    def create_cards(self):
        card_src = self.sourceAdmin.return_source()
        for phrase in self.writer.get_phrases(card_src):
            card = self.writer.write(phrase, card_src)
            #dBAdmin.algumacoisa(card)
            self.cards.append(card)
'''



class AutoCards:
    """
        Classe responsável por gerar flash cards em massa a partir de algum meio de obtenção de conteúdos em texto. """
    def __init__(self):
        self.cards = []
    
    def gen_cards_txt(self, file='frases.txt'):
        """
            Gera cartões FlashCard a partir de frases em inglês obtida através de um arquivo .txt que guarda estas frases. Esse método utiliza uma outra função dedicada para o tratamento das frases disponíveis no arquivo de extensão .txt.

            Keyword Arguments:
                file {str} -- string corerspondente ao nome do arquivo .txt (default: {'frases.txt'})

            Returns:
                list -- lista contendo os cartões gerados
                None -- nada, caso não haja frases para gerar cartões"""
        phrases = get_from_txt(file)
        if len(phrases) == 0:
            print('Sem frases para preencher cartões')
            return
        self.cards = [FlashCard(front) for front in phrases]
        return self.cards

    def gen_cards_img(self, source=r'C:\Users\Matheus\Documents\Projetos\LegendasLocal\Legendas'):
        file_names = []
        files = get_imgs_name(source)
        for file in files:            
            result = get_from_img(file)
            if result != None:                
                self.cards.append(FlashCard(result[0]))
                file_names.append(result[1])
        return file_names


class AnkiBot:
    """
        Classe responsável pelo bot que insere os AutoCards na plataforma Anki"""
#VAI DAR MERDA POR NÃO TER A POSSIBILIDADE DE PASSAR O NOME DO ARQUIVO OU O DIRETÓRIO
    def __init__(self):
        self.auto_cards = AutoCards()

    def start(self, gen_type, source='', login_path=''):                        
        """
            Método responsável pela interação com a plataforma Anki, desde o login até a inserção dos conteúdos que compõe o flash card.

            Arguments:
                gen_type {str} -- txt: Em texto;    img: Em imagem"""        
        if gen_type == 'txt':
            if source != '':
                self.auto_cards.gen_cards_txt(source)
            else:
                self.auto_cards.gen_cards_txt()                
        
        elif gen_type == 'img':
            if source != '':
                file_names = self.auto_cards.gen_cards_img(source)
            else:
                file_names = self.auto_cards.gen_cards_img()        
            
        else:
            print('parâmetro gen_type inválido.')
            return
        if len(self.auto_cards.cards) == 0:
            return
        
        #SETTINGS
        if login_path != '':
            em, pw = get_from_txt(login_path)
        else:
            em, pw = get_from_txt('login.txt')        
        url = 'https://ankiweb.net/account/login'                
        try:
            browser = Firefox()
            browser.implicitly_wait(30)
            browser.get(url)            
        except Exception as err:
            browser.close()
            print('NÃO FOI POSSÍVEL CONECTAR\n', err)
            input('\n\nPressione a tecla enter.')
            print('\nFINALIZANDO...')
        else:
            
            #LOGIN
            browser.find_element_by_css_selector('input[id="email"]').send_keys(em)
            browser.find_element_by_css_selector('input[type="password"]').send_keys(pw)
            browser.find_element_by_css_selector('input[type="submit"]').click()
            sleep(1)

            #ADD 
            browser.find_elements_by_css_selector('a[class="nav-link"]')[1].click()
            sleep(1)

            #INPUT FLASHCARDS
            for card in self.auto_cards.cards:
                browser.find_element_by_id('f0').send_keys(card.front)

                browser.find_element_by_id('f1').send_keys(card.back)
            
                browser.find_element_by_css_selector('button[class$="primary"]').click()
                sleep(1)            
            remove_imgs_list(file_names)            
        finally:
            browser.quit()
            #os.system(r'taskkill /f /im geckodriver.exe >nul')    
