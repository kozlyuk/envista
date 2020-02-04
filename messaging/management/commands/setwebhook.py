from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Setting up telegram Webhook'

    def handle(self, *args, **options):
        try:
            request = requests.get(f'{settings.MAIN_URL}/setWebhook?url={settings.WEBHOOK_URL}')
        except ConnectionError:
            raise CommandError('ConnectionError')

        self.stdout.write(self.style.SUCCESS('API answer: %s' % request.json()))
