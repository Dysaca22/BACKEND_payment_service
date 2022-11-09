# Generated by Django 4.1.3 on 2022-11-07 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0007_alter_bill__generateddate_alter_historicalpay__date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=9, verbose_name='Amount')),
                ('concept', models.TextField(blank=True, verbose_name='Concept')),
                ('type', models.CharField(choices=[('DC', 'Debit'), ('CC', 'Credit')], max_length=2, verbose_name='Type')),
                ('number', models.CharField(editable=False, max_length=16, unique=True, verbose_name='Number')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('lastName', models.CharField(max_length=50, verbose_name='Last name')),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.pay', verbose_name='Institution pay')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
            },
        ),
    ]
