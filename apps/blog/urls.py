from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, LessonViewSet, FAQViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'faq', FAQViewSet)
router.register(r'photos', PhotoViewSet, basename='photo')


urlpatterns = [
    path('', include(router.urls)),
]
