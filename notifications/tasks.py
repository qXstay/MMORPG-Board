from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from board.models import Response, Post, Category
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_response_notification(response_id):
    """Уведомление автору объявления о новом отклике"""
    try:
        response = Response.objects.get(id=response_id)
    except Response.DoesNotExist:
        return

    subject = f'Новый отклик на ваше объявление "{response.post.title}"'
    message = f'Пользователь {response.author.username} оставил отклик:\n\n{response.text}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [response.post.author.email])

@shared_task
def send_response_accepted_notification(response_id):
    """Уведомление автору отклика о его принятии"""
    try:
        response = Response.objects.get(id=response_id)
    except Response.DoesNotExist:
        return

    subject = f'Ваш отклик на "{response.post.title}" принят'
    message = f'Автор объявления "{response.post.title}" принял ваш отклик:\n\n{response.text}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [response.author.email])


@shared_task
def send_newsletter():
    # Получаем всех пользователей, подписанных на рассылку
    User = get_user_model()
    subscribers = User.objects.filter(subscribed_to_news=True)

    # Рассылаем письма
    for user in subscribers:
        context = {
            'user': user,
            'date': datetime.datetime.now().strftime("%d.%m.%Y"),
        }

        html_message = render_to_string('notifications/newsletter.html', context)
        text_message = render_to_string('notifications/newsletter.txt', context)

        send_mail(
            subject='Новостная рассылка',
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message
        )

@shared_task
def send_weekly_newsletter():
    """Еженедельная рассылка всех объявлений за неделю"""
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)

    if not posts.exists():
        return

    subscribers = User.objects.exclude(email='').values_list('email', flat=True)

    subject = 'Новые объявления за неделю'
    message = '\n\n'.join([f"{p.title} — {p.get_absolute_url()}" for p in posts])
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, subscribers)