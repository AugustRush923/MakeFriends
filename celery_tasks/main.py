from celery import Celery
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'makefriends.settings.develop'

app = Celery("increase")

app.config_from_object("celery_tasks.config")

app.autodiscover_tasks(['celery_tasks.count'])