from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Response
from notifications.tasks import send_response_notification, send_response_accepted_notification


@receiver(post_save, sender=Response)
def notify_about_new_response(sender, instance, created, **kwargs):
    """Отправка письма автору объявления о новом отклике"""
    if created:
        send_response_notification.delay(instance.id)


@receiver(pre_save, sender=Response)
def notify_about_accepted_response(sender, instance, **kwargs):
    """Отправка письма автору отклика при его принятии"""
    if not instance.pk:
        return

    try:
        old_instance = Response.objects.get(pk=instance.pk)
    except Response.DoesNotExist:
        return

    if not old_instance.accepted and instance.accepted:
        send_response_accepted_notification.delay(instance.id)