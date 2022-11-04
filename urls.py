from django.urls import path, include
from rest_framework import routers
from . import views
import diana.utils as utils
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

router = routers.DefaultRouter()

router.register(r'api/geojson/street', views.StreetGeoViewSet, basename='streets as geojson')
router.register(r'api/geojson/building', views.BuildingGeoViewSet, basename='buildings as geojson')
router.register(r'api/image', views.IIIFImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),

    # Automatically generated views
    *utils.get_model_urls('rwanda', 'api', exclude=['street', 'building', 'image']),

    path('api/schema/', 
        get_schema_view(
            title="Rwanda",
            description="Schema for the Rwanda API at the Centre for Digital Humanities",
            version="1.0.0",
            urlconf="apps.rwanda.urls"
        ), 
        name='openapi-schema'
    ),
    path('api/documentation/', 
        TemplateView.as_view(
            template_name='templates/redoc.html',
            extra_context={'schema_url':'openapi-schema'}
        ), 
        name='redoc-ui'),
]