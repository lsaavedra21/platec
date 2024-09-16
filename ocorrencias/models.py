from django.db import models
from equipamentos.models import Equipamento
from django.utils import timezone


class OcorrenciaPlatec(models.Model):
    # relationships
    equipamento = models.ForeignKey(
        Equipamento, related_name="ocorrencias", verbose_name='Código SAP Equipamento', 
        help_text="ID equipamento SAP", on_delete=models.CASCADE
    )


    CHOICES = {
        'CATEGORY': (
        ('Automação', 'Automação'),
        ('Eletrônico', 'Eletrônico'),
        ('Eletrica', 'Eletrica'),
        ('Hidráulica', 'Hidráulica'),
        ('Informática', 'Informática'),
        ('Mecanica', 'Mecanica'),
        ('Robô', 'Robô'),
        ('Outro', 'Outro'),
        ),

        'SHIFT': (
        ('1 Turno', '1° Turno'),
        ('2 Turno', '2° Turno'),
        ),
    }

    sintoma=                models.TextField(verbose_name='Sintoma',)
    causa=                  models.TextField(verbose_name='Causa', blank=True, null=True)
    remedio=                models.TextField(verbose_name='Remédio', blank=True, null=True)
    categoria=              models.CharField(max_length=25, choices=CHOICES['CATEGORY'], verbose_name='Categoria',)
    turno=                  models.CharField(max_length=25, choices=CHOICES['SHIFT'], verbose_name='Turno',)
    horario_quebra=         models.DateTimeField(default=timezone.now, verbose_name='Hora Pane', help_text="Horario da quebra", blank=True, null=True)
    horario_chamado=        models.DateTimeField(default=timezone.now, verbose_name='Hora Platec', help_text="Hora que a Platec foi acionada", blank=True, null=True)
    tempo_eqp_parado=       models.PositiveSmallIntegerField(verbose_name='Tempo parado', blank=True, null=True)
    perdas_rgu=             models.PositiveBigIntegerField(verbose_name='Perdas RGU', blank=True, null=True)
    veiculos_perdidos=      models.PositiveIntegerField(verbose_name='Perdas', help_text="Veiculos perdido", blank=True, null=True)
    marcha_degradada=       models.CharField(max_length=100, verbose_name='Marcha degradada', help_text='Se houve marcha degradada, descreva', blank=True, null=True)
    mbr=                    models.PositiveIntegerField(verbose_name='MBR', null=True, blank=True)


    def __str__(self):
        return self.sintoma

    class Meta:
        db_table = 'quebra_equipamentos'
        verbose_name = 'Quebra de equipamento'
        verbose_name_plural = 'Quebra de equipamentos'
        ordering = ['-horario_quebra']

