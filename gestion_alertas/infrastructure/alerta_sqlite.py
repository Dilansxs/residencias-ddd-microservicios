import sqlite3

from gestion_alertas.application.ports import RepositorioAlerta
from gestion_alertas.domain.entities import Alerta


class AlertaRelacionalSQLite(RepositorioAlerta):
    def __init__(self, ruta_bd: str = "alertas_plataforma.db") -> None:
        self._ruta_bd = ruta_bd
        self._inicializar_tabla()

    def _inicializar_tabla(self) -> None:
        with sqlite3.connect(self._ruta_bd) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alertas (
                    alerta_id TEXT PRIMARY KEY,
                    evento_origen_id TEXT NOT NULL,
                    residencia_id TEXT NOT NULL,
                    referencia_residente TEXT NOT NULL,
                    tipo_metrica TEXT NOT NULL,
                    valor_medido REAL NOT NULL,
                    severidad TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    creada_en TEXT NOT NULL
                )
                """
            )

    def guardar(self, alerta: Alerta) -> None:
        with sqlite3.connect(self._ruta_bd) as conn:
            conn.execute(
                """
                INSERT INTO alertas (
                    alerta_id, evento_origen_id, residencia_id, referencia_residente,
                    tipo_metrica, valor_medido, severidad, descripcion, estado, creada_en
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    alerta.alerta_id,
                    alerta.evento_origen_id,
                    alerta.residencia_id,
                    alerta.referencia_residente,
                    alerta.tipo_metrica,
                    alerta.valor_medido,
                    alerta.severidad,
                    alerta.descripcion,
                    alerta.estado,
                    alerta.creada_en.isoformat(timespec="seconds"),
                ),
            )