from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Deleting telegram Webhook'

    def handle(self, *args, **options):
        try:
            request = requests.get(f'{settings.MAIN_URL}/deleteWebhook')
        except ConnectionError:
            raise CommandError('ConnectionError')

        self.stdout.write(self.style.SUCCESS('API answer: %s' % request.json()))
