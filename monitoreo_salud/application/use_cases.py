from monitoreo_salud.application.ports import PublicadorEventos, RepositorioLectura
from monitoreo_salud.domain.entities import MonitoreoEvaluacion, Sensor
from monitoreo_salud.domain.events import AnomaliaSaludDetectada
from monitoreo_salud.domain.services import DeteccionAnomalia
from monitoreo_salud.domain.value_objects import IdentificadorResidencia


class EvaluarLecturas:
    def __init__(
        self,
        detector: DeteccionAnomalia,
        repositorio: RepositorioLectura,
        publicador: PublicadorEventos,
    ) -> None:
        self._detector = detector
        self._repositorio = repositorio
        self._publicador = publicador

    def ejecutar(
        self,
        residencia_id: IdentificadorResidencia,
        lecturas: list[Sensor],
    ) -> list[AnomaliaSaludDetectada]:
        evaluacion = MonitoreoEvaluacion(residencia_id=residencia_id)
        for lectura in lecturas:
            evaluacion.anadir_lectura(lectura)

        anomalias = self._detector.evaluar(evaluacion)

        # 1. Persistir toda la telemetría en la BD local de la residencia
        for lectura in evaluacion.lecturas:
            self._repositorio.guardar(lectura)

        # 2. Publicar únicamente las anomalías al bus de eventos
        for anomalia in anomalias:
            self._publicador.publicar(anomalia)

        return anomalias