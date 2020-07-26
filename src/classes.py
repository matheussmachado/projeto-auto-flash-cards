from time import sleep
from abc import ABC, abstractmethod
from selenium.webdriver import Firefox
from .funcs import os, get_from_txt, get_imgs_name, remove_imgs_list, shelve


class FlashCard:
    """
        Classe que representa um objeto Flash Card, que são cartões utilizados em revisões espaçadas e que possuem o conteúdo estudado na parte da frente e sua "resposta" na parte de trás."""

    def __init__(self, front: str, back: str) -> None:
        self.front = front
        self.back = back


class MyCard(FlashCard):
    """
        Classe que insere os flash cards no contexto de criação."""

    _DEFAULT_BACK = "*CONFIRA NO DICIONÁRIO CONFIGURADO OU NA FERRAMENTA DE TRADUÇÃO*"

    def __init__(self, front: str, source: str) -> None:
        super().__init__(front, back=self._DEFAULT_BACK)
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


class AbstraticSourceAdmin(ABC):
    """
        Classe que abstrai um administrador de fontes de conteúdo para criação de flash cards."""
    @abstractmethod
    def _return_sources(self) -> None:
        """
            Assinatura para estabelecer o contrato de implementação desse método que deverá retornar as fontes."""
        ...

    @abstractmethod
    def update_sources(self) -> None:
        """
            Assinatura para estabelecer o contrato de implementação desse método que deverá atualizar as fontes."""
        ...


class TextSourceAdmin(AbstraticSourceAdmin):
    """
        Classe que herda de AbstraticSourceAdmin e implementa os contratos de retorno e atualização de fontes de conteúdo para a criação de cartões, no contexto de criação através de um arquivo de texto."""
    def __init__(self, card_source: str) -> None:
        self.card_source = card_source

    def _return_sources(self) -> str:
        """
            Retorna o caminho do arquivo de texto"""
        return self.card_source

    def update_sources(self, phrases: list) -> None:
        """
            Atualiza a fonte de conteúdo após a criação de flash cards."""
        source = get_from_txt(self.card_source)
        update = [phrase for phrase in source if phrase not in phrases]
        with open(self.card_source, "w") as source:
            for phrase in update:
                source.write(f"{phrase}\n")


class ImageSourceAdmin(AbstraticSourceAdmin):
    ...


class GeneralSourceAdmin(TextSourceAdmin):
    def __init__(self, card_type: str, card_source: str) -> None:
        self.card_type = card_type
        self.card_source = card_source

    def _return_sources(self) -> "Implementação da superclasse":
        if self.card_type == "text":
            return TextSourceAdmin._return_sources(self)

    def update_sources(self, cards: list) -> "Implementação da superclasse":
        """
            Recebe uma lista de MyCards e realiza, de acordo com o contexto, o filtro do conteúdo a ser entregue para a implementação da superclasse."""
        for_update = []
        if self.card_type == "text":
            for card in cards:
                for_update.append(card.front)
            return TextSourceAdmin.update_sources(self, for_update)


class AbstraticCardWriter(ABC):
    """
        Abstração de um escritor de flash cards."""
    @abstractmethod
    def _get_phrases(self) -> None:
        """
            Assinatura de um contrato que implementa a obtenção de frases pelas classes posteriores."""
        ...

    @abstractmethod
    def _write(self) -> None:
        """
            Assinatura de um contrato que implementa a escrita de frases em objetos MyCard pelas classes posteriores."""
        ...


class TextCardWriter(AbstraticCardWriter):
    """
        Classe que herda de AbstraticCardWriter e implementa seus contratos de que garantem a criação de objetos MyCard."""
    def _get_phrases(self, source: str) -> list:
        """
            Obtém uma lista de frases a partir de um arquivo de texto e retorna essa lista.
                                   
            Args:
                source (str): path do arquivo de texto."""
        
        phrases = get_from_txt(source)
        return phrases

    def _write(self, phrase: str, source: str) -> MyCard:
        """
            Escreve um flash card em um objeto MyCard.

            Args:
                phrase (str): frase referente ao MyCard.front
                source (str): path de onde foi retirado a frase

            Returns:
                MyCard: objeto preenchido."""
        return MyCard(phrase, source)


class ImageCardWriter(AbstraticCardWriter):
    # TODO: type annotations após finalizar o método
    def _get_phrases(self, source):
        return print("obtendo frases...")

    def _write(self, phrase, source):
        return print("escrevendo card...")


class CardWriterAdmin(TextCardWriter, ImageCardWriter):
    """
        Classe responsável por gerenciar o contexto de produção de objetos MyCard de acordo com a demanda estabelecida no card_type. No fim, delega a criação para a implementação de uma de suas superclasse."""
    def __init__(self, card_type: str, card_source: str) -> None:
        self.card_type = card_type
        self.card_source = card_source

    def _write(self, phrase: str, source: str) -> "Implementação da superclasse":        
        if self.card_type == "text":
            return TextCardWriter._write(self, phrase, source)
        else:
            return ImageCardWriter._write(self, phrase, source)


class DataBaseAdmin(AbstraticSourceAdmin):
    """
        Classe que herda de AbstraticSourceAdmin e que implementa seus contratos, tornando-a responsável por gerenciar a estrutura de persistência que estoca objetos MyCard gerados em produção."""
    def __init__(self, db_cards: str, db_key: str) -> None:
        self.db_cards = db_cards
        self.db_key = db_key
        self._database = shelve

    def _verify_key(self) -> None:
        """
            Método que realiza a verificação de existencia da key/coluna que eventualmente está estocado objetos MyCard."""
        with self._database.open(self.db_cards) as db:
            if not self.db_key in db.keys():
                db[self.db_key] = []

    def update_sources(self, cards: list) -> None:
        """
            Método resposável pela atualização da estrutura de persistência, de acordo com o status de inserido do objeto MyCard.

            Args:
                cards (list): lista e objetos MyCard a serem submetido por avaliação e comparação com objetos MyCard eventualmente estocados na estrutura de db."""
        self._verify_key()
        with self._database.open(self.db_cards) as db:
            cards_temp = db[self.db_key]
            c_temp_repr = [card.representation for card in cards_temp]

            for card in cards:
                if card.inserted == False:
                    if not card.representation in c_temp_repr:
                        cards_temp.append(card)

                if card.inserted == True:
                    c_temp = card
                    c_temp.inserted = False
                    for i, c in enumerate(cards_temp):
                        if c.representation == c_temp.representation:
                            cards_temp.pop(i)

            db[self.db_key] = cards_temp

    def _return_sources(self) -> list:
        """
            Método que retorna uma lista de objetos MyCard estocados na estrutura de persistencia."""
        self._verify_key()
        with self._database.open(self.db_cards) as db:
            cards_list = db[self.db_key]
        return cards_list

#TODO: REALIZAR POR COMPOSIÇÃO O WRITE
#TODO: REALIZAR POR COMPOSIÇÃO O SOURCE
#TODO: REALIZAR POR COMPOSIÇÃO O DATABASE

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
        cards = self.data_base_admin._return_sources()
        self._cards_list += [card for card in cards]

class CardManager(CardWriterAdmin, GeneralSourceAdmin, DataBaseAdmin):
    """
        Classe que gerencia a criação de objetos MyCard, herdando as classes que em conjunto torna todo esse processo possível."""
    def __init__(
                self, card_type: str, card_source: str, 
                db_cards: str, db_key: str) -> None:

        if not (card_type == "text" or card_type == "image"):
            raise Exception('card_type field should be "text" or "image"')

        super().__init__(card_type, card_source)
        DataBaseAdmin.__init__(self, db_cards, db_key)
        self._cards_list = []    
    
    @property
    def cards_list(self) -> list:
        return self._cards_list.copy()

    def create_card(self) -> None:
        """
            Método que cria/agrupa objetos MyCard."""
        self._verify_cards()
        card_src = self._return_sources()
        src = self.card_source
        for phrase in self._get_phrases(card_src):
            card = self._write(phrase, src)
            self._cards_list.append(card)
        DataBaseAdmin.update_sources(self, self.cards_list)

    def _verify_cards(self) -> None:
        """
            Método que realiza a verificação de possiveis cards estocados na estrutura de persistência."""
        cards = DataBaseAdmin._return_sources(self)
        self._cards_list += [card for card in cards]

    def update_card(self, card: MyCard) -> None:
        """
            Método que atualiza o status de inserido dos objetos MyCard agrupados em sua lista interna.
            
            Arg:
            card (MyCard): card que foi submetido a inserção e que será comparado com os cards a qual foi originado."""
        for i, c in enumerate(self.cards_list):
            if c.representation == card.representation:
                self._cards_list[i].inserted = True
                break

    def update_sources(self) -> None:
        """
            Método que chama as implementações de atualização das superclasses referente a fontes de criação e estocagem."""
        GeneralSourceAdmin.update_sources(self, self.cards_list)
        DataBaseAdmin.update_sources(self, self.cards_list)



class AnkiBot:
    """
        Classe responsável pelo bot que insere os flash cards no site do Anki."""

    def __init__(self, card_type: str, card_source: str, 
                db_cards: str, db_key: str) -> None:
        self.cardManager = CardManager(card_type, card_source, db_cards, db_key)

    def start(self, login_path: str = "") -> None:
        """
            Método responsável pela interação com a plataforma Anki, desde o login até a inserção dos conteúdos que compõe o flash card.

            Arg:
                login_path: path do arquivo que contém o login."""

        self.cardManager.create_card()
        created_cards = self.cardManager.cards_list
        if len(created_cards) == 0:
            print("Sem cards para inserir")
            return

        # SETTINGS
        if login_path != "":
            em, pw = get_from_txt(login_path)
        else:
            em, pw = get_from_txt("login.txt")
        url = "https://ankiweb.net/account/login"
        try:
            browser = Firefox()
            browser.implicitly_wait(30)
            browser.get(url)
        except Exception as err:
            browser.close()
            print("NÃO FOI POSSÍVEL CONECTAR\n", err)
            input("\n\nPressione a tecla enter.")
            print("\nFINALIZANDO...")
        else:
            # LOGIN
            browser.find_element_by_css_selector('input[id="email"]').send_keys(em)
            browser.find_element_by_css_selector('input[type="password"]').send_keys(pw)
            browser.find_element_by_css_selector('input[type="submit"]').click()
            sleep(1)

            # ADD BUTTON
            browser.find_elements_by_css_selector('a[class="nav-link"]')[1].click()
            sleep(1)

            # INPUT FLASHCARDS
            for card in created_cards:
                try:
                    browser.find_element_by_id("f0").send_keys(card.front)

                    browser.find_element_by_id("f1").send_keys(card.back)

                    browser.find_element_by_css_selector(
                        'button[class$="primary"]'
                    ).click()
                    sleep(1)

                except Exception as err:
                    print(err)

                else:
                    self.cardManager.update_card(card)

        finally:
            self.cardManager.update_sources()
            browser.quit()
