from rest_framework import viewsets
from . import models, serializers

from diana.abstract.views import DynamicDepthViewSet, GeoViewSet
from diana.abstract.models import get_fields, DEFAULT_FIELDS

class IIIFImageViewSet(DynamicDepthViewSet):
    """
    retrieve:
    Returns a single image instance.

    list:
    Returns a list of all the existing images in the database, paginated.

    count:
    Returns a count of the existing images after the application of any filter.
    """
    
    queryset = models.Image.objects.all()
    serializer_class = serializers.TIFFImageSerializer
    filterset_fields = get_fields(models.Image, exclude=DEFAULT_FIELDS + ['iiif_file', 'file'])

# Create your views here.
class BuildingGeoViewSet(GeoViewSet):

    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    filterset_fields = get_fields(models.Building, exclude=DEFAULT_FIELDS + ['geometry'])
    bbox_filter_field = 'geometry'

class StreetGeoViewSet(GeoViewSet):

    queryset = models.Street.objects.all()
    serializer_class = serializers.StreetSerializer
    filterset_fields = get_fields(models.Street, exclude=DEFAULT_FIELDS + ['geometry'])
    bbox_filter_field = 'geometry'