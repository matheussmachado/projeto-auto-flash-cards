from .abstract_classes import AbstractCardWriter
from .cards import MyCard
from src.funcs import get_from_txt

class CardWriter(AbstractCardWriter):
    def __init__(self, source):
        self.source = source
        self.contents = []
        
    def get_phrases(self, source):
        #raise NotImplementedError
        ...
    
    def write(self, phrase, source):
        raise NotImplementedError
    
    def update_contents(self, phrase, source):
        self.contents.append(
            {'phrase': phrase, 
            'src_path': source}
        ) 


class ContentUpdaterMixIn:
    def __init__(self, source):
        self.source = source
        self.contents = []


    def update_contents(self, phrase, source):
        self.contents.append(
            {'phrase': phrase, 
            'path': source}
        ) 


class TextCardWriter(AbstractCardWriter, ContentUpdaterMixIn):
    def __init__(self, source):
        super().__init__(source)

    def get_phrases(self, source):
        phrases = get_from_txt(source)
        for phrase in phrases:
            self.update_contents(phrase, source)
        return self.contents.copy()
    
    def write(self, phrase, path):
        return MyCard(phrase, path)