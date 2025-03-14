from modeltranslation.translator import register, TranslationOptions
from .models import Ajy, CategoryPackage, Package, PackageDetail, Hotel


@register(Ajy)
class AjyTranslationOptions(TranslationOptions):
    fields = ('name', 'bio')


@register(CategoryPackage)
class CategoryPackageTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Package)
class PackageTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(PackageDetail)
class PackageDetailTranslationOptions(TranslationOptions):
    fields = ('name', 'rich')


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name', 'distance_to_mosque', 'accommodation', 'meals')

