# Generated by Django 4.1.3 on 2022-11-07 00:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_alter_service_options_alter_bill__generateddate_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'verbose_name': 'Program', 'verbose_name_plural': 'Programs'},
        ),
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 8, 8, 785528), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.semester', verbose_name='Semester'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.student', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 8, 8, 786525), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 8, 8, 786525), editable=False, verbose_name='Creation date'),
        ),
    ]
