# gestao_competencias_igor/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial),
    path('pagina_inicial/', views.pagina_inicial, name='pagina_inicial'),

    path('membros/', views.membros_view, name='membros'),
    path('adicionar_membro/', views.adicionar_membro, name='adicionar_membro'),
    path('editar_membro/<str:membro_id>/', views.editar_membro, name='editar_membro'),
    path('excluir_membro_1/<str:membro_id>/', views.excluir_membro_1, name='excluir_membro_1'),
    path('ver_competencia/<str:membro_id>/', views.ver_competencia, name='ver_competencia'),
    path('grafico_membro/<str:membro_id>/', views.grafico_membro, name='grafico_membro'),
    path('salvar_niveis/', views.salvar_niveis, name='salvar_niveis'),
    path('membro/afinidade/<str:membro_id>/', views.afinidade_membro, name='afinidade_membro'),

    path('matriz_competencias/', views.matriz_competencias, name='matriz_competencias'),

    path('competencias_por_setor/', views.competencias_por_setor, name='competencias_por_setor'),
    path('adicionar_competencia/', views.adicionar_competencia, name='adicionar_competencia'),

    path('formacoes-previstas/', views.formacoes_previstas, name='formacoes_previstas'),
    path('formacao/<str:formacao_id>/', views.detalhes_formacao, name='detalhes_formacao'),
    path('formacoes-platec/', views.formacoes_platec, name='formacoes_platec'),
    path('listar_membros_por_formacao/<int:formacao_prevista_id>/', views.listar_membros_por_formacao, name='listar_membros_por_formacao'),
    path('listar_membros_por_formacao_admin/<int:formacao_prevista_id>/', views.listar_membros_por_formacao_admin, name='listar_membros_por_formacao_admin'),
    path('excluir_formacao_prevista/<int:formacao_id>/', views.excluir_formacao_prevista, name='excluir_formacao_prevista'),
    path('excluir_membro/<int:membro_id>/', views.excluir_membro_formacao, name='excluir_membro_formacao'),
    path('adicionar_membro_formacaoprevista/<int:formacao_prevista_id>/', views.adicionar_membro_formacaoprevista, name='adicionar_membro_formacaoprevista'),

    path('formacoes-realizadas/', views.formacoes_realizadas, name='formacoes_realizadas'),

    path('matrizilu_setor/', views.matrizilu_setor, name='matrizilu_setor'),
    path('matriz_competencias_montagem_cvp/', views.matriz_competencias_montagem_cvp, name='matriz_competencias_montagem_cvp'),
    path('grafico_setor/<str:setor_nome>/', views.grafico_setor, name='grafico_setor'),
    path('matriz_competencias_carroceria_cvp/', views.matriz_competencias_carroceria_cvp, name='matriz_competencias_carroceria_cvp'),
    path('matriz_competencias_pintura_cvp/', views.matriz_competencias_pintura_cvp, name='matriz_competencias_pintura_cvp'),
    path('matriz_competencias_carroceria_cvu/', views.matriz_competencias_carroceria_cvu, name='matriz_competencias_carroceria_cvu'),
    path('matriz_competencias_montagem_cvu/', views.matriz_competencias_montagem_cvu, name='matriz_competencias_montagem_cvu'),
    path('matriz_competencias_pintura_cvu/', views.matriz_competencias_pintura_cvu, name='matriz_competencias_pintura_cvu'),

    path('matriz_template/', views.matriz_view, name='matriz_template'),
    path('atualizar/', views.atualizar_niveis_competencia_area, name='atualizar_niveis_competencia_area'),
    path('afinidade_areas/', views.afinidade_areas, name='afinidade_areas'),

    ##PAGINAS GESTOR MANUTENÇÃO

    path('pagina_inicial_admin/', views.pagina_inicial_admin, name='pagina_inicial_admin'),

    path('novas_formacoes_realizadas/', views.novas_formacoes_realizadas, name='novas_formacoes_realizadas'),

    path('formacoes_previstas_admin/', views.formacoes_previstas_admin, name='formacoes_previstas_admin'),

    path('adicionar_formacao_prevista/', views.adicionar_editar_formacao_prevista, name='adicionar_formacao_prevista'),
    path('editar_formacao_prevista_admin/<str:formacao_id>/', views.editar_formacao_prevista,
         name='editar_formacao_prevista_admin'),


    path('listar_membros_formacoes/', views.listar_membros_formacoes, name='listar_membros_formacoes'),
    # Outras URLs do aplicativo "gestao_competencias_igor", se houver
]