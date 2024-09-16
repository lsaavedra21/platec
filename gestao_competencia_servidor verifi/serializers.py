from rest_framework import serializers
from .models import Consulta_competencia

class Consulta_competenciaSerializer(serializers.ModelSerializer):
    membro = serializers.CharField(source='membro.nome')
    competencia = serializers.CharField(source='competencia.nome')

    class Meta:
        model = Consulta_competencia
        fields = ('membro', 'competencia', 'nivel')