FROM python:3.9-slim

# PYTHONDONTWRITEBYTECODE 1 - Prevents Python from writing .pyc files which can clutter the filesystem
# PYTHONUNBUFFERED 1 - Output is written straight to docker terminal without being held in buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
