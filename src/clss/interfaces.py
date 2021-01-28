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



class ImageSourceInterface(ABC):
    @abstractmethod
    def get_images(self):
        ...
    
    @abstractmethod
    def remove_images(self):
        ...
    
    @abstractmethod
    def accumulate_image_data(self):
        ...



class TextExtractorInterface(ABC):
    @abstractmethod
    def img_to_str(self):
        ...



class ConfiguratorInterface(ABC):
    @abstractmethod
    def configure(self):
        ...