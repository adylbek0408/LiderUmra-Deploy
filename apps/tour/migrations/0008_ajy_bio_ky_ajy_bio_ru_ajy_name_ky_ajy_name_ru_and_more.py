# Generated by Django 5.1.6 on 2025-02-19 14:22

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0007_hotelimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ajy',
            name='bio_ky',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Биография:'),
        ),
        migrations.AddField(
            model_name='ajy',
            name='bio_ru',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Биография:'),
        ),
        migrations.AddField(
            model_name='ajy',
            name='name_ky',
            field=models.CharField(max_length=100, null=True, verbose_name='ФИО:'),
        ),
        migrations.AddField(
            model_name='ajy',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='ФИО:'),
        ),
        migrations.AddField(
            model_name='categorypackage',
            name='name_ky',
            field=models.CharField(max_length=100, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='categorypackage',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='accommodation_ky',
            field=models.CharField(help_text='Например: Четырехместное', max_length=100, null=True, verbose_name='Размещение:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='accommodation_ru',
            field=models.CharField(help_text='Например: Четырехместное', max_length=100, null=True, verbose_name='Размещение:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='distance_to_mosque_ky',
            field=models.CharField(help_text='Например: 300 м', max_length=100, null=True, verbose_name='Расстояние до мечети:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='distance_to_mosque_ru',
            field=models.CharField(help_text='Например: 300 м', max_length=100, null=True, verbose_name='Расстояние до мечети:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='meals_ky',
            field=models.CharField(blank=True, help_text='Например: Завтрак и ужин шведский стол', max_length=200, null=True, verbose_name='Питание:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='meals_ru',
            field=models.CharField(blank=True, help_text='Например: Завтрак и ужин шведский стол', max_length=200, null=True, verbose_name='Питание:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='name_ky',
            field=models.CharField(max_length=100, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='package',
            name='description_ky',
            field=models.TextField(blank=True, null=True, verbose_name='Описание:'),
        ),
        migrations.AddField(
            model_name='package',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание:'),
        ),
        migrations.AddField(
            model_name='package',
            name='name_ky',
            field=models.CharField(max_length=155, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='package',
            name='name_ru',
            field=models.CharField(max_length=155, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='packagedetail',
            name='name_ky',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='packagedetail',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название:'),
        ),
        migrations.AddField(
            model_name='packagedetail',
            name='rich_ky',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='packagedetail',
            name='rich_ru',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
