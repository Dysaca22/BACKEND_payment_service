# Generated by Django 4.1.3 on 2022-11-05 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
