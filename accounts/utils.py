from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import uuid
import redis


if settings.DEBUG:
    redis = redis.Redis(host='127.0.0.1', port='6379')
else :
    redis = redis.Redis(host='redis', port='6379')


def _generate_code():
    return uuid.uuid4().hex


def send_multi_format_email(prefix, context, to):
    subject_file = 'accounts/%s_subject.txt' % prefix
    txt_file = 'accounts/%s.txt' % prefix
    html_file = 'accounts/%s.html' % prefix

    subject = render_to_string(subject_file)
    from_email = settings.EMAIL_HOST_USER
    text_context = render_to_string(txt_file, context)
    html_context = render_to_string(html_file, context)

    msg = EmailMultiAlternatives(subject, text_context, from_email, [to, ])
    msg.attach_alternative(html_context, 'text/html')
    msg.send()


def add_to_redis(id, state):
    token = _generate_code()
    redis.set(name=f'{state}_{id}', value=token.encode('utf-8'), ex=3600 )
    return token


def get_from_redis(id, state):
    token = redis.get(name=f'{state}_{id}').decode('utf-8')
    return token


def delete_from_redis(id, state):
    redis.delete(f'{state}_{id}')


def send_email(id, username, email, state, prefix):
    # first delte the old code in redis 
    delete_from_redis(id, state)
    context = {
        'username': username,
        'email' : email,
        'code' : add_to_redis(id, state)
    }

    send_multi_format_email(prefix, context, to=email)