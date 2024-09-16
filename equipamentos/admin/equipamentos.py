from equipamentos.models import Planta, Departamento, Area, Linha, Zona, Posto

from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import admin
from .admins_filter.filters import *
from platecplatform.services.export_csv.export_csv import ExportCsvMixin

admin.site.register(Departamento)
admin.site.register(Area)
admin.site.register(Linha)
admin.site.register(Zona)
admin.site.register(Posto)
admin.site.register(Planta)

@admin.register(Equipamento)
class EquipmentAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['denominacao', 'denominacao_linha', 'codigo_sap', 'area__codigo', 'area__traducao', 'observacoes']
    raw_id_fields = ['area','linha', 'zona', 'posto', 'equip_superior'] # Pop up de busca
    list_display = ('denominacao', 'denominacao_linha', 'sala', 'planta', 'departamento', 'area', 'linha', 'zona', 'posto') # Header
    list_filter = [PlantFilter, DepartmentFilter, AreaFilter, LinhaFilter, ZonaFilter, PostoFilter]
    actions = ["export_csv"] # Botão ação

