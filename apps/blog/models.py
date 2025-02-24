from django.db import models
from ckeditor.fields import RichTextField
from apps.tour.models import BaseModel


class Blog(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Название:')
    rich = RichTextField(verbose_name='Описание:', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания:', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class Lesson(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Название:')
    rich = RichTextField(verbose_name='Описание:', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания:', auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class DetailDescription(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="desc_blogs", null=True, blank=True)
    text = RichTextField(verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='packages/', verbose_name='Изображение', null=True, blank=True)

    class Meta:
        verbose_name = "Полная информация"
        verbose_name_plural = "Полная информация"


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")


    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

    def __str__(self):
        return self.question



class Photo(models.Model):
    photo = models.ImageField(verbose_name='Картинка')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотогалерея'

