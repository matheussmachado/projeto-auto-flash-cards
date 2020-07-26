import unittest

from src.clss.autoCards import AutoCards
from src.clss.sourceAdmins import DataBaseAdmin, TextSourceAdmin, DictBasedCardWriter
from src.clss.cards import MyCard

from src.funcs import os, get_from_txt, text_source_reset, db_cards_reset

SAMPLE_FOLDER = "amostras/"

class TestDictBasedCardWriter(unittest.TestCase):
    def setUp(self):
        file = 'frasesTestePreenchidaWriter.txt'
        self.source = os.path.join(SAMPLE_FOLDER, file)
        self.src_before = get_from_txt(self.source)
        self.writer = DictBasedCardWriter()

    def tearDown(self):
        text_source_reset(self.source, self.src_before)

    def test_update_contents_works(self):
        phrases = self.src_before
        for phrase in phrases:
            self.writer.update_contents(
                phrase, self.source
            )
        expected = [
            {'phrase': phrase, 'path': self.source} for phrase in phrases
        ]
        
        self.assertEqual(expected, self.writer.contents)

    def test_return_written_cards_return_MyCard_instances(self):
        #VERIFICAR A PRECISÃO DESSE MÉTODO EM FUNÇÃO DO MÉTODO _update_contents
        phrases = self.src_before
        for phrase in phrases:
            self.writer.update_contents(phrase, self.source)
        card_list = self.writer.return_written_cards()
        for card in card_list:
            self.assertEqual(isinstance(card, MyCard), True)



class TestTextSourceAdmin(unittest.TestCase):
    def setUp(self):
        file = 'frasesTestePreenchidaWriter.txt'
        self.source = os.path.join(SAMPLE_FOLDER, file)
        self.src_before = get_from_txt(self.source)
        self.sourceAdmin = TextSourceAdmin(self.source)

    def tearDown(self):
        text_source_reset(self.source, self.src_before)
    
    def test_update_cards_clear_all_phrases_in_file(self):        
        card_list = self.sourceAdmin.return_sources()
        
        self.sourceAdmin.update_sources(card_list)
        expected = get_from_txt(self.source)
        self.assertEqual(expected, [])


class TestDataBaseAdmin(unittest.TestCase):
    def setUp(self):
        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []

        file = 'frasesTestePreenchidaWriter.txt'
        self.text_src = os.path.join(SAMPLE_FOLDER, file)
        self.text_src_before = get_from_txt(self.text_src)
        self.textAdmin = TextSourceAdmin(self.text_src)
    
    def tearDown(self):
        db_cards_reset(
            self.db_source, self.db_key, 
            self.db_source_before)
        text_source_reset(
            self.text_src, 
            self.text_src_before)

    def test_storage_card_works_for_created_cards(self):
        db = DataBaseAdmin(self.db_source, self.db_key)
        cardsList_1 = db.return_sources()
        db.update_sources(cardsList_1)
        cardsList_2 = db.return_sources()
        cards = [card.representation for card in cardsList_1]
        expected = [card.representation for card in cardsList_2]
        
        self.assertEqual(expected, cards)

    def test_update_source_insert_all_cards(self):        
        db = DataBaseAdmin(self.db_source, self.db_key)
        card_list = self.textAdmin.return_sources()
        db.update_sources(card_list)
        for card in card_list:
            card.inserted = True
        db.update_sources(card_list)
        expected = db.return_sources()

        self.assertEqual(expected, [])        
    
    def test_update_source_when_last_card_not_inserted(self):
        db = DataBaseAdmin(self.db_source, self.db_key)
        card_list = self.textAdmin.return_sources()
        db.update_sources(card_list)
        for i in range(len(card_list) - 1):
            card_list[i].inserted = True
        last_card = card_list[-1].representation

        db.update_sources(card_list)
        db_return = db.return_sources()
        expected = db_return[0].representation

        self.assertEqual(expected, last_card)
        


class TestAutoCards(unittest.TestCase):
    def setUp(self):
        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []
        self.db_admin = DataBaseAdmin(self.db_source, self.db_key)

    def tearDown(self):
        db_cards_reset(self.db_source, 
                        self.db_key, 
                        self.db_source_before)

    #TODO: TESTAR SE AO CRIAR CARDS, VAI INSERIR NO cards_list
    #TODO: TESTAR SE O update_card IRÁ ATUALIZAR O CARD ESPERADO
    #TODO:
    #TODO:

    def test_verify_cards_returns_empty_cards_list(self):
        ac = AutoCards('_', '_', self.db_admin)
        ac._verify_cards()
        expected = ac.cards_list
        self.assertEqual(expected, [])
    
    def test_cards_list_append_created_cards_from_db(self):
        ...
    
    def test_cards_list_append_written_cards(self):
        #SE ao ser chamado a funçao de obter os cards, será inserido a mesma quantidade de cards que é solicitado(sem se preocupar com o conteúdo agora)
        #ac = AutoCards('', '', '_')
        ...
    
    

    