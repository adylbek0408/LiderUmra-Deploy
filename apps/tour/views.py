from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Ajy, CategoryPackage, TourDate, Package, Hotel, PackageDetail
from .serializers import (
    AjySerializer, CategoryPackageSerializer,
    TourDateSerializer, PackageSerializer, 
    HotelSerializer, PackageDetailSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class AjyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ajy.objects.all()
    serializer_class = AjySerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']


class CategoryPackageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CategoryPackage.objects.all()
    serializer_class = CategoryPackageSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['name']


class TourDateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TourDate.objects.all().order_by('start_tour')
    serializer_class = TourDateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_tour', 'end_tour']


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


class PackageDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PackageDetail.objects.all()
    serializer_class = PackageDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['detail_type']

    def list(self, request, *args, **kwargs):
        detail_type = self.request.query_params.get('q', None)
        if detail_type:
            queryset = PackageDetail.objects.filter(detail_type=detail_type)
            if queryset.exists():
                serializer = PackageDetailSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise NotFound("Детали с указанным типом не найдены")
        else:
            return super().list(request, *args, **kwargs)


class HotelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'stars']
    search_fields = ['name']
