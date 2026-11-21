from monitoreo_salud.domain.value_objects import Limite

RABBITMQ_HOST = "localhost"
COLA_ANOMALIAS = "anomalias_salud"

LIMITES_LOCALES: dict[str, Limite] = {
    "frecuencia_cardiaca": Limite(minimo=55.0, maximo=105.0, severidad="ALTA"),
    "temperatura": Limite(minimo=35.5, maximo=37.8, severidad="MEDIA"),
    "oxigeno_sangre": Limite(minimo=92.0, maximo=100.0, severidad="CRITICA"),
}