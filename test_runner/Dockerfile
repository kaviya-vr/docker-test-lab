FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY test_health.py .

CMD ["python", "test_health.py"]