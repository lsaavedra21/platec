from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import OcorrenciasViewSet

router = DefaultRouter()
router.register(r'ocorrencias', OcorrenciasViewSet, 'ocorrencias' )

urlpatterns = [
    path("", include(router.urls))
]
