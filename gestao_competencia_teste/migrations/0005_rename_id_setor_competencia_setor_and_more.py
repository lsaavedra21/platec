# Generated by Django 4.1 on 2023-06-22 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_competencia_teste', '0004_rename_id_membro_id_rename_cargo_membro_id_cargo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competencia',
            old_name='id_setor',
            new_name='setor',
        ),
        migrations.RenameField(
            model_name='competencia',
            old_name='id_tecnologia',
            new_name='tecnologia',
        ),
        migrations.RenameField(
            model_name='formacao',
            old_name='id_tecnologia',
            new_name='tecnologia',
        ),
        migrations.RenameField(
            model_name='membro',
            old_name='id_cargo',
            new_name='cargo',
        ),
        migrations.RenameField(
            model_name='membro',
            old_name='setor_id',
            new_name='setor',
        ),
    ]
