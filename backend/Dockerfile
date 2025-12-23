FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system deps for some libraries
RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

ENV MEDIA_ROOT=/data/media
RUN mkdir -p ${MEDIA_ROOT}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
