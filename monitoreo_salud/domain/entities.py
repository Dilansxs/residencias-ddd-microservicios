from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from monitoreo_salud.domain.value_objects import (
    IdentificadorResidencia,
    Medicion,
    ReferenciaResidente,
)


@dataclass
class Sensor:
    sensor_id: str
    residencia_id: IdentificadorResidencia
    referencia: ReferenciaResidente
    tipo_metrica: str
    medicion: Medicion
    capturado_en: datetime = field(default_factory=datetime.now)
    estado: str = "PENDIENTE"
    lectura_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class MonitoreoEvaluacion:
    residencia_id: IdentificadorResidencia
    evaluacion_id: str = field(default_factory=lambda: str(uuid4()))
    evaluado_en: datetime = field(default_factory=datetime.now)
    lecturas: list[Sensor] = field(default_factory=list)

    def anadir_lectura(self, lectura: Sensor) -> None:
        # Invariante del Agregado: no mezclar lecturas de otra residencia
        if lectura.residencia_id != self.residencia_id:
            raise ValueError(
                f"La lectura pertenece a {lectura.residencia_id.valor}, "
                f"no a {self.residencia_id.valor}."
            )
        self.lecturas.append(lectura)