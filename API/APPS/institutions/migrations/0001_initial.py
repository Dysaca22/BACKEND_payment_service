# Generated by Django 4.1.3 on 2022-11-05 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('campus', models.CharField(choices=[('BAQ', 'Barranquilla'), ('CTG', 'Cartagena'), ('SMR', 'Santa Marta'), ('SIN', 'Sincelejo'), ('MON', 'Monteria')], default='BAQ', max_length=3, verbose_name='Campus')),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('lastName', models.CharField(max_length=255, verbose_name='Last name')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution', verbose_name='Institution')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='StudentService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_status', models.BooleanField(choices=[(True, 'Paid'), (False, 'Unpaid')], default=False, verbose_name='Status')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.service', verbose_name='Service')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student service',
                'verbose_name_plural': 'Student services',
            },
        ),
    ]
