import traceback
from django.conf import settings
from django.core.mail import send_mail


class ExceptionHandler:
    def __init__(self, get_response):
        self._get_resopnse = get_response

    def __call__(self, request):
        response = self._get_resopnse(request)
        return response

    def process_exception(self, request, _):
        title = f"Fatal exception happend in {request.user}"
        send_mail(title, traceback.format_exc(), settings.DEFAULT_FROM_EMAIL, settings.ADMINS)
