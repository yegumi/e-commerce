from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

celery_app=Celery('A')
celery_app.autodiscover_tasks(['home', 'accounts'])

celery_app.conf.broker_url='amqp://guest:guest@localhost:5672//'
celery_app.conf.result_backend='rpc://'
celery_app.conf.task_serializer='json'
celery_app.conf.result_serializer='pickle'
celery_app.conf.accept_content=['json','pickle']
celery_app.conf.result_expires=timedelta(days=1)
celery_app.conf.always_eager=False
celery_app.conf.worker_prefetch_multiplier=4
# celery_app.conf.result_expires=None