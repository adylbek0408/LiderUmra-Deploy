# Generated by Django 5.1.6 on 2025-02-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_remove_packagedetail_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagedetail',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на видео'),
        ),
    ]
