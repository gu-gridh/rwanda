from django.urls import path, include
from rest_framework import routers
from . import views
import diana.utils as utils


router = routers.DefaultRouter()
endpoint = utils.build_app_endpoint("rwanda")
documentation = utils.build_app_api_documentation("rwanda", endpoint)

router.register(rf'{endpoint}/geojson/place', views.PlaceOfInterestGeoViewSet, basename='places as geojson')
router.register(rf'{endpoint}/image', views.IIIFImageViewSet, basename='image')
router.register(rf'{endpoint}/document', views.DocumentViewSet, basename='document')

# Search options
router.register(rf'{endpoint}/search/period', views.SearchPlacePeriodViewSet, basename='Featch based on period time')
router.register(rf'{endpoint}/search/type', views.SearchPlaceTypeViewSet, basename='Featch based on type')
router.register(rf'{endpoint}/search/informant', views.SearchPlaceInformantViewSet, basename='Filter for images')
router.register(rf'{endpoint}/search/text', views.SearchPlaceTextViewSet, basename='Featch based on text')
router.register(rf'{endpoint}/search/image', views.SearchPlaceImageViewSet, basename='Featch based on images')
router.register(rf'{endpoint}/search/document', views.SearchPlaceDocumentViewSet, basename='Featch based on document')
router.register(rf'{endpoint}/search/language', views.SearchPlaceLanguageViewSet, basename='Featch based on language')
router.register(rf'{endpoint}/search', views.SearchPlaceViewSet, basename='Featch if there is image or text for this place')
router.register(rf'{endpoint}/advance/search', views.AdvanceSearcViewSet, basename='Featch if there is image or text for this place')


urlpatterns = [
    path('', include(router.urls)),

    # Automatically generated views
    *utils.get_model_urls('rwanda', endpoint, 
        exclude=['placeofinterest', 'image', 'document',
            'image_authors', 'image_informants', 
            'name_languages', 'name_informants', 
            'text_authors', 'text_informants']),
    *documentation

]