from django.contrib import admin
from django.urls import path, include


# Usuários e grupos django admin, para aparecer retira-los retirar o #
#from django.contrib.auth.models import User, Group
#admin.site.unregister(User)
#admin.site.unregister(Group)


admin.site.site_title = "Administração Platec"
admin.site.site_header = "Bem vindo Painel Administrativo Platec"
admin.site.index_title = "Administração Platec"


urlpatterns = [
    path('api/v1/', include('equipamentos.urls')),
    path('api/v1/', include('ocorrencias.urls')),
    path('gestao_competencia_servidor/', include('gestao_competencia_servidor.urls')),
    path('', admin.site.urls),
]
