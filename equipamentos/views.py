from rest_framework import viewsets
from .models import Equipamento
from .serializers import EquipamentoSerializer


# Create your views here.
class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer