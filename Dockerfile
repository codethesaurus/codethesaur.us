FROM python:3-slim
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
