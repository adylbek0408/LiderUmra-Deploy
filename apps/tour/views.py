from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Ajy, CategoryPackage, TourDate, Package, Hotel, PackageDetail, HotelImage, PackageDetailImage
from .serializers import (
    AjySerializer, CategoryPackageSerializer,
    TourDateSerializer, PackageSerializer, 
    HotelSerializer, PackageDetailSerializer, 
    HotelImageSerializer, PackageDetailImageSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from UMRA.utils import with_language


class AjyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ajy.objects.all()
    serializer_class = AjySerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class CategoryPackageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CategoryPackage.objects.all()
    serializer_class = CategoryPackageSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']
    @action(detail=False, methods=['get'])
    def language_info(self, request):
        """
        Возвращает информацию о текущем языке из заголовка Accept-Language
        """
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class TourDateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TourDate.objects.all().order_by('start_tour')
    serializer_class = TourDateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_tour', 'end_tour']
    @action(detail=False, methods=['get'])
    def language_info(self, request):
        """
        Возвращает информацию о текущем языке из заголовка Accept-Language
        """
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class PackageFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='tour_date__start_tour', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='tour_date__end_tour', lookup_expr='lte')
    min_seats = filters.NumberFilter(field_name='available_seats', lookup_expr='gte')

    class Meta:
        model = Package
        fields = ['category', 'ajy', 'is_active']


class PackageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter

    def get_queryset(self):
        return Package.objects.select_related(
            'category', 'ajy', 'tour_date'
        ).filter(
            is_active=True
        ).order_by('tour_date__start_tour')

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class PackageDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PackageDetail.objects.select_related('category').prefetch_related('package_detail_images').only(
        'id', 'category', 'detail_type'
    )
    serializer_class = PackageDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['detail_type']

    def list(self, request, *args, **kwargs):
        detail_type = request.query_params.get('q')
        queryset = self.get_queryset()

        if detail_type:
            queryset = queryset.filter(detail_type=detail_type)
            if not queryset.exists():
                raise NotFound("Детали с указанным типом не найдены")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })


class PackageDetailImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PackageDetailImage.objects.select_related('package_detail').only('id', 'package_detail', 'image',
                                                                                'video_url')
    serializer_class = PackageDetailImageSerializer


class HotelViewSet(mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin, 
                  viewsets.GenericViewSet):
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'stars', 'category']
    search_fields = ['name']

    def get_queryset(self):
        return Hotel.objects.select_related(
            'category'
        ).prefetch_related(
            'hotel_images'
        ).all()

    @action(detail=False, methods=['get'])
    def language_info(self, request):
        from django.utils import translation
        current_lang = translation.get_language()
        return Response({
            "current_language": current_lang,
            "message": "Используется язык из заголовка Accept-Language"
        })
