from .models import OcorrenciaPlatec
from .serializers import OcorrenciaPlatecSerializer
from rest_framework import viewsets


class OcorrenciasViewSet(viewsets.ModelViewSet):
    queryset = OcorrenciaPlatec.objects.all()
    serializer_class = OcorrenciaPlatecSerializer