from celery import shared_task
from .utils import send_email


@shared_task
def send_email_task(id, username, email, state, prefix):
    send_email(id, username, email, state, prefix)
