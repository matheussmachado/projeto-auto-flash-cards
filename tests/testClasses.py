import sys
from myPaths import SOURCE_PATH, SAMPLE_FOLDER 
sys.path.insert(0, SOURCE_PATH)

import unittest
from src.classes import ContextManager, DataBaseAdmin, GeneralSourceAdmin, TextSourceAdmin, TextCardWriter

from src.funcs import os, get_from_txt, text_source_back, db_cards_back


class TestTextSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.textSourceAdmin = TextSourceAdmin(self.text_source)
        self.text_source_before = get_from_txt(self.text_source)

    def tearDown(self):
        text_source_back(self.text_source, self.text_source_before)


    def test_update_sources(self):
        phrase_selected = [ self.text_source_before[-1] ]
        self.textSourceAdmin.update_sources(phrase_selected)
        source_after = get_from_txt(self.text_source)
        
        self.assertEqual(source_after, phrase_selected)        
        


class TestGeneralSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.textAdmin = GeneralSourceAdmin('text', self.text_source)
        self.textWriter = TextCardWriter()
        self.text_source_before = get_from_txt(self.text_source)

    def tearDown(self):
        text_source_back(self.text_source,self.text_source_before)

    #SIMULANDO A ATUALIZAÇÃO APÓS TODOS OS CARDS INSERIDOS COM SUCESSO
    def test_upadate_sources_text_1(self):        
    
        """SIMULANDO:
            - Obter as frases de forma distinta, copiar elas
            - Obter os cards de maneira distinta, por enquanto
            - alterar o estado dos cards
            - inserir os cards no método
            - comparar o arquivo após o método
            - reescrever o arquivo com as frases para poder refazer os testes"""
        
        cards = []        
        for phrase in self.text_source:
            cards.append(self.textWriter.write(phrase, self.text_source))
        
        #SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for card in cards:
            card.inserted = True
        
        self.textAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, [])        
        
    
    #SIMULANDO A ATUALIZAÇÃO APÓS A ULTIMA INSERÇÃO TER FALHADO: valido mesmo se não for o último
    def test_update_sources_text_2(self):
        cards = []        
        for phrase in self.text_source_before:
            cards.append(self.textWriter.write(phrase, self.text_source))
        
        #SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for i in range(len(cards) - 1):
            cards[i].inserted = True
        
        self.textAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, ["Let's reconvene when you know more."])
        
                        

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.text_source_before = get_from_txt(self.text_source)

        self.db_source = os.path.join(SAMPLE_FOLDER, 'db_cards_test')
        self.db_key = 'test_key'
        self.db_source_before = []
        
        self.text_manager = ContextManager(
            'text', self.text_source, self.db_source, self.db_key
        )


    def tearDown(self):
        db_cards_back(self.db_source, self.db_key, self.db_source_before)
        text_source_back(self.text_source, self.text_source_before)


    def test_text_writer_1(self):
        self.text_manager.create_card()
        cards_front = [card.front for card in self.text_manager.cards_list]
        self.assertEqual(cards_front, self.frases)

    
    #TESTA AS FONTES DE ONDE FORAM CRIADO OS CARDS POR TEXTO
    def test_text_source_1(self):
        self.text_manager.create_card()
        cards_source = [
            card.source for card in self.text_manager.cards_list
        ]
        
        for src in cards_source:
            self.assertEqual(src, self.text_source)
        
        
    #TESTAR SE AO CRIAR OS CARDS E ENVIAR PARA O DATABASE, OS CARDS ESTARÃO LÁ
    def test_db_cards_1(self):
        self.text_manager.create_card()
        created_cards = self.text_manager.cards_list
        storage_cards = DataBaseAdmin(self.db_source, self.db_key).return_sources()
        #PELO JEITO, A REFERÊNCIA DAS DUAS INSTANCIAS, MESMO QUE TENHAM AS MESMAS CARACTERÍSTICAS, SÃO DIFERENTES NO DataBaseAdmin.database E NO ContextManager.cards_list
        front_cards = [card.front for card in created_cards]        
        front_db = [card.front for card in storage_cards]
        
        #self.assertEqual(created_cards, storage_cards)
        self.assertEqual(front_cards, front_db)        
     

    #TESTAR SE ContextManager REALIZA A BUSCA E ACUMULA POSSÍVEIS CARDS DO SEU DATABASE 
    def test_db_cards_2(self):
        self.text_manager.create_card()
        cardsList_1 = self.text_manager.cards_list[:]
        #RESETANDO O manager.cards_list
        self.text_manager.cards_list = []

        self.text_manager.verify_cards()
        cardsList_2 = self.text_manager.cards_list[:]
        '''cardsListTemp = self.text_manager.cards_list[:]
        cardsList_2 = []
        for card in cardsListTemp:
            if card not in cardsList_1:
                cardsList_2.append(card)'''

        front_1 = [card.front for card in cardsList_1]
        front_2 = [card.front for card in cardsList_2]

        self.assertEqual(front_1, front_2)
    

    def test_db_cards_3(self):        
        self.text_manager.verify_cards()

        self.assertEqual(self.text_manager.cards_list, [])
        
        


class TestAutoCards(unittest.TestCase):

    def setUp(self):
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.text_source_before = get_from_txt(self.text_source)

        self.db_source = os.path.join(SAMPLE_FOLDER, 'db_cards_test')
        self.db_key = 'test_key'
        self.db_source_before = []
        
        self.text_manager = ContextManager(
            'text', self.text_source, self.db_source, self.db_key
        )
    



#TODO: TESTE do AnkiBot e suas interações com a web



if __name__== '__main__':
    unittest.main()
