import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmorpg_board.settings')

app = Celery('mmorpg_board')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'notifications.tasks.send_weekly_newsletter',
        'schedule': crontab(minute=0, hour=9, day_of_week='monday'),
    },
}