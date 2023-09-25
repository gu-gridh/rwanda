from rest_framework import viewsets
from . import models, serializers
from django.db.models import Q
from diana.abstract.views import DynamicDepthViewSet, GeoViewSet
from diana.abstract.models import get_fields, DEFAULT_FIELDS

from django_filters import rest_framework as filters


class PlaceFilter(filters.FilterSet):
    has_no_name = filters.BooleanFilter(field_name='names', lookup_expr='isnull')

    class Meta:
        model = models.PlaceOfInterest
        fields = {
            field: ['exact', 'in'] for field in get_fields(models.PlaceOfInterest, exclude=DEFAULT_FIELDS + ['geometry'])
            }

    

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

class PlaceOfInterestGeoViewSet(GeoViewSet):
    """
    retrieve:
    Returns a single place as a GeoJSON feature.

    list:
    Returns a list of places as a GeoJSON feature collection.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    

    queryset = models.PlaceOfInterest.objects.all()
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class PlacePeriodViewSet(GeoViewSet):
    """
    list:
    Returns a list of place by given period name.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    def get_queryset(self):
        period_name = self.request.GET["period_name"]
        periods = models.Name.objects.filter(period__text__iexact=period_name)
        queryset = models.PlaceOfInterest.objects.all().filter(id__in=list(periods.values_list('referent', flat=True)))

        return queryset
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True
