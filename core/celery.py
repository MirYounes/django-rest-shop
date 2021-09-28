from django.conf import settings
from datetime import timedelta
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.pro')

app = Celery('core')
app.autodiscover_tasks()


# configs
if settings.DEBUG:
    broker_url = 'amqp://'
else:
    broker_url = 'amqp://rabbitmq'

app.conf.broker_url = broker_url
app.conf.result_backend = 'rpc://'
app.conf.accept_content = ['json', 'pickle']
app.conf.result_expires = timedelta(days=1)

