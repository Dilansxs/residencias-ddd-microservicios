from abc import ABC, abstractmethod

from gestion_alertas.domain.entities import Alerta


class RepositorioAlerta(ABC):
    @abstractmethod
    def guardar(self, alerta: Alerta) -> None:
        pass


class Notificador(ABC):
    @abstractmethod
    def notificar(self, alerta: Alerta) -> None:
        pass