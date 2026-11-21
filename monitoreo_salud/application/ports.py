from abc import ABC, abstractmethod

from monitoreo_salud.domain.entities import Sensor
from monitoreo_salud.domain.events import AnomaliaSaludDetectada


class RepositorioLectura(ABC):
    @abstractmethod
    def guardar(self, lectura: Sensor) -> None:
        pass


class PublicadorEventos(ABC):
    @abstractmethod
    def publicar(self, evento: AnomaliaSaludDetectada) -> None:
        pass