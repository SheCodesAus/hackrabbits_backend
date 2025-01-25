release: python sheinspires/manage.py migrate
web: gunicorn --pythonpath sheinspires sheinspires.wsgi --log-file -