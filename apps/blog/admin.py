from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Lesson, DetailDescription, FAQ, Photo
from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from .models import Blog, Lesson, DetailDescription, FAQ, Photo, YouTubeChannelSettings
from django.core.management import call_command


@admin.register(YouTubeChannelSettings)
class YouTubeChannelSettingsAdmin(admin.ModelAdmin):
    list_display = ['channel_id', 'auto_import', 'last_sync']
    readonly_fields = ['last_sync']
    actions = ['sync_now']

    def sync_now(self, request, queryset):
        try:
            call_command('sync_youtube')
            self.message_user(request, "Синхронизация с YouTube успешно выполнена")
        except Exception as e:
            self.message_user(request, f"Ошибка при синхронизации: {str(e)}", level='error')

    sync_now.short_description = "Синхронизировать сейчас"


class DetailDescriptionInline(admin.StackedInline):
    model = DetailDescription
    extra = 1
    fieldsets = (
        ('Кыргызча', {
            'fields': ('blog', 'text_ky', 'image')
        }),
        ('Русский', {
            'fields': ('text_ru',)
        }),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [DetailDescriptionInline]
    fieldsets = (
        ('Кыргызча', {
            'fields': ('title_ky', 'image', )
        }),
        ('Русский', {
            'fields': ('title_ru', )
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title_ky', 'title_ru', 'created_at', 'youtube_link']
    search_fields = ['title_ky', 'title_ru', 'rich_ky', 'rich_ru', 'youtube_id']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'youtube_id']
    fieldsets = (
        ('Кыргызча', {
            'fields': ('title_ky', 'rich_ky', 'video_url', 'youtube_id')
        }),
        ('Русский', {
            'fields': ('title_ru', 'rich_ru')
        }),
    )

    def youtube_link(self, obj):
        if obj.youtube_id:
            return mark_safe(f'<a href="https://www.youtube.com/watch?v={obj.youtube_id}" target="_blank">YouTube</a>')
        return '-'

    youtube_link.short_description = 'YouTube'


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
