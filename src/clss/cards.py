class FlashCard:
    """
        Classe que representa um objeto Flash Card, que são cartões utilizados em revisões espaçadas e que possuem o conteúdo estudado na parte da frente e sua "resposta" na parte de trás."""

    def __init__(self, front: str, back: str) -> None:
        self.front = front
        self.back = back


class MyCard(FlashCard):
    """
        Classe que herda de flash cards, e os implementam contexto da solução."""

    _DEFAULT_BACK = "*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*"

    def __init__(self, front: str, source: str, back: str=_DEFAULT_BACK) -> None:        
        super().__init__(front, back)
        self.source = source
        self.inserted = False

    @property
    def representation(self) -> str:
        return str(
            {
                "front": self.front,
                "back": self.back,
                "source": self.source,
                "inserted": self.inserted,
            }
        )
