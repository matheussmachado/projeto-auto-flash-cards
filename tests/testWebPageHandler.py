import re
import os
from unittest import TestCase, mock, main

from src.clss.assistants import AnkiEditPageHandler

from . import PG_SOURCE, SAMPLE_FOLDER


class TestAnkiEditPageHandler(TestCase):
    file = os.path.join(SAMPLE_FOLDER, PG_SOURCE)
    with open(file, 'r') as f:
        CONTENT = f.read()

    def setUp(self):        
        self.handler = AnkiEditPageHandler(re)
        self.handler.page_source = self.CONTENT
        self.expected_names = ['Default', 'my deck', 'deck teste testando', 'teste TESTE', 'dEcK 4.2']
        self.longest_name = len(self.expected_names[2])

    def test__key_value_filter_method(self):
        handler = AnkiEditPageHandler('_')
        filth_name = '"name": "Default"'
        expected = handler._key_value_filter(filth_name, ':')
        self.assertEqual(expected, 'Default')
    
    def test__return_deck_names_method_returns_names(self):
        expected = self.handler._return_deck_names()
        self.assertEqual(expected, self.expected_names)
    
    def test__return_resources_names_and_backsce_flag(self):
        expected = {"deck_names": self.expected_names,
            "backspace_times": self.longest_name}
        self.assertEqual(expected, self.handler.return_resources())


if __name__ == "__main__":
    main()