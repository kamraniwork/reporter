import json
from datetime import datetime
from news_letter.utils.constants.user_constants import UserConstants
from django.core.mail import EmailMessage
from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask


@shared_task()
def send_email_confirm(email):
    body: str = f"""
        با سلام،
        خوش آمدید
        http://localhost:8000/user/
        """
    message: EmailMessage = EmailMessage(
        subject='خوش آمدگویی',
        body=body,
        to=[email],
    )
    return message.send()


@shared_task()
def send_email_news(email):
    body: str = f"""
        دریافت خبرنامه
        http://localhost:8000/user/
        """
    message: EmailMessage = EmailMessage(
        subject='خبرنامه',
        body=body,
        to=[email],
    )
    return message.send()


def _create_signaler_task(email):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.SECONDS)

    PeriodicTask.objects.create(
        interval=schedule,
        name='Sending Signals {}'.format(datetime.now()),
        task='users.tasks.send_email_news',
        kwargs=json.dumps({
            UserConstants.email: email
        })
    )
