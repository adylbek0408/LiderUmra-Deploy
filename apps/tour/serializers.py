from rest_framework import serializers
from .models import Ajy, CategoryPackage, TourDate, Package, Hotel, PackageDetail, HotelImage, PackageDetailImage


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


class PackageDetailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageDetailImage
        fields = ['id', 'image', 'video_url']


class PackageDetailSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    detail_type_display = serializers.CharField(source='get_detail_type_display', read_only=True)
    package_detail_images = PackageDetailImageSerializer(many=True, read_only=True)


    class Meta:
        model = PackageDetail
        fields = ['id', 'category', 'name', 'rich', 'detail_type', 'detail_type_display',
         'package_detail_images']


class PackageSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    ajy = AjySerializer()
    tour_date = TourDateSerializer()

    class Meta:
        model = Package
        fields = [
            'id', 'place', 'category', 'ajy', 'tour_date',
            'name', 'image', 'description',
            'available_seats', 'is_active'
        ]
        depth = 1


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'video_url', 'hotel']


class HotelSerializer(serializers.ModelSerializer):
    category = CategoryPackageSerializer()
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    stars_display = serializers.CharField(source='get_stars_display', read_only=True)
    hotel_images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'category', 'name', 'city', 'city_display',
            'stars', 'stars_display', 'distance_to_mosque',
            'accommodation', 'meals', 'nights', 'hotel_images',
            'addres_url'
        ]



