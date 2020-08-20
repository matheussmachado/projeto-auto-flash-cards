"""
- o agente irá receber o page_source da pagina a partir do card deliverer
- BS irá filtrar as partes referentes ao script
- BS irá fornecer a parte do script para o regex
- regex irá realizar um primeiro filtro para obter os nomes dos decks
- regex irá fornecer as partes referentes a um outro filtro
- será obtida os nomes dos decks


- OBJETIVOS:
    - obter os nomes dos decks para validar o deck passado no card deliverer; 
    - obter o name do deck que foi renderizado na tela
"""
from typing import List
import re
from pprint import pprint
from bs4 import BeautifulSoup
from .abstractClasses import AbstractWebPageContentHandler

#WebDriver = TypeVar('WebDriver')


class AnkiEditPageHandler(AbstractWebPageContentHandler):
    

    def __init__(self, regex_agent: re, html_parser: BeautifulSoup):
        self.regex_agent = regex_agent
        #self.soup = soup(page_source, 'lxml')
        self.html_parser = html_parser
        self.page_source = None
        
    def get_content(self, content):
        self.page_source = content

    def _filter_content(self):
        parser = self.html_parser(self.page_source, 'lxml')
        scripts = parser.findAll('script')
        script = scripts[-1]
        return script.string

    def _key_value_filter(self, filth_key_value: str,
    split_target: str) -> str:
        first_strip = filth_key_value.strip()
        filth_split = first_strip.split(split_target)
        name = filth_split[1].replace('"', '').strip()
        return name

    def return_deck_names(self) -> List[str]:
        editor_deck_scope_pattern = r"editor\.decks =.*}};"
        editor_deck_re = self.regex_agent.compile(editor_deck_scope_pattern)
        #OBTIDO A STRING DO script
        filth_script = self._filter_content()
        #OBTIDO O PADRÃO editor.decks = .* NO script
        filtered_editor = editor_deck_re.findall(filth_script)[0]
        print(filtered_editor)
        #filth_any = self.regex_agent.compile(filtered_editor)
        _NAME_PATTERN = r'("name": "\w+",+?)+?'
        #name_re = self.regex_agent.compile(_NAME_PATTERN)        
        
        #filth_names = name_re.search(filtered_editor)
        #filth_names = name_re.findall(filtered_editor)
        filth_names = re.findall(_NAME_PATTERN, filtered_editor)
        names = []
        #pprint(filth_names.group())
        print(filth_names)
        for name in filth_names:
            names.append(self._key_value_filter(name, ':'))
        return names


