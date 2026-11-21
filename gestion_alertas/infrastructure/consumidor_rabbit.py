import json
import pika

from gestion_alertas.application.use_cases import ProcesarAnomaliaSalud


class ConsumidorEventosRabbit:
    def __init__(self, host: str, cola: str, caso_uso: ProcesarAnomaliaSalud) -> None:
        self._cola = cola
        self._caso_uso = caso_uso
        self._conexion = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self._canal = self._conexion.channel()
        self._canal.queue_declare(queue=self._cola, durable=True)

    def _al_recibir_mensaje(self, ch, method, properties, body: bytes) -> None:
        datos = json.loads(body.decode("utf-8"))
        self._caso_uso.ejecutar(datos)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def iniciar(self) -> None:
        self._canal.basic_qos(prefetch_count=1)
        self._canal.basic_consume(
            queue=self._cola,
            on_message_callback=self._al_recibir_mensaje,
        )
        print(f"[GESTIÓN DE ALERTAS] Escuchando eventos en la cola '{self._cola}'...\n")
        self._canal.start_consuming()

    def cerrar(self) -> None:
        if self._conexion and not self._conexion.is_closed:
            self._conexion.close()