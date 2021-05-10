# Generated by Django 3.1.7 on 2021-05-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0005_auto_20210315_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('force_stop', models.BooleanField(default=False)),
                ('force_run', models.BooleanField(default=False)),
                ('animation_start_time', models.TimeField(blank=True, null=True)),
                ('animation_end_time', models.TimeField(blank=True, null=True)),
                ('last_raspberry_pi_update', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='code',
            name='date_approved',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
