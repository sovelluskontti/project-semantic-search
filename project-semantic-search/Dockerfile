FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DATA_PATH=/app/server/data/embeddings.csv

CMD ["python", "/app/server/data_scripts/load_data.py"]
