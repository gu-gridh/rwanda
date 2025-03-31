from rest_framework_gis.serializers import GeoFeatureModelSerializer
from diana.abstract.serializers import DynamicDepthSerializer
from diana.utils import get_fields, DEFAULT_FIELDS
from .models import *

class PlaceOfInterestSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PlaceOfInterest
        fields = ['names', 'id']+get_fields(PlaceOfInterest, exclude=DEFAULT_FIELDS+['geometry']) 
        geo_field = 'geometry'
        depth = 2

class TIFFImageSerializer(DynamicDepthSerializer):

    class Meta:
        model = Image
        fields = ['id']+get_fields(Image, exclude=DEFAULT_FIELDS)


class DocumentSerializer(DynamicDepthSerializer):

    class Meta:
        model = Document
        fields = ['id']+get_fields(Document, exclude=DEFAULT_FIELDS)



class TranscriptionSerializer(DynamicDepthSerializer):

    class Meta:
        model = Transcription
        fields =  ['id']+get_fields(Transcription, exclude=DEFAULT_FIELDS)