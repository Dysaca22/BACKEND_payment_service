# Generated by Django 4.1.3 on 2022-11-14 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fase1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('payType', models.CharField(choices=[('DC', 'Debit'), ('CC', 'Credit')], max_length=2, verbose_name='Pay type')),
                ('payID', models.IntegerField(verbose_name='Pay ID')),
            ],
            options={
                'verbose_name': 'Fase1',
                'verbose_name_plural': 'Fases1',
            },
        ),
        migrations.CreateModel(
            name='Fase2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(choices=[('EB', 'East Bank'), ('WB', 'Western Bank')], max_length=2, verbose_name='Bank')),
                ('name', models.CharField(max_length=255, verbose_name='Person name')),
                ('lastName', models.CharField(max_length=255, verbose_name='Person last name')),
                ('idNumber', models.CharField(max_length=10, verbose_name='Identification number')),
                ('phone', models.CharField(max_length=10, verbose_name='Phone number')),
                ('_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, verbose_name='Value')),
                ('concept', models.CharField(blank=True, max_length=500, verbose_name='Concept')),
                ('institution', models.CharField(blank=True, max_length=100, verbose_name='Institution')),
                ('fase1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.fase1', verbose_name='Fase1')),
            ],
            options={
                'verbose_name': 'Fase2',
                'verbose_name_plural': 'Fases2',
            },
        ),
    ]
