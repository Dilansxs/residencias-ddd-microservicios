from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class AnomaliaSaludDetectada:
    residencia_id: str
    referencia_residente: str
    sensor_id: str
    tipo_metrica: str
    valor_medido: float
    severidad: str
    descripcion: str
    evento_id: str = field(default_factory=lambda: str(uuid4()))
    ocurrido_en: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "evento_id": self.evento_id,
            "ocurrido_en": self.ocurrido_en.isoformat(timespec="seconds"),
            "residencia_id": self.residencia_id,
            "referencia_residente": self.referencia_residente,
            "sensor_id": self.sensor_id,
            "tipo_metrica": self.tipo_metrica,
            "valor_medido": self.valor_medido,
            "severidad": self.severidad,
            "descripcion": self.descripcion,
        }