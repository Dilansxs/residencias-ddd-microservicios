import random

from monitoreo_salud.domain.entities import Sensor
from monitoreo_salud.domain.value_objects import (
    IdentificadorResidencia,
    Medicion,
    ReferenciaResidente,
)


class DispositivoSimulado:
    def __init__(self, residencia_id: IdentificadorResidencia) -> None:
        self._residencia_id = residencia_id
        self._residentes = ["RESIDENTE-101", "RESIDENTE-102", "RESIDENTE-103"]

    def capturar_lecturas(self) -> list[Sensor]:
        residente = ReferenciaResidente(random.choice(self._residentes))
        forzar_anomalia = random.random() < 0.35

        fc = random.uniform(115, 145) if forzar_anomalia else random.uniform(62, 95)
        temp = random.uniform(38.1, 39.5) if forzar_anomalia else random.uniform(36.1, 37.2)
        spo2 = random.uniform(84, 90) if forzar_anomalia else random.uniform(95, 99)

        return [
            Sensor(
                sensor_id=f"SENS-FC-{residente.codigo[-3:]}",
                residencia_id=self._residencia_id,
                referencia=residente,
                tipo_metrica="frecuencia_cardiaca",
                medicion=Medicion(round(fc, 1), "bpm"),
            ),
            Sensor(
                sensor_id=f"SENS-TEMP-{residente.codigo[-3:]}",
                residencia_id=self._residencia_id,
                referencia=residente,
                tipo_metrica="temperatura",
                medicion=Medicion(round(temp, 1), "°C"),
            ),
            Sensor(
                sensor_id=f"SENS-SPO2-{residente.codigo[-3:]}",
                residencia_id=self._residencia_id,
                referencia=residente,
                tipo_metrica="oxigeno_sangre",
                medicion=Medicion(round(spo2, 1), "%"),
            ),
        ]