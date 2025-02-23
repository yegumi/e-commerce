from celery import shared_task
from .models import OtpCode
from datetime import datetime, timedelta
import pytz

@shared_task
def remove_expire_codes():
    expires = datetime.now(tz=pytz.UTC) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expires).delete()
