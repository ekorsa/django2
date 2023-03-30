import datetime

from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings

from .models import Post, Category


@shared_task
def task_send_notification(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    # print(settings.DEFAULT_FROM_EMAIL)
    # print(subscribers)
    msg.send()
    # time.sleep(10)
    # print("Hello, world!")


@shared_task()
def task_mon_job_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    categories = set(posts.values_list('post_category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    # print(subscribers)

    html_content = render_to_string(
        'weekly_post.html',
        {
            'posts': posts,
            'link': settings.SITE_URL,
        }
    )

    msg = EmailMultiAlternatives(
        subject='новые статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
