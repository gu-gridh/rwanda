from rest_framework_gis.serializers import GeoFeatureModelSerializer
from diana.abstract.serializers import DynamicDepthSerializer
from diana.utils import get_fields, DEFAULT_FIELDS
from .models import *

class BuildingSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Building
        fields = get_fields(Building, exclude=DEFAULT_FIELDS)
        geo_field = 'geometry'


class StreetSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Street
        fields = get_fields(Street, exclude=DEFAULT_FIELDS)
        geo_field = 'geometry'

class TIFFImageSerializer(DynamicDepthSerializer):

    class Meta:
        model = Image
        fields = get_fields(Image, exclude=DEFAULT_FIELDS)