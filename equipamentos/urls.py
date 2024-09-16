from django.urls import path, include
from .views import EquipamentoViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'equipamentos', EquipamentoViewSet, 'equipamentos' )

urlpatterns = [
    path("", include(router.urls))
]
