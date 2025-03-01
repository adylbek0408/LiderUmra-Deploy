from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from apps.tour.models import Package


class Manager(models.Model):
    fio = models.CharField( 
        max_length=155,
        verbose_name='ФИО менеджера'
    )
    telegram_id = models.CharField(max_length=100, 
                                 unique=True, 
                                 verbose_name='Telegram ID')
    phone = PhoneNumberField(verbose_name='Номер телефона', 
                           region='KG',
                           help_text='Пример: +996555123456')
    branch = models.CharField(
        max_length=100,
        choices=Package.PLACE,
        verbose_name='Филиал',
        default=Package.BISHKEK  # Optional default
    )

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def get_display_name(self):
        return self.fio  


class Client(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('no_answer', 'Не дозвон'),
        ('thinking', 'Думает'),
        ('rejected', 'Отклонено'),
        ('success', 'Успешно'),
    ]

    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    phone = PhoneNumberField(verbose_name='Номер телефона',
                           region='KG',
                           help_text='Пример: +996555123456')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    package = models.ForeignKey(Package, 
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='clients',
                              verbose_name='Выбранный пакет')
    manager = models.ForeignKey(Manager,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='assigned_clients',
                              verbose_name='Менеджер')
    status = models.CharField(max_length=20,
                            choices=STATUS_CHOICES,
                            default='new',
                            db_index=True,
                            verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                    verbose_name='Дата обновления')

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['manager', 'status']),
        ]

    def __str__(self):
        return self.full_name
        