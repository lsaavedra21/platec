# gestao_competencias/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('colab/', views.colab, name='colab'),
    path('login/', views.login, name='login'),
    path('pagina_inicial/', views.pagina_inicial, name='pagina_inicial'),
    path('membros/', views.membros_view, name='membros'),
    path('a/', views.a, name='a'),
    path('adicionar_membro/', views.adicionar_membro, name='adicionar_membro'),
    path('editar_membro/<str:membro_id>/', views.editar_membro, name='editar_membro'),
    path('excluir_membro/<str:membro_id>/', views.excluir_membro, name='excluir_membro'),
    path('ver_competencia/<str:membro_id>/', views.ver_competencia, name='ver_competencia'),

    path('matriz_competencias/', views.matriz_competencias, name='matriz_competencias'),
    path('competencias_por_setor/', views.competencias_por_setor, name='competencias_por_setor'),
    path('formacoes-previstas/', views.formacoes_previstas, name='formacoes_previstas'),
    path('formacao/<str:formacao_id>/', views.detalhes_formacao, name='detalhes_formacao'),
    path('formacoes-platec/', views.formacoes_platec, name='formacoes_platec'),
    path('formacoes-realizadas/', views.formacoes_realizadas, name='formacoes_realizadas'),
    path('salvar_niveis/', views.salvar_niveis, name='salvar_niveis'),

    path('matrizilu_setor/', views.matrizilu_setor, name='matrizilu_setor'),
    path('matriz_competencias_montagem_cvp/', views.matriz_competencias_montagem_cvp, name='matriz_competencias_montagem_cvp'),
    path('matriz_competencias_carroceria_cvp/', views.matriz_competencias_carroceria_cvp, name='matriz_competencias_carroceria_cvp'),
    path('matriz_competencias_pintura_cvp/', views.matriz_competencias_pintura_cvp, name='matriz_competencias_pintura_cvp'),
    path('matriz_competencias_carroceria_cvu/', views.matriz_competencias_carroceria_cvu, name='matriz_competencias_carroceria_cvu'),
    path('matriz_competencias_montagem_cvu/', views.matriz_competencias_montagem_cvu, name='matriz_competencias_montagem_cvu'),
    path('matriz_competencias_pintura_cvu/', views.matriz_competencias_pintura_cvu, name='matriz_competencias_pintura_cvu'),

    path('afinidade_areas/', views.afinidade_areas, name='afinidade_areas'),
    # Outras URLs do aplicativo "gestao_competencias", se houver
]