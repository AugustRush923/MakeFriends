from celery import Celery
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'makefriends.settings.production'

app = Celery("celery_tasks")

app.config_from_object("celery_tasks.config")

app.autodiscover_tasks(['celery_tasks.count', 'celery_tasks.upload'])
