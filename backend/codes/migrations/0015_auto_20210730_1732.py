# Generated by Django 3.1.7 on 2021-07-30 17:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0014_auto_20210729_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='udp_key',
            field=models.CharField(default='ABC123', max_length=8, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
