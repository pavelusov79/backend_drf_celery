# Generated by Django 3.2.13 on 2022-04-16 06:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytasks',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 16, 6, 2, 22, 96566, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='mytrackedgoods',
            name='date_field',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата время'),
        ),
    ]
