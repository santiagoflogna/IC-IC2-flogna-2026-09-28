FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY script.py .

RUN echo "Este mensaje se ejecuta durante el build"

CMD ["python", "script.py"]