from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from .models import Blog, Lesson, DetailDescription, FAQ, Photo
from .serializers import BlogSerializer, LessonSerializer, DetailDescriptionSerializer, FAQSerializer, PhotoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.prefetch_related('desc_blogs').all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title']

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title']

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class DetailDescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetailDescription.objects.select_related('blog').all()
    serializer_class = DetailDescriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blog', 'lesson']
    search_fields = ['text']

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class PhotoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.only('id', 'photo')
    serializer_class = PhotoSerializer
