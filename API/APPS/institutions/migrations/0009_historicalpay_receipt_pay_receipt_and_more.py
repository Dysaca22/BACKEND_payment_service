# Generated by Django 4.1.3 on 2022-11-19 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0008_alter_bill__generateddate_alter_historicalpay__date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpay',
            name='receipt',
            field=models.CharField(blank=True, max_length=20, verbose_name='Receipt number'),
        ),
        migrations.AddField(
            model_name='pay',
            name='receipt',
            field=models.CharField(blank=True, max_length=20, verbose_name='Receipt number'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 23, 42, 54, 267902), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 23, 42, 54, 275901), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 18, 23, 42, 54, 275901), editable=False, verbose_name='Creation date'),
        ),
    ]
