from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название:', null=True, blank=True)
    rich = RichTextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(verbose_name='Картинка:', null=True, blank=True)
    video_url = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)

    class Meta:
        abstract = True


class Ajy(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО:')
    bio = RichTextField(verbose_name='Биография:')
    image = models.ImageField(verbose_name='Фотография:')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ажы'
        verbose_name_plural = 'Ажы'


class CategoryPackage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название:')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория пакета'
        verbose_name_plural = 'Категории пакетов'


class TourDate(models.Model):
    start_tour = models.DateTimeField(verbose_name='Дата начало:')
    end_tour = models.DateTimeField(verbose_name='Дата конец:')

    def __str__(self):
        return f"{self.start_tour.strftime('%d.%m.%Y')} - {self.end_tour.strftime('%d.%m.%Y')}"


class Package(models.Model):
    category = models.ForeignKey(CategoryPackage, on_delete=models.PROTECT, related_name='packages', verbose_name='Категория')
    ajy = models.ForeignKey(Ajy, on_delete=models.PROTECT, related_name='packages', verbose_name='Ажы башчы')
    tour_date = models.ForeignKey(TourDate, on_delete=models.PROTECT, related_name='packages', verbose_name='Дата тура')
    name = models.CharField(max_length=155, verbose_name='Название:')
    image = models.ImageField(upload_to='packages/images/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание:', null=True, blank=True)
    available_seats = models.PositiveIntegerField(
        verbose_name='Макс. мест',
        default=0
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def clean(self):
        if self.available_seats < 0:
            raise ValidationError("Available seats cannot be negative")

    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'

    def __str__(self):
        return f"{self.name} ({self.tour_date})"


class PackageDetail(BaseModel):
    category = models.ForeignKey(CategoryPackage, on_delete=models.PROTECT, related_name='package_details', verbose_name='Категория')

    FOOD_INFO = 'FoodInfo'
    REQUIREMENTS = 'Requirements'
    RESTRICTIONS = 'Restrictions'
    PLACES_TO_VISIT = 'PlacesToVisit'
    YOU_GET = 'YouGet'
    
    DETAIL_TYPES = [
        (FOOD_INFO, 'Информация о питании'),
        (REQUIREMENTS, 'Рекомендуется'),
        (RESTRICTIONS, 'Не рекомендуется'),
        (PLACES_TO_VISIT, 'Места для посещения'),
        (YOU_GET, 'Что вы получите от нас'),
    ]
    detail_type = models.CharField(max_length=100, choices=DETAIL_TYPES, verbose_name='Тип информации:')

    class Meta:
        verbose_name = 'Детали пакета'
        verbose_name_plural = 'Детали пакетов'
        ordering = ['detail_type']

    def __str__(self):
        return f"{self.get_detail_type_display()}"


class Hotel(models.Model):
    category = models.ForeignKey(CategoryPackage, on_delete=models.PROTECT, related_name='package_hotels', verbose_name='Категория')

    CITY_CHOICES = [
        ('mecca', 'Мекка'),
        ('medina', 'Медина'),
    ]
    
    STAR_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название:')
    city = models.CharField(max_length=10, choices=CITY_CHOICES, verbose_name='Город:')
    stars = models.IntegerField(choices=STAR_CHOICES, default=0, verbose_name='Звёздность отеля')
    distance_to_mosque = models.CharField(max_length=100, verbose_name='Расстояние до мечети:', help_text='Например: 300 м')
    accommodation = models.CharField(max_length=100, verbose_name='Размещение:', help_text='Например: Четырехместное')
    meals = models.CharField(
        max_length=200,
        verbose_name='Питание:',
        help_text='Например: Завтрак и ужин шведский стол',
        null=True,
        blank=True
    )
    nights = models.PositiveIntegerField(
        verbose_name='Количество ночей:',
        null=True,
        blank=True,
        help_text='Необязательное поле'
    )

    def clean(self):
        if self.stars < 1 or self.stars > 5:
            raise ValidationError("Stars must be between 1 and 5")

    def __str__(self):
        return f"{self.name} - {self.get_city_display()} {self.get_stars_display()}"

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        indexes = [
            models.Index(fields=['city', 'stars']),
        ]

    
class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images', verbose_name='Отель')
    image = models.ImageField(upload_to='hotels/images/', verbose_name='Изображение')

    def __str__(self):
            return f"{self.hotel.name} - {self.image.name}"

    class Meta:
            verbose_name = 'Изображение отеля'
            verbose_name_plural = 'Изображения отелей'

