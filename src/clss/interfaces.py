from abc import ABC, abstractmethod


class SourceAdminInterface(ABC):
    """
        Interface para um administrador de fontes de conteúdo para criação de flash cards."""
    @abstractmethod
    def return_sources(self) -> None:
        """
            Assinatura para estabelecer o contrato de implementação desse método que deverá retornar as fontes."""
        ...

    @abstractmethod
    def update_sources(self) -> None:
        """
            Assinatura para estabelecer o contrato de implementação desse método que deverá atualizar as fontes."""
        ...