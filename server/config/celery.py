from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-rates-every-ten-minutes-and-set-cache': {
        'task': 'apps.currency.tasks.update_rates',
        'schedule': crontab(minute='*/10')
    },
    'update-graphs-every-day': {
        'task': 'apps.currency.tasks.draw_graphs',
        'schedule': crontab(minute='30', hour='14')
    },
}
