from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


class Setor(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'c_setor'
        verbose_name = 'Setor'
        verbose_name_plural = 'Setors'

    def __str__(self):
        return f"{self.nome}"

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Cargo(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)

    class Meta:
        db_table = 'c_cargo'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return f"{self.nome}"


class Membro(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='c_membro', null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='c_membro', null=True)


    class Meta:
        db_table = 'c_membro'
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return f"{self.id} - {self.nome}"

class Tecnologia(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = 'c_tecnologia'
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'

    def __str__(self):
        return f"{self.nome}"


class Formacao(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE, related_name='c_formacoes', null=True)
    duracao = models.CharField(max_length=255)

    class Meta:
        db_table = 'c_formacoes'
        verbose_name = 'Formacao'
        verbose_name_plural = 'Formacoes'

    def __str__(self):
        return f"{self.nome}"



class Competencia(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='c_competencias', null=True)
    tecnologia = models.ForeignKey(Tecnologia, on_delete=models.CASCADE, related_name='c_competencias', null=True)

    class Meta:
        db_table = 'c_competencias'
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'



    def __str__(self):
        return f"{self.nome}"


class ConsultaCompetencia(models.Model):
    id = models.AutoField(primary_key=True)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='c_membro_competencias')
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, related_name='c_membro_competencias')
    nivel = models.CharField(max_length=255, default='0')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='c_membro_competencias', null=True)

    class Meta:
        db_table = 'c_membro_competencias'
        verbose_name = 'Consulta Competencia'
        verbose_name_plural = 'Consulta Competencias'
        unique_together = ('membro', 'competencia')







class ConsultaFormacao(models.Model):
    id = models.AutoField(primary_key=True)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name='c_membro_formacoes')
    formacao = models.ForeignKey(Formacao, on_delete=models.CASCADE, related_name='c_membro_formacoes')
    Data = models.DateField(max_length=255)

    class Meta:
        db_table = 'c_membro_formacoes'
        verbose_name = 'Consulta Formacao'
        verbose_name_plural = 'Consulta Formacoes'

    def __str__(self):
        return f"{self.membro.nome} ({self.membro.id}) - {self.formacao.nome} - {self.Data}"


class FormacaoPrevista(models.Model):
    id = models.AutoField(primary_key=True)
    formacao = models.ForeignKey(Formacao, on_delete=models.CASCADE, related_name='c_formacos_previstas')
    formador = models.CharField(max_length=255)
    vagas = models.CharField(max_length=255)
    duracao = models.CharField(max_length=255)
    data = models.DateField(max_length=255)

    class Meta:
        db_table = 'c_formacoes_previstas'
        verbose_name = 'Formacao Prevista'
        verbose_name_plural = 'Formacao Previstas'

    def __str__(self):
        return f"{self.formacao.nome} - {self.formador} - {self.vagas} - {self.duracao} - {self.data}"


class Matriz(models.Model):
    id = models.AutoField(primary_key=True)
    competencias = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    area = models.CharField(max_length=255)
    nivel_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'c_areas_competencias'

    def __str__(self):
        return f"Matriz #{self.id}: {self.area} - {self.competencias} - {self.setor}"

class LoginUser(models.Model):
    usuario = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    nivel = models.CharField(max_length=255)

