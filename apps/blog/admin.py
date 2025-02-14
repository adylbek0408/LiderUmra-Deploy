from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Lesson, DetailDescription, FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)  # Добавьте запятую, чтобы сделать кортеж
    search_fields = ("question", "answer")


class DetailDescriptionInline(admin.TabularInline):
    model = DetailDescription
    extra = 1
    fields = ['text', 'image']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'image']
    list_filter = ['created_at']
    exclude = ['video_url'] 
    inlines = [DetailDescriptionInline]



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']  # показываем в списке
    fields = ['name', 'video_url', 'rich']  # теперь можем включить created_at
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(DetailDescription)
class DetailDescriptionAdmin(admin.ModelAdmin):
    list_display = ['blog', 'text']
    fields = ['blog', 'text', 'image']
    list_filter = ['blog']
    search_fields = ['text']
    raw_id_fields = ['blog']