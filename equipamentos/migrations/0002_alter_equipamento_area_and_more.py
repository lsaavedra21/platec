# Generated by Django 4.1 on 2022-08-30 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='equipamentos.area'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='equipamentos.departamento'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='linha',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='equipamentos.linha'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='posto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='equipamentos.posto'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='zona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='equipamentos.zona'),
        ),
    ]