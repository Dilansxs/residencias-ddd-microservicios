from gestion_alertas.application.ports import Notificador, RepositorioAlerta
from gestion_alertas.domain.entities import Alerta


class ProcesarAnomaliaSalud:
    def __init__(
        self,
        repositorio: RepositorioAlerta,
        notificador: Notificador,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, datos_evento: dict) -> Alerta:
        alerta = Alerta(
            evento_origen_id=datos_evento["evento_id"],
            residencia_id=datos_evento["residencia_id"],
            referencia_residente=datos_evento["referencia_residente"],
            tipo_metrica=datos_evento["tipo_metrica"],
            valor_medido=datos_evento["valor_medido"],
            severidad=datos_evento["severidad"],
            descripcion=datos_evento["descripcion"],
        )

        self._repositorio.guardar(alerta)
        self._notificador.notificar(alerta)
        return alerta