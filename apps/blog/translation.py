from modeltranslation.translator import register, TranslationOptions
from .models import Blog, Lesson, DetailDescription, FAQ

@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('name', 'rich',)

@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('name', 'rich',)

@register(DetailDescription)
class DetailDescriptionTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)

