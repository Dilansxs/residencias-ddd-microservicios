FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY monitoreo_salud/ ./monitoreo_salud/

CMD ["python", "-m", "monitoreo_salud.main"]
