# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_to_event(subject, message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


#ران کردن سلری در حالت سولو
# celery -A university_portal worker --loglevel=debug --pool=solo