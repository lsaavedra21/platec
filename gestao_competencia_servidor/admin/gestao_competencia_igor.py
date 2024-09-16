from django.shortcuts import render
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.urls import path
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.db.models import Case, When, Value, CharField
from django.db.models.functions import Coalesce
from django.utils.safestring import mark_safe
from ..models import Membro, Setor, Cargo, Tecnologia, Formacao, Competencia, ConsultaCompetencia, ConsultaFormacao, FormacaoPrevista, Matriz, MembroFormacao, FormacaoCompetencia



class MembroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'setor', 'cargo')
    list_filter = ('setor', 'cargo')
    search_fields = ('id', 'nome')

    def get_list_display(self, request):
    # Define as colunas que você deseja exibir em cada linha
    # Exemplo: dividir em 3 colunas
        columns = 4
    # Obtém a lista padrão de campos de exibição
        list_display = super().get_list_display(request)
    # Divide a lista de campos em várias listas de acordo com o número de colunas
        column_lists = [[] for _ in range(columns)]
        for i, field_name in enumerate(list_display):
            column_lists[i % columns].append(field_name)
    # Retorna a lista de campos dividida em colunas
        return sum(column_lists, [])
admin.site.register(Membro, MembroAdmin)


class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor')
    list_filter = ('setor', 'tecnologia')

    def get_list_display(self, request):
    # Define as colunas que você deseja exibir em cada linha
    # Exemplo: dividir em 3 colunas
        columns = 3
    # Obtém a lista padrão de campos de exibição
        list_display = super().get_list_display(request)
    # Divide a lista de campos em várias listas de acordo com o número de colunas
        column_lists = [[] for _ in range(columns)]
        for i, field_name in enumerate(list_display):
            column_lists[i % columns].append(field_name)
    # Retorna a lista de campos dividida em colunas
        return sum(column_lists, [])
admin.site.register(Competencia, CompetenciaAdmin)


class SetorForm(forms.Form):
    setor = forms.ModelChoiceField(queryset=Setor.objects.all(), empty_label=None)










from django.contrib import admin
from django.utils.html import format_html
from ..models import ConsultaCompetencia, Membro, Competencia, Setor







class ConsultaCompetenciaAdmin(admin.ModelAdmin):
    list_filter = ('setor',)
    list_display = ('competencias_matrix',)

    def get_setores(self, request):
        return Setor.objects.all()

    def competencias_matrix(self, obj):
        setor = obj.setor
        membros = Membro.objects.filter(setor=setor)
        competencias = Competencia.objects.filter(setor=setor)
        matrix = [['Competência'] + [membro.nome for membro in membros]]

        for competencia in competencias:
            row = [competencia.nome] + [''] * len(membros)
            for i, membro in enumerate(membros):
                consulta = ConsultaCompetencia.objects.filter(membro=membro, competencia=competencia).first()
                nivel = consulta.nivel if consulta else ''
                change_url = reverse("admin:gestao_competencia_igor_consultacompetencia_change", args=[consulta.pk]) if consulta else ''
                row[i+1] = (nivel, change_url)
            matrix.append(row)

        matrix_table = '<table>'
        for i, row in enumerate(matrix):
            matrix_table += '<tr>'
            for j, cell in enumerate(row):
                if i == 0:
                    if j == 0:
                        matrix_table += f'<th>{cell}</th>'
                    else:
                        membro = membros[j-1]
                        change_url = reverse("admin:gestao_competencia_igor_membro_change", args=[membro.pk])
                        matrix_table += f'<th><a href="{change_url}">{membro.nome}</a></th>'
                else:
                    if j == 0:
                        competencia_nome = cell
                        competencia = competencias[i-1]
                        change_url = reverse("admin:gestao_competencia_igor_competencia_change", args=[competencia.pk])
                        matrix_table += f'<th><a href="{change_url}">{competencia_nome}</a></th>'
                    else:
                        nivel, change_url = cell
                        if change_url:
                            matrix_table += f'<td><a href="{change_url}">{nivel}</a></td>'
                        else:
                            matrix_table += f'<td>{nivel}</td>'
            matrix_table += '</tr>'
        matrix_table += '</table>'

        return format_html(matrix_table)

    competencias_matrix.short_description = 'Matriz de Competências por Setor'

admin.site.register(ConsultaCompetencia, ConsultaCompetenciaAdmin)














class ConsultaFormacaoAdmin(admin.ModelAdmin):
    list_display = ('membro', 'formacao', 'Data')
    list_filter = ('formacao', 'Data')
    search_fields = ('membro__id','membro__nome', 'formacao__nome')

    def get_list_display(self, request):
    # Define as colunas que você deseja exibir em cada linha
    # Exemplo: dividir em 3 colunas
        columns = 3
    # Obtém a lista padrão de campos de exibição
        list_display = super().get_list_display(request)
    # Divide a lista de campos em várias listas de acordo com o número de colunas
        column_lists = [[] for _ in range(columns)]
        for i, field_name in enumerate(list_display):
            column_lists[i % columns].append(field_name)
    # Retorna a lista de campos dividida em colunas
        return sum(column_lists, [])
admin.site.register(ConsultaFormacao, ConsultaFormacaoAdmin)

class FormacaoPrevistaAdmin(admin.ModelAdmin):
    list_display = ('formacao', 'formador', 'duracao', 'vagas')


    def get_list_display(self, request):
    # Define as colunas que você deseja exibir em cada linha
    # Exemplo: dividir em 3 colunas
        columns = 5
    # Obtém a lista padrão de campos de exibição
        list_display = super().get_list_display(request)
    # Divide a lista de campos em várias listas de acordo com o número de colunas
        column_lists = [[] for _ in range(columns)]
        for i, field_name in enumerate(list_display):
            column_lists[i % columns].append(field_name)
    # Retorna a lista de campos dividida em colunas
        return sum(column_lists, [])
admin.site.register(FormacaoPrevista, FormacaoPrevistaAdmin)

class Formacaodmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')


    def get_list_display(self, request):
    # Define as colunas que você deseja exibir em cada linha
    # Exemplo: dividir em 3 colunas
        columns = 2
    # Obtém a lista padrão de campos de exibição
        list_display = super().get_list_display(request)
    # Divide a lista de campos em várias listas de acordo com o número de colunas
        column_lists = [[] for _ in range(columns)]
        for i, field_name in enumerate(list_display):
            column_lists[i % columns].append(field_name)
    # Retorna a lista de campos dividida em colunas
        return sum(column_lists, [])
admin.site.register(Formacao, Formacaodmin)


admin.site.register(Tecnologia)
admin.site.register(Matriz)
admin.site.register(Setor)
admin.site.register(Cargo)
admin.site.register(Permission)
admin.site.register(MembroFormacao)
admin.site.register(FormacaoCompetencia)
