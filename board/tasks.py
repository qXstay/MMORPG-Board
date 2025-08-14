from celery import shared_task
from django.utils import timezone
from .models import Response
from datetime import timedelta

@shared_task
def cleanup_old_responses():
    """Удаление непринятых откликов старше 30 дней"""
    threshold = timezone.now() - timedelta(days=30)
    Response.objects.filter(
        accepted=False,
        created_at__lt=threshold
    ).delete()