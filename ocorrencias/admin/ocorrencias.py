from django.contrib import admin
from ..models import OcorrenciaPlatec

from platecplatform.services import ExportCsvMixin

@admin.register(OcorrenciaPlatec)
class EquipmentBreakdownReportAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['sintoma', 'turno', 'get_eqps', 'horario_quebra', 'veiculos_perdidos', 'tempo_eqp_parado'] # Header
    list_filter = ['horario_quebra', 'equipamento__planta'] # Filtro lateral direita
    search_fields = ['sintoma', 'causa', 'remedio', 'equipamento__denominacao', 'equipamento__codigo_sap']
    raw_id_fields = ['equipamento'] # Pop up de busca
    actions = ["export_csv"] # Botão ação
    fields = ['equipamento', 'sintoma', 'causa', 'remedio', ('turno', 'categoria'), ('mbr','marcha_degradada',),
    ('veiculos_perdidos', 'tempo_eqp_parado', 'perdas_rgu'), ('horario_quebra', 'horario_chamado'),] # Campo dentro do forms

    @admin.display(description="Equipamento")
    def get_eqps(self, obj):
        return obj.equipamento.denominacao

