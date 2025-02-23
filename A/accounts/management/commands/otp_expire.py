from django.core.management import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    # deletes useless codes
    def handle(self, *args, **options):
        expires=datetime.now(tz=pytz.UTC)- timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expires).delete()

        self.stdout.write(self.style.SUCCESS('expired codes are deleted!'))