from monitoreo_salud.domain.entities import MonitoreoEvaluacion
from monitoreo_salud.domain.events import AnomaliaSaludDetectada
from monitoreo_salud.domain.value_objects import Limite


class DeteccionAnomalia:
    def __init__(self, limites: dict[str, Limite]) -> None:
        self._limites = limites

    def evaluar(self, evaluacion: MonitoreoEvaluacion) -> list[AnomaliaSaludDetectada]:
        anomalias: list[AnomaliaSaludDetectada] = []

        for lectura in evaluacion.lecturas:
            limite = self._limites.get(lectura.tipo_metrica)
            if not limite:
                lectura.estado = "SIN_LIMITE"
                continue

            if limite.es_superado_por(lectura.medicion.valor):
                lectura.estado = "ANOMALA"
                anomalias.append(
                    AnomaliaSaludDetectada(
                        residencia_id=lectura.residencia_id.valor,
                        referencia_residente=lectura.referencia.codigo,
                        sensor_id=lectura.sensor_id,
                        tipo_metrica=lectura.tipo_metrica,
                        valor_medido=lectura.medicion.valor,
                        severidad=limite.severidad,
                        descripcion=(
                            f"{lectura.tipo_metrica} fuera de rango "
                            f"[{limite.minimo}, {limite.maximo}] "
                            f"({lectura.medicion.valor} {lectura.medicion.unidad})"
                        ),
                    )
                )
            else:
                lectura.estado = "NORMAL"

        return anomalias