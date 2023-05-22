from rest_framework_gis.serializers import GeoFeatureModelSerializer
from diana.abstract.serializers import DynamicDepthSerializer
from diana.utils import get_fields, DEFAULT_FIELDS
from .models import *

class PlaceOfInterestSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PlaceOfInterest
        fields = ['id'] + get_fields(PlaceOfInterest, exclude=DEFAULT_FIELDS) 
        geo_field = 'geometry'

class TIFFImageSerializer(DynamicDepthSerializer):

    class Meta:
        model = Image
        fields = ['id'] + get_fields(Image, exclude=DEFAULT_FIELDS)