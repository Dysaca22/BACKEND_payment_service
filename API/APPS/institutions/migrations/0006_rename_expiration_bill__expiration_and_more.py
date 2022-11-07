# Generated by Django 4.1.3 on 2022-11-07 00:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_alter_program_options_alter_bill__generateddate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='expiration',
            new_name='_expiration',
        ),
        migrations.AlterField(
            model_name='bill',
            name='_generatedDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 16, 19, 830400), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='historicalpay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 16, 19, 831396), editable=False, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 19, 16, 19, 831396), editable=False, verbose_name='Creation date'),
        ),
    ]