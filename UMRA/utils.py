from functools import wraps
from django.utils import translation


def with_language(view_func):
    """
    Декоратор для установки языка в views на основе заголовка Accept-Language
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        lang = request.headers.get('Accept-Language', 'ky')
        if lang not in ['ky', 'ru']:
            lang = 'ky'

        # Сохраняем текущий язык
        current_language = translation.get_language()

        # Устанавливаем язык на основе заголовка
        translation.activate(lang)

        try:
            # Выполняем view с выбранным языком
            response = view_func(request, *args, **kwargs)
            return response
        finally:
            # Восстанавливаем предыдущий язык
            translation.activate(current_language)

    return wrapped_view

