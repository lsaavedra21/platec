# Generated by Django 4.1 on 2023-06-21 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'c_cargo',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'c_setor',
            },
        ),
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('id_cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestao_competencia_teste.cargo')),
                ('id_setor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestao_competencia_teste.setor')),
            ],
            options={
                'db_table': 'c_membro',
            },
        ),
    ]