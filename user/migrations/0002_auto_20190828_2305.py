# Generated by Django 2.2.4 on 2019-08-28 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='added_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
