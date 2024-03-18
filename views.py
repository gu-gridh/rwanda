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


class DocumentViewSet(DynamicDepthViewSet):
    """
    retrieve:
    Returns a single image instance.

    list:
    Returns a list of all the existing images in the database, paginated.

    count:
    Returns a count of the existing images after the application of any filter.
    """
    
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filterset_fields = get_fields(models.Document, exclude=DEFAULT_FIELDS + ['filename'])


class SearchPlacePeriodViewSet(GeoViewSet):
    """
    list:
    Returns a list of place by given period name.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    def get_queryset(self):
        period_name = self.request.GET["period_name"]
        periods = models.Name.objects.filter(period__text__icontains=period_name)
        queryset = models.PlaceOfInterest.objects.all().filter(id__in=list(periods.values_list('referent', flat=True)))

        return queryset
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceTypeViewSet(GeoViewSet):
    """
    list:
    Returns a list of place by given type text.

    count:
    Returns a count of the existing places after the application of any filter.
    """

    def get_queryset(self):
        type_text = self.request.GET["text"]
        queryset = models.PlaceOfInterest.objects.filter(type__text__icontains=type_text)
        return queryset
    
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceViewSet(GeoViewSet):
    """
    list:
    Returns a list of place that has been selected at least for one image.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    images = models.Image.objects.all()
    informant = models.Text.objects.all()
    queryset = models.PlaceOfInterest.objects.filter(Q(id__in=list(images.values_list('place_of_interest', flat=True))) 
                                                     | Q(id__in=list(informant.values_list('place_of_interest', flat=True)))
                                                     )
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceInformantViewSet(GeoViewSet):
    """
    list:
    Returns a list of place there is any informant for them.

    count:
    Returns a count of the existing places after the application of any filter.
    """

    def get_queryset(self):
        info = self.request.GET["text"]
        informant = models.Text.objects.filter(informants__custom_id__icontains=info)
        queryset = models.PlaceOfInterest.objects.all().filter(id__in=list(informant.values_list('place_of_interest', flat=True)))
        return queryset
      
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceTextViewSet(GeoViewSet):
    """
    list:
    Returns a list of place that has been selected at least for one image.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    informant = models.Text.objects.all()
    queryset = models.PlaceOfInterest.objects.filter(id__in=list(informant.values_list('place_of_interest', flat=True)))
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceImageViewSet(GeoViewSet):
    """
    list:
    Returns a list of place that has been selected at least for one image.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    images = models.Image.objects.all()
    queryset = models.PlaceOfInterest.objects.filter(id__in=list(images.values_list('place_of_interest', flat=True)))
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceDocumentViewSet(GeoViewSet):
    """
    list:
    Returns a list of place that has been selected at least for one image.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    documents = models.Document.objects.all()
    queryset = models.PlaceOfInterest.objects.filter(id__in=list(documents.values_list('place_of_interest', flat=True)))
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True


class SearchPlaceLanguageViewSet(GeoViewSet):
    """
    list:
    Returns a list of place that has been selected at least for one image.

    count:
    Returns a count of the existing places after the application of any filter.
    """
    

    def get_queryset(self):
        text = self.request.GET["q"]
        name = models.Name.objects.filter(Q(languages__name__exact=text) | Q(languages__abbreviation__exact=text))
        queryset = models.PlaceOfInterest.objects.filter(id__in=list(name.values_list('referent', flat=True))) 
        return queryset
                                            
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True

class AdvanceSearcViewSet(GeoViewSet):
    serializer_class = serializers.PlaceOfInterestSerializer
    filterset_class = PlaceFilter
    search_fields = ['names__text']

    def dispatch(self, request, *args, **kwargs):
        model_name = request.GET.get('source')
        self.model_type = None
        if model_name == 'image':
            self.model_type = models.Image
        elif model_name == 'document':
            self.model_type = models.Document
        elif model_name == 'text':
            self.model_type = models.Text

        return super(AdvanceSearcViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.PlaceOfInterest.objects.all()
        model_type = self.request.query_params.get('source')
        language = self.request.query_params.get('language')
        street_type = self.request.query_params.get('place_type')
        time = self.request.query_params.get('period')
        informant = self.request.query_params.get('informant')

        if model_type:
            sources = self.model_type.objects.all()
            if language:
                name_filter = Q(languages__name__exact=language) | Q(languages__abbreviation__exact=language)
                queryset = queryset.filter(id__in=models.Name.objects.filter(name_filter).values_list('referent', flat=True))
            if street_type:
                queryset = queryset.filter(type__text__icontains=street_type)
            if time:
                period_filter = Q(period__text__icontains=time)
                queryset = queryset.filter(id__in=models.Name.objects.filter(period_filter).values_list('referent', flat=True))
            if informant:
                informant_filter = Q(informants__custom_id__icontains=informant)
                queryset = queryset.filter(id__in=models.Text.objects.filter(informant_filter).values_list('place_of_interest', flat=True))
                
            queryset = queryset.filter(id__in=list(sources.values_list('place_of_interest', flat=True)))
        else:
            if language:
                name_filter = Q(languages__name__exact=language) | Q(languages__abbreviation__exact=language)
                queryset = queryset.filter(id__in=models.Name.objects.filter(name_filter).values_list('referent', flat=True))
            if street_type:
                queryset = queryset.filter(type__text__icontains=street_type)
            if time:
                period_filter = Q(period__text__icontains=time)
                queryset = queryset.filter(id__in=models.Name.objects.filter(period_filter).values_list('referent', flat=True))
            if informant:
                informant_filter = Q(informants__custom_id__icontains=informant)
                queryset = queryset.filter(id__in=models.Text.objects.filter(informant_filter).values_list('place_of_interest', flat=True))


        return queryset.distinct()

    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True