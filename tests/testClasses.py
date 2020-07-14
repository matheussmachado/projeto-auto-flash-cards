import sys
from myPaths import SOURCE_PATH, SAMPLE_FOLDER 
sys.path.insert(0, SOURCE_PATH)

import unittest
from src.classes import ContextManager, DataBaseAdmin, GeneralSourceAdmin, TextSourceAdmin, TextCardWriter

from src.funcs import os, get_from_txt


class TestTextSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')


    def test_upadate_source(self):
        ...


class TestGeneralSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.text_source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')
        self.textAdmin = GeneralSourceAdmin('text', self.text_source)
        self.textWriter = TextCardWriter()
        self.src_before = get_from_txt(self.text_source)
        
    
    def text_source_back(self, source, source_before):
        with open(source, 'w') as src:
            for phrse in source_before:
                src.write(f'{phrse}\n')


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

        self.text_source_back(self.text_source, self.src_before)
        
    
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

        self.text_source_back(self.text_source, self.src_before)
                        

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        self.source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchida.txt')
    
    def test_writer_1(self):
        manager = ContextManager('text', self.source)
        #manager.write()
        manager.create_card()
        cards_front = [card.front for card in manager.cards]
        self.assertEqual(cards_front, self.frases)



#TODO: TESTE do AnkiBot e suas interações com a web



if __name__== '__main__':
    unittest.main()
