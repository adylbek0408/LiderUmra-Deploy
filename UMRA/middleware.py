from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        lang = request.headers.get('Accept-Language', 'ky')
        if lang not in ['ky', 'ru']:
            lang = 'ky'
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        setattr(request, '_language', lang)
        return None

    def process_response(self, request, response):
        lang = getattr(request, '_language', 'ky')
        response['Content-Language'] = lang
        return response

