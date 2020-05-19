from .funcs import get_from_file


class AutoCard:

    def __init__(self, front):
        self.front = front
        self.back = '*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*'

#Vai conter uma coleção de objetos AutoCard
class AutoDeck:
    
    def __init__(self):
        self.cards = []
    
    def get_cards(self, file='frases.txt'):
        phrases = get_from_file(file)
        if len(phrases) == 0:
            print('Sem frases para preencher cartões')
            return
        self.cards = [AutoCard(front) for front in phrases]
        return self.cards


    

#deck = [AutoCard(front) for front in get_from_file()]    
#print(deck)