# Generated by Django 4.1.3 on 2022-11-06 23:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_alter_bill__generateddate_alter_historicalpay__date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 18, 30, 41, 932941), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 18, 30, 41, 933938), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 18, 30, 41, 933938), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.CharField(choices=[('PR', 'Pregrado'), ('PS', 'Posgrado')], max_length=2, verbose_name='Type'),
        ),
    ]