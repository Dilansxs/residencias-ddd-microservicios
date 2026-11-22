import os

from gestion_alertas.application.use_cases import ProcesarAnomaliaSalud
from gestion_alertas.infrastructure.alerta_sqlite import AlertaRelacionalSQLite
from gestion_alertas.infrastructure.consumidor_rabbit import ConsumidorEventosRabbit
from gestion_alertas.infrastructure.notificador_consola import NotificadorConsola

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
ALERTAS_DB_PATH = os.getenv("ALERTAS_DB_PATH", "alertas_plataforma.db")
COLA_ANOMALIAS = "anomalias_salud"


def main() -> None:
    repositorio = AlertaRelacionalSQLite(ALERTAS_DB_PATH)
    notificador = NotificadorConsola()
    caso_uso = ProcesarAnomaliaSalud(repositorio, notificador)
    consumidor = ConsumidorEventosRabbit(
        RABBITMQ_HOST,
        COLA_ANOMALIAS,
        caso_uso,
        RABBITMQ_USER,
        RABBITMQ_PASSWORD,
    )

    try:
        consumidor.iniciar()
    except KeyboardInterrupt:
        print("\n[GESTIÓN DE ALERTAS] Detenido por el usuario.")
    finally:
        consumidor.cerrar()


if __name__ == "__main__":
    main()