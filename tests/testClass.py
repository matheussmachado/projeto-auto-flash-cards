from unittest import TestCase, mock, main

from src.clss.autoCards import AutoCards
from src.clss.sourceAdmins import DataBaseAdmin, TextSourceAdmin, DictBasedCardWriter
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cards import MyCard

from src.funcs import os, get_from_txt, text_source_reset, db_cards_reset

SAMPLE_FOLDER = "amostras/"

class TestDictBasedCardWriter(TestCase):
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
    
    def test__return_written_cards_returns_equal_amount_src(self):                
        phrases = self.src_before
        for phrase in phrases:
            self.writer.update_contents(phrase, self.source)
        card_list = self.writer.return_written_cards()
        expected = len(card_list)
        self.assertEqual(expected, len(self.src_before))

    def test_return_written_cards_returns_MyCard_instances(self):        
        #VERIFICAR A PRECISÃO DESSE MÉTODO EM FUNÇÃO DO MÉTODO _update_contents
        phrases = self.src_before
        for phrase in phrases:
            self.writer.update_contents(phrase, self.source)
        card_list = self.writer.return_written_cards()
        for card in card_list:
            self.assertEqual(isinstance(card, MyCard), True)



class TestTextSourceAdmin(TestCase):
    def setUp(self):
        file = 'frasesTestePreenchidaWriter.txt'
        self.source = os.path.join(SAMPLE_FOLDER, file)
        self.src_before = get_from_txt(self.source)
        writer = DictBasedCardWriter()
        self.sourceAdmin = TextSourceAdmin(self.source, writer)

    def tearDown(self):
        text_source_reset(self.source, self.src_before)        
    
    def test__update_cards_clear_all_phrases_in_file(self):        
        self.sourceAdmin.return_sources()        
        self.sourceAdmin.update_sources()
        expected = get_from_txt(self.source)
        self.assertEqual(expected, [])        

    def test__return_sources_returns_equal_amounts_src(self):
        card_list = self.sourceAdmin.return_sources()
        expected = len(card_list)        
        self.assertEqual(expected, len(self.src_before))



class TestDataBaseAdmin(TestCase):
    #TODO: VERIFICAR TESTES CRIADOS A SEREM REPLICADOS
    def setUp(self):
        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []
        file = 'frasesTestePreenchidaWriter.txt'
        self.text_src = os.path.join(SAMPLE_FOLDER, file)
        self.text_src_before = get_from_txt(self.text_src)
        writer = DictBasedCardWriter()
        self.textAdmin = TextSourceAdmin(self.text_src, writer)
    
    def tearDown(self):
        db_cards_reset(
            self.db_source, self.db_key, 
            self.db_source_before)
        text_source_reset(
            self.text_src, 
            self.text_src_before)

    def test__storage_card_works_for_created_cards(self):        
        db = DataBaseAdmin(self.db_source, self.db_key)
        cardsList_1 = self.textAdmin.return_sources()
        db.update_sources(cardsList_1)
        cardsList_2 = db.return_sources()
        cards = [card.representation for card in cardsList_1]
        expected = [card.representation for card in cardsList_2]        
        self.assertEqual(expected, cards)

    def test__update_source_when_all_cards_was_inserted(self):
        db = DataBaseAdmin(self.db_source, self.db_key)
        card_list = self.textAdmin.return_sources()
        db.update_sources(card_list)
        for card in card_list:
            card.inserted = True
        db.update_sources(card_list)
        expected = db.return_sources()
        self.assertEqual(expected, [])        
    
    def test__update_source_when_last_card_was_not_inserted(self):
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



class TestSeleniumAnkiBot(TestCase):
    def setUp(self):
        file = 'frasesTestePreenchidaWriter.txt'
        self.text_src = os.path.join(SAMPLE_FOLDER, file)
        self.text_src_before = get_from_txt(self.text_src)
        writer = DictBasedCardWriter()
        self.sourceAdmin = TextSourceAdmin(self.text_src, writer)
        #self.deliverer = SeleniumAnkiBot()

    def tearDown(self):
        text_source_reset(self.text_src, self.text_src_before)
        
    def test__update_card_update_card_inserted_status(self):
        card = MyCard('_', '_')
        deliverer = SeleniumAnkiBot('_', '_')        
        deliverer._card_list.append(card)
        deliverer._update_card(card)
        expected = deliverer.card_list[0].inserted
        self.assertEqual(expected, True)    



class TestAutoCards(TestCase):
    def setUp(self):
        file = 'frasesTestePreenchidaWriter.txt'
        self.text_src = os.path.join(SAMPLE_FOLDER, file)
        self.text_src_before = get_from_txt(self.text_src)
        writer = DictBasedCardWriter()
        self.textAdmin = TextSourceAdmin(self.text_src, writer)

        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []
        self.db_admin = DataBaseAdmin(self.db_source, self.db_key)

    def tearDown(self):
        db_cards_reset(self.db_source, 
                        self.db_key, 
                        self.db_source_before)
                    
        text_source_reset(self.text_src, self.text_src_before)    

    def test__verify_cards_returns_empty_cards_list(self):        
        ac = AutoCards('_', '_', self.db_admin)
        ac._verify_cards()
        expected = ac.card_list
        self.assertEqual(expected, [])    

    def test__card_list_append_created_cards_from_db(self):     
        card_list = self.textAdmin.return_sources()
        card_repr = [card.representation for card in card_list]
        db = self.db_admin
        db.update_sources(card_list)
        ac = AutoCards('_', '_', self.db_admin)
        ac._verify_cards()        
        expected = [card.representation for card in ac.card_list]
        self.assertEqual(expected, card_repr)
    
    @mock.patch('src.clss.sourceAdmins.DictBasedCardWriter.update_contents')
    def test__cards_list_append_written_cards(self, mocked):    
        ac = AutoCards('_', self.textAdmin, self.db_admin)
        ac.create_cards()
        expected = mocked.call_count
        self.assertEqual(expected, len(self.text_src_before))    

    @mock.patch('src.clss.cardDeliverers.SeleniumAnkiBot.deliver')
    def test__deliver_method_is_called_in_run_task_method(self, mocked):
        file = 'login.txt'
        login_path = os.path.join(SAMPLE_FOLDER, file)
        deliver = SeleniumAnkiBot('_', '_')        
        ac = AutoCards(deliver, self.textAdmin, self.db_admin)
        ac.run_task()
        mocked.assert_called_once_with(ac._card_list)        


if __name__ == "__main__":
    main()