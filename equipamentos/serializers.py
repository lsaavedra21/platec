from rest_framework import serializers
from .models import Area, Departamento, Planta


class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class EquipamentoSerializer(serializers.Serializer):
    codigo_sap = serializers.IntegerField(read_only=True)
    denominacao = serializers.CharField(read_only=True)
    denominacao_linha = serializers.CharField(read_only=True)
    local = serializers.CharField(read_only=True)
    planta = PlantaSerializer()
    departamento = DepartamentoSerializer()
    area = AreaSerializer()
    

  