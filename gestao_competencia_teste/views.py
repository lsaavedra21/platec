from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import ConsultaCompetencia, Competencia, Matriz
from .models import Membro, Setor, Cargo, FormacaoPrevista, Formacao, ConsultaFormacao
from django.shortcuts import render
from .forms import MembroForm
from django.shortcuts import redirect
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import F, Sum
import logging
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def colab(request):
    return render(request, 'colab.html')



def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')
def login(request):
    return render(request, 'login.html')

def a(request):
    return render(request, 'a.html')
def teste(request):
    return render(request, 'teste.html')
def teste_menu(request):
    return render(request, 'index.html')
def menu_n(request):
    return render(request, 'menu_n.html')

def membros_view(request):
    membros = Membro.objects.all()
    setores = Setor.objects.all()  # Recupere a lista de todos os setores
    setor_filtrado = request.GET.get('setor')  # Obtenha o valor do setor selecionado no filtro

    if setor_filtrado:  # Se um setor foi selecionado no filtro
        membros = membros.filter(setor_id=setor_filtrado)  # Filtrar os membros pelo setor selecionado

    return render(request, 'membros.html', {'membros': membros, 'setores': setores, 'setor_filtrado': setor_filtrado})



def editar_membro(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)

    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            return redirect('pagina_inicial')
    else:
        form = MembroForm(instance=membro)

    context = {'form': form}
    return render(request, 'editar_membros.html', context)



def adicionar_membro(request):
    if request.method == 'POST':
        id = request.POST['id']
        nome = request.POST['nome']
        setor_id = request.POST['setor']
        cargo_id = request.POST['cargo']

        setor = Setor.objects.get(id=setor_id)
        cargo = Cargo.objects.get(id=cargo_id)

        membro = Membro(id=id, nome=nome, setor=setor, cargo=cargo)
        membro.save()

        # Recuperar todas as competências do setor
        competencias_setor = Competencia.objects.filter(setor=setor)

        # Criar instâncias de ConsultaCompetencia para cada competência com nível 0
        for competencia in competencias_setor:
            ConsultaCompetencia.objects.create(membro=membro, competencia=competencia, nivel=0, setor=setor)

        return redirect('membros')  # Redirecionar para a lista de membros após salvar

    setores = Setor.objects.all()
    cargos = Cargo.objects.all()

    return render(request, 'adicionar_membro.html', {'setores': setores, 'cargos': cargos})


def excluir_membro(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    if request.method == 'POST':
        membro.delete()
        return redirect('membros')  # Redirecionar para a lista de membros após a exclusão
    return render(request, 'excluir_membro.html', {'membro': membro})  # Renderizar página de confirmação


from django.db import transaction


def ver_competencia(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    setor_id = membro.setor.id

    competencias_setor = Competencia.objects.filter(setor_id=setor_id)
    consultas = ConsultaCompetencia.objects.filter(membro=membro)
    consultas_dict = {consulta.competencia_id: consulta for consulta in consultas}

    # Ordenar as competências em ordem alfabética
    competencias_setor = sorted(competencias_setor, key=lambda comp: comp.nome)

    context = {'consultas': consultas, 'competencias_setor': competencias_setor, 'membro': membro}

    if request.method == 'POST':
        niveis_modificados = {}
        for competencia in competencias_setor:
            for nivel_name in request.POST:
                if nivel_name.startswith('salvar_nivel_'):
                    nivel_id = nivel_name.split('_')[-1]
                    if nivel_id and consultas_dict.get(int(nivel_id)):
                        novo_nivel = request.POST[nivel_name]
                        consulta_obj = consultas_dict.get(int(nivel_id))

                        if consulta_obj and novo_nivel is not None and novo_nivel != consulta_obj.nivel:
                            niveis_modificados[consulta_obj.id] = novo_nivel

        with transaction.atomic():
            for consulta_id, novo_nivel in niveis_modificados.items():
                consulta = ConsultaCompetencia.objects.get(pk=consulta_id)
                consulta.nivel = novo_nivel
                consulta.save()

            # Preenche os níveis ausentes com 0
            for competencia in competencias_setor:
                if consultas_dict.get(competencia.id) is None:
                    ConsultaCompetencia.objects.create(membro=membro, competencia=competencia, nivel=0)

            # Atualiza as entradas não modificadas para nível 0
            for consulta in consultas:
                if consulta.id not in niveis_modificados:
                    consulta.nivel = 0
                    consulta.save()

        return redirect('ver_competencia', membro_id=membro_id)

    return render(request, 'ver_competencia.html', context)
def salvar_niveis(request):
    if request.method == 'POST':
        membro_id = request.POST.get('membro_id')

        # Verifique se o membro existe
        membro = get_object_or_404(Membro, id=membro_id)

        # Obtém as competências do setor do membro
        competencias_setor = Competencia.objects.filter(setor_id=membro.setor_id)

        for competencia in competencias_setor:
            consulta_id = request.POST.get(f'niveis[{competencia.id}]')

            consulta_obj, created = ConsultaCompetencia.objects.get_or_create(
                membro=membro,
                competencia=competencia,
                defaults={'nivel': consulta_id},
            )

            # Se a consulta já existe, atualiza o nível
            if not created:
                consulta_obj.nivel = consulta_id
                consulta_obj.save()

        return redirect('ver_competencia', membro_id=membro_id)

    return HttpResponseBadRequest("Método inválido")











def competencias_por_setor(request):
    setor_id = request.GET.get('setor')
    competencias = Competencia.objects.all()

    if setor_id:
        competencias = competencias.filter(setor_id=setor_id)

    setores = Setor.objects.all()

    context = {
        'competencias': competencias,
        'setores': setores,
    }
    return render(request, 'competencias_por_setor.html', context)

def matriz_competencias(request):
    setor_id = request.GET.get('setor')  # Obtém o valor do parâmetro setor

    # Filtra as consultas com base no setor selecionado
    if setor_id:
        consultas = ConsultaCompetencia.objects.filter(setor_id=setor_id)
        membros = Membro.objects.filter(c_membro_competencias__setor_id=setor_id).distinct()
        competencias = Competencia.objects.filter(c_membro_competencias__setor_id=setor_id).distinct()
    else:
        consultas = ConsultaCompetencia.objects.all()
        membros = Membro.objects.all()
        competencias = Competencia.objects.all()

    setores = Setor.objects.all()

    return render(request, 'matriz_competencias.html',
                  {'membros': membros, 'competencias': competencias, 'consultas': consultas, 'setores': setores})



def formacoes_previstas(request):
    formacoes = FormacaoPrevista.objects.all()

    context = {
        'formacoes_previstas': formacoes,
    }

    return render(request, 'formacoes_previstas.html', context)


def detalhes_formacao(request, formacao_id):
    formacao = get_object_or_404(Formacao, id=formacao_id)

    context = {
        'formacao': formacao,
    }

    return render(request, 'detalhes_formacao.html', context)


def formacoes_platec(request):
    formacoes = Formacao.objects.all()

    context = {
        'formacoes': formacoes,
    }

    return render(request, 'formacoes_platec.html', context)


from django.db.models import Q

def formacoes_realizadas(request):
    realizacoes = ConsultaFormacao.objects.all()
    setores = Setor.objects.all()

    # Filtrar por setor (caso seja selecionado)
    setor_id = request.GET.get('setor')
    if setor_id:
        realizacoes = realizacoes.filter(membro__setor_id=setor_id)

    # Pesquisar por qualquer coisa (caso haja um termo de pesquisa)
    search_query = request.GET.get('search_query')
    if search_query:
        realizacoes = realizacoes.filter(
            Q(membro__nome__icontains=search_query) |
            Q(formacao__formacao__nome__icontains=search_query) |
            Q(Data__icontains=search_query)
        )

    context = {
        'formacoes_realizadas': realizacoes,
        'setores': setores,
    }

    return render(request, 'formacoes_realizadas.html', context)











def matrizilu_setor(request):
    return render(request, 'matrizilu_setor.html')

def matriz_competencias_montagem_cvp(request):
    setor_nome = 'Montagem CVP'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    numeros = list(range(6))  # Lista de números de 0 a 5

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
        'numeros': numeros,  # Adicione essa linha ao seu contexto
    }

    return render(request, 'matriz_competencias_montagem_cvp.html', context)

    return render(request, 'matriz_competencias_montagem_cvp.html', context)
def matriz_competencias_carroceria_cvp(request):
    setor_nome = 'Carroceria CVP'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    return render(request, 'matriz_competencias_carroceria_cvp.html', context)

def matriz_competencias_pintura_cvp(request):
    setor_nome = 'Pintura CVP'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    return render(request, 'matriz_competencias_pintura_cvp.html', context)

def matriz_competencias_montagem_cvu(request):
    setor_nome = 'Montagem CVU'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    return render(request, 'matriz_competencias_montagem_cvu.html', context)

def matriz_competencias_carroceria_cvu(request):
    setor_nome = 'Carroceria CVU'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    return render(request, 'matriz_competencias_carroceria_cvu.html', context)

def matriz_competencias_pintura_cvu(request):
    setor_nome = 'Pintura CVU'
    setor = Setor.objects.get(nome=setor_nome)

    membros = Membro.objects.filter(setor=setor).order_by('nome')
    competencias = Competencia.objects.filter(c_membro_competencias__setor=setor).distinct()

    consultas = ConsultaCompetencia.objects.filter(setor=setor)

    context = {
        'membros': membros,
        'competencias': competencias,
        'consultas': consultas,
        'setores': Setor.objects.all(),
    }

    return render(request, 'matriz_competencias_pintura_cvu.html', context)



def matriz_view(request):
    competencias = Competencia.objects.all()
    areas = Matriz.objects.values_list('area', flat=True).distinct()
    setores = Setor.objects.all()

    selected_setor = request.GET.get('setor')

    matriz_data = []

    for competencia in competencias:
        row = [competencia]
        for area in areas:
            try:
                matriz_entry = Matriz.objects.get(competencias=competencia, area=area)
                row.append(matriz_entry)
            except Matriz.DoesNotExist:
                row.append(None)
        matriz_data.append(row)

    filtered_matriz_data = []

    if selected_setor:
        filtered_matriz_data = [
            row for row in matriz_data if row[1] and row[1].setor.nome == selected_setor
        ]

    context = {
        'areas': areas,
        'setores': setores,
        'selected_setor': selected_setor,
        'matriz_data': filtered_matriz_data if filtered_matriz_data else matriz_data,
    }

    return render(request, 'matriz_template.html', context)

from django.shortcuts import redirect

def atualizar_nivel(request):
    if request.method == 'POST':
        competencia_id = request.POST['competencia_id']
        area = request.POST['area']
        nivel_percentual = request.POST['nivel_percentual']

        try:
            matriz_entry = Matriz.objects.get(competencias_id=competencia_id, area=area)
            matriz_entry.nivel_percentual = nivel_percentual
            matriz_entry.save()
        except Matriz.DoesNotExist:
            # Se a entrada não existe, você pode criar uma nova entrada se necessário
            pass

    return redirect('matriz_template')








def calculate_afinidade(member_id, area):
    total_afinidade = 0
    total_necessidade = 0

    member_competencias = ConsultaCompetencia.objects.filter(membro_id=member_id)

    for consulta in member_competencias:
        competencia_id = consulta.competencia_id
        nivel_membro = int(consulta.nivel)

        matriz = Matriz.objects.filter(competencias_id=competencia_id, area=area).first()
        if matriz:
            nivel_necessidade = matriz.nivel_percentual
            total_afinidade += (nivel_membro * nivel_necessidade)
            total_necessidade += nivel_necessidade

    if total_necessidade == 0:
        afinidade = 0
    else:
        afinidade = total_afinidade  # Calcula a soma ponderada

        # Adicione um log de depuração para verificar o valor de afinidade
        logging.debug(f'Afinidade para membro {member_id} na área {area}: {afinidade}')
    return afinidade

def afinidade_areas(request):
    members = Membro.objects.all()
    areas = Matriz.objects.values_list('area', flat=True).distinct()

    data = []

    for member in members:
        afinidades = {}

        for area in areas:
            afinidade = calculate_afinidade(member.id, area)
            afinidades[area] = afinidade

        data.append({
            'member': member,
            'afinidades': afinidades
        })

    context = {
        'members': members,
        'areas': areas,
        'data': data
    }

    return render(request, 'afinidade_areas.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import User

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Autenticação bem-sucedida
                # Redirecionar para a página principal ou fazer o que for necessário
                return redirect('home')
            else:
                # Senha incorreta
                # Retornar uma mensagem de erro
                return render(request, 'login.html', {'error': 'Senha incorreta'})
        except User.DoesNotExist:
            # Usuário não encontrado
            # Retornar uma mensagem de erro
            return render(request, 'login.html', {'error': 'Usuário não encontrado'})
    else:
        return render(request, 'login.html')
