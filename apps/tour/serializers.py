from rest_framework import serializers
from .models import Ajy, CategoryPackage, TourDate, Package, Hotel, PackageDetail


class AjySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ajy
        fields = ['id', 'name', 'bio', 'image']


class CategoryPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPackage
        fields = ['id', 'name']


class TourDateSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = TourDate
        fields = ['id', 'start_tour', 'end_tour', 'duration']

    def get_duration(self, obj):
        return (obj.end_tour - obj.start_tour).days


class PackageSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    ajy = AjySerializer()
    tour_date = TourDateSerializer()

    class Meta:
        model = Package
        fields = [
            'id', 'category', 'ajy', 'tour_date',
            'name', 'image', 'description',
            'available_seats', 'is_active'
        ]
        depth = 1


class HotelSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    stars_display = serializers.CharField(source='get_stars_display', read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'category', 'name', 'city', 'city_display',
            'stars', 'stars_display', 'distance_to_mosque',
            'accommodation', 'meals', 'nights'
        ]


class PackageDetailSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    detail_type_display = serializers.CharField(source='get_detail_type_display', read_only=True)

    class Meta:
        model = PackageDetail
        fields = ['id', 'category', 'name', 'rich', 'image', 'video_url', 'detail_type', 'detail_type_display']

