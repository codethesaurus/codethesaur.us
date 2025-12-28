FROM python:3.12-slim
ENV PYTHONBUFFERED=1
WORKDIR /code
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py migrate && \
    python manage.py collectstatic --clear --no-input && \
    python manage.py runserver 0.0.0.0:8000
