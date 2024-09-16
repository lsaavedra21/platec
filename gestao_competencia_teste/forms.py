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

