# Generated by Django 5.1.6 on 2025-02-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_manager_branch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manager',
            options={'verbose_name': 'Менеджер', 'verbose_name_plural': 'Менеджеры'},
        ),
        migrations.RemoveField(
            model_name='manager',
            name='user',
        ),
        migrations.AddField(
            model_name='manager',
            name='fio',
            field=models.CharField(default=1, max_length=155, verbose_name='ФИО менеджера'),
            preserve_default=False,
        ),
    ]
