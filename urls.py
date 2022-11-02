from django.urls import path, include
from rest_framework import routers
# from . import views
import diana.utils as utils

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Automatically generated views
    *utils.get_model_urls('rwanda', 'api', exclude=[]),
]