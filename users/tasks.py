from django.core.mail import EmailMessage
from celery import shared_task


@shared_task()
def send_email_confirm(email):
    body = f"""
        با سلام،
        خوش آمدید
        http://localhost:8000/user/
        """
    message = EmailMessage(
        subject='خوش آمدگویی', body=body, to=[email]
    )
    return message.send()


@shared_task()
def send_email_news(email):
    body = f"""
        دریافت خبرنامه
        http://localhost:8000/user/
        """
    message = EmailMessage(
        subject='خبرنامه', body=body, to=[email]
    )
    return message.send()
