from django.utils import translation


class LanguageHeaderMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get('Accept-Language', 'ky')

        if lang not in ['ky', 'ru']:
            lang = 'ky'

        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        setattr(request, '_language', lang)

        response = self.get_response(request)

        response['Content-Language'] = lang

        return response
