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
    def __init__(self, regex_agent: re):
        super().__init__()
        self.regex_agent = regex_agent
    
    def return_resources(self):
        names = self.return_deck_names()
        return names

    def _key_value_filter(self, filth_key_value: str,
    split_target: str) -> str:
        first_strip = filth_key_value.strip()
        filth_split = first_strip.split(split_target)
        name = filth_split[1].replace('"', '').strip()
        return name    

    def _return_filtered_content(self, pattern, content):
        pattern_re = self.regex_agent.compile(pattern, re.I|re.DOTALL|re.M)
        matches = pattern_re.findall(content)
        return matches

    def return_deck_names(self) -> List[str]:
        if not self.page_source:
            return
        _EDITOR_DECK_SCOPE_PATTERN = r"editor\.decks =.*}};"
        _NAME_PATTERN = r'("name": "(\w|\s|[.-=])*").+?'
        _SCRIPT_PATTERN = r'(<script>.*</script>).+?'
        
        filth_script = self._return_filtered_content(
            _SCRIPT_PATTERN, self.page_source
        )[-1]                

        filtered_editor = self._return_filtered_content(
            _EDITOR_DECK_SCOPE_PATTERN, filth_script
        )[0]
                        
        filth_names = self._return_filtered_content(
            _NAME_PATTERN, filtered_editor
        )
        
        names = []        
        str_filth_names = [n[0] for n in filth_names]
        for name in str_filth_names:
            names.append(self._key_value_filter(name, ':'))
        return names
