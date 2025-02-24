from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Lesson, DetailDescription, FAQ, Photo
from modeltranslation.admin import TranslationAdmin



# class DetailDescriptionInline(admin.StackedInline):
#     model = DetailDescription
#     extra = 1
#     fieldsets = (
#         ('Кыргызча', {
#             'fields': ('blog', 'text_ky', 'image')
#         }),
#         ('Русский', {
#             'fields': ('text_ru',)
#         }),
#     )


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     inlines = [DetailDescriptionInline]
#     fieldsets = (
#         ('Кыргызча', {
#             'fields': ('title_ky', 'rich_ky', 'image',)
#         }),
#         ('Русский', {
#             'fields': ('title_ru', 'rich_ru',)
#         }),
#     )


# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ['title_ky', 'title_ru', 'created_at']
#     search_fields = ['title_ky', 'title_ru', 'rich_ky', 'rich_ru']
#     list_filter = ['created_at']
#     readonly_fields = ['created_at']
#     fieldsets = (
#         ('Кыргызча', {
#             'fields': ('title_ky', 'rich_ky', 'video_url')
#         }),
#         ('Русский', {
#             'fields': ('title_ru', 'rich_ru')
#         }),
#     )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_ky', 'question_ru']
    search_fields = ['question_ky', 'question_ru', 'answer_ky', 'answer_ru']
    fieldsets = (
        ('Кыргызча', {
            'fields': ('question_ky', 'answer_ky')
        }),
        ('Русский', {
            'fields': ('question_ru', 'answer_ru')
        }),
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['photo']
