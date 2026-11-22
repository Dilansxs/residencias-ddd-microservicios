FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY gestion_alertas/ ./gestion_alertas/

CMD ["python", "-m", "gestion_alertas.main"]
