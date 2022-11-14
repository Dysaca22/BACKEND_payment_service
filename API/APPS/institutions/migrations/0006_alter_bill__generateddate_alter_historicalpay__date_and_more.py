# Generated by Django 4.1.3 on 2022-11-14 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_alter_bill__generateddate_alter_historicalpay__date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 10, 10, 3, 620306), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 10, 10, 3, 620306), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 10, 10, 3, 620306), editable=False, verbose_name='Creation date'),
        ),
    ]
