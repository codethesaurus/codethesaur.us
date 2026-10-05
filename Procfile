release: python manage.py migrate && python manage.py createcachetable
web: gunicorn codethesaurus.wsgi --log-file -