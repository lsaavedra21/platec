from django import forms
from .models import Setor, Membro
from django.core.exceptions import ValidationError



class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['id', 'nome', 'setor', 'cargo']  # Lista dos campos que você deseja editar
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }

class SetorForm(forms.Form):
    setor = forms.ModelChoiceField(queryset=Setor.objects.all(), empty_label=None)

from .models import FormacaoPrevista

from django import forms

STATUS_CHOICES = [
    ('prevista', 'Prevista'),
    ('confirmada', 'Confirmada'),
    ('cancelada', 'Cancelada'),
    ('concluida', 'Concluída'),
]

class FormacaoPrevistaForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = FormacaoPrevista
        fields = ['formacao', 'formador', 'vagas', 'duracao', 'local', 'datainicial', 'datafinal', 'vagasdisponiveis', 'Elearning', 'status']


from .models import Membro, MembroFormacao

class AdicionarMembroForm(forms.ModelForm):
    setor_filtro = forms.ModelChoiceField(
        queryset=Setor.objects.all(),
        label="Filtrar por Setor",
        required=False  # Isso permite que o campo seja opcional
    )

    class Meta:
        model = MembroFormacao
        fields = ['membro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membro'].queryset = Membro.objects.all()

    class Meta:
        model = Membro
        fields = ['nome', 'email']  # Inclua os campos que você deseja coletar ao adicionar membros


from django import forms
from .models import Competencia

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nome', 'setor', 'tecnologia']


