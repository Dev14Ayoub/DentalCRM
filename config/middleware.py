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

class ForceEnglishAdminMiddleware:
    """
    Middleware to force the language to English for admin URLs only.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            logger.debug("ForceEnglishAdminMiddleware activated for admin URL: setting language to en-us")
            translation.activate('en-us')
            request.LANGUAGE_CODE = 'en-us'
            response = self.get_response(request)
            translation.deactivate()
            return response
        else:
            return self.get_response(request)
