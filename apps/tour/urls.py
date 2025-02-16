from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AjyViewSet, CategoryPackageViewSet,
    TourDateViewSet, PackageViewSet, HotelViewSet, PackageDetailViewSet
)

router = DefaultRouter()
router.register('ajy', AjyViewSet, basename='ajy')
router.register('categories', CategoryPackageViewSet, basename='category')
router.register('tour-dates', TourDateViewSet, basename='tour-date')
router.register('packages', PackageViewSet, basename='package')
router.register('hotels', HotelViewSet, basename='hotel')
router.register('package-details', PackageDetailViewSet, basename='package-detail')
urlpatterns = [
    path('', include(router.urls)),
]
