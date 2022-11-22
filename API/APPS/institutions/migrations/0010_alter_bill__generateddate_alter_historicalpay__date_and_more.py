# Generated by Django 4.1.3 on 2022-11-21 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0009_historicalpay_receipt_pay_receipt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 18, 5, 20, 784447), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 18, 5, 20, 784447), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_status',
            field=models.CharField(choices=[('S', 'Successful'), ('F', 'Failed'), ('C', 'Cancelled'), ('P', 'In process')], default='P', max_length=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 21, 18, 5, 20, 784447), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_status',
            field=models.CharField(choices=[('S', 'Successful'), ('F', 'Failed'), ('C', 'Cancelled'), ('P', 'In process')], default='P', max_length=1, verbose_name='Status'),
        ),
    ]
