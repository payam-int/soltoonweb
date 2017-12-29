from django.conf import settings
from django.utils import translation


def force_language_middleware(get_response):
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
