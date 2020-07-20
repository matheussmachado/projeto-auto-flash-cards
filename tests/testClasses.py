import unittest
from src.classes import (
    ContextManager,
    DataBaseAdmin,
    GeneralSourceAdmin,
    MyCard,
    TextSourceAdmin,
    TextCardWriter,
)
from src.funcs import os, get_from_txt, text_source_back, db_cards_back

SAMPLE_FOLDER = "amostras/"


class TestTextSourceAdmin(unittest.TestCase):
    def setUp(self):
        self.text_source = os.path.join(
            SAMPLE_FOLDER, "frasesTestePreenchidaWriter.txt"
        )
        self.textSourceAdmin = TextSourceAdmin(self.text_source)
        self.text_source_before = get_from_txt(self.text_source)

    def tearDown(self):
        text_source_back(self.text_source, self.text_source_before)

    def test_text_source_admin_update(self):
        phrase_selected = [self.text_source_before[-1]]
        self.textSourceAdmin.update_sources(phrase_selected)
        source_after = get_from_txt(self.text_source)

        self.assertEqual(source_after, phrase_selected)


class TestGeneralSourceAdmin(unittest.TestCase):
    def setUp(self):
        self.text_source = os.path.join(
            SAMPLE_FOLDER, "frasesTestePreenchidaWriter.txt"
        )
        self.genSrcAdmin = GeneralSourceAdmin("text", self.text_source)
        self.textWriter = TextCardWriter()
        self.text_source_before = get_from_txt(self.text_source)

    def tearDown(self):
        text_source_back(self.text_source, self.text_source_before)

    # SIMULANDO A ATUALIZAÇÃO APÓS TODOS OS CARDS INSERIDOS COM SUCESSO
    def test_gen_src_adm_updt_src_after_successful_inserted_cards(self):

        """SIMULANDO:
            - Obter as frases de forma distinta, copiar elas
            - Obter os cards de maneira distinta, por enquanto
            - alterar o estado dos cards
            - inserir os cards no método
            - comparar o arquivo após o método
            - reescrever o arquivo com as frases para poder refazer os testes"""

        cards = []
        for phrase in self.text_source:
            cards.append(self.textWriter._write(phrase, self.text_source))

        # SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for card in cards:
            card.inserted = True

        self.genSrcAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, [])

    # SIMULANDO A ATUALIZAÇÃO APÓS A ULTIMA INSERÇÃO TER FALHADO: valido mesmo se não for o último
    def test_gen_src_adm_updt_src_after_ultimate_insert_card_failed(self):
        cards = []
        for phrase in self.text_source_before:
            cards.append(self.textWriter._write(phrase, self.text_source))

        # SIMULANDO A ATUALIZAÇÃO DO STATUS DE CARDS DO ContextManager.cards EM TEMPO DE EXECUÇÃO
        for i in range(len(cards) - 1):
            cards[i].inserted = True

        self.genSrcAdmin.update_sources(cards)
        src_after = get_from_txt(self.text_source)
        self.assertEqual(src_after, ["Let's reconvene when you know more."])


class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more.",
        ]
        self.text_source = os.path.join(
            SAMPLE_FOLDER, "frasesTestePreenchidaWriter.txt"
        )
        self.empty_text_source = os.path.join(SAMPLE_FOLDER, "frasesTesteVazia.txt")
        self.text_source_before = get_from_txt(self.text_source)

        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []

        self.text_manager = ContextManager(
            "text", self.text_source, self.db_source, self.db_key
        )
        self.empty_text_manager = ContextManager(
            "text", self.empty_text_source, self.db_source, self.db_key
        )

    def tearDown(self):
        db_cards_back(self.db_source, self.db_key, self.db_source_before)
        text_source_back(self.text_source, self.text_source_before)

    def test_context_manager_created_cards(self):
        self.text_manager.create_card()
        cards_front = [card.front for card in self.text_manager.cards_list]
        self.assertEqual(cards_front, self.frases)

    # TESTA AS FONTES DE ONDE FORAM CRIADO OS CARDS POR TEXTO
    def test_text_source_1(self):
        self.text_manager.create_card()
        cards_source = [card.source for card in self.text_manager.cards_list]

        for src in cards_source:
            self.assertEqual(src, self.text_source)

    # TESTAR SE AO CRIAR OS CARDS E ENVIAR PARA O DATABASE, OS CARDS ESTARÃO LÁ
    def test_dump_cards_after_created(self):
        self.text_manager.create_card()
        created_cards = self.text_manager.cards_list
        storage_cards = DataBaseAdmin(self.db_source, self.db_key)._return_sources()
        # PELO JEITO, A REFERÊNCIA DAS DUAS INSTANCIAS, MESMO QUE TENHAM AS MESMAS CARACTERÍSTICAS, SÃO DIFERENTES NO DataBaseAdmin.database E NO ContextManager.cards_list
        cards_list = [card.representation for card in created_cards]
        cards_db = [card.representation for card in storage_cards]

        self.assertEqual(cards_list, cards_db)

    # TESTAR SE ContextManager REALIZA A BUSCA E ACUMULA POSSÍVEIS CARDS DO SEU DATABASE
    def test_verify_and_append_cards_created_before(self):
        cards = self.text_source_before
        myCards = [MyCard(card, self.empty_text_source) for card in cards]
        db = DataBaseAdmin(self.db_source, self.db_key)
        db.update_sources(myCards)
        cardsList_1 = myCards[:]
        self.empty_text_manager.create_card()

        cardsList_2 = self.empty_text_manager.cards_list[:]
        cards_before = [card.representation for card in cardsList_1]
        cards_after = [card.representation for card in cardsList_2]

        self.assertEqual(cards_before, cards_after)

    def test_verify_and_append_no_cards_created(self):
        self.empty_text_manager.create_card()

        self.assertEqual(self.text_manager.cards_list, [])

    def test_verify_db_cards_after_inserted_cards(self):
        self.text_manager.create_card()
        for card in self.text_manager.cards_list:
            self.text_manager.update_card(card)
        self.text_manager.update_sources()

        expected = DataBaseAdmin(self.db_source, self.db_key)._return_sources()
        self.assertEqual(expected, [])

    def test_verify_db_cards_after_fail_ultimate_insert_card(self):
        self.text_manager.create_card()
        cards = self.text_manager.cards_list[:]
        for x in range(len(cards) - 1):
            self.text_manager.update_card(cards[x])
        self.text_manager.update_sources()

        db_test = DataBaseAdmin(self.db_source, self.db_key)._return_sources()[:]
        card_repr = cards[-1].representation
        expected = db_test[0].representation

        self.assertEqual(expected, card_repr)

    def test_update_cards_inserted_status(self):
        self.text_manager.create_card()
        cards_list_before = self.text_manager.cards_list[:]
        for card in cards_list_before:
            self.text_manager.update_card(card)
        cards_list_after = self.text_manager.cards_list[:]
        inserted_status = [card.inserted or card in cards_list_after]
        expected = [True for true in range(len(inserted_status))]

        self.assertEqual(inserted_status, expected)


class TestAutoCards(unittest.TestCase):
    def setUp(self):
        self.text_source = os.path.join(
            SAMPLE_FOLDER, "frasesTestePreenchidaWriter.txt"
        )
        self.text_source_before = get_from_txt(self.text_source)

        self.db_source = os.path.join(SAMPLE_FOLDER, "db_cards_test")
        self.db_key = "test_key"
        self.db_source_before = []

        self.text_manager = ContextManager(
            "text", self.text_source, self.db_source, self.db_key
        )


# TODO: TESTE do AnkiBot e suas interações com a web


if __name__ == "__main__":
    unittest.main()
