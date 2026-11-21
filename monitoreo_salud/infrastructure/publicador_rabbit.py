import json
import pika

from monitoreo_salud.application.ports import PublicadorEventos
from monitoreo_salud.domain.events import AnomaliaSaludDetectada


class PublicadorEventosRabbit(PublicadorEventos):
    def __init__(self, host: str, cola: str) -> None:
        self._cola = cola
        self._conexion = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self._canal = self._conexion.channel()
        self._canal.queue_declare(queue=self._cola, durable=True)

    def publicar(self, evento: AnomaliaSaludDetectada) -> None:
        mensaje = json.dumps(evento.to_dict(), ensure_ascii=False)
        self._canal.basic_publish(
            exchange="",
            routing_key=self._cola,
            body=mensaje.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def cerrar(self) -> None:
        if self._conexion and not self._conexion.is_closed:
            self._conexion.close()