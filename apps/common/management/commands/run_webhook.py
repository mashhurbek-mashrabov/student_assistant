import requests
from django.core.management.base import BaseCommand

from common.constants import DOMAIN
from student_bot.constants import STUDENT_BOT_TOKEN, STUDENT_WEBHOOK_URL
from tutor_bot.constants import TUTOR_WEBHOOK_URL, TUTOR_BOT_TOKEN


class Command(BaseCommand):
    help = 'Run webhook'

    def handle(self, *args, **options):
        requests.get(f'https://api.telegram.org/bot{STUDENT_BOT_TOKEN}/setWebhook?url={DOMAIN}{STUDENT_WEBHOOK_URL}')
        requests.get(f'https://api.telegram.org/bot{TUTOR_BOT_TOKEN}/setWebhook?url={DOMAIN}{TUTOR_WEBHOOK_URL}')
        self.stdout.write(self.style.SUCCESS('Webhook is running'))
