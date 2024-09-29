# PASA_django/celery.py
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LLMGuardrail.settings')

# create a Celery instance and configure it.
app = Celery('LLMGuardrail')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 使用Redis作为消息代理
app.conf.broker_url = 'redis://localhost:6380/0'

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')