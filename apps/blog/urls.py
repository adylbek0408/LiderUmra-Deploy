from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, LessonViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'faq', FAQViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
