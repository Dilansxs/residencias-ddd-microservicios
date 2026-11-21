from gestion_alertas.application.use_cases import ProcesarAnomaliaSalud
from gestion_alertas.infrastructure.alerta_sqlite import AlertaRelacionalSQLite
from gestion_alertas.infrastructure.consumidor_rabbit import ConsumidorEventosRabbit
from gestion_alertas.infrastructure.notificador_consola import NotificadorConsola

RABBITMQ_HOST = "localhost"
COLA_ANOMALIAS = "anomalias_salud"


def main() -> None:
    repositorio = AlertaRelacionalSQLite("alertas_plataforma.db")
    notificador = NotificadorConsola()
    caso_uso = ProcesarAnomaliaSalud(repositorio, notificador)
    consumidor = ConsumidorEventosRabbit(RABBITMQ_HOST, COLA_ANOMALIAS, caso_uso)

    try:
        consumidor.iniciar()
    except KeyboardInterrupt:
        print("\n[GESTIÓN DE ALERTAS] Detenido por el usuario.")
    finally:
        consumidor.cerrar()


if __name__ == "__main__":
    main()