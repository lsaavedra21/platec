from django.db import models


class Planta(models.Model):
    PLANT_CODES = (
        ('CMO1', 'CMO1'),
        ('VP01', 'VP01'),
        ('VU01', 'VU01'),
    )
    codigo=         models.CharField(max_length=4, choices=PLANT_CODES, unique=True)
    traducao=       models.CharField(max_length=20, blank=True, default='')
    def __str__(self) -> str:
        if self.traducao is None:
            return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.codigo} - {self.traducao}'
        return f'{self.codigo}'

    class Meta:
        db_table = 'plantas'
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'
        

class Departamento(models.Model):
    DEPARTMENT_CODES = (
        ('A', 'A'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('M', 'M'),
        ('O', 'O'),
        ('P', 'P'),
        ('T', 'T'),
    )

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name="departamentos")
    codigo = models.CharField(max_length=20, choices=DEPARTMENT_CODES)
    traducao= models.CharField(max_length=20, blank=True, default='')
    def __str__(self) -> str:
        if self.traducao is None:
            return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.traducao}'
        return f'{self.codigo}'
    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Area(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="areas")
    codigo = models.CharField(max_length=10, blank=True, default='')
    traducao= models.CharField(max_length=20, blank=True, default='')

    def __str__(self) -> str:
        if self.traducao is None:
            return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.codigo} - {self.traducao}'
        return f'{self.codigo}'

    class Meta:
        db_table = 'area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'


class Linha(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="linhas")
    codigo = models.CharField(max_length=10, blank=True, default='')
    traducao= models.CharField(max_length=20, blank=True, default='')

    def __str__(self) -> str:
        if self.traducao is None:
            return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.codigo} - {self.traducao}'
        return f'{self.codigo}'

    class Meta:
        db_table = 'linhas'
        verbose_name = 'Linha'
        verbose_name_plural = 'Linhas'


class Zona(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10, blank=True, default='')
    traducao= models.CharField(max_length=20, blank=True, default='')

    def __str__(self) -> str:
        if self.traducao is None: return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.codigo} - {self.traducao}'
        return f'{self.codigo}'

    class Meta:
        db_table = 'zonas'
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
    

class Posto(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10, blank=True, default='')
    traducao= models.CharField(max_length=20, blank=True, default='')

    def __str__(self) -> str:
        if self.traducao is None:
            return f'{self.codigo}'
        if len(self.traducao.split()) > 0: return f'{self.codigo} - {self.traducao}'
        return f'{self.codigo}'

    class Meta:
        db_table = 'postos'
        verbose_name = 'Posto'
        verbose_name_plural = 'Postos'


# Create your models here.
class Equipamento(models.Model):
    CODE_ABC = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    codigo_sap=             models.IntegerField(primary_key=True, verbose_name='Código SAP')
    denominacao=            models.CharField(max_length=250, blank=True)
    denominacao_linha=      models.CharField(max_length=250, blank=True)
    local=                  models.CharField(max_length=50, blank=True)
    sala=                   models.CharField(max_length=50, blank=True)
    codigo_abc=             models.CharField(max_length=4, choices=CODE_ABC)
    qrcode=                 models.CharField(max_length=255, blank=True)
    data_criacao=           models.CharField(max_length=50, blank=True)
    data_edicao=            models.CharField(max_length=50, blank=True)
    criado_por=             models.CharField(max_length=50, blank=True)
    editado_por=            models.CharField(max_length=50, blank=True)
    observacoes=            models.TextField(blank=True)

    # Relationships
    planta=                 models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    departamento=           models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    area=                   models.ForeignKey(Area, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    linha=                  models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    zona=                   models.ForeignKey(Zona, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    posto=                  models.ForeignKey(Posto, on_delete=models.CASCADE, related_name='equipamentos', blank=True, null=True)
    equip_superior=         models.ForeignKey('self', on_delete=models.CASCADE, related_name='filho', blank=True, null=True)


    def __str__(self) -> str:
        return str(f"{self.denominacao}" )
    
    class Meta:
        db_table = 'equipamentos'
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
