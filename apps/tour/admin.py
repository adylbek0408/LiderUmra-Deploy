from django.contrib import admin
from .models import (
    Ajy,
    CategoryPackage,
    TourDate,
    Package,
    Hotel,
    PackageDetail,
    HotelImage, 
    PackageDetailImage,
)
from modeltranslation.admin import TranslationAdmin


@admin.register(Ajy)
class AjyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'bio')

    fieldsets = (
        ('Кыргызча', {
            'fields': ('name_ky', 'bio_ky', 'image')
        }),
        ('Русский', {
            'fields': ('name_ru', 'bio_ru')
        }),
    )


@admin.register(CategoryPackage)
class CategoryPackageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    fieldsets = (
        ('Кыргызча', {
            'fields': ('name_ky',)
        }),
        ('Русский', {
            'fields': ('name_ru',)
        }),
    )


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ('start_tour', 'end_tour')
    list_filter = ('start_tour',)

    fieldsets = (
        ('Даты тура', {
            'fields': ('start_tour', 'end_tour')
        }),
    )


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('place', 'name', 'category', 'ajy', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('place', 'category', 'is_active')

    fieldsets = (
        ('Кыргызча', {
            'fields': ('place', 'category', 'ajy', 'tour_date', 'name_ky', 'image', 'description_ky',
            'available_seats', 'is_active')
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru')
        }),
    )


class HotelImageInline(admin.StackedInline):
    model = HotelImage
    extra = 1
    fields = ['image', 'hotel']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Предпросмотр'



@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stars', 'distance_to_mosque')
    search_fields = ('name', 'city')
    list_filter = ('city', 'stars')
    inlines = [HotelImageInline]
    
    fieldsets = (
        ('Кыргызча', {
            'fields': ('category', 'name_ky', 'city', 'stars', 'distance_to_mosque_ky',
            'accommodation_ky', 'meals_ky', 'nights')
        }),
        ('Русский', {
            'fields': ('name_ru', 'distance_to_mosque_ru', 'accommodation_ru', 'meals_ru')
        }),
    )


class PackageDetailImageInline(admin.StackedInline):
    model = PackageDetailImage
    extra = 1
    fields = ['image', 'video_url']


@admin.register(PackageDetail)
class PackageDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'detail_type')
    search_fields = ('name', 'detail_type')
    list_filter = ('category', 'detail_type')
    inlines = [PackageDetailImageInline]

    fieldsets = (
        ('Кыргызча', {
            'fields': ('category', 'detail_type', 'name_ky', 'rich_ky')
        }),
        ('Русский', {
            'fields': ('name_ru', 'rich_ru')
        }),
    )
