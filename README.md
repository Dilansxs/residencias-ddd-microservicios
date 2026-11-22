# Monitoreo de salud y gestión de alertas

Proyecto académico con dos microservicios independientes organizados con DDD y Arquitectura Limpia:

- `monitoreo_salud` simula sensores, evalúa las lecturas, guarda la telemetría en SQLite y publica anomalías en RabbitMQ.
- `gestion_alertas` consume las anomalías, guarda las alertas en su propia base SQLite y las muestra en consola.

El dominio y la aplicación dependen de puertos; las implementaciones de SQLite y RabbitMQ están en infraestructura. Cada servicio es ejecutable como módulo de Python.

## Requisitos

- Python 3.10 o superior
- Docker Desktop con Docker Compose, iniciado

## Ejecución con Docker

Docker Compose crea tres contenedores: RabbitMQ, monitoreo de salud y gestión de alertas. Los servicios se conectan al broker por el nombre `rabbitmq`; Compose espera a que esté saludable antes de iniciarlos. Sus bases SQLite se conservan en volúmenes separados.

```powershell
docker compose up --build -d
```

Consulta los registros de los servicios:

```powershell
docker compose logs -f monitoreo_salud gestion_alertas
```

El panel de RabbitMQ está disponible en `http://localhost:15672`. Para desarrollo local, el usuario y contraseña predeterminados son `residencias` y `residencias_dev`; puedes cambiarlos definiendo `RABBITMQ_USER` y `RABBITMQ_PASSWORD` en el entorno antes de iniciar Compose.

Detén los contenedores sin borrar las bases de datos:

```powershell
docker compose down
```

## Ejecución local opcional

Requiere Python 3.10 o superior. Crea y activa un entorno virtual en PowerShell e instala la dependencia:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Inicia RabbitMQ con `docker compose up -d rabbitmq` y ejecuta cada servicio desde la raíz del proyecto, en terminales separadas:

```powershell
python -m gestion_alertas.main
python -m monitoreo_salud.main RES-01
```
