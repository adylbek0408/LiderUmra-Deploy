from modeltranslation.translator import register, TranslationOptions
from apps.blog.models import Blog, Lesson, DetailDescription, FAQ


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'rich',)


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'rich',)


@register(DetailDescription)
class DetailDescriptionTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)

