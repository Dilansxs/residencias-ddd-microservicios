from gestion_alertas.application.ports import Notificador
from gestion_alertas.domain.entities import Alerta


class NotificadorConsola(Notificador):
    def notificar(self, alerta: Alerta) -> None:
        destino = (
            "SERVICIOS DE EMERGENCIA + PERSONAL MÉDICO"
            if alerta.requiere_emergencia()
            else "PERSONAL MÉDICO DE TURNO"
        )
        print(
            f"[ALERTA {alerta.severidad}] ID={alerta.alerta_id[:8]} | "
            f"Residencia={alerta.residencia_id} | Residente={alerta.referencia_residente}\n"
            f"  Detalle : {alerta.descripcion}\n"
            f"  Acción  : Guardada en BD Plataforma y derivada a -> {destino}\n"
            + "=" * 70
        )