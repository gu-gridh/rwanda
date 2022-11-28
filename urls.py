from django.urls import path, include
from rest_framework import routers
from . import views
import diana.utils as utils


router = routers.DefaultRouter()
endpoint = utils.build_app_endpoint("rwanda")
documentation = utils.build_app_api_documentation("rwanda", endpoint)

router.register(rf'{endpoint}/geojson/place', views.PlaceOfInterestGeoViewSet, basename='places as geojson')
router.register(rf'{endpoint}/image', views.IIIFImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),

    # Automatically generated views
    *utils.get_model_urls('rwanda', endpoint, 
        exclude=['placeofinterest', 'image', 
            'image_authors', 'image_informants', 
            'name_languages', 'name_informants', 
            'text_authors', 'text_informants']),
    *documentation

]