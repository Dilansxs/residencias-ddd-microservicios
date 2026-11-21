from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Alerta:
    evento_origen_id: str
    residencia_id: str
    referencia_residente: str
    tipo_metrica: str
    valor_medido: float
    severidad: str
    descripcion: str
    estado: str = "ACTIVA"
    alerta_id: str = field(default_factory=lambda: str(uuid4()))
    creada_en: datetime = field(default_factory=datetime.now)

    def requiere_emergencia(self) -> bool:
        return self.severidad == "CRITICA"