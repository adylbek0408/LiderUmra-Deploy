from rest_framework import serializers
from .models import Blog, Lesson, DetailDescription, FAQ, Photo


class DetailDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailDescription
        fields = ['id', 'text', 'image']


class BlogSerializer(serializers.ModelSerializer):
    desc_blogs = DetailDescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'name', 'rich', 'created_at', 'image', 'desc_blogs']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'rich', 'created_at', 'video_url']


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo']
