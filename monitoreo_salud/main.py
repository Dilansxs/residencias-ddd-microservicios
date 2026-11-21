import sys
import time

from monitoreo_salud.application.use_cases import EvaluarLecturas
from monitoreo_salud.domain.services import DeteccionAnomalia
from monitoreo_salud.domain.value_objects import IdentificadorResidencia
from monitoreo_salud.infrastructure.config import (
    COLA_ANOMALIAS,
    LIMITES_LOCALES,
    RABBITMQ_HOST,
)
from monitoreo_salud.infrastructure.dispositivo_simulado import DispositivoSimulado
from monitoreo_salud.infrastructure.lectura_sqlite import LecturaRelacionalSQLite
from monitoreo_salud.infrastructure.publicador_rabbit import PublicadorEventosRabbit


def main() -> None:
    codigo_residencia = sys.argv[1] if len(sys.argv) > 1 else "RES-01"
    residencia_id = IdentificadorResidencia(codigo_residencia)
    ruta_bd = f"telemetria_{codigo_residencia.lower()}.db"

    dispositivo = DispositivoSimulado(residencia_id)
    repositorio = LecturaRelacionalSQLite(ruta_bd)
    publicador = PublicadorEventosRabbit(RABBITMQ_HOST, COLA_ANOMALIAS)
    detector = DeteccionAnomalia(LIMITES_LOCALES)
    caso_uso = EvaluarLecturas(detector, repositorio, publicador)

    print(f"[MONITOREO - {codigo_residencia}] Iniciado. BD local: {ruta_bd}")
    print("Presiona Ctrl+C para detener.\n")

    try:
        while True:
            lecturas = dispositivo.capturar_lecturas()
            anomalias = caso_uso.ejecutar(residencia_id, lecturas)

            for lec in lecturas:
                print(
                    f"[{codigo_residencia}] {lec.referencia.codigo} | "
                    f"{lec.tipo_metrica}: {lec.medicion.valor} {lec.medicion.unidad} -> {lec.estado}"
                )

            if anomalias:
                print(f"  >> {len(anomalias)} evento(s) AnomaliaSaludDetectada enviado(s) a RabbitMQ.")
            print("-" * 65)
            time.sleep(4)
    except KeyboardInterrupt:
        print(f"\n[MONITOREO - {codigo_residencia}] Detenido por el usuario.")
    finally:
        publicador.cerrar()


if __name__ == "__main__":
    main()