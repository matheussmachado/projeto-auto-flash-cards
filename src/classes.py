from .funcs import get_from_file


class FlashCard:

    def __init__(self, front):
        """
            Inicialização de um objeto FlashCard que será preenchido com frases em inglês na parte da frente posteriormente.

            Arguments:
                front {str} -- parte da frente que será preenchida."""
        self.front = front
        self.back = '*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*'

#Vai conter uma coleção de objetos FlashCard
class AutoCards:
    
    def __init__(self):
        self.cards = []
    
    def get_cards(self, file='frases.txt'):
        """
            Gera cartões FlashCard a partir de frases em inglês obtida através de um arquivo .txt que guarda estas frases. Esse método utiliza uma outra função dedicada para o tratamento das frases.

            Keyword Arguments:
                file {str} -- string corerspondente ao nome do arquivo .txt (default: {'frases.txt'})

            Returns:
                list -- lista contendo os cartões gerados
                None -- nada, caso não haja frases para gerar cartões"""
        phrases = get_from_file(file)
        if len(phrases) == 0:
            print('Sem frases para preencher cartões')
            return
        self.cards = [FlashCard(front) for front in phrases]
        return self.cards
