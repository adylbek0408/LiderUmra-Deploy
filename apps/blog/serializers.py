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
        fields = ['id', 'title', 'rich', 'created_at', 'image', 'desc_blogs']


class LessonSerializer(serializers.ModelSerializer):
    youtube_embed_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'rich', 'created_at', 'video_url', 'youtube_id', 'youtube_embed_url', 'thumbnail_url']

    def get_youtube_embed_url(self, obj):
        if obj.youtube_id:
            return f"https://www.youtube.com/embed/{obj.youtube_id}"
        return None

    def get_thumbnail_url(self, obj):
        if obj.youtube_id:
            return f"https://img.youtube.com/vi/{obj.youtube_id}/maxresdefault.jpg"
        return None


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo']
