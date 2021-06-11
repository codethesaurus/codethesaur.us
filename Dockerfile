FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /code
copy requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0:8000
