# Generated by Django 3.1.7 on 2021-07-29 22:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0013_code_generated_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='udp_key',
            field=models.PositiveIntegerField(default=99999, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)]),
        ),
        migrations.AddField(
            model_name='config',
            name='udp_receive_run',
            field=models.BooleanField(default=False),
        ),
    ]
