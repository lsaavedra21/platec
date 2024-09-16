from typing import List
from django.contrib import admin
from django.db.models import Q
from equipamentos.models import Departamento

from ...models import Equipamento, Planta
import ipdb

def get_selected_value(self):
    """Essa função faz isso por causa do Código e Tradução
    Por que vem 'VU01 - Veiculos Utilitarios' e não apenas 'VU01' para o filtro
    """
    selected_value = self.value()
    if selected_value:
        return selected_value.split(' - ')[0]

    elif not selected_value:
        return None 

def get_value_in_url(request, paramstr):
    res = request.GET.get(paramstr)
    if res:
        return res.split(' - ')[0]

    elif res is None:
        return None


class PlantFilter(admin.SimpleListFilter):
    title, parameter_name, zones = 'Planta', 'planta', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        return tuple(((p, p) for p in Planta.objects.all()))
    
    def queryset(self, request, queryset):
        selected = get_selected_value(self)
        if selected is None: return queryset.all()
        return queryset.filter(planta__codigo=selected)



        

class DepartmentFilter(admin.SimpleListFilter):

    title, parameter_name, choices_v = 'Departamento', 'departamento', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        self.choices_v.clear(); planta = get_value_in_url(request, 'planta')
        if planta: 
            [self.choices_v.add(code) for code in 
            Equipamento.objects.filter(planta__codigo=planta)
            .values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]  
        
        if planta is None: 
            [self.choices_v.add(code) for code in Equipamento.objects.all().values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]  
        return ((x, x) for x in self.choices_v)

    def queryset(self, request, queryset):
        planta, depart = get_value_in_url(request, 'planta'), get_selected_value(self)
        
        if planta is None and depart: 
            queryset = queryset.filter(departamento__codigo=depart)
        
        if planta and depart and depart in self.choices_v: 
            queryset = queryset.filter(planta__codigo=planta, departamento__codigo=depart)
        
        return queryset


class AreaFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title, parameter_name, choices_v = 'Area', 'area', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        self.choices_v.clear(); 
        departamento = get_value_in_url(request, 'departamento')
        planta = get_value_in_url(request, 'planta')

        if planta and departamento:
            [self.choices_v.add(code) for code in 
            Equipamento.objects.filter(
                departamento__codigo=departamento, planta__codigo=planta
            ).values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]  
        
        if planta is None and departamento: 
            [self.choices_v.add(code) for code in
            Equipamento.objects.filter(
                departamento__codigo=departamento
            ).values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]  
        return ((x, x) for x in self.choices_v)
   
    def queryset(self, request, queryset):
        departamento, area = get_value_in_url(request, 'departamento'), get_selected_value(self)

        if departamento is None: 
            queryset = queryset.all()
        
        if departamento and area and area in self.choices_v:
            queryset = queryset.filter(
                departamento__codigo=departamento, area__codigo=area
            )
        return queryset


class LinhaFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title, parameter_name, choices_v = 'Linha', 'linha', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        self.choices_v.clear(); 
        planta = get_value_in_url(request, 'planta')
        area = get_value_in_url(request, 'area')
        departamento = get_value_in_url(request, 'departamento')

        if planta: query = Q( 
            ( 'planta__codigo', planta ), ('area__codigo', area), ('departamento__codigo', departamento))

        if planta is None: query = Q( 
            ('departamento__codigo', departamento), ( 'area__codigo', area ) )

        if area and departamento:
            [self.choices_v.add(code) for code in Equipamento.objects.filter(query).values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]    
        return ((x, x) for x in self.choices_v)
   
    def queryset(self, request, queryset):
        area, linha,  = get_value_in_url(request, 'area'), get_selected_value(self)
        if area is None:
            queryset = queryset.all()

        if area and linha and linha in self.choices_v:
            queryset = queryset.filter(
                area__codigo=area, linha__codigo=linha
                )
        return queryset


class ZonaFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title, parameter_name, choices_v = 'Zona', 'zona', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        self.choices_v.clear(); 
        planta = get_value_in_url(request, 'planta')
        departamento = get_value_in_url(request, 'departamento')
        area = get_value_in_url(request, 'area')
        linha = get_value_in_url(request, 'linha')

        if planta: query = Q( ('planta__codigo', planta), ('departamento__codigo', departamento), ('area__codigo', area), ('linha__codigo', linha) )
        if planta is None: query = Q( ('departamento__codigo', departamento), ('area__codigo', area), ('linha__codigo', linha) )
        
        if linha:
            [self.choices_v.add(code) for code in Equipamento.objects.filter(query).values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]   
        return ((x, x) for x in self.choices_v)

    def queryset(self, request, queryset):
        linha, zona,  = get_value_in_url(request, 'linha'), get_selected_value(self)
        if linha is None:
            queryset = queryset.all()

        if linha and zona and zona in self.choices_v:
            queryset = queryset.filter(
                linha__codigo=linha, zona__codigo=zona
                )
        return queryset


class PostoFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title, parameter_name, choices_v = 'Posto', 'posto', set()
    def lookups(self, request, model_admin) -> List[tuple]:
        self.choices_v.clear(); 

        planta = get_value_in_url(request, 'planta')
        departamento = get_value_in_url(request, 'departamento')
        area = get_value_in_url(request, 'area')
        linha = get_value_in_url(request, 'linha')
        zona = get_value_in_url(request, 'zona')
        
        if planta: query = Q( ('planta__codigo', planta), ('departamento__codigo', departamento), ('area__codigo', area), ('linha__codigo', linha), ('zona__codigo', zona))
        if planta is None: query = Q( ('departamento__codigo', departamento), ('area__codigo', area), ('linha__codigo', linha), ('zona__codigo', zona) )
        if zona:
            [self.choices_v.add(code) for code in Equipamento.objects.filter(query).values_list(f'{self.parameter_name}__codigo', flat=True).distinct()]   
        return ((x, x) for x in self.choices_v)

    def queryset(self, request, queryset):
        zona, posto,  = get_value_in_url(request, 'zona'), get_selected_value(self)
        if zona is None:
            queryset = queryset.all()

        if zona and posto and posto in self.choices_v:
            queryset = queryset.filter(
                zona__codigo=zona, posto__codigo=posto
                )
        return queryset
