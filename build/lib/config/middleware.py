from django.utils import translation
import logging

logger = logging.getLogger(__name__)

class ForceEnglishMiddleware:
    """
    Middleware to force the language to English for all requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("ForceEnglishMiddleware activated: setting language to en-us")
        translation.activate('en-us')
        request.LANGUAGE_CODE = 'en-us'
        response = self.get_response(request)
        translation.deactivate()
        return response
