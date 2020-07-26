from src.clss.cards import MyCard

class AutoCards:
    def __init__(self, writer, source_manager, data_base_admin):
        self.writer = writer
        self.source_manager = source_manager
        self.data_base_admin = data_base_admin
        self._cards_list = []    
    #TODO: update_sources será 
    @property
    def cards_list(self) -> list:
        return self._cards_list.copy()
    
    def _verify_cards(self) -> None:
        """
            Método que realiza a verificação de possiveis cards estocados na estrutura de persistência."""
        cards = self.data_base_admin.return_sources()
        self._cards_list += [card for card in cards]
    def write(self, phrase, path):
            return MyCard(phrase, path)        

    def create_cards(self):
        ...
        """
            - obtem os cards existentes no db            
            - obter os conteúdos:
                - para cada path e frase, deve-se criar um card
            - getphrase deve retornar a frase junto com o source?: {phrase: frase, source: fonte}
                
                - delegar getphrase para um AbstractSource: não vai rolar
        """

        
        #TODO: GET_PHRASES E O RESTANTE SERÁ COMPETENCIA DE CADA SOURCEADMIN
        self._verify_cards()
        #sources = self.source_manager.get_phrases()
        sources = self.writer.get_phrases()

        
        for source in sources:
            card = self.writer.write(source['phrase'], source['path'])
            self._cards_list.append(card)
        self.data_base_admin.update_sources(self, self.cards_list)