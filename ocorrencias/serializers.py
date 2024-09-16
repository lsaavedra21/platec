from rest_framework import serializers
from equipamentos.serializers import EquipamentoSerializer
from .models import OcorrenciaPlatec


class OcorrenciaPlatecSerializer(serializers.ModelSerializer):
    equipamento = EquipamentoSerializer(read_only=True)
    class Meta:
        model = OcorrenciaPlatec
        fields = '__all__'
