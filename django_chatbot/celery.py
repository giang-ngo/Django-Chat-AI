import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_chatbot.settings")

app = Celery("django_chatbot")


app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()
