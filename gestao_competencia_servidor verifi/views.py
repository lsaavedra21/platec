from django.shortcuts import render, redirect, get_object_or_404
from .models import ConsultaCompetencia, Competencia
from .models import Membro, Setor, Cargo, FormacaoPrevista, Formacao, ConsultaFormacao, Matriz, MembroFormacao, Competencia, FormacaoCompetencia
from django.shortcuts import render
from .forms import MembroForm, FormacaoPrevistaForm, AdicionarMembroForm
from django.db.models import Sum, F
from django.db.models import Case, When, Value, IntegerField, Sum, Avg


def pagina_inicial(request):
    return render(request, 'pagina_inicial.html')


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
        email = request.POST['email']  # Obtenha o valor do campo de email
        supervisor = request.POST['supervisor']  # Obtenha o valor do campo de supervisor
        area = request.POST['area']  # Obtenha o valor do campo de área

        setor = Setor.objects.get(id=setor_id)
        cargo = Cargo.objects.get(id=cargo_id)

        membro = Membro(id=id, nome=nome, setor=setor, cargo=cargo, email=email, supervisor=supervisor, area=area)
        membro.save()

        # Recuperar todas as competências do setor
        competencias_setor = Competencia.objects.filter(setor=setor)

        # Criar instâncias de ConsultaCompetencia para cada competência com nível 0
        for competencia in competencias_setor:
            ConsultaCompetencia.objects.create(membro=membro, competencia=competencia, nivel=0, setor=setor)


        return redirect('membros')

    setores = Setor.objects.all()
    cargos = Cargo.objects.all()

    return render(request, 'adicionar_membro.html', {'setores': setores, 'cargos': cargos})


from django.shortcuts import get_object_or_404, redirect
from .models import Membro

def excluir_membro_1(request, membro_id):
    membro = get_object_or_404(Membro, id=membro_id)
    membro.delete()
    return redirect('membros')  # Redirecionar de volta para a página de membros após a exclusão


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


## PAGINA PARA VER OS RESULTADOS DOS MEMBROS INDIVIDUALMENTE ##

from django.shortcuts import render, get_object_or_404
from .models import Membro, ConsultaCompetencia


from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, Value, IntegerField, Avg, Count, Subquery, OuterRef, F
from .models import Membro, ConsultaCompetencia, FormacaoCompetencia



from django.db.models import F, Value, Case, When, IntegerField

def contar_niveis_membro(membro):
    # Utilize Case e When para mapear os números dos níveis para letras
    counts = ConsultaCompetencia.objects.filter(
        membro=membro,
        nivel__in=['1', '2', '3', '4', '5']
    ).values('nivel').annotate(
        count=Count('nivel'),
        nivel_letra=Case(
            When(nivel='1', then=Value('NA')),
            When(nivel='2', then=Value('0')),
            When(nivel='3', then=Value('I')),
            When(nivel='4', then=Value('L')),
            When(nivel='5', then=Value('U')),
            default=F('nivel'),
            output_field=IntegerField()
        )
    ).order_by('nivel')

    return counts



def grafico_membro(request, membro_id):
    # Recuperar o membro pelo ID
    membro = get_object_or_404(Membro, id=membro_id)

    nivel_medio = ConsultaCompetencia.objects.filter(
        membro=membro,
        nivel__in=['0', '2', '3', '4', '5']
    ).annotate(
        nivel_int=Case(
            When(nivel='0', then=Value(0)),
            When(nivel='2', then=Value('0')),
            When(nivel='3', then=Value('1')),
            When(nivel='4', then=Value('2')),
            When(nivel='5', then=Value('3')),
            default='nivel',
            output_field=IntegerField()
        )
    ).aggregate(Avg('nivel_int'))['nivel_int__avg']

    nivel_medio = nivel_medio or 0

    # Consulta para contar o número de níveis para cada valor (1, 2, 3, 4, 5)
    counts = ConsultaCompetencia.objects.filter(
        membro=membro,
        nivel__in=['1', '2', '3', '4', '5']
    ).values('nivel').annotate(count=Count('nivel')).order_by('nivel')

    data = [count['count'] for count in counts]
    labels = ['NA', '0', 'I', 'L', 'U']

    # Consulta para obter as competências e níveis (ajustando o nível 2 para 0) e classificando pelo nível e nome
    competencias_nivel = ConsultaCompetencia.objects.filter(
        membro=membro,
        nivel__in=['0', '2', '3', '4', '5']
    ).select_related('competencia').order_by('nivel', 'competencia__nome')

    competencias_nivel = competencias_nivel.annotate(
        nivel_ajustado=Case(
            When(nivel='2', then=Value('0')),
            When(nivel='3', then=Value('1')),
            When(nivel='4', then=Value('2')),
            When(nivel='5', then=Value('3')),
            default=F('nivel'),
            output_field=IntegerField(),
        )
    )

    # Consulta para obter as formações correspondentes às competências
    # Usamos o relacionamento FormacaoCompetencia para obter as formações
    # associadas a cada competência
    formacoes_correspondentes = FormacaoCompetencia.objects.filter(
        competencias__in=competencias_nivel.values('competencia')
    ).values('competencias', 'formacoes__nome')

    # Adicione as formações correspondentes à competência no contexto
    competencias_nivel = competencias_nivel.annotate(
        formações_correspondentes=Subquery(
            formacoes_correspondentes.filter(competencias=OuterRef('competencia'))
                .values('formacoes__nome')[:1]
        )
    )

    context = {
        'data': data,
        'labels': labels,
        'count_data': counts,
        'competencias_nivel': competencias_nivel,
        'nivel_medio': nivel_medio,
        'nome_membro': membro.nome
    }

    return render(request, 'grafico_membro.html', context)









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


from .forms import CompetenciaForm  # Importe o formulário que você criou

def adicionar_competencia(request):
    if request.method == 'POST':
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_competencias')  # Redirecionar para a lista de competências após adicionar
    else:
        form = CompetenciaForm()

    return render(request, 'adicionar_competencia.html', {'form': form})

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

    for formacao in formacoes:
        membros_associados = MembroFormacao.objects.filter(formacao_prevista=formacao)
        formacao.vagasdisponiveis = formacao.vagas - membros_associados.count()

    context = {
        'formacoes_previstas': formacoes,
        'formacao_prevista': None,  # Pode ser None, já que estamos na página de listagem.
    }

    return render(request, 'formacoes_previstas.html', context)

##PAGINA PARA MEMBROS CADASTRADOS POR FORMAÇÃO##

def listar_membros_por_formacao(request, formacao_prevista_id):
    membros = MembroFormacao.objects.filter(formacao_prevista_id=formacao_prevista_id)
    formacao_prevista = get_object_or_404(FormacaoPrevista, id=formacao_prevista_id)

    context = {
        'formacao_prevista': formacao_prevista,
        'membros': membros,
    }

    return render(request, 'listar_membros_por_formacao.html', context)

##PAGINA PARA ADICIONAR MEMBROS PARA REALIZAR FORMAÇÕES PREVISTAS

def adicionar_membro_formacaoprevista(request, formacao_prevista_id):
    formacao_prevista = get_object_or_404(FormacaoPrevista, id=formacao_prevista_id)

    setores = Setor.objects.all()  # Obtenha todos os setores para o filtro

    membros_associados = MembroFormacao.objects.filter(formacao_prevista=formacao_prevista)

    # Filtrar membros com base no setor selecionado no formulário
    setor_id = request.POST.get('setor')
    if setor_id:
        membros_disponiveis = Membro.objects.filter(
            setor_id=setor_id
        ).exclude(
            c_formacaoid_membroid__formacao_prevista=formacao_prevista
        )
    else:
        membros_disponiveis = Membro.objects.exclude(
            c_formacaoid_membroid__formacao_prevista=formacao_prevista
        )

    if request.method == 'POST':
        membro_id = request.POST.get('membro')
        if membro_id:
            membro = get_object_or_404(Membro, id=membro_id)

            # Verifique se o membro já está associado a esta formação prevista
            existe_associacao = MembroFormacao.objects.filter(
                membro=membro,
                formacao_prevista=formacao_prevista
            ).exists()

            if not existe_associacao:
                # Associe o membro a esta formação prevista
                MembroFormacao.objects.create(
                    membro=membro,
                    formacao_prevista=formacao_prevista
                )

    context = {
        'formacao_prevista': formacao_prevista,
        'membros_associados': membros_associados,
        'membros_disponiveis': membros_disponiveis,
        'setores': setores,
    }

    return render(request, 'adicionar_membro_formacaoprevista.html', context)


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
        'setor_atual': setor,
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

##GRAFICO AMOSTRAGEM



def nivel_para_rotulo(nivel):
    nivel_mapeado = {
        '1': 'NA',
        '2': '0',
        '3': 'I',
        '4': 'L',
        '5': 'U'
    }
    return nivel_mapeado.get(nivel, nivel)

def ranking_competencias(setor_nome):
    # Filtrar membros do setor
    membros = Membro.objects.filter(setor__nome=setor_nome)

    # Use Case When para calcular a média dos níveis de competências para cada competência,
    # considerando '2' como 0
    competencias_com_media = Competencia.objects.filter(
        setor__nome=setor_nome,
        c_membro_competencias__nivel__gt='1'  # Filtrar níveis maiores que '1'
    ).annotate(
        media_niveis=Avg(
            Case(
                When(c_membro_competencias__nivel='2', then=Value(0)),
                When(c_membro_competencias__nivel='3', then=Value(1)),
                When(c_membro_competencias__nivel='4', then=Value(2)),
                When(c_membro_competencias__nivel='5', then=Value(3)),
                default='c_membro_competencias__nivel',
                output_field=IntegerField()
            )
        ),
        competencia_nome=F('nome')  # Adicione esta linha para pegar o nome da competência
    ).order_by('media_niveis')  # Classificar do menor para o maior nível médio

    # Agora, adicione uma subconsulta para pegar as formações correspondentes a cada competência
    competencias_com_media = competencias_com_media.annotate(
        formacoes_correspondentes=Subquery(
            FormacaoCompetencia.objects.filter(competencias=OuterRef('id'))
            .values('formacoes__nome')[:1]
        )
    )

    return competencias_com_media


from django.db.models import Sum


def calcular_media_setor(setor_nome):
    competencias = Competencia.objects.filter(setor__nome=setor_nome)

    # Use Case When para calcular a média dos níveis de competências para cada competência,
    # considerando '2' como 0
    competencias_com_media = competencias.annotate(
        media_niveis=Avg(
            Case(
                When(c_membro_competencias__nivel='2', then=Value(0)),
                When(c_membro_competencias__nivel='3', then=Value(1)),
                When(c_membro_competencias__nivel='4', then=Value(2)),
                When(c_membro_competencias__nivel='5', then=Value(3)),
                default='c_membro_competencias__nivel',
                output_field=IntegerField()
            )
        )
    )

    # Calcular a média do setor
    media_setor = competencias_com_media.aggregate(media_setor=Sum('media_niveis'))['media_setor']

    # Contar o número de competências no setor
    numero_competencias = competencias.count()

    # Calcular a média do setor
    if media_setor is not None and numero_competencias > 0:
        media_setor = media_setor / numero_competencias

    return media_setor


def grafico_setor(request, setor_nome):
    membros = Membro.objects.filter(setor__nome=setor_nome)

    nivel_counts = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}

    for nivel in nivel_counts.keys():
        nivel_counts[nivel] = membros.filter(c_membro_competencias__nivel=nivel).count()

    data = {
        'labels': [nivel_para_rotulo(nivel) for nivel in nivel_counts.keys()],
        'data': list(nivel_counts.values()),
    }

    competencias_com_media = ranking_competencias(setor_nome)

    # Calcular a média do setor
    media_setor = calcular_media_setor(setor_nome)

    context = {
        'data': data,
        'competencias_com_media': competencias_com_media,
        'media_setor': media_setor,  # Adicione a média do setor ao contexto
        'nome_setor': setor_nome

    }

    return render(request, 'grafico_setor.html', context)


##PAGINA MATRIZ ILU CARROCERIA CVP##
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
        'nome_setor': setor.nome
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
    # Recupere todos os setores para exibir no filtro
    setores = Setor.objects.all()

    # Obtenha o setor selecionado, se houver, a partir dos parâmetros GET
    selected_setor = request.GET.get('setor')

    # Inicialize um dicionário para armazenar os dados da matriz
    matriz_data = {}

    if selected_setor:
        # Se um setor foi selecionado, filtre as competências por esse setor
        competencias = Competencia.objects.filter(setor__nome=selected_setor)
        # Obtenha as áreas associadas a esse setor
        areas = Matriz.objects.filter(setor__nome=selected_setor).values_list('area', flat=True).distinct()
    else:
        # Se nenhum setor for selecionado, obtenha todas as competências e áreas
        competencias = Competencia.objects.all()
        areas = Matriz.objects.values_list('area', flat=True).distinct()

    # Recupere os valores existentes dos níveis a partir do banco de dados
    for competencia in competencias:
        matriz_data[competencia] = {}
        for area in areas:
            try:
                matriz = Matriz.objects.get(competencias=competencia, area=area)
                matriz_data[competencia][area] = matriz.nivel_percentual
            except Matriz.DoesNotExist:
                matriz_data[competencia][area] = None

    # Agora você tem os dados da matriz e pode passá-los para o contexto
    context = {
        'areas': areas,
        'setores': setores,
        'selected_setor': selected_setor,
        'competencias': competencias,
        'matriz_data': matriz_data,  # Adicione os dados da matriz ao contexto
    }

    return render(request, 'matriz_template.html', context)

from django.shortcuts import render, redirect
from .models import Matriz
from .models import Competencia
from .models import Setor  # Importe o modelo Setor

def atualizar_niveis_competencia_area(request):
    if request.method == 'POST':
        try:
            for key, value in request.POST.items():
                if key.startswith('competencias[') and key.endswith(']'):
                    parts = key.strip('competencias[]').split('][')
                    competencia_id = int(parts[0])
                    area_nome = request.POST['areas[{}]'.format(parts[1])]  # Obtenha o nome completo da área

                    novo_nivel = float(value)

                    # Recupere a competência com base no ID
                    competencia = Competencia.objects.get(id=competencia_id)

                    # Recupere o setor da quinta coluna da tabela
                    setor_nome = request.POST['setores[{}]'.format(parts[2])]

                    # Verifique se já existe uma matriz para esta competência, área e setor
                    try:
                        matriz = Matriz.objects.get(competencias=competencia, area=area_nome, setor__nome=setor_nome)
                        if matriz.nivel_percentual != novo_nivel:
                            matriz.nivel_percentual = novo_nivel
                            matriz.save()
                    except Matriz.DoesNotExist:
                        # Se a matriz não existir, crie uma nova com os dados da área, competência e setor
                        Matriz.objects.create(competencias=competencia, area=area_nome, nivel_percentual=novo_nivel, setor=Setor.objects.get(nome=setor_nome))
        except Exception as e:
            return render(request, 'matriz_template.html', {"error_message": str(e)})

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


##AFINIDADE DE MEMBRO POR MEMBRO


def afinidade_membro(request, membro_id):
    # Obtenha o membro selecionado
    membro = Membro.objects.get(id=membro_id)

    # Obtenha todas as áreas
    areas = Matriz.objects.values_list('area', flat=True).distinct()

    # Crie uma lista para armazenar as afinidades do membro com cada área
    afinidades = []

    for area in areas:
        area_afinidades = {
            'area_nome': area,
            'afinidades': [],
        }

        for competencia in ConsultaCompetencia.objects.filter(membro=membro):
            if Matriz.objects.filter(competencias=competencia.competencia, area=area).exists():
                area_afinidades['afinidades'].append(competencia.competencia.nome)

        afinidades.append(area_afinidades)

    context = {
        'membro': membro,
        'afinidades': afinidades,
    }

    return render(request, 'afinidade_membro.html', context)


########################## INICIO DE VIEWS PARA ADMIN#########################

##PAGINA INICIAL ADMIN##
def pagina_inicial_admin(request):
    # Sua lógica de visualização aqui, se necessário
    return render(request, 'pagina_inicial_admin.html')

##PAGINA DE ADIÇÃO DE NOVAS FORMAÇÔES REALIZADAS POR MEMBROS##
def novas_formacoes_realizadas(request):
    if request.method == 'POST':
        membro_id = request.POST['membro']
        formacao_id = request.POST['formacao']

        membro = Membro.objects.get(id=membro_id)
        formacao = Formacao.objects.get(id=formacao_id)

        consulta_formacao = ConsultaFormacao(membro=membro, formacao=formacao, Data=data)
        consulta_formacao.save()

        return redirect('novas_formacoes_realizadas')  # Substitua 'nome_da_pagina_de_redirecionamento' pela página desejada após a adição.

    membros = Membro.objects.all()
    formacoes = Formacao.objects.all()

    context = {
        'membros': membros,
        'formacoes': formacoes,
    }

    return render(request, 'novas_formacoes_realizadas.html', context)
##PAGINA DE FORMAÇÕES PREVISTAS PARA GESTOR
def formacoes_previstas_admin(request):
    formacoes = FormacaoPrevista.objects.all()

    for formacao in formacoes:
        membros_associados = MembroFormacao.objects.filter(formacao_prevista=formacao)
        formacao.vagasdisponiveis = formacao.vagas - membros_associados.count()

    context = {
        'formacoes_previstas': formacoes,
        'formacao_prevista': None,  # Pode ser None, já que estamos na página de listagem.
    }

    return render(request, 'formacoes_previstas_admin.html', context)

##PAGINA PARA ADICIONAR NOVAS FORMAÇÕES PREVISTAS OU SEJA CALENDARIO MANUAL##
def adicionar_editar_formacao_prevista(request, formacao_id=None):
    # Se formacao_id for fornecido, isso indica que estamos editando uma formação prevista existente.
    if formacao_id:
        formacao_prevista = FormacaoPrevista.objects.get(id=formacao_id)
    else:
        formacao_prevista = FormacaoPrevista()

    if request.method == 'POST':
        formacao = Formacao.objects.get(id=request.POST['formacao'])
        formador = request.POST['formador']
        vagas = request.POST['vagas']
        duracao = request.POST['duracao']
        local = request.POST['local']
        datainicial = request.POST['datainicial']
        datafinal = request.POST['datafinal']
        vagasdisponiveis = request.POST['vagasdisponiveis']
        Elearning = request.POST['elearning']

        formacao_prevista.formacao = formacao
        formacao_prevista.formador = formador
        formacao_prevista.vagas = vagas
        formacao_prevista.duracao = duracao
        formacao_prevista.local = local
        formacao_prevista.datainicial = datainicial
        formacao_prevista.datafinal = datafinal
        formacao_prevista.vagasdisponiveis = vagasdisponiveis
        formacao_prevista.Elearning = Elearning

        # Certifique-se de que o status seja definido como "prevista" antes de salvar
        formacao_prevista.status = "prevista"
        formacao_prevista.save()

        return redirect('formacoes_previstas_admin')  # Substitua 'nome_da_pagina_de_redirecionamento' pela página desejada após a edição.

    formacoes = Formacao.objects.all()

    formacoes_previstas = FormacaoPrevista.objects.all()

    context = {
        'formacao_prevista': formacao_prevista,
        'formacoes': formacoes,
        'formacoes_previstas': formacoes_previstas,
    }

    return render(request, 'novas_formacoes_previstas.html', context)


## PAGINA PARA EDIÇÃO DE FORMAÇÕES PREVISTAS ADMIN/GESTOR MANUTENÇÃO
def editar_formacao_prevista(request, formacao_id):
    formacao_prevista = get_object_or_404(FormacaoPrevista, id=formacao_id)

    if request.method == 'POST':
        form = FormacaoPrevistaForm(request.POST, instance=formacao_prevista)
        if form.is_valid():
            form.save()
            return redirect('pagina_inicial')  # Redirecione para onde você desejar após a edição
    else:
        form = FormacaoPrevistaForm(instance=formacao_prevista)

    return render(request, 'editar_formacao_prevista_admin.html', {'form': form, 'formacao_prevista': formacao_prevista})


from django.shortcuts import redirect, get_object_or_404


def excluir_formacao_prevista(request, formacao_id):
    formacao = get_object_or_404(FormacaoPrevista, id=formacao_id)
    formacao.delete()
    return redirect('formacoes_previstas_admin')


def listar_membros_por_formacao_admin(request, formacao_prevista_id):
    membros = MembroFormacao.objects.filter(formacao_prevista_id=formacao_prevista_id)
    formacao_prevista = get_object_or_404(FormacaoPrevista, id=formacao_prevista_id)

    context = {
        'formacao_prevista': formacao_prevista,
        'membros': membros,
    }

    return render(request, 'listar_membros_por_formacao_admin.html', context)


from django.shortcuts import redirect


def excluir_membro_formacao(request, membro_id):
    membro = MembroFormacao.objects.get(id=membro_id)

    # Verificar se o membro pertence à formação do usuário atual, caso necessário

    membro.delete()

    return redirect('listar_membros_por_formacao_admin', formacao_prevista_id=membro.formacao_prevista.id)


##PAGINA PARA MOSTRAR MEMBROS CADASTRADOS NAS FORMAÇÕES FUTURAS##

def listar_membros_formacoes(request):
    # Recupere todos os objetos MembroFormacao do banco de dados
    membros_formacoes = MembroFormacao.objects.all()

    # Renderize a página HTML com os objetos MembroFormacao no contexto
    return render(request, 'listar_membros_formacoes.html', {'membros_formacoes': membros_formacoes})