from django import template
from gestao_competencia.models import ConsultaCompetencia  # Importe o modelo relevante

register = template.Library()

@register.simple_tag
def get_nivel(membro_id, competencia_id, consultas):
    consulta = consultas.filter(membro_id=membro_id, competencia_id=competencia_id).first()
    if consulta:
        return consulta.nivel
    return ''