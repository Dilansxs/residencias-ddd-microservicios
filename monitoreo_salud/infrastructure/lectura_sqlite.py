import sqlite3

from monitoreo_salud.application.ports import RepositorioLectura
from monitoreo_salud.domain.entities import Sensor


class LecturaRelacionalSQLite(RepositorioLectura):
    def __init__(self, ruta_bd: str) -> None:
        self._ruta_bd = ruta_bd
        self._inicializar_tabla()

    def _inicializar_tabla(self) -> None:
        with sqlite3.connect(self._ruta_bd) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS lecturas_telemetria (
                    lectura_id TEXT PRIMARY KEY,
                    sensor_id TEXT NOT NULL,
                    residencia_id TEXT NOT NULL,
                    referencia_residente TEXT NOT NULL,
                    tipo_metrica TEXT NOT NULL,
                    valor REAL NOT NULL,
                    unidad TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    capturado_en TEXT NOT NULL
                )
                """
            )

    def guardar(self, lectura: Sensor) -> None:
        with sqlite3.connect(self._ruta_bd) as conn:
            conn.execute(
                """
                INSERT INTO lecturas_telemetria (
                    lectura_id, sensor_id, residencia_id, referencia_residente,
                    tipo_metrica, valor, unidad, estado, capturado_en
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lectura.lectura_id,
                    lectura.sensor_id,
                    lectura.residencia_id.valor,
                    lectura.referencia.codigo,
                    lectura.tipo_metrica,
                    lectura.medicion.valor,
                    lectura.medicion.unidad,
                    lectura.estado,
                    lectura.capturado_en.isoformat(timespec="seconds"),
                ),
            )