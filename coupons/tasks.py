from celery import shared_task
from datetime import datetime
from .models import Coupon


@shared_task
def expire_coupon():
    coupuns = Coupon.objects.filter(valid_to__lte=datetime.now())
    coupuns.delete()