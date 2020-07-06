from .funcs import os, get_from_txt, get_imgs_name, remove_imgs_list, verify_mnt, img_to_txt
from time import sleep
from selenium.webdriver import Firefox



class FlashCard:
    """
        Classe que representa um objeto Flash Card, que são cartões utilizados em revisões espaçadas e que possuem o conteúdo estudado na parte da frente e sua "resposta na parte de trás."""
    def __init__(self, front):
        """
            Inicialização de um objeto FlashCard que será preenchido com frases em inglês na parte da frente posteriormente.

            Arguments:
                front {str} -- parte da frente que será preenchida."""
        self.front = front
        self.back = '*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*'


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

    def gen_cards_img(self, source):
        file_names = []
        files = get_imgs_name(source)
        #check = True
        #ALGORITMO PARA VALIDAÇÃO DE EXTRAÇÃO E PERSISTÊNCIA DE FRASES EXTRAÍDAS
        """
            - Validação: uma variavel de validação irá obter o valor False
            - Persistência: registrar em uma estrutura de persistência, ou em um arquivo de texto o nomearquivo e a string extraída
            - Resguardo: No início do processo de geração de cards por imagem, verificar se há elementos já obtidos na estrutura de persistência
            - Coerência: sempre verificar se a quantidade arquivos na estrutura de persistência é o mesmo do número de arquivos no diretório das imagens. Portanto, nunca excluir as imagens até essa condição seja validada e sempre que for realizar o processo desta função, partir do len(arq_persistência) menos 1
            
        > gen_cards:

            -     
            """
        if len(files) == 0:
            print('Sem imagens para obter cartões.')
            return
            #check = False
        for file in files:
            try:
                result = img_to_txt(file)
            except Exception as err:
                print(err)
                check = False
                #escrever file_names em um arquivo txt
            else:                
                self.cards.append(FlashCard(result))
                file_names.append(file)
        return file_names


class AnkiBot:
    """
        Classe responsável pelo bot que insere os AutoCards na plataforma Anki"""

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
             #verificação do dir montado
             img_folder = get_from_txt('imgPath.txt')[0]             
             file_names = self.auto_cards.gen_cards_img(verify_mnt(img_folder))
            
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
            browser.close()
            remove_imgs_list(file_names)            
        finally:
            browser.quit()
            os.system('fusermount -u ~/gdrive')

