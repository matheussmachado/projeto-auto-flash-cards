import re
from typing import List, Tuple, Union, Dict

from .abstractClasses import AbstractWebPageContentHandler

#CRASHED HANDLER
class AnkiEditPageHandler(AbstractWebPageContentHandler):    
    def __init__(self, regex_agent: re):
        super().__init__()
        self.regex_agent = regex_agent
    
    def return_resources(self) -> Dict:
        deck_names = self._return_deck_names()
        longest_name = len(deck_names[0])
        for name in deck_names:
            if len(name) > longest_name:
                longest_name = len(name)
        resources = {
            "deck_names": deck_names,
            "backspace_times": longest_name
        }
        return resources

    def _key_value_filter(self, filth_key_value: str,
    split_target: str) -> str:
        first_strip = filth_key_value.strip()
        filth_split = first_strip.split(split_target)
        name = filth_split[1].replace('"', '').strip()
        return name    

    def _return_filtered_content(self, pattern: str, content: str) -> List[Union[str, Tuple[str]]]:
        pattern_re = self.regex_agent.compile(pattern, re.I|re.DOTALL|re.M)
        matches = pattern_re.findall(content)
        return matches

    def _return_deck_names(self) -> List[str]:
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
