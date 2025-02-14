from django.contrib import admin
from .models import (
    Ajy,
    CategoryPackage,
    TourDate,
    Package,
    Hotel,
    PackageDetail
)


@admin.register(Ajy)
class AjyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'bio')


@admin.register(CategoryPackage)
class CategoryPackageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ('start_tour', 'end_tour')
    list_filter = ('start_tour',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ajy', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active')
    raw_id_fields = ('category', 'ajy', 'tour_date')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stars')
    list_filter = ('city', 'stars')
    search_fields = ('name',)


@admin.register(PackageDetail)
class PackageDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_type', 'name')
    list_filter = ('detail_type',)
    search_fields = ('name',)
    fields = (
        'category',
        'detail_type',  # Тип информации первым
        'name',
        'rich',
        'image',
        'video_url'
    )
