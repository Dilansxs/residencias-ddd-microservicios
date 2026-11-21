# Monitoreo de salud y gestión de alertas

Proyecto académico con dos microservicios independientes organizados con DDD y Arquitectura Limpia:

- `monitoreo_salud` simula sensores, evalúa las lecturas, guarda la telemetría en SQLite y publica anomalías en RabbitMQ.
- `gestion_alertas` consume las anomalías, guarda las alertas en su propia base SQLite y las muestra en consola.

El dominio y la aplicación dependen de puertos; las implementaciones de SQLite y RabbitMQ están en infraestructura. Cada servicio es ejecutable como módulo de Python.

## Requisitos

- Python 3.10 o superior
- Docker Desktop con Docker Compose, iniciado

## Instalación y ejecución

Ejecuta estos comandos desde la raíz del proyecto. En Windows PowerShell, crea y activa el entorno virtual e instala la dependencia:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Inicia RabbitMQ:

```powershell
docker compose up -d
```

Abre dos terminales, ambas en la raíz del proyecto y con el entorno virtual activado. Ejecuta un servicio en cada terminal:

```powershell
python -m gestion_alertas.main
```

```powershell
python -m monitoreo_salud.main RES-01
```

El monitoreo registra las lecturas en `telemetria_res-01.db`; las alertas recibidas se guardan en `alertas_plataforma.db`. Ambos archivos son locales y están excluidos de Git.
