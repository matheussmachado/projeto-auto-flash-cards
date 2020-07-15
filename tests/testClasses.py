import sys
from myPaths import SOURCE_PATH, SAMPLE_FOLDER 
sys.path.insert(0, SOURCE_PATH)

import unittest
from src.classes import ContextManager, DataBaseAdmin, GeneralSourceAdmin, TextSourceAdmin, TextCardWriter

from src.funcs import os, get_from_txt, text_source_back, db_cards_back


class TestTextSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.textSourceAdmin = TextSourceAdmin(self.source)


    def test_update_sources(self):
        source_before = get_from_txt(self.source)
        phrase_selected = [ source_before[-1] ]
        self.textSourceAdmin.update_sources(phrase_selected)
        source_after = get_from_txt(self.source)
        
        self.assertEqual(source_after, phrase_selected)
        text_source_back(self.source, source_before)
        


class TestGeneralSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.textAdmin = GeneralSourceAdmin('text', self.text_source)
        self.textWriter = TextCardWriter()
        self.src_before = get_from_txt(self.text_source)                


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
        
        for phrase in self.src_before:
            cards.append(self.textWriter.write(phrase, self.text_source))
        
        #SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for card in cards:
            card.inserted = True
        
        self.textAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, [])

        text_source_back(self.text_source, self.src_before)
        
    
    #SIMULANDO A ATUALIZAÇÃO APÓS A ULTIMA INSERÇÃO TER FALHADO: valido mesmo se não for o último
    def test_upadate_sources_text_2(self):
        cards = []        
        for phrase in self.src_before:
            cards.append(self.textWriter.write(phrase, self.text_source))
        
        #SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for i in range(len(cards) - 1):
            cards[i].inserted = True
        
        self.textAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, ["Let's reconvene when you know more."])

        text_source_back(self.text_source, self.src_before)
                        

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchida.txt')
        self.db_cards = os.path.join(SAMPLE_FOLDER, 'db_cards_test')
        self.db_key = 'test_key'
        self.source_before = []
        
        self.text_manager = ContextManager(
            'text', self.text_source, self.db_cards, self.db_key
        )

    def test_text_writer_1(self):
        #TODO: ACRESCENTAR OS ARGUMENTOS DO ContextManager
        self.text_manager.create_card()
        cards_front = [card.front for card in self.text_manager.cards_list]
        self.assertEqual(cards_front, self.frases)
        db_cards_back(self.db_cards, self.db_key, self.source_before)
    
    #TODO: testar as fontes para escrita em texto
    def test_text_writer_2(self):
        self.text_manager.create_card()
        cards_source = [
            card.source for card in self.text_manager.cards_list
        ]
        
        for src in cards_source:
            self.assertEqual(src, self.text_source)
        db_cards_back(self.db_cards, self.db_key, self.source_before)

#TODO: TESTE do AnkiBot e suas interações com a web



if __name__== '__main__':
    unittest.main()
